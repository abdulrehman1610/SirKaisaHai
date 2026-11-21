<template>
  <main class="w-full">
    <section class="bg-band-hero px-4 md:px-gutter pt-24 pb-10">
      <div class="max-w-3xl mx-auto space-y-2">
        <p class="ed-eyebrow">Terms of Service</p>
        <h1 class="font-display text-3xl sm:text-4xl font-extrabold text-ink-dark">
          Community guidelines &amp; <span class="text-primary">fair use.</span>
        </h1>
        <p class="text-xs text-ink-muted">Last updated: November 2026 · SirKaisaHai Independent Student Platform</p>
      </div>
    </section>

    <section class="bg-band-light px-4 md:px-gutter py-10">
      <div class="max-w-3xl mx-auto ed-card p-6 sm:p-9 space-y-6 text-sm leading-relaxed">
        <div class="space-y-1.5">
          <h2 class="text-base font-bold text-ink-dark">1. Independent Student Project</h2>
          <p class="text-ink-muted">
            SirKaisaHai is an independent, student-built directory created to help students make informed semester registration choices. It is unaffiliated with and unendorsed by Superior University administration or faculty bodies.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-border-soft">
          <h2 class="text-base font-bold text-ink-dark">2. Verified Participation &amp; Fair Use</h2>
          <p class="text-ink-muted">
            Submitting reviews and adding faculty profiles require a verified @superior.edu.pk email session. Each student is limited to one review per professor so scores reflect authentic breadth of peer experiences.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-border-soft">
          <h2 class="text-base font-bold text-ink-dark">3. Constructive Academic Feedback</h2>
          <p class="text-ink-muted">
            Reviews must stay focused on academic factors including lecture clarity, exam structure, grading transparency, attendance policies, and workload intensity. Profanity, harassment, personal attacks outside the classroom, or private contact details are prohibited and subject to automated filtering or removal.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-border-soft">
          <h2 class="text-base font-bold text-ink-dark">4. Adding Accurate Faculty Entries</h2>
          <p class="text-ink-muted">
            When adding a missing teacher to the catalogue, provide their real full name, correct department, and academic designation. Duplicate names across departments are rejected automatically.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-border-soft">
          <h2 class="text-base font-bold text-ink-dark">5. Content Responsibility</h2>
          <p class="text-ink-muted">
            Published reviews reflect individual student opinions and are provided for informational purposes only. SirKaisaHai makes no guarantee regarding future course grading outcomes or teaching assignments.
          </p>
        </div>

        <div class="pt-4 flex flex-wrap gap-3">
          <router-link to="/privacy" class="ed-btn-primary px-5 py-2 text-xs font-semibold">
            Privacy policy →
          </router-link>
          <router-link to="/" class="ed-btn-soft px-5 py-2 text-xs font-semibold">
            Back to home
          </router-link>
        </div>
      </div>
    </section>
  </main>
</template>
