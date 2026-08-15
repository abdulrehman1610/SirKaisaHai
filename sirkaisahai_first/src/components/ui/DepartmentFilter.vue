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
  <div class="dept-filter-container">
    <button
      type="button"
      class="chip"
      :class="{ active: modelValue === 'all' }"
      @click="selectDept('all')"
    >
      All Departments
    </button>
    <button
      v-for="dept in departments"
      :key="dept.id"
      type="button"
      class="chip"
      :class="{ active: modelValue === dept.id }"
      @click="selectDept(dept.id)"
    >
      {{ dept.name }} ({{ dept.code }})
    </button>
  </div>
</template>

<style scoped>
.dept-filter-container {
  display: flex;
  gap: 0.5rem;
  overflow-x: auto;
  padding: 0.25rem 0 0.5rem 0;
  scrollbar-width: none;
}
.dept-filter-container::-webkit-scrollbar {
  display: none;
}

.chip {
  padding: 0.45rem 1rem;
  border-radius: var(--radius-full);
  font-size: 0.85rem;
  font-weight: 600;
  background: var(--bg-surface);
  color: var(--text-muted);
  border: 1px solid var(--border-medium);
  white-space: nowrap;
  transition: all var(--transition-fast);
}

.chip:hover {
  background: var(--bg-surface-elevated);
  color: var(--primary-navy);
  border-color: var(--primary-navy);
}

.chip.active {
  background: var(--primary-navy);
  color: var(--text-on-dark);
  border-color: var(--primary-navy);
  box-shadow: var(--shadow-sm);
}
</style>
