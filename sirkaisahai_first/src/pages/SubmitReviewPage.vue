<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import StarRating from '../components/ui/StarRating.vue';
import LoadingSpinner from '../components/ui/LoadingSpinner.vue';
import { useAuthStore } from '../stores/auth';
import { api } from '../api';

const authStore = useAuthStore();
const router = useRouter();
const route = useRoute();

const offerings = ref<{ id: string; label: string; courseId: string; professorId: string }[]>([]);
const isLoadingOfferings = ref(true);

const selectedOfferingId = ref('');
const ratingTeaching = ref(5);
const ratingGrading = ref(4);
const ratingWorkload = ref(3);
const gradeReceived = ref('A');
const semesterTaken = ref('Fall 2025');
const comment = ref('');

const isSubmitting = ref(false);
const errorMsg = ref('');
const isSuccess = ref(false);

const profanityList = ['garbage', 'idiot', 'stupid', 'curse', 'scam'];

const containsProfanity = computed(() => {
  const text = comment.value.toLowerCase();
  return profanityList.some((w) => text.includes(w));
});

const isFormValid = computed(() => {
  return (
    selectedOfferingId.value !== '' &&
    comment.value.trim().length >= 15 &&
    !containsProfanity.value
  );
});

onMounted(async () => {
  if (!authStore.isVerified) {
    router.push({ path: '/auth', query: { redirect: '/review/new' } });
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
      selectedOfferingId.value = offerings.value[0].id;
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

    isSuccess.value = true;
  } catch (err: any) {
    errorMsg.value = err.message || 'Failed to submit review. Try again.';
  } finally {
    isSubmitting.value = false;
  }
}
</script>

<template>
  <main class="max-w-container-max mx-auto px-4 md:px-gutter py-6 md:py-stack-lg flex items-center justify-center min-h-[80vh]">
    <div v-if="isSuccess" class="bg-white rounded-2xl md:rounded-3xl p-8 md:p-12 custom-shadow shadow-2xl-ambient text-center max-w-lg w-full">
      <span class="material-symbols-outlined text-green-600 text-6xl mb-4">task_alt</span>
      <h2 class="font-headline-lg text-headline-lg text-[#6B2A5B] mb-2">Review Published Anonymously!</h2>
      <p class="font-body-md text-on-surface-variant mb-6">
        Your feedback is live! Your email address was hashed with SHA-256 and is <strong>never stored</strong> with your review text.
      </p>
      <div class="flex gap-4 justify-center">
        <router-link to="/" class="bg-[#6B2A5B] text-white px-6 py-2.5 rounded-full font-label-sm hover:bg-[#6B2FA0] transition-colors">
          Return Home
        </router-link>
        <button @click="isSuccess = false; comment = ''" class="bg-surface-container-low px-6 py-2.5 rounded-full font-label-sm text-on-surface hover:bg-surface-variant transition-colors">
          Write Another
        </button>
      </div>
    </div>

    <div v-else class="bg-white rounded-2xl md:rounded-3xl p-5 md:p-12 custom-shadow shadow-2xl-ambient max-w-2xl w-full">
      <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-surface-variant pb-4 md:pb-6 mb-4 md:mb-6 gap-2">
        <div>
          <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full font-label-sm text-xs font-bold flex items-center gap-1 inline-flex mb-2">
            <span class="material-symbols-outlined text-[14px]">lock</span> 100% Anonymous (SHA-256 Hashed)
          </span>
          <h1 class="font-headline-lg text-headline-lg text-[#6B2A5B]">Submit Teacher Review</h1>
        </div>
      </div>

      <LoadingSpinner v-if="isLoadingOfferings" text="Loading course options..." />

      <form v-else @submit.prevent="handleSubmit" class="space-y-6">
        <div v-if="errorMsg" class="p-4 bg-red-50 border border-red-200 text-red-700 rounded-2xl text-sm font-bold">
          ⚠️ {{ errorMsg }}
        </div>

        <div>
          <label class="block font-label-sm text-label-sm uppercase text-on-surface-variant font-bold mb-2">
            1. Select Professor & Course
          </label>
          <select v-model="selectedOfferingId" class="w-full bg-surface-container-low border border-outline-variant/30 rounded-xl p-3 text-on-surface font-body-md focus:ring-2 focus:ring-[#6B2A5B] outline-none" required>
            <option value="" disabled>-- Choose teacher --</option>
            <option v-for="off in offerings" :key="off.id" :value="off.id">
              {{ off.label }}
            </option>
          </select>
        </div>

        <!-- 2. Performance Ratings Section -->
        <div>
          <label class="block font-label-sm text-label-sm uppercase text-on-surface-variant font-bold mb-2">
            2. Performance Ratings (Adjustable 1.0 - 5.0)
          </label>
          <div class="bg-surface-container-low p-5 rounded-2xl space-y-6 border border-outline-variant/20">
            <!-- Metric 1: Teaching Clarity -->
            <div class="space-y-2">
              <div class="flex justify-between items-center flex-wrap gap-2">
                <span class="font-body-md text-sm font-bold text-on-surface">Teaching Clarity</span>
                <StarRating v-model="ratingTeaching" :readonly="false" size="lg" showValue />
              </div>
              <input
                type="range"
                min="1"
                max="5"
                step="0.5"
                v-model.number="ratingTeaching"
                class="w-full accent-[#6B2A5B] cursor-pointer h-2 bg-outline-variant/30 rounded-lg"
              />
            </div>

            <!-- Metric 2: Grading Fairness -->
            <div class="space-y-2 border-t border-outline-variant/20 pt-4">
              <div class="flex justify-between items-center flex-wrap gap-2">
                <span class="font-body-md text-sm font-bold text-on-surface">Grading Fairness</span>
                <StarRating v-model="ratingGrading" :readonly="false" size="lg" showValue />
              </div>
              <input
                type="range"
                min="1"
                max="5"
                step="0.5"
                v-model.number="ratingGrading"
                class="w-full accent-[#6B2A5B] cursor-pointer h-2 bg-outline-variant/30 rounded-lg"
              />
            </div>

            <!-- Metric 3: Workload -->
            <div class="space-y-2 border-t border-outline-variant/20 pt-4">
              <div class="flex justify-between items-center flex-wrap gap-2">
                <span class="font-body-md text-sm font-bold text-on-surface">Workload Heavy (5=Heavy)</span>
                <StarRating v-model="ratingWorkload" :readonly="false" size="lg" showValue />
              </div>
              <input
                type="range"
                min="1"
                max="5"
                step="0.5"
                v-model.number="ratingWorkload"
                class="w-full accent-[#6B2A5B] cursor-pointer h-2 bg-outline-variant/30 rounded-lg"
              />
            </div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block font-label-sm text-label-sm uppercase text-on-surface-variant font-bold mb-2">
              Semester Taken
            </label>
            <select v-model="semesterTaken" class="w-full bg-surface-container-low border border-outline-variant/30 rounded-xl p-3 text-on-surface font-body-md focus:ring-2 focus:ring-[#6B2A5B] outline-none">
              <option value="Fall 2025">Fall 2025</option>
              <option value="Spring 2025">Spring 2025</option>
              <option value="Fall 2024">Fall 2024</option>
            </select>
          </div>

          <div>
            <label class="block font-label-sm text-label-sm uppercase text-on-surface-variant font-bold mb-2">
              Grade Received (Optional)
            </label>
            <div class="flex gap-1.5 flex-wrap">
              <button
                v-for="g in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'F']"
                :key="g"
                type="button"
                class="px-3 py-1.5 rounded-lg font-label-sm text-xs font-bold border transition-colors"
                :class="gradeReceived === g ? 'bg-[#6B2A5B] text-white border-[#6B2A5B]' : 'bg-surface border-outline-variant/30 text-on-surface-variant hover:bg-surface-variant'"
                @click="gradeReceived = g"
              >
                {{ g }}
              </button>
            </div>
          </div>
        </div>

        <div>
          <div class="flex justify-between items-center mb-2">
            <label class="font-label-sm text-label-sm uppercase text-on-surface-variant font-bold">
              3. Student Review Comments
            </label>
            <span class="font-label-sm text-xs text-outline" :class="{ 'text-red-500 font-bold': comment.length > 500 }">
              {{ comment.length }} / 500
            </span>
          </div>

          <textarea
            v-model="comment"
            rows="4"
            class="w-full bg-surface-container-low border border-outline-variant/30 rounded-2xl p-4 text-on-surface font-body-md placeholder:text-outline-variant focus:ring-2 focus:ring-[#6B2A5B] outline-none"
            placeholder="Share details about exams, projects, lecture clarity, attendance policies..."
            maxlength="500"
            required
          ></textarea>

          <div v-if="containsProfanity" class="mt-2 text-xs font-bold text-red-600">
            ⚠️ Please refrain from using abusive or inappropriate terms. Keep feedback constructive.
          </div>
        </div>

        <!-- Submit Button: Light Plum Tint when Draft -> Solid 100% Plum when Ready -->
        <div>
          <button
            type="submit"
            class="w-full py-4 rounded-full font-label-sm text-base font-bold transition-all duration-300"
            :class="isFormValid ? 'bg-[#6B2A5B] text-white hover:bg-[#6B2FA0] shadow-lg shadow-[#6B2A5B]/30 active:scale-[0.99] cursor-pointer' : 'bg-[#6B2A5B]/15 text-[#6B2A5B] border border-[#6B2A5B]/20 shadow-none cursor-not-allowed'"
            :disabled="!isFormValid || isSubmitting"
          >
            <span v-if="!isSubmitting">Publish Anonymous Review</span>
            <span v-else>Publishing...</span>
          </button>

          <p v-if="!isFormValid" class="text-center font-label-sm text-xs text-[#6B2A5B]/70 mt-2 font-medium">
            💡 Select a course & type at least 15 characters to publish (Current: {{ comment.trim().length }}/15)
          </p>
        </div>
      </form>
    </div>
  </main>
</template>

<style scoped></style>
