<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Professor, Review } from '../types';
import { api } from '../api';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const professor = ref<Professor | null>(null);
const reviews = ref<Review[]>([]);
const isLoading = ref(true);
const sortOption = ref('Most Helpful');

const profId = computed(() => route.params.id as string);

const recommendPercent = computed(() => {
  if (!professor.value) return 0;
  return Math.round((professor.value.overallRating / 5) * 100);
});

onMounted(async () => {
  try {
    const profData = await api.getProfessorById(profId.value);
    if (profData) {
      professor.value = profData;
      reviews.value = await api.getReviewsForProfessor(profId.value);
    }
  } finally {
    isLoading.value = false;
  }
});

function handleWriteReview() {
  if (!authStore.isVerified) {
    router.push({ path: '/auth', query: { redirect: `/review/new?profId=${profId.value}` } });
  } else {
    router.push({ path: '/review/new', query: { profId: profId.value } });
  }
}
</script>

<template>
  <main class="max-w-container-max mx-auto px-4 md:px-gutter py-6 md:py-stack-lg">
    <div v-if="isLoading" class="text-center py-20">
      <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      <p class="mt-4 text-on-surface-variant font-label-sm">Loading professor profile...</p>
    </div>

    <div v-else-if="professor" class="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
      <!-- Left Column: Hero & Stats & Review Feed -->
      <div class="lg:col-span-8 flex flex-col gap-stack-md">
        <!-- Hero Section -->
        <div class="bg-surface-container-lowest rounded-2xl md:rounded-3xl p-5 md:p-8 shadow-2xl-ambient flex flex-col md:flex-row items-center gap-5 md:gap-8 relative overflow-hidden">
          <div class="absolute -right-20 -top-20 w-64 h-64 bg-secondary-container/20 rounded-full blur-3xl pointer-events-none"></div>

          <div class="relative shrink-0">
            <div class="w-20 h-20 md:w-32 md:h-32 rounded-full overflow-hidden border-4 border-surface-bright bg-primary text-white flex items-center justify-center font-display-lg text-xl md:text-3xl font-bold">
              {{ professor.name.split(' ').map(n => n[0]).slice(0, 2).join('') }}
            </div>
            <div class="absolute -bottom-2 -right-2 bg-white rounded-full p-1 shadow-lg">
              <span class="material-symbols-outlined text-green-600 bg-green-100 rounded-full p-1" style="font-variation-settings: 'FILL' 1;">verified</span>
            </div>
          </div>

          <div class="flex-1">
            <h2 class="font-headline-lg text-lg md:text-headline-lg text-primary mb-1 text-center md:text-left">{{ professor.name }}</h2>
            <p class="font-body-lg text-sm md:text-body-lg text-on-surface-variant flex items-center justify-center md:justify-start gap-2 mb-3 md:mb-4">
              <span class="material-symbols-outlined text-[18px]">domain</span> {{ professor.departmentName }} Department
            </p>
            <div class="flex flex-wrap justify-center md:justify-start gap-2">
              <span v-for="tag in professor.tags" :key="tag" class="bg-surface-container text-on-surface-variant px-3 py-1 rounded-full font-label-sm text-label-sm border border-outline-variant/30">
                {{ tag }}
              </span>
            </div>
          </div>

          <!-- Recommendation Ring -->
          <div class="flex flex-col items-center justify-center shrink-0 w-24 h-24 md:w-32 md:h-32 relative">
            <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              <circle cx="50" cy="50" fill="none" r="45" stroke="#f3f4f6" stroke-width="8"></circle>
              <circle class="transition-all duration-1000 ease-out drop-shadow-md" cx="50" cy="50" fill="none" r="45" stroke="#2E9E4F" stroke-dasharray="283" :stroke-dashoffset="283 - (283 * recommendPercent) / 100" stroke-linecap="round" stroke-width="8"></circle>
            </svg>
            <div class="absolute inset-0 flex flex-col items-center justify-center">
              <span class="font-stat-display text-stat-display text-primary">{{ recommendPercent }}%</span>
            </div>
            <span class="absolute -bottom-5 md:-bottom-6 font-label-sm text-[10px] md:text-label-sm text-on-surface-variant text-center w-full">Recommend</span>
          </div>
        </div>

        <!-- Stat Grid (Stitch Pale Purple #EFE5FA) -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4">
          <div class="bg-[#EFE5FA] rounded-xl md:rounded-2xl p-3 md:p-4 flex flex-col justify-between h-24 md:h-32 transition-transform hover:scale-[1.02]">
            <div class="flex justify-between items-start">
              <span class="font-label-sm text-label-sm text-on-surface-variant uppercase">Overall</span>
              <span class="material-symbols-outlined text-green-600 text-[16px]">trending_up</span>
            </div>
            <div class="font-stat-display text-xl md:text-stat-display text-[#6B2FA0]">
              {{ professor.overallRating.toFixed(1) }}<span class="text-lg text-[#6B2FA0]/60">/5</span>
            </div>
          </div>

          <div class="bg-[#EFE5FA] rounded-xl md:rounded-2xl p-3 md:p-4 flex flex-col justify-between h-24 md:h-32 transition-transform hover:scale-[1.02]">
            <div class="flex justify-between items-start">
              <span class="font-label-sm text-label-sm text-on-surface-variant uppercase">Teaching</span>
              <span class="material-symbols-outlined text-green-600 text-[16px]">trending_up</span>
            </div>
            <div class="font-stat-display text-xl md:text-stat-display text-[#6B2FA0]">
              {{ (professor.avgTeaching * 2).toFixed(1) }}<span class="text-lg text-[#6B2FA0]/60">/10</span>
            </div>
          </div>

          <div class="bg-[#EFE5FA] rounded-xl md:rounded-2xl p-3 md:p-4 flex flex-col justify-between h-24 md:h-32 transition-transform hover:scale-[1.02]">
            <div class="flex justify-between items-start">
              <span class="font-label-sm text-label-sm text-on-surface-variant uppercase">Grading</span>
              <span class="material-symbols-outlined text-on-surface-variant/50 text-[16px]">horizontal_rule</span>
            </div>
            <div class="font-stat-display text-xl md:text-stat-display text-[#6B2FA0]">
              {{ (professor.avgGrading * 2).toFixed(1) }}<span class="text-lg text-[#6B2FA0]/60">/10</span>
            </div>
          </div>

          <div class="bg-[#EFE5FA] rounded-xl md:rounded-2xl p-3 md:p-4 flex flex-col justify-between h-24 md:h-32 transition-transform hover:scale-[1.02]">
            <div class="flex justify-between items-start">
              <span class="font-label-sm text-label-sm text-on-surface-variant uppercase">Workload</span>
              <span class="material-symbols-outlined text-red-500 text-[16px]">trending_down</span>
            </div>
            <div class="font-stat-display text-xl md:text-stat-display text-[#6B2FA0]">
              {{ (professor.avgWorkload * 2).toFixed(1) }}<span class="text-lg text-[#6B2FA0]/60">/10</span>
            </div>
          </div>
        </div>

        <!-- AI Summary Box -->
        <div v-if="professor.aiSummary" class="bg-blue-50 border border-blue-200 rounded-3xl p-6 relative">
          <div class="flex items-center gap-2 mb-2 text-blue-800 font-label-sm font-bold text-sm uppercase tracking-wide">
            <span class="material-symbols-outlined text-[18px]">auto_awesome</span> AI Summary of Reviews
          </div>
          <p class="font-body-md text-body-md text-blue-950 leading-relaxed">
            {{ professor.aiSummary }}
          </p>
        </div>

        <!-- Review Feed Header -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-end mt-4 border-b border-surface-variant pb-4 gap-3">
          <h2 class="font-headline-md text-lg md:text-headline-md font-bold text-on-surface">
            Student Reviews <span class="text-outline text-lg font-normal ml-2">({{ reviews.length }})</span>
          </h2>
          <div class="flex items-center gap-3">
            <select v-model="sortOption" class="bg-surface border border-surface-variant rounded-md px-3 py-1.5 font-label-sm text-label-sm text-on-surface-variant focus:ring-[#2D6FD1] focus:border-[#2D6FD1]">
              <option>Most Helpful</option>
              <option>Newest</option>
              <option>Highest Rated</option>
            </select>
            <button @click="handleWriteReview" class="bg-primary text-white font-label-sm text-label-sm px-4 py-1.5 rounded-full hover:bg-[#6B2FA0] transition-colors">
              + Review
            </button>
          </div>
        </div>

        <!-- Review Feed -->
        <div v-if="reviews.length > 0" class="flex flex-col gap-6">
          <div
            v-for="rev in reviews"
            :key="rev.id"
            class="bg-surface-container-lowest rounded-2xl md:rounded-3xl shadow-2xl-ambient p-5 md:p-8 relative"
          >
            <div class="flex justify-between items-start mb-4 md:mb-6">
              <div class="flex gap-2 md:gap-3 items-center">
                <div class="w-12 h-12 rounded-full bg-secondary-fixed flex items-center justify-center text-on-secondary-fixed font-bold text-lg font-stat-display">
                  {{ rev.courseCode.substring(0, 2) }}
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <span class="font-bold text-on-surface font-body-md text-body-md">{{ rev.courseCode }} - {{ rev.courseTitle }}</span>
                    <span class="bg-[#2E9E4F]/10 text-[#2E9E4F] px-2 py-0.5 rounded font-label-sm text-[10px] uppercase font-bold flex items-center gap-1">
                      <span class="material-symbols-outlined text-[12px]">school</span> Verified Student
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

            <p class="font-body-md text-body-md text-on-surface-variant mb-6 leading-relaxed">
              {{ rev.comment }}
            </p>

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

              <button class="flex items-center gap-1.5 text-on-surface-variant hover:text-primary transition-colors font-label-sm text-label-sm font-bold bg-surface px-3 py-1.5 rounded-full border border-surface-variant hover:border-primary">
                <span class="material-symbols-outlined text-[16px]">thumb_up</span>
                Helpful ({{ rev.helpfulCount }})
              </button>
            </div>
          </div>
        </div>

        <div v-else class="bg-surface-container-lowest rounded-3xl p-12 text-center shadow-2xl-ambient">
          <p class="text-on-surface-variant font-body-lg mb-4">No reviews posted yet for {{ professor.name }}.</p>
          <button @click="handleWriteReview" class="bg-primary text-white px-6 py-2.5 rounded-full font-label-sm text-label-sm hover:bg-[#6B2FA0] transition-colors">
            Be First to Review
          </button>
        </div>
      </div>

      <!-- Right Column: Sidebar Stats -->
      <div class="lg:col-span-4 flex flex-col gap-stack-md">
        <div class="bg-surface-container-lowest rounded-3xl p-6 shadow-2xl-ambient flex flex-col gap-4">
          <h3 class="font-headline-md text-headline-md font-bold text-on-surface">Verification Status</h3>
          <div class="p-4 bg-green-50 border border-green-200 rounded-2xl flex items-center gap-3">
            <span class="material-symbols-outlined text-green-600 text-2xl">shield</span>
            <div>
              <div class="font-bold text-green-900 font-body-md text-sm">Strict Anonymity</div>
              <div class="text-xs text-green-700">Reviews are validated via @superior.edu.pk email hashes and completely unlinked.</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center py-20">
      <h2 class="text-2xl font-bold text-primary mb-4">Professor Not Found</h2>
      <router-link to="/search" class="text-secondary font-bold hover:underline">← Back to Catalog</router-link>
    </div>
  </main>
</template>

<style scoped></style>
