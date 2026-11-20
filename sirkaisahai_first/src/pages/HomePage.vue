<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import type { Professor, Review } from '../types';
import { api } from '../api';
import MascotIllustration from '../components/ui/MascotIllustration.vue';
import ReviewCard from '../components/ui/ReviewCard.vue';
import RatingBadge from '../components/ui/RatingBadge.vue';

const router = useRouter();
const searchQuery = ref('');
const featuredProf = ref<Professor | null>(null);
const reviewsList = ref<Review[]>([]);
const isLoading = ref(true);

const slogans = [
  { top: 'Kon Sir', bottom: 'Kaisa Hai?' },
  { top: 'Asli Scene', bottom: 'Kya Hai?' },
  { top: 'GPA Bachao,', bottom: 'Real Feedback Paao.' },
  { top: 'Strict Attendance', bottom: 'Ya Chill Scenes?' },
  { top: 'Easy Grading Ya', bottom: 'Surprise Quizzes?' }
];
const currentSloganIndex = ref(0);
let sloganInterval: ReturnType<typeof setInterval> | null = null;

onMounted(async () => {
  sloganInterval = setInterval(() => {
    currentSloganIndex.value = (currentSloganIndex.value + 1) % slogans.length;
  }, 3000);

  try {
    const [profs, realReviews] = await Promise.all([api.search(''), api.getRecentReviews()]);
    reviewsList.value = realReviews;

    if (profs.length > 0) {
      const sorted = [...profs].sort((a, b) => b.rating - a.rating);
      const topProfId = sorted[0]?.id;
      if (topProfId) {
        const topProf = await api.getProfessorById(topProfId);
        if (topProf) featuredProf.value = topProf;
      }
    }
  } finally {
    isLoading.value = false;
  }
});

onUnmounted(() => {
  if (sloganInterval) clearInterval(sloganInterval);
});

function handleSearch() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/search', query: { q: searchQuery.value.trim() } });
  } else {
    router.push('/search');
  }
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
</script>

<template>
  <div class="w-full">
    <!-- BAND 1: Hero Band (#E7DBE3) -->
    <section class="bg-band-hero px-4 md:px-gutter pt-6 pb-10 md:pb-12">
      <div class="max-w-container-max mx-auto space-y-8">
        <!-- Top Eyebrow Row -->
        <div class="flex items-center justify-between gap-4">
          <p class="ed-eyebrow">
            The student perspective <span class="mx-1.5 opacity-45">/</span> Superior University
          </p>
          <p class="ed-eyebrow hidden sm:block">Est. for students</p>
        </div>

        <!-- 2-Column Editorial Hero -->
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
          <div class="lg:col-span-7 space-y-5">
            <div class="min-h-[116px] sm:min-h-[148px] md:min-h-[164px] flex items-center overflow-hidden">
              <transition name="slogan-fade" mode="out-in">
                <h1
                  :key="currentSloganIndex"
                  class="font-display text-5xl sm:text-6xl md:text-[68px] font-extrabold leading-[0.98] tracking-[-0.03em]"
                >
                  <span class="block text-ink-dark">{{ slogans[currentSloganIndex]?.top }}</span>
                  <span class="block text-primary">{{ slogans[currentSloganIndex]?.bottom }}</span>
                </h1>
              </transition>
            </div>

            <p class="text-sm sm:text-base text-ink-muted leading-relaxed max-w-md">
              Real, unfiltered &amp; anonymous teacher reviews.<br />
              Know your professors before registering.
            </p>
          </div>

          <div class="lg:col-span-5 flex justify-center lg:justify-end">
            <MascotIllustration />
          </div>
        </div>

        <!-- Wide Command Search Bar -->
        <div class="ed-search-bar p-3 sm:px-5 sm:py-4 grid grid-cols-1 md:grid-cols-12 gap-4 items-center">
          <form @submit.prevent="handleSearch" class="md:col-span-9 flex flex-col sm:flex-row sm:items-center gap-3">
            <div class="flex flex-col gap-1 flex-1 min-w-0">
              <span class="font-mono text-[9.5px] font-semibold uppercase tracking-[0.14em] text-ink-subtle pl-1">
                Good semesters start here
              </span>
              <div class="flex items-center gap-2.5 pl-1">
                <svg viewBox="0 0 20 20" fill="none" class="w-4 h-4 text-ink-subtle shrink-0" aria-hidden="true">
                  <circle cx="9" cy="9" r="6" stroke="currentColor" stroke-width="1.6" />
                  <path d="M13.5 13.5L17 17" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" />
                </svg>
                <input
                  v-model="searchQuery"
                  type="text"
                  placeholder="Search a professor or course"
                  class="w-full bg-transparent border-none focus:ring-0 outline-none text-sm sm:text-base text-ink-dark placeholder-ink-subtle py-1 p-0"
                />
              </div>
            </div>

            <button
              type="submit"
              class="ed-btn-primary px-6 py-3 text-xs font-semibold inline-flex items-center justify-center gap-3 shrink-0 self-stretch sm:self-center cursor-pointer"
            >
              <span>Find my professor</span>
              <span aria-hidden="true">→</span>
            </button>
          </form>

          <div class="md:col-span-3 md:border-l md:border-border-soft md:pl-5 flex flex-row md:flex-col justify-between gap-2 text-xs font-semibold text-ink-dark">
            <router-link
              to="/search"
              class="flex items-center justify-between gap-3 py-1 hover:text-primary transition-colors"
            >
              <span>Browse professors</span>
              <span class="text-[11px] text-ink-subtle" aria-hidden="true">↗</span>
            </router-link>
            <router-link
              to="/review/new"
              class="flex items-center justify-between gap-3 py-1 hover:text-primary transition-colors"
            >
              <span>Write a review</span>
              <span class="text-[11px] text-ink-subtle" aria-hidden="true">↗</span>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- BAND 2: Trust Strip (#DCC8D5) -->
    <div class="bg-band-strip px-4 md:px-gutter py-3">
      <div class="max-w-container-max mx-auto grid grid-cols-2 sm:grid-cols-4 gap-3 text-center font-mono text-[10px] font-semibold uppercase tracking-[0.16em] text-primary-dark/80">
        <span>100% Anonymous</span>
        <span>No Sugarcoating</span>
        <span>Student-Driven</span>
        <span>Zero Tracking</span>
      </div>
    </div>

    <!-- BAND 3: Recent Teacher Reviews (#F8F5F7) -->
    <section class="bg-band-light px-4 md:px-gutter py-14 md:py-16">
      <div class="max-w-container-max mx-auto space-y-10">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          <!-- Left Editorial Column -->
          <div class="lg:col-span-4 space-y-4">
            <p class="ed-eyebrow">01 / The latest on campus</p>
            <h2 class="font-display text-3xl md:text-4xl font-extrabold text-ink-dark leading-[1.06]">
              Recent teacher reviews
            </h2>
            <p class="text-sm text-ink-muted leading-relaxed">
              Honest experiences.<br />
              A little less guesswork.
            </p>
            <div class="pt-2">
              <router-link
                to="/search"
                class="inline-flex items-center gap-6 text-xs font-semibold text-ink-dark hover:text-primary transition-colors"
              >
                <span>View catalogue</span>
                <span aria-hidden="true">→</span>
              </router-link>
            </div>

            <!-- Featured Top Rated Faculty Compact Card (when professors exist) -->
            <div v-if="!isLoading && featuredProf" class="pt-4">
              <div class="ed-card p-5 space-y-3.5">
                <div class="flex items-center justify-between gap-2">
                  <span class="ed-eyebrow text-primary">Top rated</span>
                  <RatingBadge :score="featuredProf.overallRating" size="sm" show-scale />
                </div>
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-primary-soft text-primary flex items-center justify-center font-mono text-xs font-bold shrink-0">
                    {{ getInitials(featuredProf.name) }}
                  </div>
                  <div class="min-w-0">
                    <router-link
                      :to="`/professor/${featuredProf.id}`"
                      class="font-bold text-sm text-ink-dark hover:text-primary block truncate"
                    >
                      {{ featuredProf.name }}
                    </router-link>
                    <p class="text-xs text-ink-subtle truncate">{{ featuredProf.departmentName }}</p>
                  </div>
                </div>
                <div class="grid grid-cols-3 gap-2 pt-1 text-center font-mono text-[11px] bg-surface-recessed rounded-xl p-2.5">
                  <div>
                    <span class="block text-[9px] uppercase text-ink-subtle">Teach</span>
                    <strong class="text-ink-dark tabular-nums">{{ featuredProf.avgTeaching.toFixed(1) }}</strong>
                  </div>
                  <div>
                    <span class="block text-[9px] uppercase text-ink-subtle">Grade</span>
                    <strong class="text-ink-dark tabular-nums">{{ featuredProf.avgGrading.toFixed(1) }}</strong>
                  </div>
                  <div>
                    <span class="block text-[9px] uppercase text-ink-subtle">Load</span>
                    <strong class="text-warning tabular-nums">{{ featuredProf.avgWorkload.toFixed(1) }}</strong>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Content Column -->
          <div class="lg:col-span-8">
            <!-- Loading Skeletons -->
            <div v-if="isLoading" class="space-y-4">
              <div class="ed-card p-8 space-y-4">
                <div class="ed-skeleton h-4 w-40"></div>
                <div class="ed-skeleton h-7 w-2/3"></div>
                <div class="ed-skeleton h-4 w-full"></div>
                <div class="ed-skeleton h-10 w-64 rounded-full"></div>
              </div>
            </div>

            <!-- Live Reviews Feed -->
            <div v-else-if="reviewsList.length > 0" class="space-y-5">
              <ReviewCard v-for="rev in reviewsList" :key="rev.id" :review="rev" :show-professor="true" />
            </div>

            <!-- Empty State Card (Exact Match to Mockup) -->
            <div v-else class="ed-card p-7 sm:p-10 space-y-6">
              <div class="flex items-start justify-between gap-4">
                <span class="ed-eyebrow">The conversation is open</span>
                <div class="text-right">
                  <span class="ed-eyebrow block">0 reviews</span>
                  <span class="font-serif text-5xl leading-none text-primary block mt-1 select-none" aria-hidden="true">“</span>
                </div>
              </div>

              <div class="space-y-3 -mt-3">
                <h3 class="font-display text-2xl sm:text-3xl font-extrabold text-ink-dark leading-tight">
                  Every review starts<br />with one student.
                </h3>
                <p class="text-sm text-ink-muted max-w-md leading-relaxed">
                  No reviews published yet. Be the first to share your experience and help someone choose their next class with confidence.
                </p>
              </div>

              <div class="flex flex-wrap items-center justify-between gap-4 pt-2">
                <div class="flex flex-wrap items-center gap-3">
                  <router-link
                    to="/review/new"
                    class="ed-btn-primary px-6 py-2.5 text-xs font-semibold inline-flex items-center gap-4"
                  >
                    <span>Write a review</span>
                    <span aria-hidden="true">→</span>
                  </router-link>
                  <router-link
                    to="/search"
                    class="ed-btn-soft px-6 py-2.5 text-xs font-semibold inline-flex items-center gap-4"
                  >
                    <span>Add a teacher</span>
                    <span aria-hidden="true">→</span>
                  </router-link>
                </div>

                <span class="inline-flex items-center gap-1.5 text-[11px] text-ink-subtle">
                  <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5" aria-hidden="true">
                    <rect x="3.5" y="7" width="9" height="6.5" rx="1.5" stroke="currentColor" stroke-width="1.3" />
                    <path d="M5.5 7V5.2C5.5 3.8 6.6 2.8 8 2.8C9.4 2.8 10.5 3.8 10.5 5.2V7" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" />
                  </svg>
                  <span>Your name never appears</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- BAND 4: Before You Register (#E2DCE8) -->
    <section class="bg-band-lilac px-4 md:px-gutter pt-12 pb-10">
      <div class="max-w-container-max mx-auto space-y-7">
        <div class="space-y-1.5">
          <p class="ed-eyebrow">02 / Before you register</p>
          <h2 class="font-display text-2xl sm:text-3xl font-extrabold text-ink-dark">
            A little research goes a long way.
          </h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <div class="ed-step-card p-6 flex items-start gap-4">
            <span class="w-11 h-11 rounded-xl bg-band-light/70 border border-white/80 flex items-center justify-center font-serif italic text-xl text-primary shrink-0">
              01
            </span>
            <div class="space-y-1.5">
              <h3 class="text-sm font-bold text-ink-dark">Find your professor</h3>
              <p class="text-xs text-ink-muted leading-relaxed">
                Search by name or browse courses to see who's teaching your next class.
              </p>
            </div>
          </div>

          <div class="ed-step-card p-6 flex items-start gap-4">
            <span class="w-11 h-11 rounded-xl bg-band-light/70 border border-white/80 flex items-center justify-center font-serif italic text-xl text-primary shrink-0">
              02
            </span>
            <div class="space-y-1.5">
              <h3 class="text-sm font-bold text-ink-dark">Get the student perspective</h3>
              <p class="text-xs text-ink-muted leading-relaxed">
                Read real experiences to understand the teaching style, workload and expectations.
              </p>
            </div>
          </div>

          <div class="ed-step-card p-6 flex items-start gap-4">
            <span class="w-11 h-11 rounded-xl bg-band-light/70 border border-white/80 flex items-center justify-center font-serif italic text-xl text-primary shrink-0">
              03
            </span>
            <div class="space-y-1.5">
              <h3 class="text-sm font-bold text-ink-dark">Pay it forward</h3>
              <p class="text-xs text-ink-muted leading-relaxed">
                Verify your student email and share an anonymous review of your own.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.slogan-fade-enter-active,
.slogan-fade-leave-active {
  transition: all 0.4s ease;
}

.slogan-fade-enter-from {
  opacity: 0;
  transform: translateY(18px);
}

.slogan-fade-leave-to {
  opacity: 0;
  transform: translateY(-18px);
}
</style>
