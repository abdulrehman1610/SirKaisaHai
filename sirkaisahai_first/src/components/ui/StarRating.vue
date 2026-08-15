<script setup lang="ts">
import { ref, computed } from 'vue';

const props = withDefaults(
  defineProps<{
    modelValue?: number;
    readonly?: boolean;
    size?: 'sm' | 'md' | 'lg';
    showValue?: boolean;
    label?: string;
  }>(),
  {
    modelValue: 5,
    readonly: true,
    size: 'md',
    showValue: false,
    label: ''
  }
);

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void;
}>();

const hoverRating = ref<number | null>(null);

const activeRating = computed(() => {
  if (hoverRating.value !== null && !props.readonly) {
    return hoverRating.value;
  }
  return props.modelValue;
});

function setRating(val: number) {
  if (!props.readonly) {
    emit('update:modelValue', val);
  }
}

function handleMouseEnter(val: number) {
  if (!props.readonly) {
    hoverRating.value = val;
  }
}

function handleMouseLeave() {
  if (!props.readonly) {
    hoverRating.value = null;
  }
}
</script>

<template>
  <div class="star-rating-container" :class="[size, { interactive: !readonly }]">
    <span v-if="label" class="rating-label">{{ label }}</span>

    <div class="stars-row" @mouseleave="handleMouseLeave">
      <button
        v-for="star in 5"
        :key="star"
        type="button"
        class="star-btn"
        :disabled="readonly"
        @click="setRating(star)"
        @mouseenter="handleMouseEnter(star)"
        :aria-label="`Rate ${star} out of 5`"
      >
        <span
          class="material-symbols-outlined star-icon-symbol"
          :class="star <= Math.round(activeRating) ? 'filled' : 'empty'"
        >
          star
        </span>
      </button>
    </div>

    <!-- Quick Score Selector Pills for Interactive Mode -->
    <div v-if="!readonly" class="score-pills-selector">
      <button
        v-for="num in [1, 2, 3, 4, 5]"
        :key="num"
        type="button"
        class="score-pill"
        :class="{ active: modelValue === num }"
        @click="setRating(num)"
      >
        {{ num }}.0
      </button>
    </div>

    <span v-if="showValue" class="rating-val font-stat-display text-primary">
      {{ modelValue.toFixed(1) }} <span class="text-xs text-outline font-normal">/ 5.0</span>
    </span>
  </div>
</template>

<style scoped>
.star-rating-container {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
}

.rating-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: #50434b;
}

.stars-row {
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

.star-btn {
  padding: 0;
  border: none;
  background: transparent;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s ease;
}

.interactive .star-btn:hover {
  transform: scale(1.25);
}

.star-icon-symbol {
  font-size: 24px;
  transition: color 0.15s ease;
}

.lg .star-icon-symbol { font-size: 32px; }
.md .star-icon-symbol { font-size: 24px; }
.sm .star-icon-symbol { font-size: 18px; }

.star-icon-symbol.filled {
  color: #E59A1D;
  font-variation-settings: 'FILL' 1;
}

.star-icon-symbol.empty {
  color: #D4C1CB;
  font-variation-settings: 'FILL' 0;
}

.score-pills-selector {
  display: flex;
  gap: 0.25rem;
}

.score-pill {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.2rem 0.5rem;
  border-radius: 0.375rem;
  background: #f3f4f6;
  color: #50434b;
  border: 1px solid #d4c1cb;
  cursor: pointer;
  transition: all 0.15s ease;
}

.score-pill:hover {
  background: #ffd7ee;
  color: #501243;
}

.score-pill.active {
  background: #6b2a5b;
  color: #ffffff;
  border-color: #6b2a5b;
}

.rating-val {
  font-size: 1.1rem;
  font-weight: 700;
}
</style>
