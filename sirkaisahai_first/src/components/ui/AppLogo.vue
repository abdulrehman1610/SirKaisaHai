<script setup lang="ts">
interface Props {
  size?: 'sm' | 'md' | 'lg' | 'xl';
  variant?: 'default' | 'light';
  showSubtag?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  variant: 'default',
  showSubtag: false
});

const textSizes = {
  sm: 'text-base',
  md: 'text-lg',
  lg: 'text-2xl',
  xl: 'text-4xl md:text-5xl'
};
</script>

<template>
  <div class="inline-flex items-center gap-3.5 select-none">
    <span class="relative inline-block">
      <span
        :class="[
          textSizes[props.size],
          props.variant === 'light' ? 'text-on-primary' : 'text-primary-dark',
          'font-display font-extrabold tracking-tight leading-none block'
        ]"
      >
        SirKaisaHai
      </span>
      <span
        v-if="props.variant === 'default' && props.size !== 'xl'"
        class="block h-[2px] w-7 bg-primary mt-1 rounded-full"
      ></span>
    </span>

    <template v-if="props.showSubtag">
      <span class="h-6 w-px bg-border-soft hidden sm:block"></span>
      <span class="hidden sm:flex flex-col leading-[1.2] font-mono text-[8.5px] uppercase tracking-[0.12em] text-ink-subtle">
        <span>Superior University</span>
        <span>Student Edition</span>
      </span>
    </template>
  </div>
</template>
