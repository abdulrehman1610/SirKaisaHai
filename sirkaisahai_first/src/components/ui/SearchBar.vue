<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import type { SearchResultItem } from '../../types';
import { api } from '../../api';

withDefaults(
  defineProps<{
    placeholder?: string;
  }>(),
  {
    placeholder: 'Search a professor or course'
  }
);

const router = useRouter();
const query = ref('');
const suggestions = ref<SearchResultItem[]>([]);
const isOpen = ref(false);

let debounceTimeout: ReturnType<typeof setTimeout> | null = null;

watch(query, (newVal) => {
  if (debounceTimeout) clearTimeout(debounceTimeout);
  if (!newVal.trim()) {
    suggestions.value = [];
    isOpen.value = false;
    return;
  }

  debounceTimeout = setTimeout(async () => {
    const results = await api.search(newVal);
    suggestions.value = results.slice(0, 6);
    isOpen.value = suggestions.value.length > 0;
  }, 200);
});

function handleSearchSubmit() {
  isOpen.value = false;
  if (query.value.trim()) {
    router.push({ path: '/search', query: { q: query.value.trim() } });
  } else {
    router.push('/search');
  }
}

function selectSuggestion(item: SearchResultItem) {
  isOpen.value = false;
  query.value = '';
  router.push(item.url);
}

function closeDropdown() {
  setTimeout(() => {
    isOpen.value = false;
  }, 180);
}
</script>

<template>
  <div class="relative w-full">
    <form @submit.prevent="handleSearchSubmit" class="w-full">
      <div class="ed-search-bar flex items-center gap-2 p-2 pl-4">
        <svg viewBox="0 0 20 20" fill="none" class="w-4 h-4 text-ink-subtle shrink-0" aria-hidden="true">
          <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.6" />
          <path d="M13.5 13.5L17 17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
        </svg>
        <input
          v-model="query"
          type="text"
          class="flex-1 bg-transparent border-none focus:ring-0 outline-none text-sm text-ink-dark placeholder-ink-subtle min-w-0 py-1.5"
          :placeholder="placeholder"
          @focus="isOpen = suggestions.length > 0"
          @blur="closeDropdown"
          aria-label="Search professors or courses"
        />
        <button type="submit" class="ed-btn-primary px-5 py-2.5 text-xs font-semibold shrink-0 cursor-pointer inline-flex items-center gap-2">
          <span>Search</span>
          <span aria-hidden="true">→</span>
        </button>
      </div>
    </form>

    <div v-if="isOpen" class="ed-card absolute top-[calc(100%+8px)] left-0 right-0 z-50 overflow-hidden p-1.5">
      <button
        v-for="item in suggestions"
        :key="item.id"
        type="button"
        class="w-full text-left flex items-center gap-3 px-3.5 py-2.5 rounded-xl hover:bg-surface-recessed transition-colors cursor-pointer"
        @click="selectSuggestion(item)"
      >
        <span class="font-mono text-[10px] uppercase font-semibold text-primary bg-primary-soft px-2 py-0.5 rounded-full shrink-0">
          {{ item.type === 'professor' ? 'Faculty' : 'Course' }}
        </span>
        <span class="flex-1 min-w-0">
          <span class="block text-sm font-semibold text-ink-dark truncate">{{ item.title }}</span>
          <span class="block text-xs text-ink-subtle truncate">{{ item.department }} · {{ item.subtitle }}</span>
        </span>
        <span class="font-mono text-xs font-bold text-primary tabular-nums">{{ item.rating.toFixed(1) }}/5</span>
      </button>
    </div>
  </div>
</template>
