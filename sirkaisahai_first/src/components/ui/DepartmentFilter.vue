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
  <div class="flex gap-2.5 overflow-x-auto py-2 px-1 no-scrollbar">
    <button
      type="button"
      class="px-4 py-2 text-xs font-semibold whitespace-nowrap cursor-pointer"
      :class="modelValue === 'all' ? 'neu-btn-primary' : 'neu-pill-btn text-on-surface-variant'"
      @click="selectDept('all')"
    >
      All Departments
    </button>
    <button
      v-for="dept in departments"
      :key="dept.id"
      type="button"
      class="px-4 py-2 text-xs font-semibold whitespace-nowrap cursor-pointer"
      :class="modelValue === dept.id ? 'neu-btn-primary' : 'neu-pill-btn text-on-surface-variant'"
      @click="selectDept(dept.id)"
    >
      {{ dept.name }} ({{ dept.code }})
    </button>
  </div>
</template>
