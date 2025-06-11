<script setup>
const props = defineProps({
  label: {
    type: String,
    default: 'Click me',
    required: true,
  },
  href: {
    type: String,
    default: null,
  },
  external: {
    type: Boolean,
    default: false,
  },
  scrollTo: {
    type: String,
    default: null,
  },
  mobileOpen: {
    type: Boolean,
    default: false,
  }
})

const handleScroll = () => {
  const el = document.getElementById(props.scrollTo)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}
</script>

<template>
  <!-- External Link -->
  <a
    v-if="href && external"
    :href="href"
    target="_blank"
    rel="noopener noreferrer"
    class="bg-green-700 hover:bg-green-800 text-white font-semibold py-5 px-8 md:py-3
           rounded-full shadow-md transition-all duration-300 text-lg text-center inline-block"
  >
    {{ label }}
  </a>

  <!-- Internal Scroll Link -->
  <button
    v-else-if="scrollTo"
    @click="handleScroll"
    class="bg-green-700 hover:bg-green-800 text-white font-semibold py-5 px-8 md:py-3
           rounded-full shadow-md transition-all duration-300 text-lg"
  >
    {{ label }}
  </button>

  <!-- Regular Button -->
  <button
    v-else
    class="bg-green-700 hover:bg-green-800 text-white font-semibold py-5 px-8 md:py-3
           rounded-full shadow-md transition-all duration-300 text-lg"
  >
    {{ label }}
  </button>
</template>

