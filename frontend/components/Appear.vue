<template>
  <div
    ref="element"
    :class="[
      'transition-all duration-700 ease-out',
      isVisible
        ? 'opacity-100 blur-0 scale-100'
        : 'opacity-0 blur-sm scale-95'
    ]"
  >
    <slot />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const element = ref(null)
const isVisible = ref(false)

onMounted(() => {
  const observer = new IntersectionObserver(
    ([entry]) => {
      if (entry.isIntersecting) {
        isVisible.value = true
        observer.disconnect()
      }
    },
    { threshold: 0.1 }
  )
  if (element.value) observer.observe(element.value)
})
</script>
