<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const props = defineProps({
  label: {
    type: String,
    default: 'Buy Now',
    required: true,
  },
})

const goToPage = () => {
  router.push('/payment')
}
</script>

<template>
  <component
    @click="goToPage"
    class="bg-green-700 hover:bg-green-800 text-white font-semibold py-5 px-8 md:py-3
           rounded-full shadow-md transition-all duration-300 text-lg  hover:scale-105 transform"
  >
    {{ label }}
  </component>
</template>
