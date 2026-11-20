<script setup lang="ts">
import AppLogo from '../ui/AppLogo.vue';

const currentYear = new Date().getFullYear();
</script>

<template>
  <footer class="max-w-container-max mx-auto px-4 md:px-gutter pt-12 pb-10 w-full">
    <div class="neu-surface-lg p-5 sm:p-7 md:p-8 space-y-5">
      <!-- Inner Recessed Tray (Exact Double-Layered Soft UI Frame) -->
      <div class="neu-inset-tray p-6 sm:p-8 md:p-10">
        <div class="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-10">
          <!-- Column 1: Brand & Quick Links -->
          <div class="md:col-span-5 flex flex-col justify-between gap-6">
            <div class="space-y-3">
              <AppLogo size="md" :boxed="false" />
              <p class="text-[13px] text-on-surface-variant leading-relaxed max-w-xs">
                Elevating transparency at Superior University. 100% anonymous, student-driven insights.
              </p>
            </div>

            <div class="flex items-center gap-3">
              <a
                href="https://github.com/abdulrehman1610/sirkaisahai"
                target="_blank"
                rel="noopener noreferrer"
                class="neu-tile w-9 h-9 flex items-center justify-center text-on-surface-variant hover:text-primary transition-colors"
                aria-label="GitHub repository"
              >
                <svg viewBox="0 0 20 20" fill="none" class="w-4 h-4">
                  <path
                    d="M10 2.5C5.86 2.5 2.5 5.86 2.5 10C2.5 13.32 4.65 16.12 7.63 17.11C8 17.18 8.14 16.95 8.14 16.75C8.14 16.57 8.13 15.98 8.13 15.35C6.25 15.7 5.76 14.9 5.61 14.48C5.53 14.27 5.16 13.62 4.84 13.44C4.58 13.3 4.21 12.95 4.83 12.94C5.42 12.93 5.84 13.48 5.98 13.71C6.65 14.84 7.72 14.52 8.17 14.32C8.24 13.84 8.43 13.51 8.64 13.32C6.97 13.13 5.23 12.48 5.23 9.61C5.23 8.79 5.52 8.12 6 7.6C5.92 7.41 5.66 6.64 6.08 5.6C6.08 5.6 6.71 5.4 8.14 6.37C8.74 6.2 9.38 6.12 10.02 6.12C10.66 6.12 11.3 6.2 11.9 6.37C13.33 5.39 13.96 5.6 13.96 5.6C14.38 6.64 14.12 7.41 14.04 7.6C14.52 8.12 14.81 8.78 14.81 9.61C14.81 12.49 13.06 13.13 11.39 13.32C11.66 13.55 11.89 14 11.89 14.7C11.89 15.7 11.88 16.5 11.88 16.75C11.88 16.95 12.02 17.19 12.39 17.11C15.36 16.12 17.5 13.31 17.5 10C17.5 5.86 14.14 2.5 10 2.5Z"
                    stroke="currentColor"
                    stroke-width="1.35"
                    stroke-linejoin="round"
                  />
                </svg>
              </a>
              <router-link
                to="/privacy"
                class="neu-tile w-9 h-9 flex items-center justify-center text-on-surface-variant hover:text-primary transition-colors"
                aria-label="Privacy policy"
              >
                <svg viewBox="0 0 20 20" fill="none" class="w-4 h-4">
                  <rect x="3" y="5" width="14" height="10" rx="2" stroke="currentColor" stroke-width="1.4" />
                  <path d="M4 6.5L10 11L16 6.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
              </router-link>
            </div>
          </div>

          <!-- Column 2: Explore -->
          <div class="md:col-span-3 space-y-3.5">
            <h4 class="text-[11px] font-bold uppercase tracking-[0.14em] text-on-surface">Explore</h4>
            <ul class="space-y-2.5 text-[13px] text-on-surface-variant">
              <li>
                <router-link to="/search" class="hover:text-primary transition-colors">Top Professors</router-link>
              </li>
              <li>
                <router-link to="/courses" class="hover:text-primary transition-colors">Course Reviews</router-link>
              </li>
              <li>
                <router-link to="/auth" class="hover:text-primary transition-colors">Student Verification</router-link>
              </li>
            </ul>
          </div>

          <!-- Column 3: Our Promise & Legal -->
          <div class="md:col-span-4 space-y-3.5">
            <h4 class="text-[11px] font-bold uppercase tracking-[0.14em] text-on-surface">Our Promise</h4>
            <ul class="space-y-2.5 text-[13px] text-on-surface-variant">
              <li class="flex items-center gap-2">
                <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5 text-primary shrink-0">
                  <path d="M3.5 8.5L6.5 11.5L12.5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <span>Zero Tracking</span>
              </li>
              <li class="flex items-center gap-2">
                <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5 text-primary shrink-0">
                  <path d="M3.5 8.5L6.5 11.5L12.5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <span>SHA-256 Hashed</span>
              </li>
              <li class="flex items-center gap-2">
                <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5 text-primary shrink-0">
                  <path d="M3.5 8.5L6.5 11.5L12.5 5" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
                </svg>
                <span>Moderated</span>
              </li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Bottom Copyright Row -->
      <div class="flex flex-col sm:flex-row justify-between items-center gap-2 px-1 text-[11px] text-outline">
        <p>© {{ currentYear }} SirKaisaHai · Superior University edition</p>
        <div class="flex items-center gap-4">
          <router-link to="/privacy" class="hover:text-primary transition-colors">Privacy</router-link>
          <router-link to="/terms" class="hover:text-primary transition-colors">Terms</router-link>
          <span>Built with care. By students.</span>
        </div>
      </div>
    </div>
  </footer>
</template>
