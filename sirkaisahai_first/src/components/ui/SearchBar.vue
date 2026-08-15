<script setup lang="ts">
import { ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import type { SearchResultItem } from '../../types';
import { api } from '../../api';

const props = withDefaults(
  defineProps<{
    placeholder?: string;
    size?: 'md' | 'lg';
  }>(),
  {
    placeholder: 'Search by professor name (e.g. Dr. Tariq) or course code (e.g. CS-201)...',
    size: 'md'
  }
);

const router = useRouter();
const query = ref('');
const suggestions = ref<SearchResultItem[]>([]);
const isOpen = ref(false);
const isLoading = ref(false);

let debounceTimeout: any = null;

watch(query, (newVal) => {
  if (debounceTimeout) clearTimeout(debounceTimeout);
  if (!newVal.trim()) {
    suggestions.value = [];
    isOpen.value = false;
    return;
  }

  isLoading.value = true;
  debounceTimeout = setTimeout(async () => {
    try {
      const results = await api.search(newVal);
      suggestions.value = results.slice(0, 6); // top 6 suggestions
      isOpen.value = suggestions.value.length > 0;
    } finally {
      isLoading.value = false;
    }
  }, 200);
});

function handleSearchSubmit() {
  isOpen.value = false;
  if (query.value.trim()) {
    router.push({ path: '/search', query: { q: query.value.trim() } });
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
  }, 200);
}
</script>

<template>
  <div class="search-bar-wrapper" :class="[size]">
    <form @submit.prevent="handleSearchSubmit" class="search-form">
      <div class="input-container">
        <svg viewBox="0 0 24 24" fill="none" class="search-icon">
          <path
            d="M21 21L15 15M17 10C17 13.866 13.866 17 10 17C6.13401 17 3 13.866 3 10C3 6.13401 6.13401 3 10 3C13.866 3 17 6.13401 17 10Z"
            stroke="var(--text-muted)"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />
        </svg>

        <input
          v-model="query"
          type="text"
          class="search-input"
          :placeholder="placeholder"
          @focus="isOpen = suggestions.length > 0"
          @blur="closeDropdown"
          aria-label="Search professors or courses"
        />

        <button v-if="query" type="button" class="clear-btn" @click="query = ''">✕</button>

        <button type="submit" class="submit-btn">
          Search
        </button>
      </div>
    </form>

    <!-- Suggestions Dropdown -->
    <transition name="fade">
      <div v-if="isOpen" class="suggestions-dropdown glass-card">
        <div
          v-for="item in suggestions"
          :key="item.id"
          class="suggestion-item"
          @click="selectSuggestion(item)"
        >
          <div class="item-badge" :class="item.type">
            {{ item.type === 'professor' ? '👨‍🏫 PROF' : '📚 COURSE' }}
          </div>
          <div class="item-info">
            <span class="item-title">{{ item.title }}</span>
            <span class="item-dept">{{ item.department }} • {{ item.subtitle }}</span>
          </div>
          <div class="item-rating">
            ★ {{ item.rating.toFixed(1) }}
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.search-bar-wrapper {
  position: relative;
  width: 100%;
}

.search-form {
  width: 100%;
}

.input-container {
  display: flex;
  align-items: center;
  background: var(--bg-surface);
  border: 2px solid var(--border-medium);
  border-radius: var(--radius-xl);
  padding: 0.35rem 0.5rem 0.35rem 1rem;
  box-shadow: var(--shadow-md);
  transition: all var(--transition-normal);
}

.input-container:focus-within {
  border-color: var(--accent-gold);
  box-shadow: 0 0 0 4px rgba(217, 119, 6, 0.15), var(--shadow-lg);
}

.search-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  margin-right: 0.5rem;
}

.search-input {
  width: 100%;
  border: none;
  outline: none;
  background: transparent;
  color: var(--text-main);
  font-size: 0.95rem;
  font-weight: 500;
}

.lg .search-input {
  font-size: 1.1rem;
  padding: 0.4rem 0;
}

.clear-btn {
  color: var(--text-subtle);
  font-size: 1rem;
  padding: 0 0.5rem;
}

.submit-btn {
  background: linear-gradient(135deg, var(--primary-navy) 0%, var(--primary-navy-light) 100%);
  color: var(--text-on-dark);
  font-weight: 600;
  font-family: var(--font-heading);
  padding: 0.6rem 1.25rem;
  border-radius: var(--radius-lg);
  transition: transform var(--transition-fast), background var(--transition-fast);
  flex-shrink: 0;
  margin-left: 0.5rem;
}

.submit-btn:hover {
  background: var(--accent-gold);
  color: #FFFFFF;
}

.lg .submit-btn {
  padding: 0.75rem 1.75rem;
  font-size: 1.05rem;
}

/* Dropdown */
.suggestions-dropdown {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  right: 0;
  background: var(--bg-surface);
  border: 1px solid var(--border-medium);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  z-index: 100;
  overflow: hidden;
  max-height: 380px;
  overflow-y: auto;
}

.suggestion-item {
  display: flex;
  align-items: center;
  gap: 0.85rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid var(--border-light);
  cursor: pointer;
  transition: background var(--transition-fast);
}

.suggestion-item:last-child {
  border-bottom: none;
}

.suggestion-item:hover {
  background: var(--bg-surface-elevated);
}

.item-badge {
  font-size: 0.7rem;
  font-weight: 700;
  padding: 0.2rem 0.5rem;
  border-radius: var(--radius-sm);
  letter-spacing: 0.05em;
  flex-shrink: 0;
}

.item-badge.professor {
  background: #EFF6FF;
  color: #1D4ED8;
}

.item-badge.course {
  background: #FEF3C7;
  color: #B45309;
}

.item-info {
  display: flex;
  flex-direction: column;
  flex: 1;
}

.item-title {
  font-weight: 600;
  font-size: 0.95rem;
  color: var(--primary-navy);
}

.item-dept {
  font-size: 0.8rem;
  color: var(--text-muted);
}

.item-rating {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--accent-gold);
}

/* Vue Transitions */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
