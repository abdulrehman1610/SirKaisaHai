<script setup lang="ts">
import { ref } from 'vue';
import AppLogo from '../ui/AppLogo.vue';

const currentYear = new Date().getFullYear();
const isHovered = ref(false);
</script>

<template>
  <footer class="modern-footer mt-12 md:mt-24 relative overflow-hidden">
    <!-- Ambient Background Effects -->
    <div class="absolute inset-0 bg-primary overflow-hidden -z-10">
      <div class="absolute -top-[50%] -left-[10%] w-[70%] h-[150%] bg-gradient-to-br from-[#6B2FA0]/40 to-transparent rounded-[100%] blur-[120px] mix-blend-overlay animate-pulse-slow"></div>
      <div class="absolute -bottom-[50%] -right-[10%] w-[60%] h-[150%] bg-gradient-to-tl from-[#2D6FD1]/30 to-transparent rounded-[100%] blur-[100px] mix-blend-overlay"></div>
    </div>

    <div class="max-w-container-max mx-auto px-4 md:px-gutter pt-10 md:pt-20 pb-6 md:pb-8 relative z-10">
      <!-- Floating Glass Card for Main Content -->
      <div class="glass-footer-card rounded-2xl md:rounded-[2rem] p-5 md:p-12 shadow-2xl-ambient border border-white/10 relative overflow-hidden mb-8 md:mb-12 transform transition-transform duration-700 hover:-translate-y-2"
           @mouseenter="isHovered = true" 
           @mouseleave="isHovered = false">
        
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 md:gap-12 relative z-10">
          
          <!-- Brand Column -->
          <div class="md:col-span-5 flex flex-col justify-between">
            <div>
              <div class="mb-4">
                <AppLogo size="lg" textColor="text-white" />
              </div>
              <p class="font-body-lg text-white/70 leading-relaxed max-w-sm font-medium">
                Elevating transparency at Superior University. 100% anonymous, student-driven insights.
              </p>
            </div>
            
            <div class="mt-4 md:mt-8 flex gap-4">
              <a href="#" class="social-btn">
                <span class="material-symbols-outlined">link</span>
              </a>
              <a href="#" class="social-btn">
                <span class="material-symbols-outlined">mail</span>
              </a>
            </div>
          </div>

          <!-- Links Grid -->
          <div class="md:col-span-7 grid grid-cols-2 gap-4 md:gap-8">
            <div class="nav-column">
              <h4 class="column-title">Explore</h4>
              <ul class="nav-list">
                <li><router-link to="/search" class="nav-link">Top Professors</router-link></li>
                <li><router-link to="/search" class="nav-link">Course Reviews</router-link></li>
                <li><router-link to="/auth" class="nav-link">Student Verification</router-link></li>
              </ul>
            </div>
            
            <div class="nav-column">
              <h4 class="column-title">Our Promise</h4>
              <ul class="nav-list">
                <li class="flex items-center gap-2 text-white/80"><span class="material-symbols-outlined text-sm text-green-400">shield</span> Zero Tracking</li>
                <li class="flex items-center gap-2 text-white/80"><span class="material-symbols-outlined text-sm text-green-400">lock</span> SHA-256 Hashed</li>
                <li class="flex items-center gap-2 text-white/80"><span class="material-symbols-outlined text-sm text-green-400">gavel</span> Moderated</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Decorative animated line -->
        <div class="absolute bottom-0 left-0 h-1 bg-gradient-to-r from-secondary to-action-blue transition-all duration-1000 ease-in-out"
             :class="isHovered ? 'w-full' : 'w-0'"></div>
      </div>

      <!-- Bottom Bar -->
      <div class="flex flex-col md:flex-row justify-between items-center gap-4 pt-6 border-t border-white/10 font-label-sm text-xs text-white/50 font-medium tracking-wide">
        <p>© {{ currentYear }} SirKaisaHai — Superior University Edition.</p>
        <p class="flex items-center gap-1">
          Built with <span class="material-symbols-outlined text-red-400 text-sm animate-pulse">favorite</span> by students
        </p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.modern-footer {
  border-top-left-radius: 1.5rem;
  border-top-right-radius: 1.5rem;
}

@media (min-width: 768px) {
  .modern-footer {
    border-top-left-radius: 3rem;
    border-top-right-radius: 3rem;
  }
}

.glass-footer-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

.column-title {
  font-family: var(--font-heading);
  font-weight: 800;
  font-size: 1rem;
  color: var(--secondary-fixed);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 1.5rem;
  position: relative;
  display: inline-block;
}

.column-title::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -4px;
  width: 20px;
  height: 2px;
  background: var(--secondary-fixed);
  border-radius: 2px;
}

.nav-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.nav-link {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
  transition: all 0.3s ease;
  position: relative;
  display: inline-flex;
  align-items: center;
}

.nav-link::before {
  content: '→';
  position: absolute;
  left: -20px;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
  color: var(--secondary-fixed);
}

.nav-link:hover {
  color: #FFFFFF;
  transform: translateX(20px);
}

.nav-link:hover::before {
  opacity: 1;
  transform: translateX(0);
}

.social-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  color: white;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.social-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  border-color: var(--secondary-fixed);
  color: var(--secondary-fixed);
}

.animate-pulse-slow {
  animation: pulse 8s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>
