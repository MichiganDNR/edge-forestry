<template>
  <div id="map" class="map-container"></div>
</template>

<script setup>
import { onMounted, ref, onBeforeUnmount, watch } from 'vue'

// Props: Accepts a GeoJSON URL from the parent
const props = defineProps({
  geojsonUrl: {
    type: String,
    required: true
  }
})

let map = null
let L = null
let geojsonLayer = null

onMounted(async () => {
  if (import.meta.client) {
    // Dynamically import Leaflet (for SSR safety)
    L = (await import('leaflet')).default

    map = L.map('map').setView([37.7749, -122.4194], 10)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map)

    // Optionally add a sample marker (remove if not needed)
    // L.marker([37.7749, -122.4194]).addTo(map).bindPopup('Sample Tree').openPopup()

    // Load GeoJSON initially if URL exists
    if (props.geojsonUrl) {
      await loadGeoJSON(props.geojsonUrl)
    }
  }
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})

// Watch for GeoJSON URL changes (reactive updates)
watch(() => props.geojsonUrl, (newUrl) => {
  if (newUrl) {
    loadGeoJSON(newUrl)
  }
})

async function loadGeoJSON(url) {
  try {
    const res = await fetch(url)
    const data = await res.json()

    // Remove old layer if needed
    if (geojsonLayer) {
      geojsonLayer.remove()
    }

    geojsonLayer = L.geoJSON(data, {
      pointToLayer: (feature, latlng) => {
        return L.circleMarker(latlng, {
          radius: 6,
          fillColor: '#2f855a',
          color: '#2f855a',
          weight: 1,
          opacity: 1,
          fillOpacity: 0.85
        })
      },
      onEachFeature: (feature, layer) => {
        const props = feature.properties || {}
        layer.bindPopup(`
          <strong>${props.filename || 'Image'}</strong><br/>
          Condition: ${props.classification || 'N/A'}<br/>
          Probability: ${props.prediction ?? 'N/A'}
        `)
      }
    }).addTo(map)

    // Zoom to data
    map.fitBounds(geojsonLayer.getBounds())

  } catch (error) {
    console.error('Error loading GeoJSON:', error)
  }
}
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 500px;
  border-radius: 1rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
</style>
