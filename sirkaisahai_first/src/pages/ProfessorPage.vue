<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Professor, Review } from '../types';
import { api } from '../api';
import { useAuthStore } from '../stores/auth';
import ReviewCard from '../components/ui/ReviewCard.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const professor = ref<Professor | null>(null);
const reviews = ref<Review[]>([]);
const isLoading = ref(true);
const sortOption = ref<'Most Helpful' | 'Newest' | 'Highest Rated'>('Most Helpful');

const profId = computed(() => route.params.id as string);

const recommendPercent = computed(() => {
  if (!professor.value) return 0;
  return Math.round((professor.value.overallRating / 5) * 100);
});

const ringOffset = computed(() => {
  const circumference = 2 * Math.PI * 42;
  return circumference - (circumference * recommendPercent.value) / 100;
});

const sortedReviews = computed(() => {
  const copy = [...reviews.value];
  if (sortOption.value === 'Most Helpful') {
    return copy.sort((a, b) => b.helpfulCount - a.helpfulCount);
  }
  if (sortOption.value === 'Highest Rated') {
    return copy.sort((a, b) => b.overallScore - a.overallScore);
  }
  return copy.sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
});

const gradeDistribution = computed(() => {
  const counts: Record<string, number> = {};
  reviews.value.forEach((rev) => {
    if (rev.gradeReceived) {
      counts[rev.gradeReceived] = (counts[rev.gradeReceived] || 0) + 1;
    }
  });
  const totalGraded = Object.values(counts).reduce((sum, count) => sum + count, 0);
  const order = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'F'];
  return order
    .filter((grade) => counts[grade])
    .map((grade) => ({
      grade,
      count: counts[grade] || 0,
      percent: totalGraded > 0 ? Math.round(((counts[grade] || 0) / totalGraded) * 100) : 0
    }));
});

const coursesReviewed = computed(() => {
  const unique = new Map<string, string>();
  reviews.value.forEach((rev) => {
    if (rev.courseCode) {
      unique.set(rev.courseCode, rev.courseTitle || rev.courseCode);
    }
  });
  return Array.from(unique.entries()).map(([code, title]) => ({ code, title }));
});

const workloadDescriptor = computed(() => {
  if (!professor.value) return '';
  if (professor.value.avgWorkload >= 4.0) return 'Heavy';
  if (professor.value.avgWorkload >= 2.5) return 'Moderate';
  return 'Light';
});

async function loadProfessor() {
  isLoading.value = true;
  try {
    const profData = await api.getProfessorById(profId.value);
    if (profData) {
      professor.value = profData;
      reviews.value = await api.getReviewsForProfessor(profId.value);
    } else {
      professor.value = null;
      reviews.value = [];
    }
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadProfessor);
watch(profId, loadProfessor);

function handleWriteReview() {
  if (!authStore.isVerified) {
    router.push({ path: '/auth', query: { redirect: `/review/new?profId=${profId.value}` } });
  } else {
    router.push({ path: '/review/new', query: { profId: profId.value } });
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
  <main class="max-w-container-max mx-auto px-4 md:px-gutter pt-4 pb-10">
    <!-- Loading Skeletons -->
    <div v-if="isLoading" class="grid grid-cols-1 lg:grid-cols-12 gap-7">
      <div class="lg:col-span-8 space-y-6">
        <div class="neu-card p-6 space-y-5">
          <div class="flex items-center gap-4">
            <div class="neu-skeleton w-16 h-16 rounded-xl"></div>
            <div class="space-y-2 flex-1">
              <div class="neu-skeleton h-6 w-1/2"></div>
              <div class="neu-skeleton h-4 w-1/3"></div>
            </div>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div class="neu-skeleton h-16"></div>
            <div class="neu-skeleton h-16"></div>
            <div class="neu-skeleton h-16"></div>
            <div class="neu-skeleton h-16"></div>
          </div>
        </div>
        <div class="neu-card p-6 space-y-3">
          <div class="neu-skeleton h-4 w-1/3"></div>
          <div class="neu-skeleton h-4 w-full"></div>
          <div class="neu-skeleton h-4 w-3/4"></div>
        </div>
      </div>
      <div class="lg:col-span-4 space-y-5">
        <div class="neu-card p-6 space-y-3">
          <div class="neu-skeleton h-5 w-1/2"></div>
          <div class="neu-skeleton h-10 w-full rounded-full"></div>
        </div>
      </div>
    </div>

    <div v-else-if="professor" class="grid grid-cols-1 lg:grid-cols-12 gap-7 items-start">
      <!-- Left Column -->
      <div class="lg:col-span-8 space-y-6">
        <div class="neu-surface-lg p-6 md:p-8 space-y-6">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-5">
            <div class="flex items-start gap-4 min-w-0">
              <div class="neu-tile w-16 h-16 flex items-center justify-center font-mono text-xl font-bold text-primary shrink-0">
                {{ getInitials(professor.name) }}
              </div>
              <div class="min-w-0 space-y-1">
                <h1 class="text-2xl md:text-3xl font-extrabold text-primary leading-tight">
                  {{ professor.name }}
                </h1>
                <p class="text-sm text-on-surface-variant">
                  {{ professor.title }} · {{ professor.departmentName }} Department
                </p>
                <div v-if="professor.tags.length > 0" class="flex flex-wrap gap-1.5 pt-1.5">
                  <span
                    v-for="tag in professor.tags"
                    :key="tag"
                    class="neu-inset px-2.5 py-0.5 rounded-full text-[11px] text-on-surface-variant"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>

            <div class="flex items-center gap-3 shrink-0 self-start sm:self-center">
              <div class="w-16 h-16 relative">
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
                    :stroke-dashoffset="ringOffset"
                  />
                </svg>
                <span class="absolute inset-0 flex items-center justify-center font-mono text-sm font-bold text-on-surface tabular-nums">
                  {{ recommendPercent }}%
                </span>
              </div>
              <span class="text-xs text-outline leading-snug">
                Approval<br />Index
              </span>
            </div>
          </div>

          <!-- Unified /5.0 Stat Tray -->
          <div class="neu-inset-tray p-4 grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div>
              <div class="font-mono text-[10px] uppercase text-outline">Overall</div>
              <div class="font-mono text-2xl font-bold text-primary tabular-nums mt-1">
                {{ professor.overallRating.toFixed(1) }}<span class="text-xs text-outline font-normal">/5</span>
              </div>
            </div>
            <div>
              <div class="font-mono text-[10px] uppercase text-outline">Teaching</div>
              <div class="font-mono text-2xl font-bold text-on-surface tabular-nums mt-1">
                {{ professor.avgTeaching.toFixed(1) }}<span class="text-xs text-outline font-normal">/5</span>
              </div>
            </div>
            <div>
              <div class="font-mono text-[10px] uppercase text-outline">Grading</div>
              <div class="font-mono text-2xl font-bold text-on-surface tabular-nums mt-1">
                {{ professor.avgGrading.toFixed(1) }}<span class="text-xs text-outline font-normal">/5</span>
              </div>
            </div>
            <div>
              <div class="font-mono text-[10px] uppercase text-outline">Workload ({{ workloadDescriptor }})</div>
              <div class="font-mono text-2xl font-bold text-warning tabular-nums mt-1">
                {{ professor.avgWorkload.toFixed(1) }}<span class="text-xs text-outline font-normal">/5</span>
              </div>
            </div>
          </div>

          <!-- Student Review Summary -->
          <div v-if="professor.aiSummary" class="neu-inset-tray p-4 space-y-1">
            <div class="text-[11px] font-bold uppercase tracking-[0.12em] text-primary">
              Student Review Summary
            </div>
            <p class="text-sm text-on-surface-variant leading-relaxed">
              {{ professor.aiSummary }}
            </p>
          </div>
        </div>

        <!-- Review Feed Header -->
        <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 pt-2">
          <div class="flex items-center gap-2.5">
            <h2 class="text-lg font-bold text-on-surface">Student Reviews</h2>
            <span class="neu-circle-badge min-w-[26px] h-[26px] px-2 inline-flex items-center justify-center font-mono text-xs font-semibold text-on-surface-variant tabular-nums">
              {{ reviews.length }}
            </span>
          </div>

          <div class="flex items-center gap-3">
            <select
              v-model="sortOption"
              aria-label="Sort student reviews"
              class="neu-inset rounded-full px-4 py-2 text-xs font-semibold text-on-surface focus:ring-0 focus:outline-none cursor-pointer"
            >
              <option value="Most Helpful">Most Helpful</option>
              <option value="Newest">Newest</option>
              <option value="Highest Rated">Highest Rated</option>
            </select>

            <button
              type="button"
              @click="handleWriteReview"
              class="neu-btn-primary px-5 py-2 text-xs font-semibold cursor-pointer"
            >
              + Review
            </button>
          </div>
        </div>

        <div v-if="sortedReviews.length > 0" class="space-y-5">
          <ReviewCard v-for="rev in sortedReviews" :key="rev.id" :review="rev" :show-professor="false" />
        </div>

        <div v-else class="neu-card p-9 text-center space-y-4">
          <p class="text-sm text-on-surface-variant">
            No reviews posted yet for {{ professor.name }}.
          </p>
          <button
            type="button"
            @click="handleWriteReview"
            class="neu-btn-primary px-6 py-2.5 text-xs font-semibold cursor-pointer"
          >
            Be First to Review
          </button>
        </div>
      </div>

      <!-- Right Sidebar -->
      <aside class="lg:col-span-4 space-y-6 lg:sticky lg:top-24">
        <div class="neu-card p-6 space-y-4">
          <h3 class="text-base font-bold text-on-surface">Rate This Professor</h3>
          <p class="text-xs text-on-surface-variant leading-relaxed">
            Studied with {{ professor.name }}? Submit your honest, anonymous evaluation to guide fellow students.
          </p>
          <button
            type="button"
            @click="handleWriteReview"
            class="neu-btn-primary w-full py-2.5 text-xs font-semibold cursor-pointer"
          >
            Write Anonymous Review
          </button>
        </div>

        <div v-if="gradeDistribution.length > 0" class="neu-card p-6 space-y-4">
          <h3 class="text-base font-bold text-on-surface">Reported Grades</h3>
          <div class="space-y-2.5">
            <div v-for="item in gradeDistribution" :key="item.grade" class="flex items-center gap-2.5 text-xs font-mono">
              <span class="w-7 font-semibold text-on-surface">{{ item.grade }}</span>
              <div class="flex-1 h-2 neu-inset rounded-full overflow-hidden">
                <div class="h-full bg-primary rounded-full" :style="{ width: `${item.percent}%` }"></div>
              </div>
              <span class="w-7 text-right text-outline tabular-nums">{{ item.count }}</span>
            </div>
          </div>
        </div>

        <div v-if="coursesReviewed.length > 0" class="neu-card p-6 space-y-3">
          <h3 class="text-base font-bold text-on-surface">Courses Reviewed</h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="course in coursesReviewed"
              :key="course.code"
              class="neu-tile px-3 py-1 font-mono text-xs text-primary font-semibold"
            >
              {{ course.code }}
            </span>
          </div>
        </div>

        <div class="neu-card p-6 space-y-2.5">
          <h3 class="text-xs font-bold uppercase tracking-[0.12em] text-on-surface">Strict Anonymity</h3>
          <p class="text-xs text-on-surface-variant leading-relaxed">
            Reviews are validated via @superior.edu.pk SHA-256 hashes and stored with zero link to your identity.
          </p>
          <router-link to="/privacy" class="inline-block text-xs font-semibold text-primary hover:underline pt-1">
            Read privacy architecture →
          </router-link>
        </div>
      </aside>
    </div>

    <div v-else class="neu-card p-10 text-center max-w-md mx-auto space-y-4">
      <h2 class="text-xl font-bold text-primary">Professor Not Found</h2>
      <p class="text-xs text-on-surface-variant">
        The requested faculty profile could not be found in the catalogue.
      </p>
      <router-link to="/search" class="neu-btn-primary inline-block px-6 py-2.5 text-xs font-semibold">
        Back to Catalogue
      </router-link>
    </div>
  </main>
</template>
