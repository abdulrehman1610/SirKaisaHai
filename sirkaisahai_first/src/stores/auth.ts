import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { api } from '../api';

function maskEmailDisplay(raw: string): string {
  const cleaned = raw.trim().toLowerCase();
  if (!cleaned.includes('@')) return cleaned;
  const [local, domain] = cleaned.split('@');
  if (!local || local.includes('***')) return cleaned;
  const maskedLocal =
    local.length <= 4 ? `${local[0] || ''}***` : `${local.slice(0, 2)}***${local.slice(-2)}`;
  return `${maskedLocal}@${domain}`;
}

export const useAuthStore = defineStore('auth', () => {
  const email = ref<string>(localStorage.getItem('skh_user_email') || '');
  const pendingEmail = ref<string>('');
  const isVerified = ref<boolean>(false);
  // Session token lives exclusively in the httpOnly skh_session cookie!
  const isInitializing = ref<boolean>(true);

  const universityDomain = 'superior.edu.pk';

  const isValidSuperiorEmail = computed(() => {
    return email.value.trim().toLowerCase().endsWith(`@${universityDomain}`);
  });

  function clearLocalSession() {
    isVerified.value = false;
    email.value = '';
    pendingEmail.value = '';
    localStorage.removeItem('skh_user_email');
  }

  async function initSession() {
    isInitializing.value = true;
    try {
      const session = await api.checkSession();
      if (session.authenticated) {
        isVerified.value = true;
      } else {
        clearLocalSession();
      }
    } finally {
      isInitializing.value = false;
    }
  }

  async function requestOTP(targetEmail: string) {
    pendingEmail.value = targetEmail.trim().toLowerCase();
    const res = await api.sendOTP(pendingEmail.value);
    return res;
  }

  async function verifyOTP(code: string) {
    const target = pendingEmail.value || email.value;
    const res = await api.verifyOTP(target, code);
    if (res.success) {
      isVerified.value = true;
      const masked = maskEmailDisplay(res.email || target);
      email.value = masked;
      pendingEmail.value = '';
      localStorage.setItem('skh_user_email', masked);
    }
    return res;
  }

  async function logout() {
    await api.logout(); // Immediately invalidate session on server and clear cookie
    clearLocalSession();
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
    clearLocalSession,
    initSession
  };
});
