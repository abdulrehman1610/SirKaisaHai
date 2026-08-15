<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
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

onMounted(async () => {
  try {
    const cData = await api.getCourseById(courseId.value);
    if (cData) {
      course.value = cData;
      reviews.value = await api.getReviewsForCourse(courseId.value);
    }
  } finally {
    isLoading.value = false;
  }
});

function handleWriteReview() {
  if (!authStore.isVerified) {
    router.push({ path: '/auth', query: { redirect: `/review/new?courseId=${courseId.value}` } });
  } else {
    router.push({ path: '/review/new', query: { courseId: courseId.value } });
  }
}
</script>

<template>
  <div class="course-page container">
    <LoadingSpinner v-if="isLoading" text="Loading course profile..." />

    <div v-else-if="course">
      <!-- ERP-Style Course Header Card -->
      <div class="course-header-card erp-card">
        <div class="header-top">
          <div>
            <div class="code-badge">📚 {{ course.code }} • {{ course.creditHours }} Credit Hours</div>
            <h1 class="course-title">{{ course.title }}</h1>
            <p class="dept-text">Department of {{ course.departmentName }} • Superior University</p>
          </div>

          <div class="rating-box">
            <RatingBadge :score="course.avgRating" size="lg" />
            <span class="reviews-count">{{ course.totalReviews }} verified reviews</span>
          </div>
        </div>

        <p class="course-desc">{{ course.description }}</p>

        <!-- Stat Boxes Row -->
        <div class="stat-boxes-grid">
          <div class="erp-stat-box">
            <span class="erp-stat-number">{{ course.avgRating.toFixed(1) }}</span>
            <span class="erp-stat-label">Average Score</span>
          </div>
          <div class="erp-stat-box">
            <span class="erp-stat-number">{{ course.creditHours }}</span>
            <span class="erp-stat-label">Credit Hours</span>
          </div>
          <div class="erp-stat-box">
            <span class="erp-stat-number">{{ reviews.length }}</span>
            <span class="erp-stat-label">Student Feedback</span>
          </div>
        </div>
      </div>

      <!-- AI Course Summary -->
      <div v-if="course.aiSummary" class="ai-summary-card">
        <div class="ai-header">
          <span class="sparkle-icon">✨</span>
          <span class="ai-title">AI Summary of Course Reviews</span>
        </div>
        <p class="ai-text">{{ course.aiSummary }}</p>
      </div>

      <!-- Reviews Section -->
      <div class="reviews-section-header">
        <h2>Course Reviews & Ratings ({{ reviews.length }})</h2>

        <button type="button" class="write-btn" @click="handleWriteReview">
          ✍️ Write a Review
        </button>
      </div>

      <div v-if="reviews.length > 0" class="reviews-list">
        <ReviewCard v-for="rev in reviews" :key="rev.id" :review="rev" />
      </div>

      <div v-else class="erp-card empty-reviews">
        <p>No reviews posted yet for {{ course.code }}. Help Superior students by sharing your experience!</p>
        <button type="button" class="write-btn" @click="handleWriteReview">
          Submit First Review
        </button>
      </div>
    </div>

    <div v-else class="not-found container">
      <h2>Course Not Found</h2>
      <router-link to="/search" class="back-link">← Return to Catalog</router-link>
    </div>
  </div>
</template>

<style scoped>
.course-page {
  padding-top: 2rem;
  padding-bottom: 4rem;
}

.course-header-card {
  margin-bottom: 2rem;
}

.header-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border);
  flex-wrap: wrap;
}

.code-badge {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--primary-700);
  text-transform: uppercase;
  letter-spacing: 0.04em;
  margin-bottom: 0.25rem;
}

.course-title {
  font-size: 2.1rem;
  line-height: 1.2;
}

.dept-text {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.rating-box {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.35rem;
}

.reviews-count {
  font-size: 0.825rem;
  color: var(--text-secondary);
}

.course-desc {
  margin: 1.25rem 0 1.5rem 0;
  font-size: 0.975rem;
  color: var(--text-primary);
  line-height: 1.6;
}

.stat-boxes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1.25rem;
  padding-top: 1rem;
}

/* AI Summary */
.ai-summary-card {
  background: var(--info-bg);
  border: 1px solid rgba(45, 111, 209, 0.2);
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-bottom: 0.35rem;
}

.ai-title {
  font-family: var(--font-heading);
  font-weight: 700;
  color: var(--info);
  font-size: 0.875rem;
  text-transform: uppercase;
}

.ai-text {
  font-size: 0.95rem;
  color: #1E3A8A;
  line-height: 1.55;
}

.reviews-section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.write-btn {
  background: var(--primary-700);
  color: #FFFFFF;
  font-family: var(--font-heading);
  font-weight: 700;
  padding: 0.55rem 1.15rem;
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  transition: background var(--transition-fast);
}

.write-btn:hover {
  background: var(--primary-900);
}

.empty-reviews {
  text-align: center;
  padding: 3rem 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
</style>
