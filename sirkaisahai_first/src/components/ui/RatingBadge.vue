<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    score: number;
    size?: 'sm' | 'md' | 'lg';
    showStar?: boolean;
  }>(),
  {
    size: 'md',
    showStar: true
  }
);

const badgeClass = computed(() => {
  if (props.score >= 4.0) return 'rating-high';
  if (props.score >= 3.0) return 'rating-med';
  return 'rating-low';
});

const formattedScore = computed(() => props.score.toFixed(1));
</script>

<template>
  <div class="rating-badge" :class="[badgeClass, size]">
    <span class="score-num">{{ formattedScore }}</span>
    <span v-if="showStar" class="star">★</span>
  </div>
</template>

<style scoped>
.rating-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 800;
  border-radius: var(--radius-full);
  font-family: var(--font-mono);
}

.rating-high {
  background-color: var(--success-bg);
  color: var(--success);
  border: 1px solid rgba(46, 158, 79, 0.2);
}

.rating-med {
  background-color: var(--warning-bg);
  color: var(--warning);
  border: 1px solid rgba(224, 138, 31, 0.2);
}

.rating-low {
  background-color: var(--danger-bg);
  color: var(--danger);
  border: 1px solid rgba(214, 59, 59, 0.2);
}

/* Sizes */
.sm {
  padding: 0.15rem 0.5rem;
  font-size: 0.75rem;
}
.md {
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
}
.lg {
  padding: 0.4rem 1rem;
  font-size: 1.15rem;
}

.star {
  font-size: 0.85em;
  font-family: sans-serif;
}
</style>
