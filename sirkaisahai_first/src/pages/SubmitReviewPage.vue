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
    errorMsg.value = err instanceof Error ? err.message : 'Failed to submit review. Please try again.';
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <main class="max-w-container-max mx-auto px-4 md:px-gutter pt-4 pb-12 flex items-start justify-center min-h-[75vh]">
    <!-- Success Card -->
    <div v-if="isSuccess" class="neu-surface-lg p-8 md:p-10 text-center max-w-md w-full space-y-5 mt-6">
      <div class="neu-tile w-14 h-14 mx-auto flex items-center justify-center text-success">
        <svg viewBox="0 0 20 20" fill="none" class="w-6 h-6">
          <path d="M4.5 10.5L8.2 14.2L15.5 6.5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" />
        </svg>
      </div>
      <div class="space-y-1.5">
        <h1 class="text-xl font-extrabold text-primary">Review Published Anonymously</h1>
        <p class="text-xs text-on-surface-variant leading-relaxed">
          Your feedback is live. Your email address was hashed with SHA-256 and is never stored with your review text.
        </p>
      </div>
      <div class="flex flex-wrap gap-3 justify-center pt-1">
        <router-link
          v-if="submittedProfId"
          :to="`/professor/${submittedProfId}`"
          class="neu-btn-primary px-6 py-2.5 text-xs font-semibold"
        >
          View Profile
        </router-link>
        <router-link to="/" class="neu-pill-btn px-6 py-2.5 text-xs font-semibold">
          Return Home
        </router-link>
      </div>
    </div>

    <!-- Review Form Card -->
    <div v-else class="neu-surface-lg p-6 sm:p-8 md:p-10 max-w-2xl w-full space-y-7">
      <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
        <div class="space-y-1.5">
          <span class="inline-block font-mono text-[10px] uppercase tracking-wider font-semibold text-success bg-success-soft px-3 py-1 rounded-full">
            100% Anonymous · SHA-256 Verified
          </span>
          <h1 class="text-2xl md:text-3xl font-extrabold text-primary">
            Submit Teacher Review
          </h1>
        </div>

        <div class="neu-inset-tray px-4 py-2.5 flex items-center gap-3 self-start">
          <span class="font-mono text-[10px] uppercase text-outline">Computed</span>
          <RatingBadge :score="liveOverallScore" size="md" show-scale />
        </div>
      </div>

      <LoadingSpinner v-if="isLoadingOfferings" text="Loading faculty list..." :rows="2" />

      <form v-else @submit.prevent="handleSubmit" class="space-y-6">
        <div v-if="errorMsg" class="neu-inset rounded-xl p-3.5 text-xs font-semibold text-error">
          {{ errorMsg }}
        </div>

        <!-- 1. Professor Select -->
        <div class="space-y-2">
          <div class="flex items-baseline justify-between gap-2">
            <label for="prof-select" class="text-[11px] font-bold uppercase tracking-wider text-outline">
              1. Select Professor
            </label>
            <router-link to="/search" class="text-xs font-semibold text-primary hover:underline">
              Teacher missing? Add them
            </router-link>
          </div>
          <select
            id="prof-select"
            v-model="selectedOfferingId"
            class="w-full neu-inset rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-0 focus:outline-none"
            required
          >
            <option value="" disabled>Choose a professor</option>
            <option v-for="off in offerings" :key="off.id" :value="off.id">
              {{ off.label }}
            </option>
          </select>
        </div>

        <!-- 2. Criteria Ratings -->
        <div class="space-y-2">
          <span class="block text-[11px] font-bold uppercase tracking-wider text-outline">
            2. Performance Ratings (1.0 - 5.0)
          </span>

          <div class="neu-inset-tray p-5 space-y-6">
            <div class="space-y-2.5">
              <div class="flex justify-between items-center flex-wrap gap-2">
                <span class="text-sm font-bold text-on-surface">Teaching Clarity</span>
                <StarRating v-model="ratingTeaching" :readonly="false" show-value />
              </div>
              <input
                v-model.number="ratingTeaching"
                type="range"
                min="1"
                max="5"
                step="0.5"
                class="w-full accent-primary cursor-pointer"
              />
              <div class="flex justify-between font-mono text-[10px] text-outline">
                <span>1.0 Unclear</span>
                <span>5.0 Crystal Clear</span>
              </div>
            </div>

            <div class="space-y-2.5 border-t border-surface-variant pt-5">
              <div class="flex justify-between items-center flex-wrap gap-2">
                <span class="text-sm font-bold text-on-surface">Grading Fairness</span>
                <StarRating v-model="ratingGrading" :readonly="false" show-value />
              </div>
              <input
                v-model.number="ratingGrading"
                type="range"
                min="1"
                max="5"
                step="0.5"
                class="w-full accent-primary cursor-pointer"
              />
              <div class="flex justify-between font-mono text-[10px] text-outline">
                <span>1.0 Strict / Unclear</span>
                <span>5.0 Fair Rubric</span>
              </div>
            </div>

            <div class="space-y-2.5 border-t border-surface-variant pt-5">
              <div class="flex justify-between items-center flex-wrap gap-2">
                <span class="text-sm font-bold text-on-surface">Workload Intensity</span>
                <StarRating v-model="ratingWorkload" :readonly="false" mode="intensity" show-value />
              </div>
              <input
                v-model.number="ratingWorkload"
                type="range"
                min="1"
                max="5"
                step="0.5"
                class="w-full accent-warning cursor-pointer"
              />
              <div class="flex justify-between font-mono text-[10px] text-outline">
                <span>1.0 Light</span>
                <span>5.0 Heavy Assignments &amp; Quizzes</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 3. Semester & Grade -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
          <div class="space-y-2">
            <label for="sem-select" class="block text-[11px] font-bold uppercase tracking-wider text-outline">
              Semester Taken
            </label>
            <select
              id="sem-select"
              v-model="semesterTaken"
              class="w-full neu-inset rounded-xl px-4 py-3 text-sm text-on-surface focus:ring-0 focus:outline-none"
            >
              <option value="Spring 2026">Spring 2026</option>
              <option value="Fall 2025">Fall 2025</option>
              <option value="Spring 2025">Spring 2025</option>
              <option value="Fall 2024">Fall 2024</option>
            </select>
          </div>

          <div class="space-y-2">
            <span class="block text-[11px] font-bold uppercase tracking-wider text-outline">
              Grade Received (Optional)
            </span>
            <div class="flex gap-2 flex-wrap pt-0.5">
              <button
                v-for="g in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'F']"
                :key="g"
                type="button"
                class="px-3 py-1.5 font-mono text-xs font-semibold cursor-pointer"
                :class="gradeReceived === g ? 'neu-btn-primary' : 'neu-pill-btn text-on-surface-variant'"
                @click="gradeReceived = g"
              >
                {{ g }}
              </button>
            </div>
          </div>
        </div>

        <!-- 4. Comments -->
        <div class="space-y-2">
          <div class="flex justify-between items-center">
            <label for="comment-box" class="text-[11px] font-bold uppercase tracking-wider text-outline">
              3. Student Review Comments
            </label>
            <span
              class="font-mono text-xs tabular-nums"
              :class="comment.length > 500 ? 'text-error font-bold' : 'text-outline'"
            >
              {{ comment.length }} / 500
            </span>
          </div>

          <textarea
            id="comment-box"
            v-model="comment"
            rows="4"
            class="w-full neu-inset rounded-2xl p-4 text-sm text-on-surface placeholder-outline focus:ring-0 focus:outline-none"
            placeholder="Share details about exams, projects, lecture clarity, attendance policies..."
            maxlength="500"
            required
          ></textarea>

          <p v-if="containsProfanity" class="text-xs font-semibold text-error">
            Please keep feedback constructive and remove inappropriate terms.
          </p>
        </div>

        <!-- Submit -->
        <div class="space-y-2.5 pt-1">
          <button
            type="submit"
            class="w-full py-3.5 text-sm font-semibold cursor-pointer"
            :class="isFormValid ? 'neu-btn-primary' : 'neu-inset rounded-full text-outline cursor-not-allowed'"
            :disabled="!isFormValid || isSubmitting"
          >
            {{ isSubmitting ? 'Publishing...' : 'Publish Anonymous Review' }}
          </button>

          <p v-if="!isFormValid" class="text-center text-xs text-outline">
            Select a teacher and type at least 15 characters ({{ comment.trim().length }}/15).
          </p>
        </div>
      </form>
    </div>
  </main>
</template>
