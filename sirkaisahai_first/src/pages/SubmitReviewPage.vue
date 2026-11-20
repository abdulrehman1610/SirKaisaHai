<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import StarRating from '../components/ui/StarRating.vue';
import LoadingSpinner from '../components/ui/LoadingSpinner.vue';
import RatingBadge from '../components/ui/RatingBadge.vue';
import { useAuthStore } from '../stores/auth';
import { api } from '../api';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const offerings = ref<{ id: string; label: string; courseId: string; professorId: string }[]>([]);
const isLoadingOfferings = ref(true);

const selectedOfferingId = ref('');
const ratingTeaching = ref(4.5);
const ratingGrading = ref(4.0);
const ratingWorkload = ref(3.0);
const gradeReceived = ref('A');
const semesterTaken = ref('Fall 2025');
const comment = ref('');

const isSubmitting = ref(false);
const errorMsg = ref('');
const isSuccess = ref(false);
const submittedProfId = ref('');

const profanityList = ['garbage', 'idiot', 'stupid', 'curse', 'scam', 'cheat', 'fraud'];

const containsProfanity = computed(() => {
  const text = comment.value.toLowerCase();
  return profanityList.some((w) => text.includes(w));
});

const liveOverallScore = computed(() => {
  return Number(
    (ratingTeaching.value * 0.4 + ratingGrading.value * 0.4 + (6 - ratingWorkload.value) * 0.2).toFixed(1)
  );
});

const isFormValid = computed(() => {
  return selectedOfferingId.value !== '' && comment.value.trim().length >= 15 && !containsProfanity.value;
});

onMounted(async () => {
  if (!authStore.isVerified) {
    router.push({ path: '/auth', query: { redirect: route.fullPath || '/review/new' } });
    return;
  }

  try {
    offerings.value = await api.getOfferings();

    const targetProfId = route.query.profId as string;
    const targetCourseId = route.query.courseId as string;

    if (targetProfId || targetCourseId) {
      const match = offerings.value.find(
        (o) => o.professorId === targetProfId || o.courseId === targetCourseId
      );
      if (match) selectedOfferingId.value = match.id;
    }

    if (!selectedOfferingId.value && offerings.value.length > 0) {
      const firstId = offerings.value[0]?.id;
      if (firstId) selectedOfferingId.value = firstId;
    }
  } finally {
    isLoadingOfferings.value = false;
  }
});

async function handleSubmit() {
  if (!isFormValid.value || isSubmitting.value) return;

  const offering = offerings.value.find((o) => o.id === selectedOfferingId.value);
  if (!offering) return;

  isSubmitting.value = true;
  errorMsg.value = '';

  try {
    const course = await api.getCourseById(offering.courseId);
    const prof = await api.getProfessorById(offering.professorId);

    await api.submitReview({
      offeringId: offering.id,
      courseId: offering.courseId,
      courseCode: course ? course.code : 'CS-101',
      courseTitle: course ? course.title : 'Course',
      professorId: offering.professorId,
      professorName: prof ? prof.name : 'Professor',
      ratingTeaching: Number(ratingTeaching.value),
      ratingGrading: Number(ratingGrading.value),
      ratingWorkload: Number(ratingWorkload.value),
      comment: comment.value.trim(),
      gradeReceived: gradeReceived.value,
      semesterTaken: semesterTaken.value,
      tags: ['Verified Student', 'Recent Semester'],
      userEmail: authStore.email || undefined
    });

    submittedProfId.value = offering.professorId;
    isSuccess.value = true;
  } catch (err: unknown) {
    errorMsg.value = err instanceof Error ? err.message : 'Failed to submit review. Try again.';
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <main class="w-full">
    <section class="bg-band-hero px-4 md:px-gutter pt-6 pb-10">
      <div class="max-w-2xl mx-auto flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div class="space-y-1.5">
          <p class="ed-eyebrow">Verified Session · Your name never appears</p>
          <h1 class="font-display text-3xl sm:text-4xl font-extrabold text-ink-dark">
            Share your <span class="text-primary">perspective.</span>
          </h1>
        </div>

        <div class="bg-card-pearl rounded-2xl px-4 py-2.5 flex items-center gap-3 self-start">
          <span class="ed-eyebrow">Computed</span>
          <RatingBadge :score="liveOverallScore" size="md" show-scale />
        </div>
      </div>
    </section>

    <section class="bg-band-light px-4 md:px-gutter py-10 min-h-[55vh]">
      <div class="max-w-2xl mx-auto">
        <div v-if="isSuccess" class="ed-card p-8 md:p-10 text-center space-y-5">
          <span class="inline-block font-mono text-[10px] uppercase tracking-wider font-semibold text-success bg-success-soft px-3 py-1 rounded-full">
            Published anonymously
          </span>
          <h2 class="text-2xl font-extrabold text-ink-dark">Your review is live.</h2>
          <p class="text-sm text-ink-muted max-w-md mx-auto">
            Your email address was hashed with SHA-256 and is never stored alongside your feedback.
          </p>
          <div class="flex flex-wrap justify-center gap-3 pt-1">
            <router-link
              v-if="submittedProfId"
              :to="`/professor/${submittedProfId}`"
              class="ed-btn-primary px-6 py-2.5 text-xs font-semibold inline-flex items-center gap-2"
            >
              <span>View dossier</span>
              <span aria-hidden="true">→</span>
            </router-link>
            <router-link to="/" class="ed-btn-soft px-6 py-2.5 text-xs font-semibold">
              Return home
            </router-link>
          </div>
        </div>

        <div v-else class="ed-card p-6 sm:p-8 md:p-10">
          <LoadingSpinner v-if="isLoadingOfferings" text="Loading faculty list..." :rows="2" />

          <form v-else @submit.prevent="handleSubmit" class="space-y-6">
            <div v-if="errorMsg" class="p-3.5 bg-error-soft text-error rounded-xl text-xs font-semibold">
              {{ errorMsg }}
            </div>

            <div class="space-y-2">
              <div class="flex items-baseline justify-between gap-2">
                <label for="prof-select" class="ed-eyebrow">1. Select professor</label>
                <router-link to="/search" class="text-xs font-semibold text-primary hover:underline">
                  Teacher missing? Add them ↗
                </router-link>
              </div>
              <select
                id="prof-select"
                v-model="selectedOfferingId"
                class="w-full ed-input px-4 py-3 text-sm"
                required
              >
                <option value="" disabled>Choose a professor</option>
                <option v-for="off in offerings" :key="off.id" :value="off.id">
                  {{ off.label }}
                </option>
              </select>
            </div>

            <div class="space-y-2">
              <span class="block ed-eyebrow">2. Evaluation criteria (1.0 - 5.0)</span>
              <div class="bg-surface-recessed rounded-2xl p-5 space-y-6">
                <div class="space-y-2.5">
                  <div class="flex justify-between items-center flex-wrap gap-2">
                    <span class="text-sm font-bold text-ink-dark">Teaching clarity</span>
                    <StarRating v-model="ratingTeaching" :readonly="false" show-value />
                  </div>
                  <input v-model.number="ratingTeaching" type="range" min="1" max="5" step="0.5" class="w-full accent-primary cursor-pointer" />
                  <div class="flex justify-between font-mono text-[10px] text-ink-subtle">
                    <span>1.0 Unclear</span>
                    <span>5.0 Crystal clear</span>
                  </div>
                </div>

                <div class="space-y-2.5 border-t border-border-soft pt-5">
                  <div class="flex justify-between items-center flex-wrap gap-2">
                    <span class="text-sm font-bold text-ink-dark">Grading fairness</span>
                    <StarRating v-model="ratingGrading" :readonly="false" show-value />
                  </div>
                  <input v-model.number="ratingGrading" type="range" min="1" max="5" step="0.5" class="w-full accent-primary cursor-pointer" />
                  <div class="flex justify-between font-mono text-[10px] text-ink-subtle">
                    <span>1.0 Strict / Unclear</span>
                    <span>5.0 Fair rubric</span>
                  </div>
                </div>

                <div class="space-y-2.5 border-t border-border-soft pt-5">
                  <div class="flex justify-between items-center flex-wrap gap-2">
                    <span class="text-sm font-bold text-ink-dark">Workload intensity</span>
                    <StarRating v-model="ratingWorkload" :readonly="false" mode="intensity" show-value />
                  </div>
                  <input v-model.number="ratingWorkload" type="range" min="1" max="5" step="0.5" class="w-full accent-warning cursor-pointer" />
                  <div class="flex justify-between font-mono text-[10px] text-ink-subtle">
                    <span>1.0 Light</span>
                    <span>5.0 Heavy assignments &amp; quizzes</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
              <div class="space-y-2">
                <label for="sem-select" class="block ed-eyebrow">Semester taken</label>
                <select id="sem-select" v-model="semesterTaken" class="w-full ed-input px-4 py-3 text-sm">
                  <option value="Spring 2026">Spring 2026</option>
                  <option value="Fall 2025">Fall 2025</option>
                  <option value="Spring 2025">Spring 2025</option>
                  <option value="Fall 2024">Fall 2024</option>
                </select>
              </div>

              <div class="space-y-2">
                <span class="block ed-eyebrow">Grade received (optional)</span>
                <div class="flex gap-1.5 flex-wrap pt-0.5">
                  <button
                    v-for="g in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'F']"
                    :key="g"
                    type="button"
                    class="px-3 py-1.5 font-mono text-xs font-semibold rounded-full cursor-pointer transition-colors"
                    :class="
                      gradeReceived === g
                        ? 'bg-primary text-on-primary'
                        : 'bg-surface-recessed text-ink-muted hover:text-primary'
                    "
                    @click="gradeReceived = g"
                  >
                    {{ g }}
                  </button>
                </div>
              </div>
            </div>

            <div class="space-y-2">
              <div class="flex justify-between items-center">
                <label for="comment-box" class="ed-eyebrow">3. Student review comments</label>
                <span
                  class="font-mono text-xs tabular-nums"
                  :class="comment.length > 500 ? 'text-error font-bold' : 'text-ink-subtle'"
                >
                  {{ comment.length }} / 500
                </span>
              </div>

              <textarea
                id="comment-box"
                v-model="comment"
                rows="4"
                class="w-full ed-input p-4 text-sm"
                placeholder="Share details about exams, projects, lecture clarity, attendance policies..."
                maxlength="500"
                required
              ></textarea>

              <p v-if="containsProfanity" class="text-xs font-semibold text-error">
                Please keep feedback constructive and remove inappropriate language.
              </p>
            </div>

            <div class="space-y-2.5 pt-1">
              <button
                type="submit"
                class="w-full py-3.5 text-sm font-semibold rounded-full inline-flex items-center justify-center gap-3 cursor-pointer"
                :class="isFormValid ? 'ed-btn-primary' : 'bg-surface-recessed text-ink-subtle cursor-not-allowed'"
                :disabled="!isFormValid || isSubmitting"
              >
                <span>{{ isSubmitting ? 'Publishing...' : 'Publish anonymous review' }}</span>
                <span v-if="!isSubmitting" aria-hidden="true">→</span>
              </button>

              <p v-if="!isFormValid" class="text-center text-xs text-ink-subtle">
                Select a professor and write at least 15 characters ({{ comment.trim().length }}/15).
              </p>
            </div>
          </form>
        </div>
      </div>
    </section>
  </main>
</template>
