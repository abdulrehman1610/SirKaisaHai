<template>
  <main class="max-w-3xl mx-auto px-4 md:px-gutter pt-4 pb-10 space-y-7">
    <div class="neu-surface-lg p-7 md:p-10 space-y-6">
      <header class="space-y-2">
        <p class="text-[10px] font-semibold uppercase tracking-[0.18em] text-outline">
          Terms of Service
        </p>
        <h1 class="text-2xl md:text-3xl font-extrabold text-primary">
          Community guidelines and usage terms
        </h1>
        <p class="text-xs text-outline">
          Last updated: November 2026 · SirKaisaHai Independent Student Platform
        </p>
      </header>

      <div class="neu-inset-tray p-6 md:p-7 space-y-5 text-sm leading-relaxed">
        <div class="space-y-1.5">
          <h2 class="text-base font-bold text-on-surface">1. Independent Student Project</h2>
          <p class="text-on-surface-variant">
            SirKaisaHai is an independent, student-built directory created to help students make informed semester registration choices. It is unaffiliated with and unendorsed by Superior University administration or faculty bodies.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-surface-variant">
          <h2 class="text-base font-bold text-on-surface">2. Verified Participation &amp; Fair Use</h2>
          <p class="text-on-surface-variant">
            Submitting reviews and adding faculty profiles require a verified @superior.edu.pk email session. Each student is limited to one review per professor so scores reflect authentic breadth of peer experiences.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-surface-variant">
          <h2 class="text-base font-bold text-on-surface">3. Constructive Academic Feedback</h2>
          <p class="text-on-surface-variant">
            Reviews must stay focused on academic factors including lecture clarity, exam structure, grading transparency, attendance policies, and workload intensity. Profanity, harassment, personal attacks outside the classroom, or private contact details are prohibited and subject to automated filtering or removal.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-surface-variant">
          <h2 class="text-base font-bold text-on-surface">4. Adding Accurate Faculty Entries</h2>
          <p class="text-on-surface-variant">
            When adding a missing teacher to the catalogue, provide their real full name, correct department, and academic designation. Duplicate names across departments are rejected automatically.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-surface-variant">
          <h2 class="text-base font-bold text-on-surface">5. Content Responsibility</h2>
          <p class="text-on-surface-variant">
            Published reviews reflect individual student opinions and are provided for informational purposes only. SirKaisaHai makes no guarantee regarding future course grading outcomes or teaching assignments.
          </p>
        </div>
      </div>

      <div class="flex flex-wrap gap-3">
        <router-link to="/privacy" class="neu-pill-btn px-5 py-2 text-xs font-semibold text-primary">
          Privacy Policy
        </router-link>
        <router-link to="/" class="neu-pill-btn px-5 py-2 text-xs font-semibold text-on-surface-variant">
          Back to Home
        </router-link>
      </div>
    </div>
  </main>
</template>

