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
  <div class="rating-badge neu-tile tabular-nums" :class="[badgeClass, size]">
    <span class="score-num">{{ formattedScore }}</span>
    <span v-if="showScale" class="scale">/5</span>
  </div>
</template>

<style scoped>
.rating-badge {
  display: inline-flex;
  align-items: baseline;
  gap: 0.12rem;
  font-weight: 700;
  font-family: var(--font-mono);
  line-height: 1;
  border-radius: 10px;
}

.rating-high {
  color: var(--success);
}

.rating-med {
  color: var(--warning);
}

.rating-low {
  color: var(--danger);
}

.sm {
  padding: 0.3rem 0.55rem;
  font-size: 0.75rem;
}

.md {
  padding: 0.42rem 0.7rem;
  font-size: 0.875rem;
}

.lg {
  padding: 0.55rem 0.9rem;
  font-size: 1.05rem;
}

.scale {
  font-size: 0.74em;
  color: var(--text-muted);
  font-weight: 500;
}
</style>
