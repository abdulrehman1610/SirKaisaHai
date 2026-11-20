<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../../stores/auth';
import AppLogo from '../ui/AppLogo.vue';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const searchQuery = ref('');
const isMobileMenuOpen = ref(false);
const showLogoutModal = ref(false);

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

function handleSearchSubmit() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value.trim() } });
  } else {
    router.push('/search');
  }
  isMobileMenuOpen.value = false;
}

function confirmLogout() {
  authStore.logout();
  showLogoutModal.value = false;
  isMobileMenuOpen.value = false;
  router.push('/');
}
</script>

<template>
  <nav class="sticky top-0 z-50 w-full bg-background/95">
    <div class="max-w-container-max mx-auto px-4 md:px-gutter h-20 flex items-center justify-between gap-4">
      <!-- Left: Raised Logo + Recessed Pill Search -->
      <div class="flex items-center gap-6 lg:gap-10 min-w-0 flex-1">
        <router-link to="/" class="shrink-0">
          <AppLogo size="sm" class="md:hidden" />
          <AppLogo size="md" class="hidden md:inline-flex" />
        </router-link>

        <form @submit.prevent="handleSearchSubmit" class="hidden lg:flex items-center neu-inset rounded-full px-4 py-2 w-72 xl:w-80">
          <svg
            viewBox="0 0 20 20"
            fill="none"
            class="w-4 h-4 text-outline shrink-0 mr-2.5"
            aria-hidden="true"
          >
            <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.6" />
            <path d="M13.5 13.5L17 17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
          <input
            v-model="searchQuery"
            class="w-full bg-transparent border-none focus:ring-0 outline-none text-[13px] text-on-surface placeholder-outline p-0"
            placeholder="Search professors or courses"
            type="text"
          />
        </form>
      </div>

      <!-- Right: Clean Nav Links + Raised Soft Pill Verify CTA -->
      <div class="flex items-center gap-4 lg:gap-7 shrink-0">
        <div class="hidden xl:flex items-center gap-7">
          <router-link to="/search" class="nav-link-item" :class="{ active: isProfessorsActive }">
            Browse professors
          </router-link>
          <router-link to="/courses" class="nav-link-item" :class="{ active: isCoursesActive }">
            Browse courses
          </router-link>
          <router-link to="/review/new" class="nav-link-item" :class="{ active: isReviewActive }">
            Write a review
          </router-link>
        </div>

        <div class="flex items-center gap-2.5">
          <router-link
            v-if="!authStore.isVerified"
            to="/auth"
            class="neu-pill-btn px-5 py-2.5 text-[13px] font-semibold text-on-surface whitespace-nowrap"
          >
            <span class="hidden sm:inline">Verify email</span>
            <span class="sm:hidden">Verify</span>
          </router-link>

          <div v-else class="flex items-center gap-2">
            <router-link
              to="/auth"
              class="neu-pill-btn px-4 py-2 text-xs font-semibold text-success inline-flex items-center gap-2"
              title="View Verification Status"
            >
              <span class="w-2 h-2 rounded-full bg-success"></span>
              <span>Verified</span>
            </router-link>
            <button
              type="button"
              @click="showLogoutModal = true"
              class="neu-tile w-9 h-9 flex items-center justify-center text-on-surface-variant hover:text-error transition-colors cursor-pointer"
              title="Unlink Email / Logout"
              aria-label="Unlink Email and Log Out"
            >
              <svg viewBox="0 0 18 18" fill="none" class="w-4 h-4" aria-hidden="true">
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
            class="xl:hidden neu-tile w-9 h-9 flex items-center justify-center text-on-surface-variant hover:text-primary cursor-pointer"
            :aria-expanded="isMobileMenuOpen"
            aria-label="Toggle navigation menu"
          >
            <svg v-if="!isMobileMenuOpen" viewBox="0 0 20 20" fill="none" class="w-5 h-5">
              <path d="M3.5 6H16.5M3.5 10H16.5M3.5 14H16.5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
            </svg>
            <svg v-else viewBox="0 0 20 20" fill="none" class="w-5 h-5">
              <path d="M5 5L15 15M15 5L5 15" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Drawer -->
    <div v-if="isMobileMenuOpen" class="xl:hidden px-4 pb-4">
      <div class="neu-card p-4 flex flex-col gap-2 max-w-container-max mx-auto">
        <form @submit.prevent="handleSearchSubmit" class="flex lg:hidden items-center neu-inset rounded-full px-4 py-2 mb-1">
          <svg viewBox="0 0 20 20" fill="none" class="w-4 h-4 text-outline shrink-0 mr-2.5">
            <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.6" />
            <path d="M13.5 13.5L17 17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
          <input
            v-model="searchQuery"
            class="w-full bg-transparent border-none focus:ring-0 outline-none text-sm text-on-surface placeholder-outline p-0"
            placeholder="Search professors or courses"
            type="text"
          />
        </form>

        <router-link to="/search" class="mobile-nav-link" :class="{ active: isProfessorsActive }">
          Browse professors
        </router-link>
        <router-link to="/courses" class="mobile-nav-link" :class="{ active: isCoursesActive }">
          Browse courses
        </router-link>
        <router-link to="/review/new" class="mobile-nav-link" :class="{ active: isReviewActive }">
          Write a review
        </router-link>
        <router-link to="/auth" class="mobile-nav-link">
          Student verification
        </router-link>
      </div>
    </div>
  </nav>

  <!-- Logout Modal -->
  <div
    v-if="showLogoutModal"
    class="fixed inset-0 z-50 bg-on-surface/35 flex items-center justify-center p-4"
    role="dialog"
    aria-modal="true"
  >
    <div class="neu-card p-7 max-w-sm w-full text-center space-y-4">
      <div class="neu-tile w-12 h-12 mx-auto flex items-center justify-center text-error">
        <svg viewBox="0 0 20 20" fill="none" class="w-5 h-5">
          <path d="M8 4H5C4.45 4 4 4.45 4 5V15C4 15.55 4.45 16 5 16H8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          <path d="M12.5 7L15.5 10L12.5 13M15.5 10H8" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
      <div class="space-y-1.5">
        <h3 class="text-lg font-bold text-on-surface">Unlink &amp; Log Out?</h3>
        <p class="text-xs text-on-surface-variant leading-relaxed">
          Are you sure you want to unlink your student email? You will need a fresh OTP the next time you submit a review.
        </p>
      </div>
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
</template>

<style scoped>
.nav-link-item {
  font-size: 13px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: color 0.18s ease;
  text-decoration: none;
}

.nav-link-item:hover,
.nav-link-item.active {
  color: var(--primary);
}

.nav-link-item.active {
  font-weight: 700;
}

.mobile-nav-link {
  display: block;
  padding: 10px 14px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  transition: color 0.18s ease, box-shadow 0.18s ease;
}

.mobile-nav-link:hover,
.mobile-nav-link.active {
  color: var(--primary);
  font-weight: 600;
  box-shadow:
    inset 3px 3px 6px var(--neu-shadow-dark-soft),
    inset -3px -3px 6px var(--neu-shadow-light);
}
</style>
