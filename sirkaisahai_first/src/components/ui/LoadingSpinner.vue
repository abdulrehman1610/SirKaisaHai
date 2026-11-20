<script setup lang="ts">
withDefaults(
  defineProps<{
    text?: string;
    rows?: number;
  }>(),
  {
    text: '',
    rows: 3
  }
);
</script>

<template>
  <div class="space-y-4 w-full py-2" role="status" aria-live="polite">
    <div v-for="i in rows" :key="i" class="ed-card p-6 space-y-3">
      <div class="ed-skeleton h-4 w-2/5"></div>
      <div class="ed-skeleton h-3 w-full"></div>
      <div class="ed-skeleton h-3 w-3/4"></div>
    </div>
    <span v-if="text" class="sr-only">{{ text }}</span>
  </div>
</template>
