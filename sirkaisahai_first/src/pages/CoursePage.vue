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
  <main class="max-w-container-max mx-auto px-4 md:px-gutter pt-4 pb-10 space-y-7">
    <LoadingSpinner v-if="isLoading" text="Loading course profile..." :rows="3" />

    <template v-else-if="course">
      <div class="neu-surface-lg p-6 md:p-8 space-y-6">
        <div class="flex flex-col sm:flex-row justify-between items-start gap-4">
          <div class="space-y-1">
            <div class="font-mono text-xs font-bold text-primary uppercase">
              {{ course.code }} · {{ course.creditHours }} Credit Hours
            </div>
            <h1 class="text-2xl md:text-3xl font-extrabold text-primary">
              {{ course.title }}
            </h1>
            <p class="text-sm text-on-surface-variant">
              Department of {{ course.departmentName }} · Superior University
            </p>
          </div>

          <div class="flex flex-col items-start sm:items-end gap-1.5">
            <RatingBadge :score="course.avgRating" size="lg" show-scale />
            <span class="font-mono text-xs text-outline tabular-nums">{{ reviews.length }} reviews</span>
          </div>
        </div>

        <p class="text-sm text-on-surface-variant leading-relaxed">
          {{ course.description }}
        </p>

        <div class="neu-inset-tray p-4 grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <div class="font-mono text-[10px] uppercase text-outline">Average Score</div>
            <div class="font-mono text-xl font-bold text-primary tabular-nums mt-0.5">
              {{ course.avgRating.toFixed(1) }}/5
            </div>
          </div>
          <div>
            <div class="font-mono text-[10px] uppercase text-outline">Credit Hours</div>
            <div class="font-mono text-xl font-bold text-on-surface tabular-nums mt-0.5">
              {{ course.creditHours }}
            </div>
          </div>
          <div>
            <div class="font-mono text-[10px] uppercase text-outline">Student Feedback</div>
            <div class="font-mono text-xl font-bold text-on-surface tabular-nums mt-0.5">
              {{ reviews.length }}
            </div>
          </div>
        </div>

        <div v-if="course.aiSummary" class="neu-inset-tray p-4 space-y-1">
          <div class="text-[11px] font-bold uppercase tracking-[0.12em] text-primary">
            Course Overview Summary
          </div>
          <p class="text-sm text-on-surface-variant leading-relaxed">{{ course.aiSummary }}</p>
        </div>
      </div>

      <div class="flex flex-wrap justify-between items-center gap-3">
        <div class="flex items-center gap-2.5">
          <h2 class="text-lg font-bold text-on-surface">Course Reviews</h2>
          <span class="neu-circle-badge min-w-[26px] h-[26px] px-2 inline-flex items-center justify-center font-mono text-xs font-semibold text-on-surface-variant tabular-nums">
            {{ reviews.length }}
          </span>
        </div>

        <button
          type="button"
          class="neu-btn-primary px-5 py-2.5 text-xs font-semibold cursor-pointer"
          @click="handleWriteReview"
        >
          Write a Review
        </button>
      </div>

      <div v-if="reviews.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <ReviewCard v-for="rev in reviews" :key="rev.id" :review="rev" :show-professor="true" />
      </div>

      <div v-else class="neu-card p-9 text-center max-w-md mx-auto space-y-4">
        <p class="text-sm text-on-surface-variant">
          No reviews posted yet for {{ course.code }}. Help Superior students by sharing your experience!
        </p>
        <button
          type="button"
          class="neu-btn-primary px-6 py-2.5 text-xs font-semibold cursor-pointer"
          @click="handleWriteReview"
        >
          Submit First Review
        </button>
      </div>
    </template>

    <div v-else class="neu-card p-10 text-center max-w-md mx-auto space-y-4">
      <h2 class="text-xl font-bold text-primary">Course Not Found</h2>
      <router-link to="/courses" class="neu-btn-primary inline-block px-6 py-2.5 text-xs font-semibold">
        Return to Courses
      </router-link>
    </div>
  </main>
</template>
