<script setup>
const props = defineProps({
  label: {
    type: String,
    default: 'Buy Now',
    required: true,
  },
  href: {
    type: String,
    default: null,
  },
})
</script>

<template>
  <component
    :is="href ? 'NuxtLink' : 'button'"
    :to="href"
    class="bg-green-700 hover:bg-green-800 text-white font-semibold py-5 px-8 md:py-3
           rounded-full shadow-md transition-all duration-300 text-lg  hover:scale-105 transform"
  >
    {{ label }}
  </component>
</template>
