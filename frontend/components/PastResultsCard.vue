<template>
  <tr class="hover:bg-gray-50">
    <td class="border border-gray-300 px-4 py-2 break-words max-w-xs">
      {{ upload.entryName }}
    </td>
    <td class="border border-gray-300 px-4 py-2 break-words max-w-xs">
      {{ upload.disease }}
    </td>
    <td class="border border-gray-300 px-4 py-2">
      {{ formattedDate }}
    </td>
    <td class="border border-gray-300 px-4 py-2 whitespace-nowrap">
      <a
        :href="upload.csvLink"
        download
        class="bg-green-700 text-white px-3 py-1 rounded-xl hover:bg-green-800 text-xs inline-block mr-2"
      >
        CSV
      </a>
      <a
        :href="upload.geojsonLink"
        download
        class="bg-green-700 text-white px-3 py-1 rounded-xl hover:bg-green-800 text-xs inline-block mr-2"
      >
        GeoJSON
      </a>
      <button
        @click="$emit('see-results', upload)"
        class="bg-green-600 text-white px-3 py-1 rounded-xl hover:bg-green-800 text-xs"
      >
        See Results
      </button>
    </td>
  </tr>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  upload: Object
})

const formattedDate = computed(() => {
  const date = props.upload.timestamp
  return date instanceof Date ? date.toLocaleString() : ''
})
</script>