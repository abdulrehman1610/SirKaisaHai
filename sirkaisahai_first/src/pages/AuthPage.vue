<script setup lang="ts">
import { ref, computed, nextTick } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const step = ref<'email' | 'otp' | 'success'>(authStore.isVerified ? 'success' : 'email');
const emailInput = ref(authStore.email || '');
const otpDigits = ref<string[]>(['', '', '', '', '', '']);
const otpRefs = ref<(HTMLInputElement | null)[]>([]);
const isLoading = ref(false);
const errorMsg = ref('');
const successMsg = ref('');
const showLogoutModal = ref(false);

const otpInput = computed(() => otpDigits.value.join(''));
const redirectPath = (route.query.redirect as string) || '/';

function setOtpRef(el: unknown, index: number) {
  otpRefs.value[index] = el as HTMLInputElement | null;
}

function handleDigitInput(index: number, event: Event) {
  const input = event.target as HTMLInputElement;
  const cleaned = input.value.replace(/\D/g, '');
  if (!cleaned) {
    otpDigits.value[index] = '';
    return;
  }

  if (cleaned.length > 1) {
    const chars = cleaned.slice(0, 6).split('');
    chars.forEach((ch, idx) => {
      if (idx < 6) otpDigits.value[idx] = ch;
    });
    const focusIdx = Math.min(chars.length, 5);
    otpRefs.value[focusIdx]?.focus();
    return;
  }

  otpDigits.value[index] = cleaned;
  if (index < 5) {
    otpRefs.value[index + 1]?.focus();
  }
}

function handleDigitKeydown(index: number, event: KeyboardEvent) {
  if (event.key === 'Backspace' && !otpDigits.value[index] && index > 0) {
    otpDigits.value[index - 1] = '';
    otpRefs.value[index - 1]?.focus();
  }
}

function handleDigitPaste(event: ClipboardEvent) {
  const pasted = event.clipboardData?.getData('text') || '';
  const digits = pasted.replace(/\D/g, '').slice(0, 6);
  if (!digits) return;
  event.preventDefault();
  for (let i = 0; i < 6; i++) {
    otpDigits.value[i] = digits[i] || '';
  }
  const focusIdx = Math.min(digits.length, 5);
  otpRefs.value[focusIdx]?.focus();
}

async function handleSendOTP() {
  errorMsg.value = '';
  if (!emailInput.value.trim()) {
    errorMsg.value = 'Please enter your student email address.';
    return;
  }
  if (!emailInput.value.toLowerCase().endsWith('@superior.edu.pk')) {
    errorMsg.value = 'Only Superior University emails (@superior.edu.pk) are accepted for verification.';
    return;
  }

  isLoading.value = true;
  try {
    const res = await authStore.requestOTP(emailInput.value);
    if (res.success) {
      successMsg.value = res.message;
      otpDigits.value = ['', '', '', '', '', ''];
      step.value = 'otp';
      await nextTick();
      otpRefs.value[0]?.focus();
    } else {
      errorMsg.value = res.message;
    }
  } finally {
    isLoading.value = false;
  }
}

async function handleVerifyOTP() {
  errorMsg.value = '';
  if (otpInput.value.length !== 6) {
    errorMsg.value = 'Please enter all 6 digits of your verification code.';
    return;
  }

  isLoading.value = true;
  try {
    const res = await authStore.verifyOTP(otpInput.value);
    if (res.success) {
      step.value = 'success';
      setTimeout(() => {
        router.push(redirectPath);
      }, 1200);
    } else {
      errorMsg.value = res.message || 'Verification failed.';
    }
  } finally {
    isLoading.value = false;
  }
}

function confirmLogout() {
  authStore.logout();
  showLogoutModal.value = false;
  step.value = 'email';
  emailInput.value = '';
  otpDigits.value = ['', '', '', '', '', ''];
}
</script>

<template>
  <main class="w-full">
    <section class="bg-band-hero px-4 md:px-gutter pt-8 pb-16 min-h-[76vh] flex items-center justify-center">
      <div class="max-w-3xl w-full ed-card overflow-hidden grid grid-cols-1 md:grid-cols-12">
        <!-- Left Deep Plum Trust Column -->
        <aside class="md:col-span-5 bg-primary-dark text-on-primary p-7 md:p-8 flex flex-col justify-between gap-6">
          <div class="space-y-4">
            <p class="font-mono text-[10px] uppercase tracking-[0.16em] text-on-primary/55">
              Zero-Knowledge Auth
            </p>
            <h1 class="font-display text-2xl sm:text-3xl font-extrabold text-on-primary leading-tight">
              Your identity stays yours.
            </h1>
            <p class="text-xs text-on-primary/75 leading-relaxed">
              We verify your campus email once to stop spam, then disconnect your email completely from your reviews.
            </p>

            <ol class="space-y-3 pt-2 text-xs text-on-primary/85">
              <li class="flex gap-2.5">
                <span class="font-serif italic text-base text-band-strip leading-none">01</span>
                <span>One-time 6-digit code sent to @superior.edu.pk.</span>
              </li>
              <li class="flex gap-2.5">
                <span class="font-serif italic text-base text-band-strip leading-none">02</span>
                <span>Email is irreversibly hashed with SHA-256 into an httpOnly cookie.</span>
              </li>
              <li class="flex gap-2.5">
                <span class="font-serif italic text-base text-band-strip leading-none">03</span>
                <span>Published reviews carry zero foreign keys back to your email.</span>
              </li>
            </ol>
          </div>

          <div class="pt-4 border-t border-on-primary/15 flex gap-4 font-mono text-[10px] uppercase tracking-wider">
            <router-link to="/privacy" class="text-on-primary/75 hover:text-on-primary underline">Privacy</router-link>
            <router-link to="/terms" class="text-on-primary/75 hover:text-on-primary underline">Terms</router-link>
          </div>
        </aside>

        <!-- Right Interactive Auth Column -->
        <section class="md:col-span-7 p-7 md:p-9 flex flex-col justify-center space-y-5">
          <div class="space-y-1.5">
            <p class="ed-eyebrow">Superior University</p>
            <h2 class="font-display text-2xl font-extrabold text-ink-dark">
              {{
                step === 'email'
                  ? 'Verify student email'
                  : step === 'otp'
                    ? 'Enter 6-digit code'
                    : 'Session verified'
              }}
            </h2>
            <p class="text-xs text-ink-muted leading-relaxed">
              <template v-if="step === 'email'">
                Enter your official @superior.edu.pk address to receive a one-time code.
              </template>
              <template v-else-if="step === 'otp'">
                Enter the code sent to <strong class="text-ink-dark">{{ emailInput }}</strong>.
              </template>
              <template v-else>
                Your anonymous student session is active in this browser.
              </template>
            </p>
          </div>

          <div v-if="errorMsg" class="p-3 bg-error-soft text-error rounded-xl text-xs font-semibold">
            {{ errorMsg }}
          </div>
          <div v-if="successMsg && step === 'otp'" class="p-3 bg-success-soft text-success rounded-xl text-xs font-semibold">
            {{ successMsg }}
          </div>

          <!-- Step 1: Email -->
          <form v-if="step === 'email'" @submit.prevent="handleSendOTP" class="space-y-4">
            <div class="space-y-1.5">
              <label for="student-email" class="block ed-eyebrow">Student email address</label>
              <input
                id="student-email"
                v-model="emailInput"
                type="email"
                placeholder="bsse-f22-045@superior.edu.pk"
                class="w-full ed-input px-4 py-3 text-sm"
                required
                :disabled="isLoading"
              />
              <span class="text-[11px] text-ink-subtle block">
                Must end with <strong class="text-ink-muted">@superior.edu.pk</strong>
              </span>
            </div>

            <button
              type="submit"
              class="ed-btn-primary w-full py-3 text-xs font-semibold inline-flex items-center justify-center gap-3 cursor-pointer disabled:opacity-50"
              :disabled="isLoading"
            >
              <span>{{ isLoading ? 'Sending code...' : 'Send verification code' }}</span>
              <span v-if="!isLoading" aria-hidden="true">→</span>
            </button>
          </form>

          <!-- Step 2: 6 Individual OTP Boxes -->
          <form v-else-if="step === 'otp'" @submit.prevent="handleVerifyOTP" class="space-y-5">
            <div class="space-y-2">
              <label class="block ed-eyebrow">6-digit one-time passcode</label>
              <div class="grid grid-cols-6 gap-2" @paste="handleDigitPaste">
                <input
                  v-for="(_, index) in otpDigits"
                  :key="index"
                  :ref="(el) => setOtpRef(el, index)"
                  :value="otpDigits[index]"
                  type="text"
                  inputmode="numeric"
                  maxlength="6"
                  autocomplete="one-time-code"
                  :aria-label="`OTP digit ${index + 1}`"
                  :disabled="isLoading"
                  @input="handleDigitInput(index, $event)"
                  @keydown="handleDigitKeydown(index, $event)"
                  class="ed-input h-12 text-center font-mono text-lg font-bold tabular-nums text-primary"
                />
              </div>
              <span class="text-[11px] text-ink-subtle block">
                5 failed attempts trigger a 15-minute lockout for security.
              </span>
            </div>

            <div class="flex gap-3">
              <button
                type="button"
                @click="step = 'email'; errorMsg = ''"
                class="ed-btn-soft px-4 py-2.5 text-xs font-semibold cursor-pointer"
                :disabled="isLoading"
              >
                Change
              </button>
              <button
                type="submit"
                class="flex-1 ed-btn-primary py-2.5 text-xs font-semibold cursor-pointer disabled:opacity-50"
                :disabled="isLoading || otpInput.length !== 6"
              >
                {{ isLoading ? 'Verifying...' : 'Verify & continue →' }}
              </button>
            </div>
          </form>

          <!-- Step 3: Verified -->
          <div v-else class="space-y-4">
            <div class="bg-success-soft rounded-2xl p-4 space-y-1">
              <p class="font-mono text-[10px] uppercase font-semibold text-success">Verified Campus Session</p>
              <p class="text-sm font-bold text-ink-dark">
                {{ authStore.email || 'Superior University Student' }}
              </p>
            </div>

            <div class="flex flex-wrap gap-3">
              <router-link to="/review/new" class="ed-btn-primary px-5 py-2.5 text-xs font-semibold inline-flex items-center gap-2">
                <span>Write a review</span>
                <span aria-hidden="true">→</span>
              </router-link>
              <button
                type="button"
                @click="showLogoutModal = true"
                class="ed-btn-soft px-5 py-2.5 text-xs font-semibold text-error cursor-pointer"
              >
                Unlink / log out
              </button>
            </div>
          </div>
        </section>
      </div>
    </section>

    <!-- Logout Modal -->
    <div
      v-if="showLogoutModal"
      class="fixed inset-0 z-50 bg-ink-dark/40 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
    >
      <div class="ed-card p-7 max-w-sm w-full text-center space-y-4">
        <h3 class="text-xl font-bold text-ink-dark">Unlink &amp; Log Out?</h3>
        <p class="text-xs text-ink-muted leading-relaxed">
          This clears your active session cookie. You will need a new OTP next time you post a review.
        </p>
        <div class="flex gap-3 pt-1">
          <button
            type="button"
            @click="showLogoutModal = false"
            class="flex-1 ed-btn-soft py-2.5 text-xs font-semibold cursor-pointer"
          >
            Cancel
          </button>
          <button
            type="button"
            @click="confirmLogout"
            class="flex-1 bg-error text-on-primary rounded-full py-2.5 text-xs font-semibold hover:opacity-90 cursor-pointer"
          >
            Yes, unlink
          </button>
        </div>
      </div>
    </div>
  </main>
</template>
