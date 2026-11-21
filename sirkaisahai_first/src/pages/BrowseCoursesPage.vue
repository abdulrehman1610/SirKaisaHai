<template>
  <div class="courses-stage flex-1 w-full bg-band-hero relative overflow-hidden flex items-center justify-center px-4 md:px-gutter pt-24 pb-12">
    <!-- Leading Diagonal Sweep Accent Veil -->
    <div class="diagonal-veil" aria-hidden="true"></div>

    <!-- Primary Prominent Plum-Pink (#61204C) Top-Left to Bottom-Right Curtain -->
    <div class="diagonal-curtain" aria-hidden="true"></div>

    <!-- Centered Editorial Content -->
    <section class="courses-content relative z-10 max-w-container-max w-full mx-auto text-center space-y-6">
      <p class="font-mono text-[10px] sm:text-[11px] font-semibold uppercase tracking-[0.18em] text-on-primary/65">
        Browse Courses · Superior University
      </p>

      <h1 class="font-display text-4xl sm:text-5xl md:text-[62px] font-extrabold text-on-primary leading-[1.03] tracking-[-0.03em] max-w-3xl mx-auto">
        This section is not available right now.
      </h1>

      <p class="text-sm sm:text-base text-on-primary/75 max-w-md mx-auto leading-relaxed">
        Dedicated course pages are still being prepared. You can search and review professors right now.
      </p>

      <div class="flex flex-wrap items-center justify-center gap-3.5 pt-2">
        <router-link
          to="/search"
          class="bg-card-pearl text-primary hover:bg-band-hero px-6 py-3 rounded-full text-xs font-bold inline-flex items-center gap-3 transition-colors"
        >
          <span>Browse professors</span>
          <span aria-hidden="true">→</span>
        </router-link>

        <router-link
          to="/"
          class="border border-on-primary/30 text-on-primary hover:bg-on-primary/10 px-6 py-3 rounded-full text-xs font-semibold transition-colors"
        >
          Back to home
        </router-link>
      </div>
    </section>
  </div>
</template>

<style scoped>
.courses-stage {
  min-height: 100vh;
}

.diagonal-veil,
.diagonal-curtain {
  position: absolute;
  inset: 0;
  pointer-events: none;
  will-change: clip-path;
}

.diagonal-veil {
  background-color: #7c2d63;
  clip-path: polygon(0% 0%, 0% 0%, 0% 0%);
  animation: diagonalSweep 0.8s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}

.diagonal-curtain {
  background-color: #61204c;
  clip-path: polygon(0% 0%, 0% 0%, 0% 0%);
  animation: diagonalSweep 0.9s cubic-bezier(0.22, 1, 0.36, 1) 0.08s forwards;
}

.courses-content {
  opacity: 0;
  transform: translateY(18px);
  animation: contentReveal 0.6s cubic-bezier(0.22, 1, 0.36, 1) 0.42s forwards;
}

@keyframes diagonalSweep {
  0% {
    clip-path: polygon(0% 0%, 0% 0%, 0% 0%);
  }
  100% {
    clip-path: polygon(0% 0%, 220% 0%, 0% 220%);
  }
}

@keyframes contentReveal {
  0% {
    opacity: 0;
    transform: translateY(18px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .diagonal-veil,
  .diagonal-curtain {
    animation: none;
    clip-path: polygon(0% 0%, 220% 0%, 0% 220%);
  }

  .courses-content {
    animation: none;
    opacity: 1;
    transform: none;
  }
}
</style>
