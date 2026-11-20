<template>
  <main class="w-full">
    <section class="bg-band-hero px-4 md:px-gutter pt-6 pb-10">
      <div class="max-w-3xl mx-auto space-y-2">
        <p class="ed-eyebrow">Privacy Policy &amp; Architecture</p>
        <h1 class="font-display text-3xl sm:text-4xl font-extrabold text-ink-dark">
          How your identity <span class="text-primary">stays yours.</span>
        </h1>
        <p class="text-xs text-ink-muted">Last updated: November 2026 · Superior University Edition</p>
      </div>
    </section>

    <section class="bg-band-light px-4 md:px-gutter py-10">
      <div class="max-w-3xl mx-auto ed-card p-6 sm:p-9 space-y-6 text-sm leading-relaxed">
        <div class="space-y-1.5">
          <h2 class="text-base font-bold text-ink-dark">1. One-Time Email Verification</h2>
          <p class="text-ink-muted">
            Students verify enrollment once using an institutional @superior.edu.pk address. A 6-digit One-Time Password (OTP) is generated in memory with a 10-minute expiration window and immediately consumed once verified.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-border-soft">
          <h2 class="text-base font-bold text-ink-dark">2. Irreversible SHA-256 Hashing</h2>
          <p class="text-ink-muted">
            Upon verification, your institutional email is converted into a one-way SHA-256 cryptographic hash. The database stores only this hash and a random session token inside an httpOnly cookie (skh_session) that client-side JavaScript cannot access.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-border-soft">
          <h2 class="text-base font-bold text-ink-dark">3. Unlinked Review Storage</h2>
          <p class="text-ink-muted">
            Review records contain only the professor reference, course metadata, ratings, optional grade received, semester taken, and comment text. Reviews carry zero foreign keys linking back to your verified user record. A separate submission log enforces the one-review-per-professor limit without linking to review content.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-border-soft">
          <h2 class="text-base font-bold text-ink-dark">4. New Faculty Addition Audit Log</h2>
          <p class="text-ink-muted">
            When a verified student adds a new teacher profile to the catalogue, the server records a teacher creation audit entry tied to the verified account strictly to prevent duplicate or abusive profile entries. Regular faculty reviews remain completely unlinked.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-border-soft">
          <h2 class="text-base font-bold text-ink-dark">5. Rate Limiting &amp; Session Termination</h2>
          <p class="text-ink-muted">
            OTP requests and failed code checks are rate-limited to 5 attempts per 15 minutes to prevent abuse. Logging out invalidates your session token on the server and clears your browser cookie immediately.
          </p>
        </div>

        <div class="pt-4 flex flex-wrap gap-3">
          <router-link to="/terms" class="ed-btn-primary px-5 py-2 text-xs font-semibold">
            Terms of service →
          </router-link>
          <router-link to="/" class="ed-btn-soft px-5 py-2 text-xs font-semibold">
            Back to home
          </router-link>
        </div>
      </div>
    </section>
  </main>
</template>
