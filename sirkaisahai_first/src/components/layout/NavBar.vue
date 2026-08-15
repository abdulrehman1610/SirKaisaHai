<script setup lang="ts">
import { ref, computed, watch } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '../../stores/auth';

import AppLogo from '../ui/AppLogo.vue';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();
const searchQuery = ref('');

// Mobile menu state
const isMobileMenuOpen = ref(false);

const isProfessorsActive = computed(() => {
  return (
    (route.path === '/search' && route.query.tab !== 'courses') ||
    route.name === 'professor-detail'
  );
});

const isCoursesActive = computed(() => {
  return (
    route.path === '/courses' ||
    route.name === 'course-detail' ||
    route.query.tab === 'courses'
  );
});

const isReviewActive = computed(() => {
  return (
    route.path === '/review/new' ||
    route.query.redirect === '/review/new'
  );
});

// Close mobile menu on route change
watch(() => route.path, () => {
  isMobileMenuOpen.value = false;
});

function handleSearchSubmit() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value.trim() } });
  }
  isMobileMenuOpen.value = false;
}

const showLogoutModal = ref(false);

function confirmLogout() {
  authStore.logout();
  showLogoutModal.value = false;
  isMobileMenuOpen.value = false;
  router.push('/');
}
</script>

<template>
  <nav class="sticky top-0 z-50 w-full bg-white/80 backdrop-blur-md border-b border-outline-variant/20">
    <div class="max-w-container-max mx-auto px-4 md:px-gutter h-16 md:h-20 flex items-center justify-between">
      <div class="flex items-center gap-4 md:gap-12">
        <router-link to="/" class="transition-transform active:scale-95">
          <AppLogo size="sm" class="md:hidden" />
          <AppLogo size="md" class="hidden md:inline-flex" />
        </router-link>

        <form @submit.prevent="handleSearchSubmit" class="relative hidden lg:block group">
          <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant/40 group-focus-within:text-primary transition-colors">
            search
          </span>
          <input
            v-model="searchQuery"
            class="bg-surface-container-low border border-outline-variant/30 rounded-xl py-2.5 pl-12 pr-4 text-on-surface font-body-md placeholder-on-surface-variant/40 focus:ring-2 focus:ring-primary/20 focus:border-primary/40 transition-all w-72 focus:w-96 outline-none"
            placeholder="Search professors or courses..."
            type="text"
          />
        </form>
      </div>

      <div class="flex items-center gap-3 md:gap-8">
        <!-- Desktop Nav Links -->
        <div class="hidden xl:flex items-center gap-8">
          <router-link
            to="/search"
            class="nav-link-item"
            :class="{ active: isProfessorsActive }"
          >
            Browse Professors
          </router-link>

          <router-link
            to="/courses"
            class="nav-link-item"
            :class="{ active: isCoursesActive }"
          >
            Browse Courses
          </router-link>

          <router-link
            to="/review/new"
            class="nav-link-item"
            :class="{ active: isReviewActive }"
          >
            Write a Review
          </router-link>
        </div>

        <div class="h-6 w-px bg-outline-variant/30 hidden xl:block"></div>

        <!-- Auth Buttons (always visible) -->
        <div class="flex items-center gap-2 md:gap-4">
          <router-link v-if="!authStore.isVerified" to="/auth" class="bg-primary text-on-primary px-4 md:px-6 py-2 md:py-2.5 rounded-full font-label-sm text-[11px] md:text-label-sm hover:bg-[#6B2FA0] shadow-lg shadow-primary/20 transition-all active:scale-95 flex items-center gap-1.5">
            <span class="material-symbols-outlined text-[16px] md:text-[18px]">verified_user</span>
            <span class="hidden sm:inline">Verify Email</span>
            <span class="sm:hidden">Verify</span>
          </router-link>

          <div v-else class="flex items-center gap-1.5 md:gap-2">
            <router-link to="/auth" class="bg-green-100 text-green-700 px-3 py-1.5 md:px-4 md:py-2 rounded-full font-label-sm text-[10px] md:text-xs font-bold flex items-center gap-1 hover:bg-green-200 transition-all" title="View Verification Status">
              <span class="material-symbols-outlined text-[14px] md:text-[16px]">check_circle</span>
              <span class="hidden sm:inline">Verified</span>
            </router-link>
            <button
              @click="showLogoutModal = true"
              class="p-1.5 md:p-2 text-on-surface-variant hover:text-red-600 hover:bg-red-50 rounded-full transition-colors flex items-center"
              title="Unlink Email / Logout"
            >
              <span class="material-symbols-outlined text-[18px] md:text-[20px]">logout</span>
            </button>
          </div>

          <!-- Mobile Hamburger Button -->
          <button
            @click="isMobileMenuOpen = !isMobileMenuOpen"
            class="xl:hidden p-2 text-on-surface-variant hover:text-primary hover:bg-primary/5 rounded-xl transition-colors flex items-center"
            :aria-expanded="isMobileMenuOpen"
            aria-label="Toggle navigation menu"
          >
            <span class="material-symbols-outlined text-[24px]">
              {{ isMobileMenuOpen ? 'close' : 'menu' }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu Dropdown -->
    <transition name="mobile-menu">
      <div v-if="isMobileMenuOpen" class="xl:hidden bg-white/95 backdrop-blur-xl border-t border-outline-variant/10 shadow-2xl">
        <div class="max-w-container-max mx-auto px-4 py-4 flex flex-col gap-2">
          <!-- Mobile Search -->
          <form @submit.prevent="handleSearchSubmit" class="relative lg:hidden mb-2">
            <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-on-surface-variant/40">
              search
            </span>
            <input
              v-model="searchQuery"
              class="w-full bg-surface-container-low border border-outline-variant/30 rounded-xl py-3 pl-12 pr-4 text-on-surface font-body-md placeholder-on-surface-variant/40 focus:ring-2 focus:ring-primary/20 focus:border-primary/40 outline-none"
              placeholder="Search professors..."
              type="text"
            />
          </form>

          <!-- Mobile Nav Links -->
          <router-link
            to="/search"
            class="mobile-nav-link"
            :class="{ 'mobile-nav-link-active': isProfessorsActive }"
          >
            <span class="material-symbols-outlined text-[20px]">person_search</span>
            Browse Professors
          </router-link>

          <router-link
            to="/courses"
            class="mobile-nav-link"
            :class="{ 'mobile-nav-link-active': isCoursesActive }"
          >
            <span class="material-symbols-outlined text-[20px]">school</span>
            Browse Courses
          </router-link>

          <router-link
            to="/review/new"
            class="mobile-nav-link"
            :class="{ 'mobile-nav-link-active': isReviewActive }"
          >
            <span class="material-symbols-outlined text-[20px]">rate_review</span>
            Write a Review
          </router-link>

          <router-link
            to="/auth"
            class="mobile-nav-link"
          >
            <span class="material-symbols-outlined text-[20px]">verified_user</span>
            Student Verification
          </router-link>
        </div>
      </div>
    </transition>
  </nav>

  <!-- Logout Confirmation Modal -->
  <div v-if="showLogoutModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl p-6 md:p-8 max-w-sm w-full shadow-2xl relative text-center animate-in fade-in zoom-in duration-200">
      <div class="w-14 h-14 md:w-16 md:h-16 bg-red-100 text-red-600 rounded-full flex items-center justify-center mx-auto text-3xl mb-4">
        <span class="material-symbols-outlined text-[28px] md:text-[32px]">logout</span>
      </div>

      <h3 class="font-headline-lg text-lg md:text-xl font-bold text-on-surface mb-2">Unlink & Log Out?</h3>
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
</template>

<style scoped>
.nav-link-item {
  position: relative;
  padding-bottom: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  letter-spacing: 0.05em;
  font-weight: 500;
  color: rgba(80, 67, 75, 0.7);
  transition: all 0.2s ease;
  text-decoration: none;
}

.nav-link-item:hover {
  color: #501243;
}

.nav-link-item.active {
  color: #501243;
  font-weight: 700;
}

.nav-link-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2.5px;
  background-color: #501243;
  border-radius: 2px;
}

/* Mobile Nav Styles */
.mobile-nav-link {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border-radius: 12px;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  font-weight: 600;
  color: rgba(80, 67, 75, 0.8);
  transition: all 0.2s ease;
}

.mobile-nav-link:hover,
.mobile-nav-link:active {
  background: rgba(80, 18, 67, 0.05);
  color: #501243;
}

.mobile-nav-link-active {
  background: rgba(80, 18, 67, 0.08);
  color: #501243;
  font-weight: 700;
}

/* Mobile menu transition */
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition: all 0.25s ease;
  transform-origin: top;
}

.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
