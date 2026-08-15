<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  showText?: boolean;
  textColor?: string;
  variant?: 'default' | 'light';
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  showText: true,
  textColor: 'text-primary',
  variant: 'default'
});

const isLight = computed(() => props.variant === 'light' || props.textColor.includes('text-white'));

const sizeClasses = {
  sm: 'w-7 h-7',
  md: 'w-8 h-8',
  lg: 'w-10 h-10',
  xl: 'w-14 h-14'
};

const textSizeClasses = {
  sm: 'text-base',
  md: 'text-xl',
  lg: 'text-2xl',
  xl: 'text-4xl'
};
</script>

<template>
  <div class="inline-flex items-center gap-2.5 select-none group">
    <!-- Clean Graduation Cap Icon -->
    <div :class="[sizeClasses[props.size], 'shrink-0 relative transition-transform duration-300 group-hover:scale-105']">
      <!-- Light / Dark Background Adaptable SVG -->
      <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-full drop-shadow-sm">
        <template v-if="isLight">
          <!-- Cap Board (Crisp White with Lavender Rim) -->
          <polygon points="32,8 60,22 32,36 4,22" fill="#FFFFFF"/>
          <!-- Cap Base (Bright Purple / White glow) -->
          <path d="M16,28 L16,38 C16,46 48,46 48,38 L48,28" fill="none" stroke="#deb7ff" stroke-width="4" stroke-linecap="round"/>
          <!-- Tassel String (Vivid Cyan/Gold) -->
          <line x1="52" y1="24" x2="56" y2="40" stroke="#00E5FF" stroke-width="3" stroke-linecap="round"/>
          <!-- Tassel Ball -->
          <circle cx="56" cy="42" r="3" fill="#00E5FF"/>
          <!-- Star in contrast Deep Plum -->
          <path d="M32,24 L33.8,29 L39,29.5 L35,33 L36.2,38 L32,35.5 L27.8,38 L29,33 L25,29.5 L30.2,29 Z" fill="#501243"/>
        </template>
        <template v-else>
          <!-- Cap Board (Deep Plum) -->
          <polygon points="32,8 60,22 32,36 4,22" fill="#501243"/>
          <!-- Cap Base (Purple Bowl) -->
          <path d="M16,28 L16,38 C16,46 48,46 48,38 L48,28" fill="none" stroke="#6B2FA0" stroke-width="3.5" stroke-linecap="round"/>
          <!-- Tassel String -->
          <line x1="52" y1="24" x2="56" y2="40" stroke="#7C41B1" stroke-width="2.5" stroke-linecap="round"/>
          <!-- Tassel Ball -->
          <circle cx="56" cy="42" r="2.5" fill="#7C41B1"/>
          <!-- Star (White Rating Star) -->
          <path d="M32,24 L33.8,29 L39,29.5 L35,33 L36.2,38 L32,35.5 L27.8,38 L29,33 L25,29.5 L30.2,29 Z" fill="white" opacity="0.95"/>
        </template>
      </svg>
    </div>

    <!-- Brand Typography -->
    <span
      v-if="props.showText"
      :class="[
        textSizeClasses[props.size],
        props.textColor,
        'font-display-lg font-black tracking-tight'
      ]"
    >
      SirKaisaHai
    </span>
  </div>
</template>
