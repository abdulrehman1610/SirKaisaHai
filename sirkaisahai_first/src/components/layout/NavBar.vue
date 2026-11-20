<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import AppLogo from '../ui/AppLogo.vue';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const isMobileMenuOpen = ref(false);
const showLogoutModal = ref(false);

const isHomeActive = computed(() => route.path === '/');

const isProfessorsActive = computed(() => {
  return (route.path === '/search' && route.query.tab !== 'courses') || route.name === 'professor-detail';
});

const isCoursesActive = computed(() => {
  return route.path === '/courses' || route.name === 'course-detail' || route.query.tab === 'courses';
});

const isReviewActive = computed(() => {
  return route.path === '/review/new' || route.query.redirect === '/review/new';
});

watch(
  () => route.path,
  () => {
    isMobileMenuOpen.value = false;
  }
);

function confirmLogout() {
  authStore.logout();
  showLogoutModal.value = false;
  isMobileMenuOpen.value = false;
  router.push('/');
}
</script>

<template>
  <header class="sticky top-0 z-50 w-full bg-band-hero/95 pt-3.5 pb-2 px-4 md:px-gutter">
    <div class="max-w-container-max mx-auto">
      <nav class="ed-pill-nav px-4 sm:px-6 h-14 flex items-center justify-between gap-4">
        <!-- Left: Brand Wordmark + Stacked University Tag -->
        <router-link to="/" class="shrink-0">
          <AppLogo size="md" :show-subtag="true" />
        </router-link>

        <!-- Center Nav Links -->
        <div class="hidden lg:flex items-center gap-7">
          <router-link to="/" class="nav-link-item" :class="{ active: isHomeActive }">
            Home
          </router-link>
          <router-link to="/search" class="nav-link-item" :class="{ active: isProfessorsActive }">
            Browse professors
          </router-link>
          <router-link to="/courses" class="nav-link-item" :class="{ active: isCoursesActive }">
            Browse courses
          </router-link>
          <router-link
            to="/review/new"
            class="nav-link-item inline-flex items-center gap-1"
            :class="{ active: isReviewActive }"
          >
            <span>Write a review</span>
            <span class="text-[11px] opacity-75" aria-hidden="true">↗</span>
          </router-link>
        </div>

        <!-- Right: Verify Email Pill + Mobile Toggle -->
        <div class="flex items-center gap-2 shrink-0">
          <router-link
            v-if="!authStore.isVerified"
            to="/auth"
            class="ed-btn-soft px-4 py-2 text-xs font-semibold inline-flex items-center gap-2 whitespace-nowrap"
          >
            <span class="hidden sm:inline">Verify email</span>
            <span class="sm:hidden">Verify</span>
            <span aria-hidden="true">→</span>
          </router-link>

          <div v-else class="flex items-center gap-2">
            <router-link
              to="/auth"
              class="ed-btn-soft px-3.5 py-1.5 text-xs font-semibold text-success inline-flex items-center gap-1.5"
              title="View Verification Status"
            >
              <span class="w-1.5 h-1.5 rounded-full bg-success"></span>
              <span>Verified</span>
            </router-link>
            <button
              type="button"
              @click="showLogoutModal = true"
              class="ed-btn-soft w-8 h-8 flex items-center justify-center text-ink-muted hover:text-error cursor-pointer"
              title="Unlink Email / Logout"
              aria-label="Unlink Email and Log Out"
            >
              <svg viewBox="0 0 18 18" fill="none" class="w-3.5 h-3.5" aria-hidden="true">
                <path
                  d="M7 3H4.5C3.95 3 3.5 3.45 3.5 4V14C3.5 14.55 3.95 15 4.5 15H7"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                />
                <path
                  d="M11.5 6L14.5 9L11.5 12M14.5 9H7"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </button>
          </div>

          <button
            type="button"
            @click="isMobileMenuOpen = !isMobileMenuOpen"
            class="lg:hidden ed-btn-soft w-9 h-9 flex items-center justify-center text-ink-dark cursor-pointer"
            :aria-expanded="isMobileMenuOpen"
            aria-label="Toggle navigation menu"
          >
            <svg v-if="!isMobileMenuOpen" viewBox="0 0 20 20" fill="none" class="w-4 h-4">
              <path d="M3.5 6H16.5M3.5 10H16.5M3.5 14H16.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
            </svg>
            <svg v-else viewBox="0 0 20 20" fill="none" class="w-4 h-4">
              <path d="M5 5L15 15M15 5L5 15" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
            </svg>
          </button>
        </div>
      </nav>

      <!-- Mobile Menu -->
      <div v-if="isMobileMenuOpen" class="lg:hidden mt-2.5 ed-card p-3 flex flex-col gap-1">
        <router-link to="/" class="mobile-nav-link" :class="{ active: isHomeActive }">Home</router-link>
        <router-link to="/search" class="mobile-nav-link" :class="{ active: isProfessorsActive }">Browse professors</router-link>
        <router-link to="/courses" class="mobile-nav-link" :class="{ active: isCoursesActive }">Browse courses</router-link>
        <router-link to="/review/new" class="mobile-nav-link" :class="{ active: isReviewActive }">Write a review ↗</router-link>
        <router-link to="/auth" class="mobile-nav-link">Student verification</router-link>
      </div>
    </div>
  </header>

  <!-- Logout Confirmation Modal -->
  <div
    v-if="showLogoutModal"
    class="fixed inset-0 z-50 bg-ink-dark/40 flex items-center justify-center p-4"
    role="dialog"
    aria-modal="true"
  >
    <div class="ed-card p-7 max-w-sm w-full text-center space-y-4">
      <div class="space-y-1.5">
        <h3 class="text-xl font-bold text-ink-dark">Unlink &amp; Log Out?</h3>
        <p class="text-xs text-ink-muted leading-relaxed">
          Your browser session will be cleared immediately. You will need a fresh 6-digit OTP next time you post a review.
        </p>
      </div>
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
          class="flex-1 bg-error text-on-primary rounded-full py-2.5 text-xs font-semibold hover:opacity-90 transition-opacity cursor-pointer"
        >
          Yes, Unlink
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.nav-link-item {
  position: relative;
  padding: 4px 0;
  font-size: 13px;
  font-weight: 500;
  color: var(--ink-muted);
  transition: color 0.16s ease;
  text-decoration: none;
}

.nav-link-item:hover {
  color: var(--ink-dark);
}

.nav-link-item.active {
  color: var(--ink-dark);
  font-weight: 700;
}

.nav-link-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 1.5px;
  background-color: var(--ink-dark);
}

.mobile-nav-link {
  display: block;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  color: var(--ink-muted);
  transition: background-color 0.16s ease, color 0.16s ease;
}

.mobile-nav-link:hover,
.mobile-nav-link.active {
  background: var(--primary-soft);
  color: var(--primary);
  font-weight: 700;
}
</style>
