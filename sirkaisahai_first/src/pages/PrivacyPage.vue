<template>
  <main class="max-w-3xl mx-auto px-4 md:px-gutter pt-4 pb-10 space-y-7">
    <div class="neu-surface-lg p-7 md:p-10 space-y-6">
      <header class="space-y-2">
        <p class="text-[10px] font-semibold uppercase tracking-[0.18em] text-outline">
          Privacy Policy &amp; Architecture
        </p>
        <h1 class="text-2xl md:text-3xl font-extrabold text-primary">
          How SirKaisaHai protects student anonymity
        </h1>
        <p class="text-xs text-outline">
          Last updated: November 2026 · Superior University Edition
        </p>
      </header>

      <div class="neu-inset-tray p-6 md:p-7 space-y-5 text-sm leading-relaxed">
        <div class="space-y-1.5">
          <h2 class="text-base font-bold text-on-surface">1. One-Time Email Verification</h2>
          <p class="text-on-surface-variant">
            Students verify enrollment once using an institutional @superior.edu.pk address. A 6-digit One-Time Password (OTP) is generated in memory with a 10-minute expiration window and immediately consumed once verified.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-surface-variant">
          <h2 class="text-base font-bold text-on-surface">2. Irreversible SHA-256 Hashing</h2>
          <p class="text-on-surface-variant">
            Upon verification, your institutional email is converted into a one-way SHA-256 cryptographic hash. The database stores only this hash and a random session token inside an httpOnly cookie (skh_session) that client-side JavaScript cannot access.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-surface-variant">
          <h2 class="text-base font-bold text-on-surface">3. Unlinked Review Storage</h2>
          <p class="text-on-surface-variant">
            Review records contain only the professor reference, course metadata, ratings, optional grade received, semester taken, and comment text. Reviews carry zero foreign keys linking back to your verified user record. A separate submission log enforces the one-review-per-professor limit without linking to review content.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-surface-variant">
          <h2 class="text-base font-bold text-on-surface">4. New Faculty Addition Audit Log</h2>
          <p class="text-on-surface-variant">
            When a verified student adds a new teacher profile to the catalogue, the server records a teacher creation audit entry tied to the verified account strictly to prevent duplicate or abusive profile entries. Regular faculty reviews remain completely unlinked.
          </p>
        </div>

        <div class="space-y-1.5 pt-4 border-t border-surface-variant">
          <h2 class="text-base font-bold text-on-surface">5. Rate Limiting &amp; Session Termination</h2>
          <p class="text-on-surface-variant">
            OTP requests and failed code checks are rate-limited to 5 attempts per 15 minutes to prevent abuse. Logging out invalidates your session token on the server and clears your browser cookie immediately.
          </p>
        </div>
      </div>

      <div class="flex flex-wrap gap-3">
        <router-link to="/terms" class="neu-pill-btn px-5 py-2 text-xs font-semibold text-primary">
          Terms of Service
        </router-link>
        <router-link to="/" class="neu-pill-btn px-5 py-2 text-xs font-semibold text-on-surface-variant">
          Back to Home
        </router-link>
      </div>
    </div>
  </main>
</template>

