<template>
  <div
    class="flex items-center justify-center min-h-screen bg-gray-50 px-4"
  >
    <div class="text-center">
      <h1 class="text-green-950 text-5xl font-extrabold mb-4">
        Under Construction
      </h1>
      <p class="text-green-950 text-lg">
        This page is coming soon. Please check back later.
      </p>
      <button
        @click="$router.push('/')"
        class="mt-8 px-6 py-3 bg-green-900 text-white rounded-2xl hover:bg-green-800 transition"
      >
        Go Back Home
      </button>
    </div>
  </div>
</template>
