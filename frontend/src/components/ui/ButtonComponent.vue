<template>
  <button
    :class="buttonClass"
    :style="buttonStyle"
    :type="resolvedType"
    :form="form"
    :disabled="disabled || isLoading"
    :aria-busy="isLoading ? 'true' : 'false'"
    :aria-live="isLoading ? 'polite' : 'off'"
  >
  <div class="button-content">
    <div class="loader" :class="{ active: showLoader }"></div>
    <span class="label" :class="{ hidden: showLoader }">
      {{ label }}
    </span>
  </div>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  backgroundColor: { type: String, default: null },
  variant: { type: Number, default: 1 },
  label: { type: String, default: '' },
  isLoading: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  type: { type: String, default: 'button' },
  form: { type: String, default: null },
})

const resolvedType = computed(() => props.type || 'button')

const buttonClass = computed(() => {
  if (props.variant === 3) return 'outline'
  if (props.variant === 2) return 'secondary'
  return 'main'
})

const buttonStyle = computed(() => {
  if (props.disabled) {
    return { backgroundColor: 'var(--color-light-gray)' }
  }
  if (props.variant === 1) {
    return { backgroundColor: props.backgroundColor || 'var(--color-main)' }
  }
  if (props.variant === 3) {
    return { backgroundColor: props.backgroundColor || 'var(--color-white)' }
  }
  return undefined
})

const showLoader = computed(() => props.variant === 1 && props.isLoading)
</script>

<style scoped>
.loader {
  height: 10px;
  aspect-ratio: 5;
  -webkit-mask: linear-gradient(90deg,#0000 ,#ffffff 20% 80%,#0000);
  background: radial-gradient(closest-side at 37.5% 50%,#ffffff 94%,#0000) 0/calc(80%/3) 100%;
  animation: l48 .75s infinite ease;
}
@keyframes l48 {
  100% {background-position: 36.36%}
}
.main{
    font-family: 'Jost';
    font-size: 16px;
    cursor: pointer;
    background-color: var(--color-main);
    border: none;
    height: 50px;
    padding: 20px 50px;
    border-radius: 32px;
    color: var(--color-white);
    font-weight: 500;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.main[disabled] {
    cursor: not-allowed;
}

/* .secondary{
    font-size: 12px;
    cursor: pointer;
    background-color: var(--color-gray);
    border: none;
    height: 40px;
    padding: 10px 20px;
    border-radius: 7px;
    color: var(--color-black);
    font-weight: 900;
    width: 100%;
}
.secondary:hover{
    background-color: var(--color-gray-dark)
} */

.outline{
    font-family: 'Jost';
    font-size: 16px;
    cursor: pointer;
    background-color: var(--color-white);
    border: 1px dashed var(--color-main);
    height: 50px;
    padding: 20px 50px;
    border-radius: 32px;
    color: var(--color-black);
    font-weight: 600;
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.button-content {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.loader {
  position: absolute;
  opacity: 0;
  transition: opacity 0.1s ease;
}

.loader.active {
  opacity: 1;
}

.label {
  transition: opacity 0.1s ease;
}

.label.hidden {
  opacity: 0;
}
</style>