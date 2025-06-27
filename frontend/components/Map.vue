<template>
  <div id="map" class="map-container"></div>
</template>

<script setup>
import { onMounted, ref, onBeforeUnmount, watch } from 'vue'

const props = defineProps({
  geojsonUrl: {
    type: [String, null],
    required: true
  }
})

let map = null
let L = null
let geojsonLayer = null

// Function to choose an icon based on probability
function getIcon(probability) {
  let iconFile = 'green.png'

  const numProb = parseFloat(probability?.replace('%', '')) || 0

  if (numProb >= 99.5) iconFile = 'red.png'
  else if (numProb >= 90) iconFile = 'orange.png'

  return L.icon({
    iconUrl: `/images/${iconFile}`,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32]
  })
}

onMounted(async () => {
  if (import.meta.client) {
    L = (await import('leaflet')).default

    map = L.map('map').setView([37.7749, -122.4194], 10)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map)

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

watch(() => props.geojsonUrl, (newUrl) => {
  if (newUrl) {
    loadGeoJSON(newUrl)
  }
})

async function loadGeoJSON(url) {
  try {
    const res = await fetch(url)
    const data = await res.json()

    if (geojsonLayer) {
      geojsonLayer.remove()
    }

    geojsonLayer = L.geoJSON(data, {
      pointToLayer: (feature, latlng) => {
        const icon = getIcon(feature.properties?.prediction)
        return L.marker(latlng, { icon })
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
