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
  <main class="max-w-container-max mx-auto px-4 md:px-gutter py-10 flex items-center justify-center min-h-[74vh]">
    <div class="neu-surface-lg p-7 sm:p-10 max-w-md w-full text-center space-y-6">
      <div class="neu-tile w-14 h-14 mx-auto flex items-center justify-center text-primary">
        <svg viewBox="0 0 20 20" fill="none" class="w-6 h-6" aria-hidden="true">
          <path
            d="M10 2.5L15.5 4.8V9.2C15.5 13 13.1 16 10 17C6.9 16 4.5 13 4.5 9.2V4.8L10 2.5Z"
            stroke="currentColor"
            stroke-width="1.6"
            stroke-linejoin="round"
          />
          <path
            d="M7.5 10L9.2 11.7L12.7 8.2"
            stroke="currentColor"
            stroke-width="1.6"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>
      </div>

      <div class="space-y-2">
        <p class="text-[10px] font-semibold uppercase tracking-[0.18em] text-outline">
          Zero-Knowledge Auth
        </p>
        <h1 class="text-2xl font-extrabold text-primary">
          {{
            step === 'email'
              ? 'Student Verification'
              : step === 'otp'
                ? 'Enter 6-Digit Code'
                : 'Verified Successfully'
          }}
        </h1>
        <p class="text-xs text-on-surface-variant leading-relaxed">
          Verification protects reviews from spam. Your email address is SHA-256 hashed and never stored with your review text.
        </p>
      </div>

      <div v-if="errorMsg" class="neu-inset rounded-xl p-3 text-xs font-semibold text-error text-left">
        {{ errorMsg }}
      </div>

      <div v-if="successMsg && step === 'otp'" class="neu-inset rounded-xl p-3 text-xs font-semibold text-success text-left">
        {{ successMsg }}
      </div>

      <!-- Step 1: Email -->
      <form v-if="step === 'email'" @submit.prevent="handleSendOTP" class="space-y-4 text-left">
        <div class="space-y-1.5">
          <label for="student-email" class="block text-[11px] font-bold uppercase tracking-wider text-outline">
            Student Email Address
          </label>
          <div class="neu-inset rounded-full flex items-center px-4 py-2.5 gap-2.5">
            <svg viewBox="0 0 20 20" fill="none" class="w-4 h-4 text-outline shrink-0">
              <rect x="3" y="5" width="14" height="10" rx="2" stroke="currentColor" stroke-width="1.5" />
              <path d="M4 6.5L10 11L16 6.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
            </svg>
            <input
              id="student-email"
              v-model="emailInput"
              type="email"
              placeholder="bsse-f22-045@superior.edu.pk"
              class="w-full bg-transparent border-none focus:ring-0 outline-none text-sm text-on-surface placeholder-outline p-0"
              required
              :disabled="isLoading"
            />
          </div>
          <span class="text-[11px] text-outline block pl-1">
            Must end with <strong class="text-on-surface-variant">@superior.edu.pk</strong>
          </span>
        </div>

        <button
          type="submit"
          class="neu-btn-primary w-full py-3 text-xs font-semibold cursor-pointer disabled:opacity-50"
          :disabled="isLoading"
        >
          {{ isLoading ? 'Sending...' : 'Send Verification Code' }}
        </button>
      </form>

      <!-- Step 2: 6 Individual OTP Boxes -->
      <form v-else-if="step === 'otp'" @submit.prevent="handleVerifyOTP" class="space-y-5 text-left">
        <div class="space-y-2">
          <label class="block text-[11px] font-bold uppercase tracking-wider text-outline">
            Enter 6-Digit OTP Code
          </label>
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
              class="neu-inset rounded-xl h-12 text-center font-mono text-lg font-bold tabular-nums text-primary focus:ring-0 focus:outline-none"
            />
          </div>
          <span class="text-[11px] text-outline block text-center">
            Check your student inbox. 5 failed attempts trigger a 15-minute lockout.
          </span>
        </div>

        <div class="flex gap-3">
          <button
            type="button"
            @click="step = 'email'; errorMsg = ''"
            class="neu-pill-btn px-4 py-2.5 text-xs font-semibold cursor-pointer"
            :disabled="isLoading"
          >
            Change
          </button>
          <button
            type="submit"
            class="flex-1 neu-btn-primary py-2.5 text-xs font-semibold cursor-pointer disabled:opacity-50"
            :disabled="isLoading || otpInput.length !== 6"
          >
            {{ isLoading ? 'Verifying...' : 'Verify & Continue' }}
          </button>
        </div>
      </form>

      <!-- Step 3: Verified -->
      <div v-else class="space-y-4">
        <div class="neu-inset-tray p-4 space-y-1">
          <p class="text-xs font-semibold text-success uppercase font-mono">Active Campus Session</p>
          <p class="text-sm font-semibold text-on-surface">
            {{ authStore.email || 'Superior University Student' }}
          </p>
        </div>

        <div class="flex flex-wrap justify-center gap-3 pt-1">
          <router-link to="/review/new" class="neu-btn-primary px-5 py-2.5 text-xs font-semibold">
            Write Review
          </router-link>
          <button
            type="button"
            @click="showLogoutModal = true"
            class="neu-pill-btn px-5 py-2.5 text-xs font-semibold text-error cursor-pointer"
          >
            Unlink / Logout
          </button>
        </div>
      </div>

      <div class="pt-2 flex justify-center gap-4 text-[11px] text-outline">
        <router-link to="/privacy" class="hover:text-primary transition-colors">Privacy Policy</router-link>
        <span>·</span>
        <router-link to="/terms" class="hover:text-primary transition-colors">Terms of Service</router-link>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div
      v-if="showLogoutModal"
      class="fixed inset-0 z-50 bg-on-surface/35 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
    >
      <div class="neu-card p-7 max-w-sm w-full text-center space-y-4">
        <h3 class="text-lg font-bold text-on-surface">Unlink &amp; Log Out?</h3>
        <p class="text-xs text-on-surface-variant leading-relaxed">
          Are you sure you want to unlink your student email? You will need to verify with a new OTP next time you submit a review.
        </p>
        <div class="flex gap-3 pt-1">
          <button
            type="button"
            @click="showLogoutModal = false"
            class="flex-1 neu-pill-btn py-2.5 text-xs font-semibold cursor-pointer"
          >
            Cancel
          </button>
          <button
            type="button"
            @click="confirmLogout"
            class="flex-1 bg-error text-on-primary rounded-full py-2.5 text-xs font-semibold hover:opacity-90 transition-opacity cursor-pointer"
          >
            Yes, Unlink
          </button>
        </div>
      </div>
    </div>
  </main>
</template>
