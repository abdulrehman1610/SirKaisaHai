<script setup lang="ts">
import { mockCourses } from '../api/mockData';
import RatingBadge from '../components/ui/RatingBadge.vue';
</script>

<template>
  <main class="w-full">
    <section class="bg-band-hero px-4 md:px-gutter pt-6 pb-10">
      <div class="max-w-container-max mx-auto flex flex-col md:flex-row md:items-end justify-between gap-5">
        <div class="space-y-1.5">
          <p class="ed-eyebrow">Course Reference Catalogue</p>
          <h1 class="font-display text-3xl sm:text-4xl md:text-5xl font-extrabold text-ink-dark">
            Browse <span class="text-primary">courses.</span>
          </h1>
          <p class="text-sm text-ink-muted max-w-xl leading-relaxed">
            Explore core Computing &amp; IT courses below. Live student reviews are currently indexed directly by professor in the faculty directory.
          </p>
        </div>

        <router-link
          to="/search"
          class="ed-btn-primary px-6 py-2.5 text-xs font-semibold inline-flex items-center gap-3 self-start md:self-auto shrink-0"
        >
          <span>Browse professors</span>
          <span aria-hidden="true">→</span>
        </router-link>
      </div>
    </section>

    <section class="bg-band-light px-4 md:px-gutter py-10 min-h-[50vh]">
      <div class="max-w-container-max mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        <article
          v-for="course in mockCourses"
          :key="course.id"
          class="ed-card p-6 flex flex-col justify-between gap-5"
        >
          <div class="space-y-3">
            <div class="flex items-start justify-between gap-3">
              <div class="space-y-1">
                <div class="font-mono text-xs font-bold text-primary">
                  {{ course.code }} <span class="text-ink-subtle font-normal">· {{ course.creditHours }} Credit Hours</span>
                </div>
                <h2 class="text-xl font-extrabold text-ink-dark">
                  <router-link :to="`/course/${course.id}`" class="hover:text-primary transition-colors">
                    {{ course.title }}
                  </router-link>
                </h2>
                <p class="text-xs text-ink-subtle">{{ course.departmentName }}</p>
              </div>

              <RatingBadge :score="course.avgRating" size="md" show-scale />
            </div>

            <p class="text-sm text-ink-muted leading-relaxed">
              {{ course.description }}
            </p>
          </div>

          <div class="flex items-center justify-between gap-3 pt-2 border-t border-border-soft/60">
            <span class="font-mono text-xs text-ink-subtle tabular-nums">
              {{ course.totalReviews }} reference notes
            </span>
            <router-link
              :to="`/course/${course.id}`"
              class="text-xs font-semibold text-primary hover:underline inline-flex items-center gap-2"
            >
              <span>Inspect course</span>
              <span aria-hidden="true">→</span>
            </router-link>
          </div>
        </article>
      </div>
    </section>
  </main>
</template>
