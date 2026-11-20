<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import type { Professor, Review } from '../types';
import { api } from '../api';
import ReviewCard from '../components/ui/ReviewCard.vue';

const router = useRouter();
const searchQuery = ref('');
const featuredProf = ref<Professor | null>(null);
const reviewsList = ref<Review[]>([]);
const isLoading = ref(true);

const slogans = [
  'Kon Sir Kaisa Hai?',
  'Asli Scene Kya Hai?',
  'GPA Bachao, Real Feedback Paao.',
  'Strict Attendance Ya Chill Scenes?',
  'Easy Grading Ya Surprise Quizzes?'
];
const currentSloganIndex = ref(0);
let sloganInterval: ReturnType<typeof setInterval> | null = null;

const featuredPercent = computed(() => {
  if (!featuredProf.value) return 0;
  return Math.round((featuredProf.value.overallRating / 5) * 100);
});

const featuredRingOffset = computed(() => {
  const circumference = 2 * Math.PI * 42;
  return circumference - (circumference * featuredPercent.value) / 100;
});

onMounted(async () => {
  sloganInterval = setInterval(() => {
    currentSloganIndex.value = (currentSloganIndex.value + 1) % slogans.length;
  }, 3000);

  try {
    const [profs, realReviews] = await Promise.all([api.search(''), api.getRecentReviews()]);
    reviewsList.value = realReviews;

    if (profs.length > 0) {
      const sorted = [...profs].sort((a, b) => b.rating - a.rating);
      const topProfId = sorted[0]?.id;
      if (topProfId) {
        const topProf = await api.getProfessorById(topProfId);
        if (topProf) featuredProf.value = topProf;
      }
    }
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

function getInitials(name: string) {
  return name
    .split(' ')
    .filter(Boolean)
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();
}
</script>

<template>
  <div class="max-w-container-max mx-auto px-4 md:px-gutter pt-4 pb-8 space-y-12">
    <!-- Hero Card (Soft Extruded Neumorphic Slab) -->
    <section class="neu-surface-lg px-5 py-12 sm:px-10 md:py-16">
      <div class="max-w-xl mx-auto text-center space-y-5">
        <p class="text-[10px] sm:text-[11px] font-semibold uppercase tracking-[0.18em] text-outline">
          Superior University
        </p>

        <div class="h-16 sm:h-20 md:h-24 flex items-center justify-center overflow-hidden">
          <transition name="slogan-fade" mode="out-in">
            <h1
              :key="currentSloganIndex"
              class="text-2xl sm:text-4xl md:text-[42px] font-extrabold text-primary tracking-tight leading-tight"
            >
              {{ slogans[currentSloganIndex] }}
            </h1>
          </transition>
        </div>

        <p class="text-sm text-on-surface-variant max-w-md mx-auto leading-relaxed">
          Real, unfiltered &amp; anonymous teacher reviews by Superior University students. Know your professors before registering!
        </p>

        <!-- Recessed Pill Search Bar -->
        <form
          @submit.prevent="handleSearch"
          class="neu-inset rounded-full p-1.5 pl-5 flex items-center gap-2 max-w-lg mx-auto mt-6"
        >
          <svg
            viewBox="0 0 20 20"
            fill="none"
            class="w-4 h-4 text-outline shrink-0"
            aria-hidden="true"
          >
            <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.6" />
            <path d="M13.5 13.5L17 17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
          <input
            v-model="searchQuery"
            class="flex-1 bg-transparent border-none focus:ring-0 outline-none text-sm text-on-surface placeholder-outline py-2 px-1 min-w-0"
            placeholder="Search teacher..."
            type="text"
          />
          <button
            type="submit"
            class="neu-btn-primary px-7 py-2.5 text-xs font-semibold shrink-0 cursor-pointer"
          >
            Search
          </button>
        </form>

        <!-- 3 Raised Soft Pill Quick Actions -->
        <div class="flex flex-wrap justify-center gap-3.5 pt-2">
          <router-link
            to="/search"
            class="neu-pill-btn px-5 py-2 text-xs font-medium text-on-surface-variant inline-flex items-center gap-2"
          >
            <svg viewBox="0 0 18 18" fill="none" class="w-3.5 h-3.5 text-primary" aria-hidden="true">
              <path
                d="M3.5 4.5H14.5M3.5 9H11.5M3.5 13.5H9.5"
                stroke="currentColor"
                stroke-width="1.5"
                stroke-linecap="round"
              />
            </svg>
            <span>Browse</span>
          </router-link>

          <router-link
            to="/review/new"
            class="neu-pill-btn px-5 py-2 text-xs font-medium text-on-surface-variant inline-flex items-center gap-2"
          >
            <svg viewBox="0 0 18 18" fill="none" class="w-3.5 h-3.5 text-primary" aria-hidden="true">
              <path
                d="M4 14L4.7 11.1L11.8 4L14 6.2L6.9 13.3L4 14Z"
                stroke="currentColor"
                stroke-width="1.4"
                stroke-linejoin="round"
              />
            </svg>
            <span>Review</span>
          </router-link>

          <router-link
            to="/auth"
            class="neu-pill-btn px-5 py-2 text-xs font-medium text-on-surface-variant inline-flex items-center gap-2"
          >
            <svg viewBox="0 0 18 18" fill="none" class="w-3.5 h-3.5 text-primary" aria-hidden="true">
              <path
                d="M9 2.5L14 4.5V8.6C14 11.9 11.8 14.5 9 15.5C6.2 14.5 4 11.9 4 8.6V4.5L9 2.5Z"
                stroke="currentColor"
                stroke-width="1.4"
                stroke-linejoin="round"
              />
              <path
                d="M6.8 9L8.3 10.5L11.3 7.5"
                stroke="currentColor"
                stroke-width="1.4"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
            <span>Verify</span>
          </router-link>
        </div>

        <!-- Subtle Privacy Caption -->
        <p class="pt-3 inline-flex items-center justify-center gap-1.5 text-[11px] text-outline">
          <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5 text-outline" aria-hidden="true">
            <path
              d="M8 2L12.5 3.8V7.6C12.5 10.6 10.6 13 8 13.8C5.4 13 3.5 10.6 3.5 7.6V3.8L8 2Z"
              stroke="currentColor"
              stroke-width="1.3"
              stroke-linejoin="round"
            />
          </svg>
          <span>100% anonymous. Your identity stays yours.</span>
        </p>
      </div>
    </section>

    <!-- Loading Skeletons -->
    <section v-if="isLoading" class="space-y-6" aria-label="Loading reviews">
      <div class="flex justify-between items-center">
        <div class="neu-skeleton h-5 w-48"></div>
        <div class="neu-skeleton h-4 w-28"></div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="neu-card p-6 space-y-3">
          <div class="neu-skeleton h-5 w-1/2"></div>
          <div class="neu-skeleton h-4 w-full"></div>
          <div class="neu-skeleton h-4 w-4/5"></div>
        </div>
        <div class="neu-card p-6 space-y-3">
          <div class="neu-skeleton h-5 w-2/5"></div>
          <div class="neu-skeleton h-4 w-full"></div>
          <div class="neu-skeleton h-4 w-3/4"></div>
        </div>
      </div>
    </section>

    <template v-else>
      <!-- Top Rated Faculty Card (Only renders when professors exist in DB) -->
      <section v-if="featuredProf" class="space-y-5">
        <div class="flex items-center justify-between gap-4">
          <h2 class="text-lg font-bold text-on-surface">Top Rated Faculty</h2>
          <router-link
            to="/search"
            class="text-xs font-medium text-on-surface-variant hover:text-primary inline-flex items-center gap-1.5 transition-colors"
          >
            <span>View directory</span>
            <span aria-hidden="true">→</span>
          </router-link>
        </div>

        <div class="neu-card p-6 md:p-7 flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div class="flex items-center gap-4 min-w-0">
            <div class="neu-tile w-14 h-14 flex items-center justify-center font-mono text-lg font-bold text-primary shrink-0">
              {{ getInitials(featuredProf.name) }}
            </div>
            <div class="min-w-0 space-y-1">
              <router-link
                :to="`/professor/${featuredProf.id}`"
                class="text-lg font-bold text-primary hover:underline block truncate"
              >
                {{ featuredProf.name }}
              </router-link>
              <p class="text-xs text-on-surface-variant">
                {{ featuredProf.title }} · {{ featuredProf.departmentName }}
              </p>
              <div v-if="featuredProf.tags.length > 0" class="flex flex-wrap gap-1.5 pt-1">
                <span
                  v-for="tag in featuredProf.tags.slice(0, 3)"
                  :key="tag"
                  class="neu-inset px-2.5 py-0.5 rounded-full text-[11px] text-on-surface-variant"
                >
                  {{ tag }}
                </span>
              </div>
            </div>
          </div>

          <div class="neu-inset-tray p-3.5 grid grid-cols-2 sm:grid-cols-4 gap-3 lg:w-[400px] shrink-0">
            <div class="text-center">
              <div class="font-mono text-[10px] uppercase text-outline">Overall</div>
              <div class="font-mono text-base font-bold text-primary tabular-nums mt-0.5">
                {{ featuredProf.overallRating.toFixed(1) }}/5
              </div>
            </div>
            <div class="text-center">
              <div class="font-mono text-[10px] uppercase text-outline">Teaching</div>
              <div class="font-mono text-base font-bold text-on-surface tabular-nums mt-0.5">
                {{ featuredProf.avgTeaching.toFixed(1) }}/5
              </div>
            </div>
            <div class="text-center">
              <div class="font-mono text-[10px] uppercase text-outline">Grading</div>
              <div class="font-mono text-base font-bold text-on-surface tabular-nums mt-0.5">
                {{ featuredProf.avgGrading.toFixed(1) }}/5
              </div>
            </div>
            <div class="text-center">
              <div class="font-mono text-[10px] uppercase text-outline">Workload</div>
              <div class="font-mono text-base font-bold text-warning tabular-nums mt-0.5">
                {{ featuredProf.avgWorkload.toFixed(1) }}/5
              </div>
            </div>
          </div>

          <div class="flex items-center justify-between lg:justify-end gap-4 shrink-0">
            <div class="flex items-center gap-2.5">
              <div class="w-12 h-12 relative">
                <svg class="w-full h-full -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="42" fill="none" stroke="#d8dae5" stroke-width="8" />
                  <circle
                    cx="50"
                    cy="50"
                    r="42"
                    fill="none"
                    stroke="#1f6e43"
                    stroke-width="8"
                    stroke-linecap="round"
                    :stroke-dasharray="2 * Math.PI * 42"
                    :stroke-dashoffset="featuredRingOffset"
                  />
                </svg>
                <span class="absolute inset-0 flex items-center justify-center font-mono text-[11px] font-bold text-on-surface tabular-nums">
                  {{ featuredPercent }}%
                </span>
              </div>
              <span class="text-[11px] text-outline leading-tight">
                Recommend
              </span>
            </div>

            <router-link
              :to="`/professor/${featuredProf.id}`"
              class="neu-pill-btn px-4 py-2 text-xs font-semibold text-primary"
            >
              View Profile
            </router-link>
          </div>
        </div>
      </section>

      <!-- Recent Teacher Reviews -->
      <section class="space-y-6">
        <div class="flex items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <h2 class="text-lg font-bold text-on-surface">Recent Teacher Reviews</h2>
            <span class="neu-circle-badge min-w-[26px] h-[26px] px-2 inline-flex items-center justify-center font-mono text-xs font-semibold text-on-surface-variant tabular-nums">
              {{ reviewsList.length }}
            </span>
          </div>

          <router-link
            to="/search"
            class="text-xs font-medium text-on-surface-variant hover:text-primary inline-flex items-center gap-1.5 transition-colors"
          >
            <span>View catalogue</span>
            <span aria-hidden="true">→</span>
          </router-link>
        </div>

        <div v-if="reviewsList.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <ReviewCard v-for="rev in reviewsList" :key="rev.id" :review="rev" :show-professor="true" />
        </div>

        <!-- Centered Empty State Card (Exact Match to Chosen Design) -->
        <div v-else class="py-4">
          <div class="neu-card px-6 py-10 sm:px-10 max-w-md mx-auto text-center space-y-5">
            <div class="neu-tile w-12 h-12 mx-auto flex items-center justify-center text-primary">
              <svg viewBox="0 0 20 20" fill="none" class="w-5 h-5" aria-hidden="true">
                <path
                  d="M4.5 5.5C4.5 4.67 5.17 4 6 4H14C14.83 4 15.5 4.67 15.5 5.5V12C15.5 12.83 14.83 13.5 14 13.5H8L4.5 16V5.5Z"
                  stroke="currentColor"
                  stroke-width="1.5"
                  stroke-linejoin="round"
                />
                <path d="M7.5 8H12.5M7.5 10.5H10.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" />
              </svg>
            </div>

            <div class="space-y-1.5">
              <h3 class="text-base font-bold text-on-surface">No reviews published yet</h3>
              <p class="text-xs text-on-surface-variant leading-relaxed max-w-xs mx-auto">
                Be the first student to add a teacher and share anonymous feedback for your campus!
              </p>
            </div>

            <div class="flex flex-wrap justify-center gap-3.5 pt-1">
              <router-link
                to="/search"
                class="neu-btn-primary px-6 py-2.5 text-xs font-semibold"
              >
                + Add Teacher
              </router-link>
              <router-link
                to="/review/new"
                class="neu-pill-btn px-6 py-2.5 text-xs font-semibold text-on-surface"
              >
                Write Review
              </router-link>
            </div>
          </div>
        </div>
      </section>
    </template>
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
