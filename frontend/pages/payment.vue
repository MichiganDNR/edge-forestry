<template>
  <Appear>
  <div class="min-h-screen flex flex-col items-center justify-center text-center px-4">
    <div class="max-w-md">
      <div class="text-green-700 mb-6">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-24 w-24 mx-auto" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h1 class="text-4xl font-bold text-green-950 mb-4">Page Under Construction</h1>
      <p class="text-lg text-green-950 mb-6">We're working on something awesome. Check back soon!</p>
      <NuxtLink
        to="/"
        class="inline-block bg-green-700 text-white px-6 py-3 rounded-lg shadow hover:bg-green-800 transition"
      >
        Go Back Home
      </NuxtLink>
    </div>
  </div>
  </Appear>
</template>

<script>
import Appear from '/components/Appear.vue'

</script>
