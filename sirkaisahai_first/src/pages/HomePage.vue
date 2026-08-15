<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import type { Professor, Review } from '../types';
import { api } from '../api';

const router = useRouter();
const searchQuery = ref('');
const featuredProf = ref<Professor | null>(null);
const reviewsList = ref<Review[]>([]);
const isLoading = ref(true);

// Animated Slang Headlines
const slogans = [
  "Kon Sir Kaisa Hai?",
  "Asli Scene Kya Hai?",
  "GPA Bachao, Real Feedback Paao.",
  "Strict Attendance Ya Chill Scenes?",
  "Easy Grading Ya Surprise Quizzes?"
];
const currentSloganIndex = ref(0);
let sloganInterval: any = null;

onMounted(async () => {
  sloganInterval = setInterval(() => {
    currentSloganIndex.value = (currentSloganIndex.value + 1) % slogans.length;
  }, 3000);

  try {
    const profs = await api.search('');
    if (profs.length > 0) {
      // Find top rated professor from live database
      const sorted = [...profs].sort((a, b) => b.rating - a.rating);
      const topProfId = sorted[0]?.id;
      if (topProfId) {
        const topProf = await api.getProfessorById(topProfId);
        if (topProf) featuredProf.value = topProf;
      }
    }
    // Fetch real live reviews from database
    const realReviews = await api.getRecentReviews();
    reviewsList.value = realReviews;
  } finally {
    isLoading.value = false;
  }
});

onUnmounted(() => {
  if (sloganInterval) clearInterval(sloganInterval);
});

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value.trim() } });
  } else {
    router.push('/search');
  }
}
</script>

<template>
  <div class="max-w-container-max mx-auto px-4 md:px-gutter pb-16 md:pb-32">
    <!-- Hero Section -->
    <section class="py-8 md:py-24 relative overflow-hidden rounded-2xl md:rounded-3xl mt-4 md:mt-stack-md">
      <div class="absolute inset-0 bg-gradient-to-br from-primary-container/20 to-transparent rounded-3xl pointer-events-none"></div>
      <div class="relative z-10 flex flex-col items-center text-center max-w-3xl mx-auto space-y-4 md:space-y-stack-md px-2">
        
        <!-- Animated Rotating Student Slang Headline -->
        <div class="h-16 md:h-28 flex items-center justify-center overflow-hidden">
          <transition name="slogan-fade" mode="out-in">
            <h1
              :key="currentSloganIndex"
              class="font-display-lg md:text-5xl text-xl sm:text-2xl font-extrabold text-[#6B2A5B] tracking-tight leading-tight"
            >
              {{ slogans[currentSloganIndex] }}
            </h1>
          </transition>
        </div>

        <p class="font-body-lg text-sm md:text-body-lg text-on-surface-variant max-w-xl px-2">
          Real, unfiltered & anonymous teacher reviews by Superior University students. Know your professors before registering!
        </p>

        <!-- Glassmorphic Search -->
        <form @submit.prevent="handleSearch" class="glass-panel w-full max-w-2xl rounded-full p-1.5 md:p-2 flex items-center shadow-lg relative mt-4 md:mt-6 transition-all hover:shadow-2xl-ambient">
          <span class="material-symbols-outlined pl-3 md:pl-4 text-primary opacity-60 text-[20px] md:text-[24px]">search</span>
          <input
            v-model="searchQuery"
            class="flex-1 bg-transparent border-none focus:ring-0 text-on-surface text-sm md:text-body-lg py-2.5 md:py-3 px-3 md:px-4 placeholder-on-surface/40 outline-none min-w-0"
            placeholder="Search teacher..."
            type="text"
          />
          <button type="submit" class="bg-primary text-on-primary rounded-full px-5 md:px-8 py-2.5 md:py-3 font-label-sm text-[11px] md:text-label-sm hover:bg-[#6B2FA0] transition-colors duration-300 whitespace-nowrap">
            Search
          </button>
        </form>

        <!-- Floating Action Chips -->
        <div class="flex flex-wrap justify-center gap-2 md:gap-3 mt-4 md:mt-8">
          <router-link to="/search" class="glass-panel px-3 md:px-4 py-1.5 md:py-2 rounded-full font-label-sm text-[10px] md:text-label-sm text-primary flex items-center gap-1.5 md:gap-2 hover:bg-white transition-colors">
            <span class="material-symbols-outlined text-[14px] md:text-[16px]">person_search</span> Browse
          </router-link>
          <router-link to="/review/new" class="glass-panel px-3 md:px-4 py-1.5 md:py-2 rounded-full font-label-sm text-[10px] md:text-label-sm text-primary flex items-center gap-1.5 md:gap-2 hover:bg-white transition-colors">
            <span class="material-symbols-outlined text-[14px] md:text-[16px]">rate_review</span> Review
          </router-link>
          <router-link to="/auth" class="glass-panel px-3 md:px-4 py-1.5 md:py-2 rounded-full font-label-sm text-[10px] md:text-label-sm text-primary flex items-center gap-1.5 md:gap-2 hover:bg-white transition-colors">
            <span class="material-symbols-outlined text-[14px] md:text-[16px]">verified_user</span> Verify
          </router-link>
        </div>
      </div>
    </section>

    <!-- Featured Professor Profile Section (Bento Grid) -->
    <section v-if="featuredProf" class="mt-stack-lg">
      <div class="flex justify-between items-end mb-4 border-b border-surface-variant pb-2">
        <h2 class="font-headline-md text-headline-md font-bold text-on-surface">
          Top Rated Faculty
        </h2>
        <router-link to="/search" class="font-label-sm text-label-sm text-primary font-bold hover:underline">
          View All →
        </router-link>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-stack-md">
        <!-- Main Identity Card -->
        <div class="lg:col-span-8 bg-surface-container-lowest rounded-2xl md:rounded-3xl p-5 md:p-8 shadow-2xl-ambient flex flex-col md:flex-row items-center gap-5 md:gap-8 relative overflow-hidden">
          <div class="absolute -right-20 -top-20 w-64 h-64 bg-secondary-container/20 rounded-full blur-3xl pointer-events-none"></div>
          <div class="relative shrink-0">
            <div class="w-20 h-20 md:w-32 md:h-32 rounded-full overflow-hidden border-4 border-surface-bright bg-primary text-white flex items-center justify-center font-display-lg text-xl md:text-3xl font-extrabold">
              {{ featuredProf.name.split(' ').map(n => n[0]).slice(0, 2).join('') }}
            </div>
            <div class="absolute -bottom-2 -right-2 bg-white rounded-full p-1 shadow-lg">
              <span class="material-symbols-outlined text-green-600 bg-green-100 rounded-full p-1" style="font-variation-settings: 'FILL' 1;">verified</span>
            </div>
          </div>
          <div class="flex-1">
            <h2 class="font-headline-lg text-lg md:text-headline-lg text-primary mb-1 text-center md:text-left">
              <router-link :to="`/professor/${featuredProf.id}`" class="hover:underline">
                {{ featuredProf.name }}
              </router-link>
            </h2>
            <p class="font-body-lg text-sm md:text-body-lg text-on-surface-variant flex items-center justify-center md:justify-start gap-2 mb-3 md:mb-4">
              <span class="material-symbols-outlined text-[16px] md:text-[18px]">domain</span> {{ featuredProf.departmentName }}
            </p>
            <div class="flex flex-wrap justify-center md:justify-start gap-2">
              <span v-for="tag in featuredProf.tags" :key="tag" class="bg-surface-container text-on-surface-variant px-3 py-1 rounded-full font-label-sm text-label-sm border border-outline-variant/30">
                {{ tag }}
              </span>
            </div>
          </div>
          <!-- Recommendation Ring -->
          <div class="flex flex-col items-center justify-center shrink-0 w-24 h-24 md:w-32 md:h-32 relative">
            <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle cx="50" cy="50" fill="none" r="45" stroke="#f3f4f6" stroke-width="8"></circle>
              <circle class="transition-all duration-1000 ease-out drop-shadow-md" cx="50" cy="50" fill="none" r="45" stroke="#2E9E4F" stroke-dasharray="283" stroke-dashoffset="17" stroke-linecap="round" stroke-width="8"></circle>
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center">
              <span class="font-stat-display text-stat-display text-primary">
                {{ Math.round((featuredProf.overallRating / 5) * 100) }}%
              </span>
            </div>
            <span class="absolute -bottom-5 md:-bottom-6 font-label-sm text-[10px] md:text-label-sm text-on-surface-variant text-center w-full">Recommend</span>
          </div>
        </div>

        <!-- Stat Boxes Grid -->
        <div class="lg:col-span-4 grid grid-cols-2 gap-3 md:gap-4">
          <div class="bg-[#EFE5FA] rounded-xl md:rounded-2xl p-3 md:p-4 flex flex-col justify-between h-24 md:h-32 transition-transform hover:scale-[1.02]">
            <div class="flex justify-between items-start">
              <span class="font-label-sm text-label-sm text-on-surface-variant uppercase">Overall</span>
              <span class="material-symbols-outlined text-green-600 text-[16px]">trending_up</span>
            </div>
            <div class="font-stat-display text-xl md:text-stat-display text-[#6B2FA0]">
              {{ featuredProf.overallRating.toFixed(1) }}<span class="text-lg text-[#6B2FA0]/60">/5</span>
            </div>
          </div>

          <div class="bg-[#EFE5FA] rounded-xl md:rounded-2xl p-3 md:p-4 flex flex-col justify-between h-24 md:h-32 transition-transform hover:scale-[1.02]">
            <div class="flex justify-between items-start">
              <span class="font-label-sm text-label-sm text-on-surface-variant uppercase">Teaching</span>
              <span class="material-symbols-outlined text-green-600 text-[16px]">trending_up</span>
            </div>
            <div class="font-stat-display text-xl md:text-stat-display text-[#6B2FA0]">
              {{ (featuredProf.avgTeaching * 2).toFixed(1) }}<span class="text-lg text-[#6B2FA0]/60">/10</span>
            </div>
          </div>

          <div class="bg-[#EFE5FA] rounded-xl md:rounded-2xl p-3 md:p-4 flex flex-col justify-between h-24 md:h-32 transition-transform hover:scale-[1.02]">
            <div class="flex justify-between items-start">
              <span class="font-label-sm text-label-sm text-on-surface-variant uppercase">Fairness</span>
              <span class="material-symbols-outlined text-on-surface-variant/50 text-[16px]">horizontal_rule</span>
            </div>
            <div class="font-stat-display text-xl md:text-stat-display text-[#6B2FA0]">
              {{ (featuredProf.avgGrading * 2).toFixed(1) }}<span class="text-lg text-[#6B2FA0]/60">/10</span>
            </div>
          </div>

          <div class="bg-[#EFE5FA] rounded-xl md:rounded-2xl p-3 md:p-4 flex flex-col justify-between h-24 md:h-32 transition-transform hover:scale-[1.02]">
            <div class="flex justify-between items-start">
              <span class="font-label-sm text-label-sm text-on-surface-variant uppercase">Workload</span>
              <span class="material-symbols-outlined text-red-500 text-[16px]">trending_down</span>
            </div>
            <div class="font-stat-display text-xl md:text-stat-display text-[#6B2FA0]">
              {{ (featuredProf.avgWorkload * 2).toFixed(1) }}<span class="text-lg text-[#6B2FA0]/60">/10</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Recent Reviews Section -->
    <section class="mt-stack-lg">
      <div class="flex justify-between items-end mb-6 border-b border-surface-variant pb-4">
        <h2 class="font-headline-md text-headline-md font-bold text-on-surface">
          Recent Teacher Reviews <span class="text-outline text-lg font-normal ml-2">({{ reviewsList.length }})</span>
        </h2>
        <router-link to="/search" class="font-label-sm text-label-sm text-primary font-bold hover:underline">
          View Catalog →
        </router-link>
      </div>

      <div v-if="reviewsList.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-stack-md">
        <div
          v-for="rev in reviewsList"
          :key="rev.id"
          class="bg-surface-container-lowest rounded-2xl md:rounded-3xl shadow-2xl-ambient p-5 md:p-8 relative flex flex-col justify-between"
        >
          <div>
            <div class="flex justify-between items-start mb-4 md:mb-6">
              <div class="flex gap-2 md:gap-3 items-center">
                <div class="w-10 h-10 md:w-12 md:h-12 rounded-full bg-secondary-fixed flex items-center justify-center text-on-secondary-fixed font-bold text-sm md:text-lg font-stat-display">
                  {{ rev.courseCode ? rev.courseCode.substring(0, 2) : 'SK' }}
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-on-surface font-body-md text-sm md:text-body-md">{{ rev.professorName }}</span>
                    <span class="bg-[#2E9E4F]/10 text-[#2E9E4F] px-1.5 md:px-2 py-0.5 rounded font-label-sm text-[8px] md:text-[10px] uppercase font-bold hidden sm:flex items-center gap-1">
                      <span class="material-symbols-outlined text-[12px]">school</span> Verified
                    </span>
                  </div>
                  <div class="text-outline font-label-sm text-label-sm flex items-center gap-1 mt-0.5">
                    <span class="material-symbols-outlined text-[14px]">lock</span> 100% Anonymous • {{ rev.semesterTaken }}
                  </div>
                </div>
              </div>
              <div class="flex flex-col items-end">
                <div class="bg-[#2E9E4F] text-white font-bold px-3 py-1 rounded-lg text-lg mb-1 shadow-sm font-stat-display">
                  {{ rev.overallScore.toFixed(1) }}
                </div>
                <span class="font-label-sm text-[10px] text-outline uppercase tracking-wide">Overall</span>
              </div>
            </div>

            <p class="font-body-md text-xs md:text-body-md text-on-surface-variant mb-4 md:mb-6 leading-relaxed">
              {{ rev.comment }}
            </p>
          </div>

          <div class="flex justify-between items-center border-t border-surface-variant pt-4 mt-4">
            <div class="flex gap-4">
              <div class="flex flex-col gap-1 w-24">
                <span class="font-label-sm text-[10px] uppercase text-outline font-bold">Teaching</span>
                <div class="h-1.5 w-full bg-surface-variant rounded-full overflow-hidden">
                  <div class="h-full bg-secondary" :style="{ width: `${(rev.ratingTeaching / 5) * 100}%` }"></div>
                </div>
              </div>
              <div class="flex flex-col gap-1 w-24">
                <span class="font-label-sm text-[10px] uppercase text-outline font-bold">Workload</span>
                <div class="h-1.5 w-full bg-surface-variant rounded-full overflow-hidden">
                  <div class="h-full bg-error" :style="{ width: `${(rev.ratingWorkload / 5) * 100}%` }"></div>
                </div>
              </div>
            </div>
            <span class="font-label-sm text-label-sm text-outline">
              Helpful ({{ rev.helpfulCount }})
            </span>
          </div>
        </div>
      </div>

      <!-- Clean Empty State when no reviews exist yet -->
      <div v-else class="text-center py-10 md:py-16 bg-white rounded-2xl md:rounded-3xl shadow-2xl-ambient p-5 md:p-8 max-w-lg mx-auto">
        <div class="w-16 h-16 bg-primary/10 text-primary rounded-full flex items-center justify-center mx-auto text-3xl mb-4">
          <span class="material-symbols-outlined text-[32px]">rate_review</span>
        </div>
        <h3 class="text-xl font-bold text-on-surface mb-2">No reviews published yet</h3>
        <p class="text-sm text-on-surface-variant mb-6">
          Be the first student to add a teacher and share anonymous feedback for your campus!
        </p>
        <div class="flex justify-center gap-3">
          <router-link to="/search" class="bg-primary text-white px-6 py-2.5 rounded-full font-label-sm text-xs font-bold hover:bg-[#6B2FA0] transition-colors shadow-md">
            + Add Teacher
          </router-link>
          <router-link to="/review/new" class="border border-outline-variant/40 text-primary px-6 py-2.5 rounded-full font-label-sm text-xs font-bold hover:bg-surface-variant transition-colors">
            Write Review
          </router-link>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.slogan-fade-enter-active,
.slogan-fade-leave-active {
  transition: all 0.4s ease;
}

.slogan-fade-enter-from {
  opacity: 0;
  transform: translateY(18px);
}

.slogan-fade-leave-to {
  opacity: 0;
  transform: translateY(-18px);
}
</style>
