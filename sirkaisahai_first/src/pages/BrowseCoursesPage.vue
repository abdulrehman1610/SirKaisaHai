<script setup lang="ts">
import { useRouter } from 'vue-router';

const router = useRouter();

function goHome() {
  router.push('/');
}

function goSearchProfessors() {
  router.push({ path: '/search', query: { tab: 'professors' } });
}
</script>

<template>
  <main class="max-w-container-max mx-auto px-gutter py-stack-lg flex items-center justify-center min-h-[75vh]">
    <div class="bg-white rounded-3xl p-8 md:p-14 custom-shadow shadow-2xl-ambient max-w-xl w-full text-center relative overflow-hidden">
      <!-- Ambient Glow Decor -->
      <div class="absolute -right-20 -top-20 w-64 h-64 bg-secondary-container/20 rounded-full blur-3xl pointer-events-none"></div>

      <!-- Icon -->
      <div class="w-20 h-20 bg-secondary-container/30 text-secondary-container text-primary rounded-full flex items-center justify-center mx-auto mb-6 shadow-sm">
        <span class="material-symbols-outlined text-4xl">construction</span>
      </div>

      <!-- Content -->
      <span class="inline-block bg-secondary-container/50 text-secondary-accent px-4 py-1.5 rounded-full font-label-sm text-xs font-bold uppercase tracking-wider mb-4">
        Module Under Construction
      </span>

      <h1 class="font-display-lg text-display-lg text-primary text-3xl md:text-4xl mb-4">
        Still Working On It!
      </h1>

      <p class="font-body-lg text-body-lg text-on-surface-variant mb-8 leading-relaxed">
        The dedicated <strong>Browse Courses</strong> module is currently under active development. You can still search for professors directly!
      </p>

      <!-- Buttons -->
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <button
          @click="goSearchProfessors"
          class="bg-primary text-white px-8 py-3 rounded-full font-label-sm text-sm font-bold hover:bg-[#6B2FA0] transition-colors shadow-lg shadow-primary/20 flex items-center justify-center gap-2"
        >
          <span class="material-symbols-outlined text-[18px]">person_search</span>
          Search Professor
        </button>

        <button
          @click="goHome"
          class="bg-surface-container-low text-on-surface border border-outline-variant/30 px-8 py-3 rounded-full font-label-sm text-sm font-bold hover:bg-surface-variant transition-colors"
        >
          Return to Home
        </button>
      </div>
    </div>
  </main>
</template>

<style scoped></style>
