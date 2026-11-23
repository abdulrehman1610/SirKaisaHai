<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Department, SearchResultItem } from '../types';
import { api, ApiError } from '../api';
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

let searchDebounceTimer: ReturnType<typeof setTimeout> | null = null;

async function loadResults(showFullSkeleton = false) {
  if (showFullSkeleton || results.value.length === 0) {
    isLoading.value = true;
  }
  try {
    results.value = await api.search(queryText.value, selectedDept.value);
  } finally {
    isLoading.value = false;
  }
}

async function loadData() {
  await loadResults(results.value.length === 0);
}

onMounted(async () => {
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
});

watch([() => route.query.q, () => route.query.dept], ([newQ, newDept]) => {
  const nextQ = (newQ as string) || '';
  const nextDept = typeof newDept === 'string' && newDept ? newDept : 'all';
  if (nextQ === queryText.value && nextDept === selectedDept.value) return;
  queryText.value = nextQ;
  selectedDept.value = nextDept;
  loadResults(false);
});

watch(selectedDept, (dept) => {
  const targetDept = dept === 'all' ? undefined : dept;
  if ((route.query.dept || undefined) !== targetDept) {
    router.replace({ query: { ...route.query, dept: targetDept } });
  }
  loadResults(false);
});

function handleSearchInput() {
  if (searchDebounceTimer) clearTimeout(searchDebounceTimer);
  searchDebounceTimer = setTimeout(() => {
    router.replace({ query: { ...route.query, q: queryText.value || undefined } });
    loadResults(false);
  }, 250);
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
      tags: ['New Faculty', 'Student Verified']
    });

    addSuccessMsg.value = `Added ${newProf.name} to the catalogue.`;
    newProfName.value = '';
    setTimeout(() => {
      showAddModal.value = false;
      addSuccessMsg.value = '';
      loadData();
    }, 1000);
  } catch (err: unknown) {
    if (err instanceof ApiError && err.status === 401) {
      authStore.clearLocalSession();
      showAddModal.value = false;
      router.push({ path: '/auth', query: { redirect: route.fullPath } });
      return;
    }
    addErrorMsg.value = err instanceof Error ? err.message : 'Failed to add teacher.';
  } finally {
    isSubmittingProf.value = false;
  }
}
</script>

<template>
  <main class="w-full">
    <!-- Top Blush Header Band -->
    <section class="bg-band-hero px-4 md:px-gutter pt-24 pb-10">
      <div class="max-w-container-max mx-auto space-y-6">
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div class="space-y-1.5">
            <p class="ed-eyebrow">Superior University · Faculty Catalogue</p>
            <h1 class="font-display text-3xl sm:text-4xl md:text-5xl font-extrabold text-ink-dark">
              Find your <span class="text-primary">professor.</span>
            </h1>
          </div>

          <button
            type="button"
            @click="authStore.isVerified ? (showAddModal = true) : router.push({ path: '/auth', query: { redirect: '/search' } })"
            class="ed-btn-primary px-6 py-2.5 text-xs font-semibold inline-flex items-center gap-3 self-start md:self-auto cursor-pointer"
          >
            <span>+ Add a teacher</span>
            <span aria-hidden="true">→</span>
          </button>
        </div>

        <div class="ed-search-bar p-2 pl-4 flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
          <div class="flex items-center gap-2.5 flex-1 min-w-0">
            <svg viewBox="0 0 20 20" fill="none" class="w-4 h-4 text-ink-subtle shrink-0" aria-hidden="true">
              <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.6" />
              <path d="M13.5 13.5L17 17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
            </svg>
            <input
              v-model="queryText"
              @input="handleSearchInput"
              class="w-full bg-transparent border-none focus:ring-0 outline-none text-sm sm:text-base text-ink-dark placeholder-ink-subtle py-2 p-0"
              placeholder="Search by name or title (e.g. Dr. Tariq)..."
              type="text"
            />
          </div>
          <button
            type="button"
            @click="loadData"
            class="ed-btn-primary px-6 py-2.5 text-xs font-semibold shrink-0 cursor-pointer inline-flex items-center justify-center gap-2"
          >
            <span>Search</span>
            <span aria-hidden="true">→</span>
          </button>
        </div>
      </div>
    </section>

    <!-- Main Directory Band -->
    <section class="bg-band-light px-4 md:px-gutter py-10 min-h-[55vh]">
      <div class="max-w-container-max mx-auto space-y-7">
        <!-- Filters + Sort -->
        <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-border-soft">
          <DepartmentFilter v-model="selectedDept" :departments="departments" class="flex-1 min-w-0" />

          <div class="flex items-center gap-2.5 shrink-0 self-end lg:self-auto">
            <label for="dir-sort" class="ed-eyebrow">Sort</label>
            <select
              id="dir-sort"
              v-model="sortBy"
              class="ed-input rounded-full px-4 py-1.5 text-xs font-semibold text-ink-dark cursor-pointer"
            >
              <option value="rating">Highest rated</option>
              <option value="reviews">Most reviewed</option>
              <option value="name">Name (A-Z)</option>
            </select>
          </div>
        </div>

        <!-- Count Row -->
        <div class="flex items-baseline justify-between gap-2">
          <h2 class="text-lg font-bold text-ink-dark">
            Showing faculty <span v-if="queryText" class="font-normal text-ink-muted">matching "{{ queryText }}"</span>
          </h2>
          <span class="ed-eyebrow tabular-nums">{{ filteredResults.length }} found</span>
        </div>

        <!-- Skeletons -->
        <div v-if="isLoading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="n in 6" :key="n" class="ed-card p-6 space-y-4">
            <div class="flex justify-between items-start gap-3">
              <div class="flex items-center gap-3 flex-1">
                <div class="ed-skeleton w-11 h-11 rounded-xl shrink-0"></div>
                <div class="space-y-2 flex-1">
                  <div class="ed-skeleton h-4 w-3/4"></div>
                  <div class="ed-skeleton h-3 w-1/2"></div>
                </div>
              </div>
              <div class="ed-skeleton w-12 h-7"></div>
            </div>
            <div class="ed-skeleton h-12 w-full"></div>
            <div class="ed-skeleton h-9 w-full rounded-full"></div>
          </div>
        </div>

        <!-- Results Grid -->
        <div v-else-if="filteredResults.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          <article v-for="item in filteredResults" :key="item.id" class="ed-card p-6 flex flex-col gap-5">
            <div class="flex items-start justify-between gap-3">
              <div class="flex items-start gap-3 min-w-0">
                <div class="w-11 h-11 rounded-xl bg-primary-soft text-primary flex items-center justify-center font-mono text-sm font-bold shrink-0">
                  {{ getInitials(item.title) }}
                </div>
                <div class="min-w-0">
                  <h3 class="text-base font-bold text-ink-dark leading-snug">
                    <router-link :to="item.url" class="hover:text-primary transition-colors">
                      {{ item.title }}
                    </router-link>
                  </h3>
                  <p class="text-xs text-ink-muted mt-0.5">{{ item.department }}</p>
                  <span class="inline-block mt-2 bg-surface-recessed px-2.5 py-0.5 rounded-full text-[11px] text-ink-muted">
                    {{ item.subtitle }}
                  </span>
                </div>
              </div>

              <RatingBadge :score="item.rating" size="md" show-scale />
            </div>

            <div class="bg-surface-recessed rounded-xl p-3.5 flex items-center justify-between gap-4 mt-auto">
              <div class="flex-1">
                <div class="flex justify-between font-mono text-[10px] uppercase text-ink-subtle mb-1.5">
                  <span>Rating</span>
                  <span class="text-ink-dark font-semibold tabular-nums">{{ item.rating.toFixed(1) }}/5</span>
                </div>
                <div class="h-1.5 w-full bg-border-soft rounded-full overflow-hidden">
                  <div class="h-full bg-primary rounded-full" :style="{ width: `${(item.rating / 5) * 100}%` }"></div>
                </div>
              </div>

              <div class="text-right pl-3 border-l border-border-soft">
                <div class="font-mono text-[10px] uppercase text-ink-subtle">Reviews</div>
                <div class="font-mono text-base font-bold text-primary tabular-nums">{{ item.reviewCount }}</div>
              </div>
            </div>

            <router-link
              :to="item.url"
              class="ed-btn-soft w-full py-2.5 text-xs font-semibold text-center text-primary inline-flex items-center justify-center gap-2"
            >
              <span>View dossier</span>
              <span aria-hidden="true">→</span>
            </router-link>
          </article>
        </div>

        <!-- Empty State -->
        <div v-else class="ed-card p-10 text-center max-w-lg mx-auto space-y-4">
          <span class="font-serif text-4xl text-primary block leading-none" aria-hidden="true">“</span>
          <h3 class="text-xl font-extrabold text-ink-dark">No professors found</h3>
          <p class="text-sm text-ink-muted">
            Cannot find your teacher? Add them to the Superior University catalogue so students can start reviewing.
          </p>
          <div class="flex flex-wrap justify-center gap-3 pt-1">
            <button
              type="button"
              @click="authStore.isVerified ? (showAddModal = true) : router.push({ path: '/auth', query: { redirect: '/search' } })"
              class="ed-btn-primary px-6 py-2.5 text-xs font-semibold cursor-pointer inline-flex items-center gap-2"
            >
              <span>Add a teacher</span>
              <span aria-hidden="true">→</span>
            </button>
            <button
              v-if="queryText || selectedDept !== 'all'"
              type="button"
              @click="queryText = ''; selectedDept = 'all'; handleSearchInput()"
              class="ed-btn-soft px-5 py-2.5 text-xs font-semibold cursor-pointer"
            >
              Reset filters
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Add New Teacher Modal -->
    <div
      v-if="showAddModal"
      class="fixed inset-0 z-50 bg-ink-dark/40 flex items-center justify-center p-4"
      role="dialog"
      aria-modal="true"
    >
      <div class="ed-card p-7 max-w-md w-full relative space-y-5">
        <button
          type="button"
          @click="showAddModal = false"
          class="ed-btn-soft w-8 h-8 flex items-center justify-center absolute top-5 right-5 text-ink-subtle hover:text-primary cursor-pointer"
          aria-label="Close modal"
        >
          <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5">
            <path d="M4 4L12 12M12 4L4 12" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
          </svg>
        </button>

        <div>
          <p class="ed-eyebrow mb-1">Campus Catalogue</p>
          <h3 class="text-xl font-extrabold text-ink-dark">Add a new teacher</h3>
          <p class="text-xs text-ink-muted mt-1">
            Duplicate names across departments are checked automatically.
          </p>
        </div>

        <div v-if="addErrorMsg" class="p-3 bg-error-soft text-error rounded-xl text-xs font-semibold">
          {{ addErrorMsg }}
        </div>
        <div v-if="addSuccessMsg" class="p-3 bg-success-soft text-success rounded-xl text-xs font-semibold">
          {{ addSuccessMsg }}
        </div>

        <form @submit.prevent="handleCreateProfessor" class="space-y-4">
          <div class="space-y-1.5">
            <label class="block ed-eyebrow">Teacher full name</label>
            <input
              v-model="newProfName"
              type="text"
              placeholder="e.g. Dr. Hammad Raza"
              class="w-full ed-input px-3.5 py-2.5 text-sm"
              required
            />
          </div>

          <div class="space-y-1.5">
            <label class="block ed-eyebrow">Department</label>
            <select v-model="newProfDeptId" class="w-full ed-input px-3.5 py-2.5 text-sm">
              <option v-for="d in departments" :key="d.id" :value="d.id">
                {{ d.name }} ({{ d.code }})
              </option>
            </select>
          </div>

          <div class="space-y-1.5">
            <label class="block ed-eyebrow">Title / designation</label>
            <select v-model="newProfTitle" class="w-full ed-input px-3.5 py-2.5 text-sm">
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
              class="ed-btn-soft px-5 py-2.5 text-xs font-semibold cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="flex-1 ed-btn-primary py-2.5 text-xs font-semibold cursor-pointer disabled:opacity-50"
              :disabled="isSubmittingProf"
            >
              {{ isSubmittingProf ? 'Saving...' : 'Add teacher' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>
