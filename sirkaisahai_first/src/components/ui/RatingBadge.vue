<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    score: number;
    size?: 'sm' | 'md' | 'lg';
    showScale?: boolean;
  }>(),
  {
    size: 'md',
    showScale: false
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
  <div class="rating-badge tabular-nums" :class="[badgeClass, size]">
    <span class="score-num">{{ formattedScore }}</span>
    <span v-if="showScale" class="scale">/5</span>
  </div>
</template>

<style scoped>
.rating-badge {
  display: inline-flex;
  align-items: baseline;
  gap: 0.14rem;
  font-family: var(--font-mono);
  font-weight: 700;
  line-height: 1;
  border-radius: 10px;
}

.rating-high {
  background: var(--success-bg);
  color: var(--success);
}

.rating-med {
  background: var(--warning-bg);
  color: var(--warning);
}

.rating-low {
  background: var(--danger-bg);
  color: var(--danger);
}

.sm {
  padding: 0.28rem 0.5rem;
  font-size: 0.75rem;
}

.md {
  padding: 0.4rem 0.68rem;
  font-size: 0.875rem;
}

.lg {
  padding: 0.5rem 0.85rem;
  font-size: 1.05rem;
}

.scale {
  font-size: 0.72em;
  opacity: 0.7;
  font-weight: 500;
}
</style>
