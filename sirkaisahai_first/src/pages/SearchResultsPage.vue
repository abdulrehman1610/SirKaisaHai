<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Department, SearchResultItem } from '../types';
import { api } from '../api';
import { useAuthStore } from '../stores/auth';
import DepartmentFilter from '../components/ui/DepartmentFilter.vue';
import RatingBadge from '../components/ui/RatingBadge.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const queryText = ref((route.query.q as string) || '');
const selectedDept = ref<string>((route.query.dept as string) || 'all');
const sortBy = ref<'rating' | 'reviews' | 'name'>('rating');
const departments = ref<Department[]>([]);
const results = ref<SearchResultItem[]>([]);
const isLoading = ref(true);

const showAddModal = ref(false);
const newProfName = ref('');
const newProfDeptId = ref('dept-cs');
const newProfTitle = ref('Assistant Professor');
const isSubmittingProf = ref(false);
const addErrorMsg = ref('');
const addSuccessMsg = ref('');

const filterTab = computed(() => (route.query.tab as string) || 'professors');

const filteredResults = computed(() => {
  let list = results.value;
  if (filterTab.value === 'professors') {
    list = list.filter((r) => r.type === 'professor');
  } else if (filterTab.value === 'courses') {
    list = list.filter((r) => r.type === 'course');
  }

  return [...list].sort((a, b) => {
    if (sortBy.value === 'reviews') return b.reviewCount - a.reviewCount;
    if (sortBy.value === 'name') return a.title.localeCompare(b.title);
    return b.rating - a.rating;
  });
});

async function loadData() {
  isLoading.value = true;
  try {
    const [depts, items] = await Promise.all([
      api.getDepartments(),
      api.search(queryText.value, selectedDept.value)
    ]);
    departments.value = depts;
    results.value = items;
  } finally {
    isLoading.value = false;
  }
}

onMounted(loadData);

watch([() => route.query.q, () => route.query.dept], ([newQ, newDept]) => {
  queryText.value = (newQ as string) || '';
  if (typeof newDept === 'string' && newDept) {
    selectedDept.value = newDept;
  }
  loadData();
});

watch(selectedDept, (dept) => {
  router.replace({ query: { ...route.query, dept: dept === 'all' ? undefined : dept } });
  loadData();
});

function handleSearchInput() {
  router.replace({ query: { ...route.query, q: queryText.value || undefined } });
}

function getInitials(name: string) {
  return name
    .split(' ')
    .filter(Boolean)
    .map((part) => part[0])
    .slice(0, 2)
    .join('')
    .toUpperCase();
}

async function handleCreateProfessor() {
  addErrorMsg.value = '';
  addSuccessMsg.value = '';

  if (!newProfName.value.trim()) {
    addErrorMsg.value = 'Please enter the professor name.';
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

    addSuccessMsg.value = `Successfully added ${newProf.name}.`;
    newProfName.value = '';
    setTimeout(() => {
      showAddModal.value = false;
      addSuccessMsg.value = '';
      loadData();
    }, 1000);
  } catch (err: unknown) {
    addErrorMsg.value = err instanceof Error ? err.message : 'Failed to add teacher.';
  } finally {
    isSubmittingProf.value = false;
  }
}
</script>

<template>
  <main class="w-full max-w-container-max mx-auto px-4 md:px-gutter pt-4 pb-10 space-y-8">
    <!-- Search Banner Card -->
    <section class="neu-surface-lg px-5 py-9 sm:px-10 text-center space-y-4">
      <p class="text-[10px] font-semibold uppercase tracking-[0.18em] text-outline">
        Superior University Catalogue
      </p>
      <h1 class="text-2xl sm:text-3xl md:text-4xl font-extrabold text-primary">
        Search Professors
      </h1>
      <p class="text-sm text-on-surface-variant max-w-lg mx-auto">
        Search faculty by name or designation across all 8 Computing &amp; IT departments.
      </p>

      <div class="neu-inset rounded-full p-1.5 pl-5 flex items-center gap-2 max-w-xl mx-auto mt-3">
        <svg viewBox="0 0 20 20" fill="none" class="w-4 h-4 text-outline shrink-0" aria-hidden="true">
          <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.6" />
          <path d="M13.5 13.5L17 17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
        </svg>
        <input
          v-model="queryText"
          @input="handleSearchInput"
          class="w-full bg-transparent border-none focus:ring-0 outline-none text-sm text-on-surface placeholder-outline py-2 px-1 min-w-0"
          placeholder="Type professor name (e.g. Dr. Tariq)..."
          type="text"
        />
        <button
          type="button"
          @click="loadData"
          class="neu-btn-primary px-6 py-2.5 text-xs font-semibold shrink-0 cursor-pointer"
        >
          Search
        </button>
      </div>
    </section>

    <!-- Department Filters + Controls -->
    <section class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
      <DepartmentFilter v-model="selectedDept" :departments="departments" class="flex-1 min-w-0" />

      <div class="flex items-center gap-3 shrink-0 self-end lg:self-auto">
        <select
          v-model="sortBy"
          aria-label="Sort professors"
          class="neu-inset rounded-full px-4 py-2 text-xs font-semibold text-on-surface focus:ring-0 focus:outline-none cursor-pointer"
        >
          <option value="rating">Highest Rated</option>
          <option value="reviews">Most Reviewed</option>
          <option value="name">Name (A-Z)</option>
        </select>

        <button
          type="button"
          @click="authStore.isVerified ? (showAddModal = true) : router.push({ path: '/auth', query: { redirect: '/search' } })"
          class="neu-btn-primary px-5 py-2.5 text-xs font-semibold whitespace-nowrap cursor-pointer"
        >
          + Add Teacher
        </button>
      </div>
    </section>

    <!-- Results Header -->
    <div class="flex items-center justify-between gap-3">
      <div class="flex items-center gap-2.5">
        <h2 class="text-base font-bold text-on-surface">
          Professors <span v-if="queryText" class="font-normal text-on-surface-variant">for "{{ queryText }}"</span>
        </h2>
        <span class="neu-circle-badge min-w-[26px] h-[26px] px-2 inline-flex items-center justify-center font-mono text-xs font-semibold text-on-surface-variant tabular-nums">
          {{ filteredResults.length }}
        </span>
      </div>
    </div>

    <!-- Loading Skeleton Grid -->
    <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="n in 6" :key="n" class="neu-card p-6 space-y-4">
        <div class="flex items-center justify-between gap-3">
          <div class="flex items-center gap-3 flex-1">
            <div class="neu-skeleton w-12 h-12 rounded-xl shrink-0"></div>
            <div class="space-y-2 flex-1">
              <div class="neu-skeleton h-4 w-3/4"></div>
              <div class="neu-skeleton h-3 w-1/2"></div>
            </div>
          </div>
          <div class="neu-skeleton w-12 h-8"></div>
        </div>
        <div class="neu-skeleton h-12 w-full"></div>
        <div class="neu-skeleton h-9 w-full rounded-full"></div>
      </div>
    </div>

    <!-- Professor Cards Grid -->
    <div v-else-if="filteredResults.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <article
        v-for="item in filteredResults"
        :key="item.id"
        class="neu-card p-6 flex flex-col gap-5"
      >
        <div class="flex items-start justify-between gap-3">
          <div class="flex items-start gap-3 min-w-0">
            <div class="neu-tile w-12 h-12 flex items-center justify-center font-mono text-sm font-bold text-primary shrink-0">
              {{ getInitials(item.title) }}
            </div>
            <div class="min-w-0">
              <h3 class="text-base font-bold text-on-surface leading-snug">
                <router-link :to="item.url" class="hover:text-primary transition-colors">
                  {{ item.title }}
                </router-link>
              </h3>
              <p class="text-xs text-on-surface-variant mt-0.5">{{ item.department }}</p>
              <span class="inline-block mt-2 neu-inset px-2.5 py-0.5 rounded-full text-[11px] text-on-surface-variant">
                {{ item.subtitle }}
              </span>
            </div>
          </div>

          <RatingBadge :score="item.rating" size="md" show-scale />
        </div>

        <div class="neu-inset-tray p-3.5 flex items-center justify-between gap-4 mt-auto">
          <div class="flex-1">
            <div class="flex justify-between font-mono text-[10px] uppercase text-outline mb-1.5">
              <span>Rating</span>
              <span class="text-on-surface font-semibold tabular-nums">{{ item.rating.toFixed(1) }}/5</span>
            </div>
            <div class="h-1.5 w-full bg-surface-variant/80 rounded-full overflow-hidden">
              <div class="h-full bg-primary rounded-full" :style="{ width: `${(item.rating / 5) * 100}%` }"></div>
            </div>
          </div>

          <div class="text-right pl-3 border-l border-surface-variant">
            <div class="font-mono text-[10px] uppercase text-outline">Reviews</div>
            <div class="font-mono text-base font-bold text-primary tabular-nums">{{ item.reviewCount }}</div>
          </div>
        </div>

        <router-link
          :to="item.url"
          class="neu-pill-btn w-full py-2.5 text-xs font-semibold text-center text-primary"
        >
          View {{ item.reviewCount }} Reviews
        </router-link>
      </article>
    </div>

    <!-- Empty State -->
    <div v-else class="py-4">
      <div class="neu-card px-6 py-10 max-w-md mx-auto text-center space-y-4">
        <div class="neu-tile w-12 h-12 mx-auto flex items-center justify-center text-primary">
          <svg viewBox="0 0 20 20" fill="none" class="w-5 h-5">
            <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.5" />
            <path d="M13.5 13.5L17 17" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
          </svg>
        </div>
        <div class="space-y-1">
          <h3 class="text-base font-bold text-on-surface">No professors found</h3>
          <p class="text-xs text-on-surface-variant">
            Cannot find your teacher? Add them directly to the Superior University catalogue.
          </p>
        </div>
        <div class="flex flex-wrap justify-center gap-3 pt-1">
          <button
            type="button"
            @click="authStore.isVerified ? (showAddModal = true) : router.push({ path: '/auth', query: { redirect: '/search' } })"
            class="neu-btn-primary px-6 py-2.5 text-xs font-semibold cursor-pointer"
          >
            + Add Teacher
          </button>
          <button
            v-if="queryText || selectedDept !== 'all'"
            type="button"
            @click="queryText = ''; selectedDept = 'all'; handleSearchInput()"
            class="neu-pill-btn px-5 py-2.5 text-xs font-semibold cursor-pointer"
          >
            Reset Filters
          </button>
        </div>
      </div>
    </div>

    <!-- Add New Teacher Modal -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 z-50 bg-on-surface/35 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
    >
      <div class="neu-card p-7 max-w-md w-full relative space-y-5">
        <button
          type="button"
          @click="showAddModal = false"
          class="neu-tile w-8 h-8 flex items-center justify-center absolute top-5 right-5 text-outline hover:text-primary cursor-pointer"
          aria-label="Close modal"
        >
          <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5">
            <path d="M4 4L12 12M12 4L4 12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
        </button>

        <div>
          <h3 class="text-lg font-bold text-primary">Add a New Teacher</h3>
          <p class="text-xs text-on-surface-variant mt-1">
            Add a missing professor to the Superior University catalogue.
          </p>
        </div>

        <div v-if="addErrorMsg" class="neu-inset rounded-xl p-3 text-xs font-semibold text-error">
          {{ addErrorMsg }}
        </div>
        <div v-if="addSuccessMsg" class="neu-inset rounded-xl p-3 text-xs font-semibold text-success">
          {{ addSuccessMsg }}
        </div>

        <form @submit.prevent="handleCreateProfessor" class="space-y-4">
          <div class="space-y-1.5">
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-outline">
              Teacher Full Name
            </label>
            <input
              v-model="newProfName"
              type="text"
              placeholder="e.g. Dr. Hammad Raza"
              class="w-full neu-inset rounded-xl px-4 py-2.5 text-sm text-on-surface placeholder-outline focus:ring-0 focus:outline-none"
              required
            />
          </div>

          <div class="space-y-1.5">
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-outline">
              Department
            </label>
            <select
              v-model="newProfDeptId"
              class="w-full neu-inset rounded-xl px-4 py-2.5 text-sm text-on-surface focus:ring-0 focus:outline-none"
            >
              <option v-for="d in departments" :key="d.id" :value="d.id">
                {{ d.name }} ({{ d.code }})
              </option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="block text-[11px] font-semibold uppercase tracking-wider text-outline">
              Title / Designation
            </label>
            <select
              v-model="newProfTitle"
              class="w-full neu-inset rounded-xl px-4 py-2.5 text-sm text-on-surface focus:ring-0 focus:outline-none"
            >
              <option value="Professor & HOD">Professor &amp; HOD</option>
              <option value="Professor">Professor</option>
              <option value="Associate Professor">Associate Professor</option>
              <option value="Assistant Professor">Assistant Professor</option>
              <option value="Senior Lecturer">Senior Lecturer</option>
              <option value="Lecturer">Lecturer</option>
            </select>
          </div>

          <div class="flex gap-3 pt-2">
            <button
              type="button"
              @click="showAddModal = false"
              class="neu-pill-btn px-5 py-2.5 text-xs font-semibold cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="flex-1 neu-btn-primary py-2.5 text-xs font-semibold cursor-pointer disabled:opacity-50"
              :disabled="isSubmittingProf"
            >
              {{ isSubmittingProf ? 'Saving...' : 'Add Teacher' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>
