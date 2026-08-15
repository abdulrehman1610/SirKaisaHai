<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Department, SearchResultItem } from '../types';
import { api } from '../api';
import { useAuthStore } from '../stores/auth';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const queryText = ref((route.query.q as string) || '');
const selectedDept = ref<string>('all');
const departments = ref<Department[]>([]);
const results = ref<SearchResultItem[]>([]);
const isLoading = ref(true);

// Add Teacher Modal State
const showAddModal = ref(false);
const newProfName = ref('');
const newProfDeptId = ref('dept-cs');
const newProfTitle = ref('Assistant Professor');
const isSubmittingProf = ref(false);
const addErrorMsg = ref('');
const addSuccessMsg = ref('');

const filterTab = computed(() => (route.query.tab as string) || 'professors');

const filteredResults = computed(() => {
  if (filterTab.value === 'professors') {
    return results.value.filter((r) => r.type === 'professor');
  }
  if (filterTab.value === 'courses') {
    return results.value.filter((r) => r.type === 'course');
  }
  return results.value;
});

async function loadData() {
  isLoading.value = true;
  try {
    departments.value = await api.getDepartments();
    results.value = await api.search(queryText.value, selectedDept.value);
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadData);

watch([() => route.query.q, selectedDept], ([newQ]) => {
  queryText.value = (newQ as string) || '';
  loadData();
});

function handleSearchInput() {
  router.replace({ query: { ...route.query, q: queryText.value } });
}

async function handleCreateProfessor() {
  addErrorMsg.value = '';
  addSuccessMsg.value = '';

  if (!newProfName.value.trim()) {
    addErrorMsg.value = 'Please enter professor name.';
    return;
  }

  isSubmittingProf.value = true;
  try {
    const newProf = await api.addProfessor({
      name: newProfName.value.trim(),
      departmentId: newProfDeptId.value,
      title: newProfTitle.value,
      tags: ['New Faculty', 'Student Verified'],
      userEmail: authStore.email || undefined
    });

    addSuccessMsg.value = `Successfully added ${newProf.name}!`;
    newProfName.value = '';
    setTimeout(() => {
      showAddModal.value = false;
      addSuccessMsg.value = '';
      loadData();
    }, 1200);
  } catch (err: any) {
    addErrorMsg.value = err.message || 'Failed to add teacher.';
  } finally {
    isSubmittingProf.value = false;
  }
}
</script>

<template>
  <main class="flex-grow w-full max-w-container-max mx-auto px-4 md:px-gutter py-6 md:py-stack-lg flex flex-col gap-4 md:gap-stack-lg">
    <!-- Hero Search Section -->
    <section class="text-center w-full max-w-3xl mx-auto space-y-3 md:space-y-stack-md pt-2 md:pt-stack-md">
      <div class="flex justify-center items-center gap-2 mb-1 md:mb-2">
        <h1 class="font-display-lg text-2xl md:text-[48px] text-primary">
          Search Teacher
        </h1>
      </div>
      <p class="font-body-lg text-sm md:text-body-lg text-on-surface-variant px-2">
        Search professors by name, department, or course code to view ratings & student feedback.
      </p>

      <div class="relative w-full shadow-xl rounded-full bg-white flex items-center p-1.5 md:p-2 border border-outline-variant/30 custom-shadow focus-within:ring-2 focus-within:ring-[#2D6FD1] transition-all">
        <span class="material-symbols-outlined text-outline ml-3 md:ml-4 text-[22px] md:text-[28px]">search</span>
        <input
          v-model="queryText"
          @input="handleSearchInput"
          class="w-full bg-transparent border-none text-base md:text-headline-md font-headline-md text-on-surface focus:ring-0 px-3 md:px-4 py-2.5 md:py-3 placeholder:text-outline-variant outline-none min-w-0"
          placeholder="Type professor name (e.g. Dr. Tariq)..."
          type="text"
        />
        <button @click="loadData" class="bg-primary text-white px-5 md:px-8 py-2.5 md:py-3 rounded-full text-sm md:text-body-lg hover:bg-[#6B2FA0] transition-colors shadow-md flex items-center gap-1 md:gap-2 whitespace-nowrap">
          Search <span class="material-symbols-outlined text-[18px] md:text-[20px]">arrow_forward</span>
        </button>
      </div>
    </section>

    <!-- Department Filters & Add Teacher Button -->
    <section class="flex flex-col sm:flex-row flex-wrap justify-between items-start sm:items-center gap-3 md:gap-4 pb-4 border-b border-surface-variant">
      <div class="flex overflow-x-auto gap-2 md:gap-4 no-scrollbar items-center w-full sm:w-auto pb-1">
        <span class="font-label-sm text-label-sm text-on-surface-variant uppercase tracking-wider whitespace-nowrap">Department:</span>
        <button
          class="px-4 md:px-6 py-1.5 md:py-2 rounded-full text-xs md:text-body-md whitespace-nowrap transition-colors border"
          :class="selectedDept === 'all' ? 'bg-primary-container text-white shadow-md' : 'bg-surface-container-low text-on-surface-variant hover:bg-surface-variant'"
          @click="selectedDept = 'all'"
        >
          All Departments
        </button>

        <button
          v-for="dept in departments"
          :key="dept.id"
          class="px-4 md:px-6 py-1.5 md:py-2 rounded-full text-xs md:text-body-md whitespace-nowrap transition-colors border"
          :class="selectedDept === dept.id ? 'bg-primary-container text-white shadow-md' : 'bg-surface-container-low text-on-surface-variant hover:bg-surface-variant'"
          @click="selectedDept = dept.id"
        >
          {{ dept.name }}
        </button>
      </div>

      <button
        @click="showAddModal = true"
        class="bg-[#6B2A5B] text-white px-5 py-2 rounded-full font-label-sm text-xs font-bold hover:bg-[#6B2FA0] transition-colors flex items-center gap-1.5 shadow-md ml-auto"
      >
        <span class="material-symbols-outlined text-[18px]">person_add</span>
        + Add New Teacher
      </button>
    </section>

    <!-- Results Header -->
    <div class="flex flex-col sm:flex-row items-start sm:items-end justify-between gap-2">
      <h2 class="font-headline-lg text-lg md:text-headline-lg text-on-surface">
        Showing Professors <span v-if="queryText">for "{{ queryText }}"</span>
      </h2>
      <span class="font-label-sm text-label-sm text-on-surface-variant">{{ filteredResults.length }} Professors Found</span>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="text-center py-20">
      <div class="inline-block w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
      <p class="mt-4 text-on-surface-variant font-label-sm">Searching professors...</p>
    </div>

    <!-- Results Bento Grid -->
    <div v-else-if="filteredResults.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-stack-md">
      <div
        v-for="item in filteredResults"
        :key="item.id"
        class="bg-white rounded-[20px] md:rounded-[24px] p-5 md:p-8 custom-shadow flex flex-col gap-4 md:gap-6 relative group hover:-translate-y-1 transition-transform duration-300 shadow-2xl-ambient"
      >
        <div class="absolute -top-3 md:-top-4 -left-3 md:-left-4 bg-[#2E9E4F] text-white px-3 md:px-4 py-1.5 md:py-2 rounded-xl font-stat-display text-[16px] md:text-[20px] shadow-lg flex items-center gap-1 z-10">
          {{ item.rating.toFixed(1) }} <span class="material-symbols-outlined text-[16px]">star</span>
        </div>

        <div class="flex items-start gap-3 md:gap-4 mt-2">
          <div class="w-12 h-12 md:w-16 md:h-16 rounded-full overflow-hidden bg-primary text-white flex-shrink-0 border-2 border-white shadow-md flex items-center justify-center font-display-lg text-base md:text-xl font-bold">
            {{ item.title.split(' ').map(n => n[0]).slice(0, 2).join('') }}
          </div>
          <div class="flex-grow pt-1">
            <h3 class="font-headline-md text-headline-md text-on-surface leading-tight">
              <router-link :to="item.url" class="hover:underline">{{ item.title }}</router-link>
            </h3>
            <p class="font-body-md text-body-md text-on-surface-variant mt-1">{{ item.department }}</p>
            <div class="flex gap-2 mt-3">
              <span class="bg-surface-container-low px-3 py-1 rounded-md font-label-sm text-label-sm text-on-surface-variant">{{ item.subtitle }}</span>
            </div>
          </div>
        </div>

        <div class="bg-surface p-4 rounded-xl flex justify-between items-center mt-auto border border-outline-variant/20">
          <div class="flex flex-col">
            <span class="font-label-sm text-label-sm text-on-surface-variant uppercase">Rating</span>
            <div class="w-24 h-2 bg-[#F4F5F7] rounded-full mt-2 overflow-hidden">
              <div class="h-full bg-gradient-to-r from-[#6B2FA0] to-[#2D6FD1] rounded-full" :style="{ width: `${(item.rating / 5) * 100}%` }"></div>
            </div>
          </div>
          <div class="text-right flex flex-col items-end">
            <span class="font-label-sm text-label-sm text-on-surface-variant uppercase">Reviews</span>
            <span class="font-stat-display text-[20px] text-primary mt-1">{{ item.reviewCount }}</span>
          </div>
        </div>

        <router-link :to="item.url" class="w-full py-3 rounded-xl border-2 border-primary text-primary font-body-md text-body-md font-semibold text-center hover:bg-primary/5 transition-colors active:scale-[0.98]">
          View {{ item.reviewCount }} Reviews
        </router-link>
      </div>
    </div>

    <div v-else class="text-center py-20 bg-white rounded-3xl shadow-2xl-ambient">
      <span class="material-symbols-outlined text-4xl text-on-surface-variant/40 mb-2">search_off</span>
      <h3 class="text-xl font-bold text-on-surface">No professors found</h3>
      <p class="text-on-surface-variant mb-4">Can't find your teacher? Add them to the catalog!</p>
      <button @click="showAddModal = true" class="bg-primary text-white px-6 py-2.5 rounded-full font-label-sm">
        + Add New Teacher
      </button>
    </div>

    <!-- Modal: Add New Teacher -->
    <div v-if="showAddModal" class="fixed inset-0 z-50 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl relative">
        <button @click="showAddModal = false" class="absolute top-4 right-4 text-outline hover:text-primary">
          <span class="material-symbols-outlined">close</span>
        </button>

        <h3 class="font-headline-lg text-xl font-bold text-primary mb-1">Add a New Teacher</h3>
        <p class="text-xs text-on-surface-variant mb-6">Add a missing professor to Superior University catalog.</p>

        <div v-if="addErrorMsg" class="p-3 mb-4 bg-red-50 text-red-700 rounded-xl text-xs font-bold">
          ⚠️ {{ addErrorMsg }}
        </div>
        <div v-if="addSuccessMsg" class="p-3 mb-4 bg-green-50 text-green-700 rounded-xl text-xs font-bold">
          ✓ {{ addSuccessMsg }}
        </div>

        <form @submit.prevent="handleCreateProfessor" class="space-y-4">
          <div>
            <label class="block text-xs font-bold uppercase text-on-surface-variant mb-1">Teacher Full Name</label>
            <input
              v-model="newProfName"
              type="text"
              placeholder="e.g. Dr. Hammad Raza"
              class="w-full bg-surface-container-low border border-outline-variant/30 rounded-xl p-3 text-sm focus:ring-2 focus:ring-primary outline-none"
              required
            />
          </div>

          <div>
            <label class="block text-xs font-bold uppercase text-on-surface-variant mb-1">Department</label>
            <select v-model="newProfDeptId" class="w-full bg-surface-container-low border border-outline-variant/30 rounded-xl p-3 text-sm focus:ring-2 focus:ring-primary outline-none">
              <option v-for="d in departments" :key="d.id" :value="d.id">
                {{ d.name }} ({{ d.code }})
              </option>
            </select>
          </div>

          <div>
            <label class="block text-xs font-bold uppercase text-on-surface-variant mb-1">Title / Designation</label>
            <select v-model="newProfTitle" class="w-full bg-surface-container-low border border-outline-variant/30 rounded-xl p-3 text-sm focus:ring-2 focus:ring-primary outline-none">
              <option value="Professor & HOD">Professor & HOD</option>
              <option value="Professor">Professor</option>
              <option value="Associate Professor">Associate Professor</option>
              <option value="Assistant Professor">Assistant Professor</option>
              <option value="Senior Lecturer">Senior Lecturer</option>
              <option value="Lecturer">Lecturer</option>
            </select>
          </div>

          <div class="flex gap-3 pt-2">
            <button type="button" @click="showAddModal = false" class="px-5 py-3 rounded-full text-xs font-bold border border-outline-variant/30 text-on-surface-variant">
              Cancel
            </button>
            <button type="submit" class="flex-1 bg-primary text-white py-3 rounded-full text-xs font-bold hover:bg-[#6B2FA0]" :disabled="isSubmittingProf">
              <span v-if="!isSubmittingProf">Add Teacher</span>
              <span v-else>Saving...</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>

<style scoped></style>
