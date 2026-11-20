<script setup lang="ts">
import { mockCourses } from '../api/mockData';
import RatingBadge from '../components/ui/RatingBadge.vue';
</script>

<template>
  <main class="max-w-container-max mx-auto px-4 md:px-gutter pt-4 pb-10 space-y-8">
    <section class="neu-surface-lg px-6 py-9 sm:px-10 flex flex-col md:flex-row md:items-center justify-between gap-5">
      <div class="space-y-2">
        <p class="text-[10px] font-semibold uppercase tracking-[0.18em] text-outline">
          Course Reference Catalogue
        </p>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-primary">
          Browse Courses
        </h1>
        <p class="text-sm text-on-surface-variant max-w-xl leading-relaxed">
          Explore sample core Computing &amp; IT courses below. Live student reviews are currently indexed directly by professor in the faculty catalogue.
        </p>
      </div>

      <router-link
        to="/search"
        class="neu-btn-primary px-6 py-2.5 text-xs font-semibold self-start md:self-center shrink-0"
      >
        Browse Professors
      </router-link>
    </section>

    <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <article
        v-for="course in mockCourses"
        :key="course.id"
        class="neu-card p-6 flex flex-col justify-between gap-5"
      >
        <div class="space-y-3">
          <div class="flex items-start justify-between gap-3">
            <div class="space-y-1">
              <div class="font-mono text-xs font-bold text-primary">
                {{ course.code }} <span class="text-outline font-normal">· {{ course.creditHours }} Credit Hours</span>
              </div>
              <h2 class="text-lg font-bold text-on-surface">
                <router-link :to="`/course/${course.id}`" class="hover:text-primary transition-colors">
                  {{ course.title }}
                </router-link>
              </h2>
              <p class="text-xs text-outline">{{ course.departmentName }}</p>
            </div>

            <RatingBadge :score="course.avgRating" size="md" show-scale />
          </div>

          <p class="text-sm text-on-surface-variant leading-relaxed">
            {{ course.description }}
          </p>
        </div>

        <div class="flex items-center justify-between gap-3 pt-1">
          <span class="font-mono text-xs text-outline tabular-nums">
            {{ course.totalReviews }} reference notes
          </span>
          <router-link
            :to="`/course/${course.id}`"
            class="neu-pill-btn px-4 py-2 text-xs font-semibold text-primary"
          >
            View Course →
          </router-link>
        </div>
      </article>
    </section>
  </main>
</template>
