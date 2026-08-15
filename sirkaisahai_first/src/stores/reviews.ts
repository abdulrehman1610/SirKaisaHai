import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Department, SearchResultItem } from '../types';
import { api } from '../api';

export const useReviewsStore = defineStore('reviews', () => {
  const departments = ref<Department[]>([]);
  const searchQuery = ref<string>('');
  const selectedDepartment = ref<string>('all');
  const searchResults = ref<SearchResultItem[]>([]);
  const isLoading = ref<boolean>(false);

  async function fetchDepartments() {
    if (departments.value.length === 0) {
      departments.value = await api.getDepartments();
    }
  }

  async function performSearch(query?: string, deptId?: string) {
    if (query !== undefined) searchQuery.value = query;
    if (deptId !== undefined) selectedDepartment.value = deptId;

    isLoading.value = true;
    try {
      searchResults.value = await api.search(searchQuery.value, selectedDepartment.value);
    } finally {
      isLoading.value = false;
    }
  }

  return {
    departments,
    searchQuery,
    selectedDepartment,
    searchResults,
    isLoading,
    fetchDepartments,
    performSearch
  };
});
