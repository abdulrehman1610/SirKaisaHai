<script setup lang="ts">
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const step = ref<'email' | 'otp' | 'success'>(authStore.isVerified ? 'success' : 'email');
const emailInput = ref(authStore.email || '');
const otpInput = ref('');
const isLoading = ref(false);
const errorMsg = ref('');
const successMsg = ref('');

const redirectPath = (route.query.redirect as string) || '/';

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
      step.value = 'otp';
    } else {
      errorMsg.value = res.message;
    }
  } finally {
    isLoading.value = false;
  }
}

async function handleVerifyOTP() {
  errorMsg.value = '';
  if (!otpInput.value.trim()) {
    errorMsg.value = 'Please enter the 6-digit verification code.';
    return;
  }

  isLoading.value = true;
  try {
    const res = await authStore.verifyOTP(otpInput.value);
    if (res.success) {
      step.value = 'success';
      setTimeout(() => {
        router.push(redirectPath);
      }, 1400);
    } else {
      errorMsg.value = res.message || 'Verification failed.';
    }
  } finally {
    isLoading.value = false;
  }
}

const showLogoutModal = ref(false);

function confirmLogout() {
  authStore.logout();
  showLogoutModal.value = false;
  step.value = 'email';
  emailInput.value = '';
  otpInput.value = '';
}
</script>

<template>
  <main class="max-w-container-max mx-auto px-gutter py-stack-lg flex items-center justify-center min-h-[75vh]">
    <div class="bg-white rounded-3xl p-8 md:p-12 custom-shadow shadow-2xl-ambient max-w-md w-full text-center">
      <div class="inline-block p-4 bg-primary-container/10 rounded-full text-primary mb-4">
        <span class="material-symbols-outlined text-4xl">verified_user</span>
      </div>

      <h1 class="font-headline-lg text-headline-lg text-primary mb-2">Student Verification</h1>
      <p class="font-body-md text-body-md text-on-surface-variant mb-6">
        Verification protects reviews from spam. Your email address is SHA-256 hashed and <strong>never stored</strong> with your review text.
      </p>

      <div v-if="errorMsg" class="p-4 mb-4 bg-red-50 border border-red-200 text-red-700 rounded-2xl text-sm font-bold text-left">
        ⚠️ {{ errorMsg }}
      </div>

      <div v-if="successMsg && step === 'otp'" class="p-4 mb-4 bg-blue-50 border border-blue-200 text-blue-700 rounded-2xl text-sm font-bold text-left">
        📩 {{ successMsg }}
      </div>

      <!-- Step 1: Email -->
      <form v-if="step === 'email'" @submit.prevent="handleSendOTP" class="space-y-4 text-left">
        <div>
          <label class="block font-label-sm text-xs uppercase text-on-surface-variant font-bold mb-2">
            Student Email Address
          </label>
          <div class="relative">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-outline">mail</span>
            <input
              v-model="emailInput"
              type="email"
              placeholder="bsse-f22-045@superior.edu.pk"
              class="w-full bg-surface-container-low border border-outline-variant/30 rounded-xl py-3 pl-12 pr-4 text-on-surface font-body-md focus:ring-2 focus:ring-primary outline-none"
              required
              :disabled="isLoading"
            />
          </div>
          <span class="text-xs text-outline mt-1 block">Must end with <strong>@superior.edu.pk</strong></span>
        </div>

        <button
          type="submit"
          class="w-full bg-primary text-white py-3.5 rounded-full font-label-sm text-sm font-bold hover:bg-[#6B2FA0] transition-colors shadow-lg disabled:opacity-50"
          :disabled="isLoading"
        >
          <span v-if="!isLoading">Send Verification Code →</span>
          <span v-else>Sending...</span>
        </button>
      </form>

      <!-- Step 2: OTP -->
      <form v-else-if="step === 'otp'" @submit.prevent="handleVerifyOTP" class="space-y-4 text-left">
        <div>
          <label class="block font-label-sm text-xs uppercase text-on-surface-variant font-bold mb-2">
            Enter 6-Digit OTP Code
          </label>
          <input
            v-model="otpInput"
            type="text"
            placeholder="6-digit code"
            maxlength="6"
            class="w-full text-center font-stat-display text-2xl tracking-[0.3em] bg-surface-container-low border-2 border-outline-variant/30 rounded-xl p-3 text-on-surface focus:ring-2 focus:ring-primary outline-none"
            required
            :disabled="isLoading"
          />
          <span class="text-xs text-outline mt-1 block text-center">Check your student email inbox or terminal log for code</span>
        </div>

        <div class="flex gap-3">
          <button type="button" @click="step = 'email'" class="px-4 py-3 rounded-full font-label-sm text-xs border border-outline-variant/30 text-on-surface-variant font-bold" :disabled="isLoading">
            ← Change
          </button>
          <button
            type="submit"
            class="flex-1 bg-primary text-white py-3 rounded-full font-label-sm text-sm font-bold hover:bg-[#6B2FA0] transition-colors shadow-lg disabled:opacity-50"
            :disabled="isLoading"
          >
            <span v-if="!isLoading">Verify & Continue</span>
            <span v-else>Verifying...</span>
          </button>
        </div>
      </form>

      <!-- Step 3: Success -->
      <div v-else-if="step === 'success'" class="space-y-4">
        <div class="w-16 h-16 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto text-3xl font-bold">
          ✓
        </div>
        <h3 class="text-xl font-bold text-on-surface">Verified Successfully!</h3>
        <p class="text-sm text-on-surface-variant">Verified as <strong>{{ authStore.email }}</strong></p>

        <button @click="showLogoutModal = true" class="text-xs text-red-600 underline font-bold pt-2 hover:text-red-700">
          Unlink Email / Logout
        </button>
      </div>
    </div>

    <!-- Confirmation Modal -->
    <div v-if="showLogoutModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-white rounded-3xl p-8 max-w-sm w-full shadow-2xl relative text-center animate-in fade-in zoom-in duration-200">
        <div class="w-16 h-16 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto text-3xl mb-4">
          <span class="material-symbols-outlined text-[32px]">logout</span>
        </div>

        <h3 class="font-headline-lg text-xl font-bold text-on-surface mb-2">Unlink & Log Out?</h3>
        <p class="text-xs text-on-surface-variant leading-relaxed mb-6">
          Are you sure you want to unlink your student email? You will need to verify with a new OTP next time you submit a review.
        </p>

        <div class="flex gap-3">
          <button
            type="button"
            @click="showLogoutModal = false"
            class="flex-1 px-4 py-3 rounded-full text-xs font-bold border border-outline-variant/40 text-on-surface hover:bg-surface-variant transition-colors"
          >
            Cancel
          </button>
          <button
            type="button"
            @click="confirmLogout"
            class="flex-1 bg-red-600 text-white py-3 rounded-full text-xs font-bold hover:bg-red-700 transition-colors shadow-md"
          >
            Yes, Unlink
          </button>
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped></style>
