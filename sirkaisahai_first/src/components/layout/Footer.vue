<script setup lang="ts">
import AppLogo from '../ui/AppLogo.vue';

const currentYear = new Date().getFullYear();
</script>

<template>
  <footer class="bg-band-lilac px-4 md:px-gutter pt-4 pb-8 w-full">
    <div class="max-w-container-max mx-auto bg-primary-dark text-on-primary rounded-[26px] px-6 py-10 sm:px-10 md:px-12 md:py-12">
      <div class="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-10">
        <!-- Brand Column -->
        <div class="md:col-span-6 space-y-4">
          <AppLogo size="xl" variant="light" />
          <p class="text-sm text-on-primary/70 leading-relaxed max-w-xs">
            Better choices. Stronger student voices.<br />
            100% anonymous, student-driven insights.
          </p>
        </div>

        <!-- Explore Column -->
        <div class="md:col-span-3 space-y-3.5">
          <h4 class="font-mono text-[10px] font-semibold uppercase tracking-[0.16em] text-on-primary/50">
            Explore
          </h4>
          <ul class="space-y-2.5 text-[13px] text-on-primary/80">
            <li>
              <router-link to="/search" class="hover:text-on-primary transition-colors">Top professors</router-link>
            </li>
            <li>
              <router-link to="/courses" class="hover:text-on-primary transition-colors">Course reviews</router-link>
            </li>
            <li>
              <router-link to="/auth" class="hover:text-on-primary transition-colors">Student verification</router-link>
            </li>
          </ul>
        </div>

        <!-- Our Promise Column -->
        <div class="md:col-span-3 space-y-3.5">
          <h4 class="font-mono text-[10px] font-semibold uppercase tracking-[0.16em] text-on-primary/50">
            Our Promise
          </h4>
          <ul class="space-y-2.5 text-[13px] text-on-primary/80">
            <li class="flex items-center gap-2">
              <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5 text-on-primary/60 shrink-0">
                <path d="M3.5 8.5L6.5 11.5L12.5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <span>Zero tracking</span>
            </li>
            <li class="flex items-center gap-2">
              <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5 text-on-primary/60 shrink-0">
                <path d="M3.5 8.5L6.5 11.5L12.5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <span>SHA-256 hashed</span>
            </li>
            <li class="flex items-center gap-2">
              <svg viewBox="0 0 16 16" fill="none" class="w-3.5 h-3.5 text-on-primary/60 shrink-0">
                <path d="M3.5 8.5L6.5 11.5L12.5 5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
              </svg>
              <span>Moderated</span>
            </li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="mt-10 pt-5 border-t border-on-primary/15 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 text-[11px] text-on-primary/55">
        <p>© {{ currentYear }} SirKaisaHai · Superior University edition</p>
        <div class="flex items-center gap-4">
          <router-link to="/privacy" class="hover:text-on-primary transition-colors">Privacy</router-link>
          <router-link to="/terms" class="hover:text-on-primary transition-colors">Terms</router-link>
          <span>Built with care. By students.</span>
        </div>
      </div>
    </div>
  </footer>
</template>
