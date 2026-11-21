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
  <main class="w-full">
    <!-- Top Blush Band: Professor Header -->
    <section class="bg-band-hero px-4 md:px-gutter pt-24 pb-10">
      <div class="max-w-container-max mx-auto">
        <div v-if="isLoading" class="ed-card p-7 space-y-4">
          <div class="flex items-center gap-4">
            <div class="ed-skeleton w-16 h-16 rounded-2xl"></div>
            <div class="space-y-2 flex-1">
              <div class="ed-skeleton h-6 w-1/2"></div>
              <div class="ed-skeleton h-4 w-1/3"></div>
            </div>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
            <div class="ed-skeleton h-16"></div>
            <div class="ed-skeleton h-16"></div>
            <div class="ed-skeleton h-16"></div>
            <div class="ed-skeleton h-16"></div>
          </div>
        </div>

        <div v-else-if="professor" class="ed-card p-6 md:p-8 space-y-6">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-5">
            <div class="flex items-start gap-4 min-w-0">
              <div class="w-16 h-16 rounded-2xl bg-primary-soft text-primary flex items-center justify-center font-mono text-xl font-bold shrink-0">
                {{ getInitials(professor.name) }}
              </div>
              <div class="min-w-0 space-y-1">
                <p class="ed-eyebrow">{{ professor.departmentName }} Department</p>
                <h1 class="font-display text-2xl sm:text-3xl md:text-4xl font-extrabold text-ink-dark leading-tight">
                  {{ professor.name }}
                </h1>
                <p class="text-sm text-ink-muted">{{ professor.title }}</p>
                <div v-if="professor.tags.length > 0" class="flex flex-wrap gap-1.5 pt-1.5">
                  <span
                    v-for="tag in professor.tags"
                    :key="tag"
                    class="bg-surface-recessed text-ink-muted px-2.5 py-0.5 rounded-full text-[11px]"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>
            </div>

            <div class="flex items-center gap-3 shrink-0 self-start sm:self-center">
              <div class="w-16 h-16 relative">
                <svg class="w-full h-full -rotate-90" viewBox="0 0 100 100">
                  <circle cx="50" cy="50" r="42" fill="none" stroke="#ded4dc" stroke-width="8" />
                  <circle
                    cx="50"
                    cy="50"
                    r="42"
                    fill="none"
                    stroke="#1d6b42"
                    stroke-width="8"
                    stroke-linecap="round"
                    :stroke-dasharray="2 * Math.PI * 42"
                    :stroke-dashoffset="ringOffset"
                  />
                </svg>
                <span class="absolute inset-0 flex items-center justify-center font-mono text-sm font-bold text-ink-dark tabular-nums">
                  {{ recommendPercent }}%
                </span>
              </div>
              <span class="text-xs text-ink-muted leading-snug">
                Approval<br />Index
              </span>
            </div>
          </div>

          <div class="bg-surface-recessed rounded-2xl p-4 grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div>
              <div class="font-mono text-[10px] uppercase text-ink-subtle">Overall</div>
              <div class="font-mono text-2xl font-bold text-primary tabular-nums mt-0.5">
                {{ professor.overallRating.toFixed(1) }}<span class="text-xs text-ink-subtle font-normal">/5</span>
              </div>
            </div>
            <div>
              <div class="font-mono text-[10px] uppercase text-ink-subtle">Teaching</div>
              <div class="font-mono text-2xl font-bold text-ink-dark tabular-nums mt-0.5">
                {{ professor.avgTeaching.toFixed(1) }}<span class="text-xs text-ink-subtle font-normal">/5</span>
              </div>
            </div>
            <div>
              <div class="font-mono text-[10px] uppercase text-ink-subtle">Grading</div>
              <div class="font-mono text-2xl font-bold text-ink-dark tabular-nums mt-0.5">
                {{ professor.avgGrading.toFixed(1) }}<span class="text-xs text-ink-subtle font-normal">/5</span>
              </div>
            </div>
            <div>
              <div class="font-mono text-[10px] uppercase text-ink-subtle">Workload ({{ workloadDescriptor }})</div>
              <div class="font-mono text-2xl font-bold text-warning tabular-nums mt-0.5">
                {{ professor.avgWorkload.toFixed(1) }}<span class="text-xs text-ink-subtle font-normal">/5</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Body Band -->
    <section class="bg-band-light px-4 md:px-gutter py-10 min-h-[45vh]">
      <div class="max-w-container-max mx-auto">
        <div v-if="isLoading" class="grid grid-cols-1 lg:grid-cols-12 gap-7">
          <div class="lg:col-span-8 space-y-4">
            <div class="ed-card p-6 space-y-3">
              <div class="ed-skeleton h-4 w-1/3"></div>
              <div class="ed-skeleton h-4 w-full"></div>
              <div class="ed-skeleton h-4 w-4/5"></div>
            </div>
          </div>
          <div class="lg:col-span-4">
            <div class="ed-card p-6 space-y-3">
              <div class="ed-skeleton h-5 w-1/2"></div>
              <div class="ed-skeleton h-10 w-full rounded-full"></div>
            </div>
          </div>
        </div>

        <div v-else-if="professor" class="grid grid-cols-1 lg:grid-cols-12 gap-7 items-start">
          <!-- Left: Summary + Reviews -->
          <div class="lg:col-span-8 space-y-6">
            <div v-if="professor.aiSummary" class="ed-card p-6 space-y-1.5">
              <p class="ed-eyebrow text-primary">Student review summary</p>
              <p class="text-sm text-ink-muted leading-relaxed">
                {{ professor.aiSummary }}
              </p>
            </div>

            <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 pb-3 border-b border-border-soft">
              <div class="flex items-baseline gap-2.5">
                <h2 class="text-xl font-extrabold text-ink-dark">Student reviews</h2>
                <span class="ed-eyebrow tabular-nums">({{ reviews.length }})</span>
              </div>

              <div class="flex items-center gap-3">
                <select
                  v-model="sortOption"
                  aria-label="Sort student reviews"
                  class="ed-input rounded-full px-4 py-1.5 text-xs font-semibold cursor-pointer"
                >
                  <option value="Most Helpful">Most helpful</option>
                  <option value="Newest">Newest</option>
                  <option value="Highest Rated">Highest rated</option>
                </select>

                <button
                  type="button"
                  @click="handleWriteReview"
                  class="ed-btn-primary px-5 py-2 text-xs font-semibold cursor-pointer"
                >
                  + Review
                </button>
              </div>
            </div>

            <div v-if="sortedReviews.length > 0" class="space-y-5">
              <ReviewCard v-for="rev in sortedReviews" :key="rev.id" :review="rev" :show-professor="false" />
            </div>

            <div v-else class="ed-card p-8 space-y-4">
              <p class="ed-eyebrow">The conversation is open</p>
              <h3 class="text-xl font-extrabold text-ink-dark">
                No reviews for {{ professor.name }} yet.
              </h3>
              <p class="text-sm text-ink-muted">
                Be the first student to share honest feedback about lectures, grading, and workload.
              </p>
              <button
                type="button"
                @click="handleWriteReview"
                class="ed-btn-primary px-6 py-2.5 text-xs font-semibold cursor-pointer inline-flex items-center gap-3"
              >
                <span>Write first review</span>
                <span aria-hidden="true">→</span>
              </button>
            </div>
          </div>

          <!-- Right Sticky Rail -->
          <aside class="lg:col-span-4 space-y-5 lg:sticky lg:top-24">
            <div class="ed-card p-6 space-y-4">
              <h3 class="text-base font-bold text-ink-dark">Rate this professor</h3>
              <p class="text-xs text-ink-muted leading-relaxed">
                Share your experience with {{ professor.name }}. Your identity never appears on published reviews.
              </p>
              <button
                type="button"
                @click="handleWriteReview"
                class="ed-btn-primary w-full py-2.5 text-xs font-semibold cursor-pointer inline-flex items-center justify-center gap-2"
              >
                <span>Write a review</span>
                <span aria-hidden="true">→</span>
              </button>
            </div>

            <div v-if="gradeDistribution.length > 0" class="ed-card p-6 space-y-4">
              <h3 class="text-base font-bold text-ink-dark">Reported grades</h3>
              <div class="space-y-2.5">
                <div v-for="item in gradeDistribution" :key="item.grade" class="flex items-center gap-2.5 text-xs font-mono">
                  <span class="w-7 font-semibold text-ink-dark">{{ item.grade }}</span>
                  <div class="flex-1 h-2 bg-surface-recessed rounded-full overflow-hidden">
                    <div class="h-full bg-primary rounded-full" :style="{ width: `${item.percent}%` }"></div>
                  </div>
                  <span class="w-7 text-right text-ink-subtle tabular-nums">{{ item.count }}</span>
                </div>
              </div>
            </div>

            <div v-if="coursesReviewed.length > 0" class="ed-card p-6 space-y-3">
              <h3 class="text-base font-bold text-ink-dark">Courses reviewed</h3>
              <div class="flex flex-wrap gap-2">
                <span
                  v-for="course in coursesReviewed"
                  :key="course.code"
                  class="bg-primary-soft text-primary px-3 py-1 rounded-full font-mono text-xs font-semibold"
                >
                  {{ course.code }}
                </span>
              </div>
            </div>

            <div class="ed-card p-6 space-y-2.5">
              <p class="ed-eyebrow">Strict anonymity</p>
              <p class="text-xs text-ink-muted leading-relaxed">
                Verified via @superior.edu.pk SHA-256 hashes and stored without any link back to your email.
              </p>
              <router-link to="/privacy" class="inline-block text-xs font-semibold text-primary hover:underline pt-1">
                Read privacy policy →
              </router-link>
            </div>
          </aside>
        </div>

        <div v-else class="ed-card p-10 text-center max-w-md mx-auto space-y-4">
          <h2 class="text-2xl font-extrabold text-ink-dark">Professor not found</h2>
          <p class="text-sm text-ink-muted">
            The requested faculty profile could not be located in the catalogue.
          </p>
          <router-link to="/search" class="ed-btn-primary inline-flex items-center gap-2 px-6 py-2.5 text-xs font-semibold">
            <span>Back to catalogue</span>
            <span aria-hidden="true">→</span>
          </router-link>
        </div>
      </div>
    </section>
  </main>
</template>
