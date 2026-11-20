<script setup lang="ts">
import type { Department } from '../../types';

defineProps<{
  departments: Department[];
  modelValue: string;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', val: string): void;
}>();

function selectDept(id: string) {
  emit('update:modelValue', id);
}
</script>

<template>
  <div class="flex gap-2 overflow-x-auto py-1.5 px-0.5 no-scrollbar">
    <button
      type="button"
      class="px-4 py-2 text-xs font-semibold whitespace-nowrap cursor-pointer"
      :class="modelValue === 'all' ? 'ed-btn-primary' : 'ed-btn-soft text-ink-muted'"
      @click="selectDept('all')"
    >
      All departments
    </button>
    <button
      v-for="dept in departments"
      :key="dept.id"
      type="button"
      class="px-4 py-2 text-xs font-semibold whitespace-nowrap cursor-pointer"
      :class="modelValue === dept.id ? 'ed-btn-primary' : 'ed-btn-soft text-ink-muted'"
      @click="selectDept(dept.id)"
    >
      {{ dept.name }} ({{ dept.code }})
    </button>
  </div>
</template>
