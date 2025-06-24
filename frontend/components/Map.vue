<template>
  <div id="map" class="map-container"></div>
</template>

<script setup>
import { onMounted, ref, onBeforeUnmount } from 'vue'

let map = null
let L = null

onMounted(async () => {
  if (import.meta.client) { // Only run on client side
    // Dynamically import Leaflet to avoid SSR errors
    L = (await import('leaflet')).default

    map = L.map('map').setView([37.7749, -122.4194], 10)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map)

    L.marker([37.7749, -122.4194]).addTo(map)
      .bindPopup('Sample Tree')
      .openPopup()
  }
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 500px;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
</style>

