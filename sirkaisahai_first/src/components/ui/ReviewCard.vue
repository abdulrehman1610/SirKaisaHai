<script setup lang="ts">
import { ref } from 'vue';
import type { Review } from '../../types';
import RatingBadge from './RatingBadge.vue';
import { api } from '../../api';

const props = defineProps<{
  review: Review;
}>();

const isHelpful = ref(props.review.isHelpfulVoted || false);
const helpfulCount = ref(props.review.helpfulCount);
const isVoting = ref(false);

async function toggleHelpful() {
  if (isVoting.value) return;
  isVoting.value = true;
  try {
    const res = await api.voteHelpful(props.review.id);
    if (res.success) {
      isHelpful.value = !isHelpful.value;
      helpfulCount.value = res.newCount;
    }
  } finally {
    isVoting.value = false;
  }
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
}
</script>

<template>
  <div class="review-card stitch-card">
    <!-- Header -->
    <div class="review-header">
      <div class="user-meta">
        <div class="dept-avatar">
          {{ review.courseCode.substring(0, 2) }}
        </div>
        <div class="meta-details">
          <div class="title-row">
            <router-link :to="`/course/${review.courseId}`" class="course-title-link">
              {{ review.courseCode }} - {{ review.courseTitle }}
            </router-link>
            <span class="verified-tag">
              🎓 Verified Student
            </span>
          </div>
          <div class="sub-meta">
            <router-link :to="`/professor/${review.professorId}`" class="prof-link">
              {{ review.professorName }}
            </router-link>
            <span class="dot">•</span>
            <span>🔒 100% Anonymous</span>
            <span class="dot">•</span>
            <span>{{ review.semesterTaken }}</span>
          </div>
        </div>
      </div>

      <div class="score-badge-box">
        <RatingBadge :score="review.overallScore" size="lg" />
        <span class="overall-label">OVERALL</span>
      </div>
    </div>

    <!-- Comment -->
    <p class="comment-body">{{ review.comment }}</p>

    <!-- Mini Progress Metrics -->
    <div class="metrics-bars-row">
      <div class="mini-bar-item">
        <div class="mini-bar-header">
          <span>TEACHING</span>
          <strong class="bar-num">{{ review.ratingTeaching.toFixed(1) }}</strong>
        </div>
        <div class="mini-track">
          <div class="mini-fill" :style="{ width: `${(review.ratingTeaching / 5) * 100}%` }"></div>
        </div>
      </div>

      <div class="mini-bar-item">
        <div class="mini-bar-header">
          <span>GRADING</span>
          <strong class="bar-num">{{ review.ratingGrading.toFixed(1) }}</strong>
        </div>
        <div class="mini-track">
          <div class="mini-fill" :style="{ width: `${(review.ratingGrading / 5) * 100}%` }"></div>
        </div>
      </div>

      <div class="mini-bar-item">
        <div class="mini-bar-header">
          <span>WORKLOAD</span>
          <strong class="bar-num">{{ review.ratingWorkload.toFixed(1) }}</strong>
        </div>
        <div class="mini-track">
          <div class="mini-fill warning" :style="{ width: `${(review.ratingWorkload / 5) * 100}%` }"></div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="review-card-footer">
      <div class="tags-group">
        <span v-if="review.gradeReceived" class="grade-pill">
          Grade: <strong>{{ review.gradeReceived }}</strong>
        </span>
        <span v-for="tag in review.tags" :key="tag" class="tag-pill">
          {{ tag }}
        </span>
      </div>

      <button
        type="button"
        class="helpful-button"
        :class="{ active: isHelpful }"
        @click="toggleHelpful"
        :disabled="isVoting"
      >
        <span class="thumb-icon">👍</span>
        <span>Helpful ({{ helpfulCount }})</span>
      </button>
    </div>
  </div>
</template>

<style scoped>
.review-card {
  margin-bottom: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 1rem;
}

.user-meta {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.dept-avatar {
  width: 48px;
  height: 48px;
  background: var(--secondary-fixed);
  color: var(--secondary-accent);
  font-family: var(--font-heading);
  font-weight: 800;
  font-size: 1.1rem;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.meta-details {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.title-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.course-title-link {
  font-weight: 700;
  font-size: 1.05rem;
  color: var(--text-primary);
  text-decoration: none;
}

.course-title-link:hover {
  color: var(--primary-container);
}

.verified-tag {
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--success);
  background: var(--success-bg);
  padding: 0.15rem 0.5rem;
  border-radius: var(--radius-sm);
  text-transform: uppercase;
}

.sub-meta {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.prof-link {
  color: var(--primary-container);
  font-weight: 700;
}

.dot { color: var(--text-muted); }

.score-badge-box {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.2rem;
}

.overall-label {
  font-family: var(--font-mono);
  font-size: 0.65rem;
  font-weight: 700;
  color: var(--text-muted);
  letter-spacing: 0.05em;
}

.comment-body {
  font-size: 1rem;
  line-height: 1.6;
  color: var(--text-secondary);
}

.metrics-bars-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1.25rem;
  padding: 0.85rem 1.25rem;
  background: var(--bg-page);
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
}

.mini-bar-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.mini-bar-header {
  display: flex;
  justify-content: space-between;
  font-family: var(--font-mono);
  font-size: 0.7rem;
  font-weight: 700;
  color: var(--text-muted);
}

.bar-num {
  color: var(--text-primary);
}

.mini-track {
  height: 6px;
  background: var(--border);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.mini-fill {
  height: 100%;
  background: linear-gradient(90deg, #6B2FA0 0%, #2D6FD1 100%);
  border-radius: var(--radius-full);
}

.mini-fill.warning {
  background: var(--warning);
}

.review-card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border);
}

.tags-group {
  display: flex;
  gap: 0.4rem;
  flex-wrap: wrap;
}

.grade-pill {
  font-family: var(--font-mono);
  font-size: 0.78rem;
  padding: 0.2rem 0.6rem;
  background: var(--warning-bg);
  color: var(--warning);
  border-radius: var(--radius-sm);
}

.tag-pill {
  font-size: 0.78rem;
  padding: 0.2rem 0.55rem;
  background: var(--action-blue-bg);
  color: var(--action-blue);
  border-radius: var(--radius-sm);
}

.helpful-button {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  font-family: var(--font-mono);
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-secondary);
  padding: 0.4rem 0.85rem;
  border-radius: var(--radius-full);
  background: var(--bg-page);
  border: 1px solid var(--border);
  transition: all var(--transition-fast);
}

.helpful-button:hover, .helpful-button.active {
  background: var(--primary-container);
  color: #FFFFFF;
  border-color: var(--primary-container);
}
</style>
