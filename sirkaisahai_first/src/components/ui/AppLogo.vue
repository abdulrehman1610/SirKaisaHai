<script setup lang="ts">
interface Props {
  size?: 'sm' | 'md' | 'lg';
  showText?: boolean;
  boxed?: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  showText: true,
  boxed: true
});

const boxClasses = {
  sm: 'w-8 h-8 rounded-[10px]',
  md: 'w-9 h-9 rounded-[11px]',
  lg: 'w-10 h-10 rounded-[12px]'
};

const iconClasses = {
  sm: 'w-4 h-4',
  md: 'w-[18px] h-[18px]',
  lg: 'w-5 h-5'
};

const textClasses = {
  sm: 'text-[15px]',
  md: 'text-[17px]',
  lg: 'text-[19px]'
};
</script>

<template>
  <div class="inline-flex items-center gap-2.5 select-none">
    <div
      :class="[
        props.boxed ? `${boxClasses[props.size]} neu-tile flex items-center justify-center` : 'inline-flex items-center',
        'shrink-0 text-primary'
      ]"
    >
      <svg
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        :class="iconClasses[props.size]"
        aria-hidden="true"
      >
        <path
          d="M12 4L22 9L12 14L2 9L12 4Z"
          stroke="currentColor"
          stroke-width="1.75"
          stroke-linejoin="round"
        />
        <path
          d="M6 11.2V16.2C6 18 8.7 19.5 12 19.5C15.3 19.5 18 18 18 16.2V11.2"
          stroke="currentColor"
          stroke-width="1.75"
          stroke-linecap="round"
        />
        <path d="M21 9.5V15" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" />
      </svg>
    </div>

    <span v-if="props.showText" :class="[textClasses[props.size], 'font-bold tracking-tight text-primary']">
      SirKaisaHai
    </span>
  </div>
</template>
