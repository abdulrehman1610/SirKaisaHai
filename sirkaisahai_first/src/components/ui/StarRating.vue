<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    modelValue?: number;
    readonly?: boolean;
    showValue?: boolean;
    label?: string;
    mode?: 'rating' | 'intensity';
  }>(),
  {
    modelValue: 5,
    readonly: true,
    showValue: false,
    label: '',
    mode: 'rating'
  }
);

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void;
}>();

const intensityLabels: Record<number, string> = {
  1: 'Light',
  2: 'Easy',
  3: 'Moderate',
  4: 'Heavy',
  5: 'Intense'
};

function setRating(val: number) {
  if (!props.readonly) {
    emit('update:modelValue', val);
  }
}
</script>

<template>
  <div class="inline-flex items-center gap-3 flex-wrap">
    <span v-if="label" class="text-sm font-semibold text-on-surface">{{ label }}</span>

    <div v-if="!readonly" class="inline-flex gap-1.5 flex-wrap" role="radiogroup" :aria-label="label || 'Rating'">
      <button
        v-for="num in [1, 2, 3, 4, 5]"
        :key="num"
        type="button"
        class="px-3 py-1.5 font-mono text-xs font-semibold cursor-pointer tabular-nums"
        :class="
          Math.round(modelValue) === num
            ? mode === 'intensity'
              ? 'neu-pill-btn neu-active text-warning'
              : 'neu-btn-primary'
            : 'neu-pill-btn text-on-surface-variant'
        "
        @click="setRating(num)"
      >
        {{ mode === 'intensity' ? `${num} ${intensityLabels[num]}` : `${num}.0` }}
      </button>
    </div>

    <span v-if="showValue" class="font-mono text-sm font-bold text-primary tabular-nums">
      {{ modelValue.toFixed(1) }} <span class="text-xs font-normal text-outline">/ 5.0</span>
    </span>
  </div>
</template>
