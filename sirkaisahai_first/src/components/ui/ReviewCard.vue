<script setup lang="ts">
import { ref } from 'vue';
import type { Review } from '../../types';
import RatingBadge from './RatingBadge.vue';
import { api } from '../../api';

const props = withDefaults(
  defineProps<{
    review: Review;
    showProfessor?: boolean;
  }>(),
  {
    showProfessor: true
  }
);

const isHelpful = ref(props.review.isHelpfulVoted || false);
const helpfulCount = ref(props.review.helpfulCount);
const isVoting = ref(false);

async function toggleHelpful() {
  if (isVoting.value || isHelpful.value) return;
  isVoting.value = true;
  try {
    const res = await api.voteHelpful(props.review.id);
    if (res.success) {
      isHelpful.value = true;
      helpfulCount.value = res.newCount;
    }
  } finally {
    isVoting.value = false;
  }
}

function formatDate(iso: string) {
  const date = new Date(iso);
  if (Number.isNaN(date.getTime())) return '';
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
}
</script>

<template>
  <article class="ed-card p-6 flex flex-col justify-between gap-5">
    <div class="space-y-4">
      <div class="flex items-start justify-between gap-3">
        <div class="flex items-start gap-3 min-w-0">
          <div class="w-10 h-10 rounded-xl bg-primary-soft text-primary flex items-center justify-center font-mono text-xs font-bold shrink-0">
            {{ review.courseCode ? review.courseCode.substring(0, 2).toUpperCase() : 'SK' }}
          </div>
          <div class="min-w-0 space-y-0.5">
            <div class="flex items-center gap-2 flex-wrap">
              <router-link
                v-if="showProfessor"
                :to="`/professor/${review.professorId}`"
                class="font-bold text-[15px] text-ink-dark hover:text-primary transition-colors"
              >
                {{ review.professorName }}
              </router-link>
              <span v-else class="font-bold text-[15px] text-ink-dark">
                {{ review.courseCode }} · {{ review.courseTitle }}
              </span>
              <span class="font-mono text-[10px] uppercase font-semibold text-success bg-success-soft px-2 py-0.5 rounded-full">
                Verified
              </span>
            </div>
            <div class="text-xs text-ink-subtle flex items-center gap-1.5 flex-wrap">
              <span v-if="showProfessor">{{ review.courseCode }}</span>
              <span v-if="showProfessor">·</span>
              <span>Anonymous</span>
              <span>·</span>
              <span>{{ review.semesterTaken }}</span>
              <template v-if="formatDate(review.createdAt)">
                <span>·</span>
                <span>{{ formatDate(review.createdAt) }}</span>
              </template>
            </div>
          </div>
        </div>

        <RatingBadge :score="review.overallScore" size="md" show-scale />
      </div>

      <p class="text-sm text-ink-muted leading-relaxed">
        {{ review.comment }}
      </p>

      <div class="bg-surface-recessed rounded-xl p-3.5 grid grid-cols-3 gap-3">
        <div class="space-y-1.5">
          <div class="flex justify-between font-mono text-[10px] uppercase text-ink-subtle">
            <span>Teaching</span>
            <strong class="text-ink-dark tabular-nums">{{ review.ratingTeaching.toFixed(1) }}</strong>
          </div>
          <div class="h-1.5 bg-border-soft rounded-full overflow-hidden">
            <div class="h-full bg-primary rounded-full" :style="{ width: `${(review.ratingTeaching / 5) * 100}%` }"></div>
          </div>
        </div>

        <div class="space-y-1.5">
          <div class="flex justify-between font-mono text-[10px] uppercase text-ink-subtle">
            <span>Grading</span>
            <strong class="text-ink-dark tabular-nums">{{ review.ratingGrading.toFixed(1) }}</strong>
          </div>
          <div class="h-1.5 bg-border-soft rounded-full overflow-hidden">
            <div class="h-full bg-primary rounded-full" :style="{ width: `${(review.ratingGrading / 5) * 100}%` }"></div>
          </div>
        </div>

        <div class="space-y-1.5">
          <div class="flex justify-between font-mono text-[10px] uppercase text-ink-subtle">
            <span>Workload</span>
            <strong class="text-warning tabular-nums">{{ review.ratingWorkload.toFixed(1) }}</strong>
          </div>
          <div class="h-1.5 bg-border-soft rounded-full overflow-hidden">
            <div class="h-full bg-warning rounded-full" :style="{ width: `${(review.ratingWorkload / 5) * 100}%` }"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="flex items-center justify-between gap-3 pt-1 border-t border-border-soft/60">
      <div>
        <span
          v-if="review.gradeReceived"
          class="inline-block px-2.5 py-1 rounded-full bg-surface-recessed font-mono text-[11px] text-ink-muted tabular-nums"
        >
          Grade: <strong class="text-primary">{{ review.gradeReceived }}</strong>
        </span>
      </div>

      <button
        type="button"
        class="px-3.5 py-1.5 font-mono text-[11px] font-semibold inline-flex items-center gap-1.5 cursor-pointer tabular-nums rounded-full transition-colors"
        :class="
          isHelpful
            ? 'bg-primary text-on-primary cursor-default'
            : 'bg-surface-recessed text-ink-muted hover:text-primary hover:bg-primary-soft'
        "
        @click="toggleHelpful"
        :disabled="isVoting || isHelpful"
      >
        <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5" aria-hidden="true">
          <path
            d="M8 3L12.5 8H9.5V13H6.5V8H3.5L8 3Z"
            stroke="currentColor"
            stroke-width="1.4"
            stroke-linejoin="round"
          />
        </svg>
        <span>Helpful ({{ helpfulCount }})</span>
      </button>
    </div>
  </article>
</template>
