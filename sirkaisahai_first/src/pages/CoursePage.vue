<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import RatingBadge from '../components/ui/RatingBadge.vue';
import ReviewCard from '../components/ui/ReviewCard.vue';
import LoadingSpinner from '../components/ui/LoadingSpinner.vue';
import type { Course, Review } from '../types';
import { api } from '../api';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const course = ref<Course | null>(null);
const reviews = ref<Review[]>([]);
const isLoading = ref(true);

const courseId = computed(() => route.params.id as string);

async function loadCourse() {
  isLoading.value = true;
  try {
    const cData = await api.getCourseById(courseId.value);
    if (cData) {
      course.value = cData;
      reviews.value = await api.getReviewsForCourse(courseId.value);
    } else {
      course.value = null;
      reviews.value = [];
    }
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadCourse);
watch(courseId, loadCourse);

function handleWriteReview() {
  if (!authStore.isVerified) {
    router.push({ path: '/auth', query: { redirect: `/review/new?courseId=${courseId.value}` } });
  } else {
    router.push({ path: '/review/new', query: { courseId: courseId.value } });
  }
}
</script>

<template>
  <main class="w-full">
    <section class="bg-band-hero px-4 md:px-gutter pt-24 pb-10">
      <div class="max-w-container-max mx-auto">
        <LoadingSpinner v-if="isLoading" text="Loading course profile..." :rows="2" />

        <div v-else-if="course" class="ed-card p-6 md:p-8 space-y-6">
          <div class="flex flex-col sm:flex-row justify-between items-start gap-4">
            <div class="space-y-1">
              <p class="ed-eyebrow text-primary">
                {{ course.code }} · {{ course.creditHours }} Credit Hours
              </p>
              <h1 class="font-display text-2xl sm:text-3xl md:text-4xl font-extrabold text-ink-dark">
                {{ course.title }}
              </h1>
              <p class="text-sm text-ink-muted">
                Department of {{ course.departmentName }} · Superior University
              </p>
            </div>

            <div class="flex flex-col items-start sm:items-end gap-1">
              <RatingBadge :score="course.avgRating" size="lg" show-scale />
              <span class="ed-eyebrow tabular-nums">{{ reviews.length }} reviews</span>
            </div>
          </div>

          <p class="text-sm text-ink-muted leading-relaxed">
            {{ course.description }}
          </p>

          <div class="bg-surface-recessed rounded-2xl p-4 grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <div class="font-mono text-[10px] uppercase text-ink-subtle">Average score</div>
              <div class="font-mono text-xl font-bold text-primary tabular-nums mt-0.5">
                {{ course.avgRating.toFixed(1) }}/5
              </div>
            </div>
            <div>
              <div class="font-mono text-[10px] uppercase text-ink-subtle">Credit hours</div>
              <div class="font-mono text-xl font-bold text-ink-dark tabular-nums mt-0.5">
                {{ course.creditHours }}
              </div>
            </div>
            <div>
              <div class="font-mono text-[10px] uppercase text-ink-subtle">Student feedback</div>
              <div class="font-mono text-xl font-bold text-ink-dark tabular-nums mt-0.5">
                {{ reviews.length }}
              </div>
            </div>
          </div>

          <div v-if="course.aiSummary" class="bg-surface-recessed rounded-2xl p-4 space-y-1">
            <p class="ed-eyebrow text-primary">Course overview summary</p>
            <p class="text-sm text-ink-muted leading-relaxed">{{ course.aiSummary }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="bg-band-light px-4 md:px-gutter py-10 min-h-[45vh]">
      <div class="max-w-container-max mx-auto space-y-6">
        <template v-if="!isLoading && course">
          <div class="flex flex-wrap justify-between items-center gap-3 pb-3 border-b border-border-soft">
            <div class="flex items-baseline gap-2.5">
              <h2 class="text-xl font-extrabold text-ink-dark">Course reviews</h2>
              <span class="ed-eyebrow tabular-nums">({{ reviews.length }})</span>
            </div>

            <button
              type="button"
              class="ed-btn-primary px-5 py-2.5 text-xs font-semibold cursor-pointer inline-flex items-center gap-2"
              @click="handleWriteReview"
            >
              <span>Write a review</span>
              <span aria-hidden="true">→</span>
            </button>
          </div>

          <div v-if="reviews.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ReviewCard v-for="rev in reviews" :key="rev.id" :review="rev" :show-professor="true" />
          </div>

          <div v-else class="ed-card p-9 text-center max-w-md mx-auto space-y-4">
            <p class="text-sm text-ink-muted">
              No reviews posted yet for {{ course.code }}. Share your experience with fellow Superior students.
            </p>
            <button
              type="button"
              class="ed-btn-primary px-6 py-2.5 text-xs font-semibold cursor-pointer"
              @click="handleWriteReview"
            >
              Submit first review →
            </button>
          </div>
        </template>

        <div v-else-if="!isLoading" class="ed-card p-10 text-center max-w-md mx-auto space-y-4">
          <h2 class="text-2xl font-extrabold text-ink-dark">Course not found</h2>
          <router-link to="/courses" class="ed-btn-primary inline-block px-6 py-2.5 text-xs font-semibold">
            Return to courses →
          </router-link>
        </div>
      </div>
    </section>
  </main>
</template>
