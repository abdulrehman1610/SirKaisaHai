import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { api } from '../api';

export const useAuthStore = defineStore('auth', () => {
  const email = ref<string>(localStorage.getItem('skh_user_email') || '');
  const isVerified = ref<boolean>(false);
  // We no longer store the token directly in the client — it lives in the httpOnly cookie!
  const isInitializing = ref<boolean>(true);

  const universityDomain = 'superior.edu.pk';

  const isValidSuperiorEmail = computed(() => {
    return email.value.trim().toLowerCase().endsWith(`@${universityDomain}`);
  });

  async function initSession() {
    isInitializing.value = true;
    try {
      const session = await api.checkSession();
      if (session.authenticated) {
        isVerified.value = true;
      } else {
        isVerified.value = false;
        email.value = '';
        localStorage.removeItem('skh_user_email');
      }
    } finally {
      isInitializing.value = false;
    }
  }

  async function requestOTP(targetEmail: string) {
    email.value = targetEmail.trim();
    const res = await api.sendOTP(email.value);
    return res;
  }

  async function verifyOTP(code: string) {
    const res = await api.verifyOTP(email.value, code);
    if (res.success) {
      isVerified.value = true;
      if (res.email) {
        email.value = res.email;
        localStorage.setItem('skh_user_email', res.email);
      }
    }
    return res;
  }

  async function logout() {
    await api.logout(); // Clear cookie on server
    isVerified.value = false;
    email.value = '';
    localStorage.removeItem('skh_user_email');
  }

  // Initialize session on store creation
  initSession();

  return {
    email,
    isVerified,
    isInitializing,
    isValidSuperiorEmail,
    requestOTP,
    verifyOTP,
    logout,
    initSession
  };
});
