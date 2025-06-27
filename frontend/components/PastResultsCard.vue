<template>
  <div class="bg-white rounded-2xl shadow-md p-6 w-full max-w-2xs">
    <h2 class="text-xl font-semibold text-green-950 mb-2">{{ upload.entryName }}</h2>
    <p class="text-md text-green-950 mb-1"><span class="font-semibold">Disease:</span> {{ upload.disease }}</p>
    <p class="text-md text-green-950 mb-4"><span class="font-semibold">Date:</span> {{ formattedDate }}</p>

    <div class="flex flex-col gap-2">
      <a
        :href="upload.csvLink"
        download
        class="bg-green-700 text-white px-4 py-2 rounded-xl hover:bg-green-800 text-sm text-center"
      >
        Download CSV
      </a>
      <a
        :href="upload.geojsonLink"
        download
        class="bg-green-700 text-white px-4 py-2 rounded-xl hover:bg-green-800 text-sm text-center"
      >
        Download GeoJSON
      </a>
      <button
        @click="$emit('see-results', upload)"
        class="bg-green-600 text-white px-4 py-2 rounded-xl hover:bg-green-800 text-sm"
      >
        See Results
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  upload: Object
})

const formattedDate = computed(() => {
  if (!props.upload.timestamp?.toDate) return ''
  return props.upload.timestamp.toDate().toLocaleString()
})
</script>
