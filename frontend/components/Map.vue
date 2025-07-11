<template>
  <div id="map" class="map-container"></div>
</template>

<script setup>
import { onMounted, onBeforeUnmount, watch } from 'vue'

const props = defineProps({
  geojsonUrl: {
    type: [String, null],
    required: true,
  },
})

let map = null
let L = null
let geojsonLayer = null

// Select marker icon based on probability
function getIcon(probability) {
  const value = parseFloat(probability?.replace('%', '')) || 0
  let iconName = 'green.png'
  if (value >= 99.5) iconName = 'red.png'
  else if (value >= 90) iconName = 'orange.png'

  return L.icon({
    iconUrl: `/images/${iconName}`,
    iconSize: [32, 32],
    iconAnchor: [16, 32],
    popupAnchor: [0, -32],
  })
}

onMounted(async () => {
  if (import.meta.client) {
    L = (await import('leaflet')).default

    map = L.map('map').setView([37.7749, -122.4194], 10)

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors',
    }).addTo(map)

    if (props.geojsonUrl) await loadGeoJSON(props.geojsonUrl)
  }
})

onBeforeUnmount(() => {
  if (map) {
    map.remove()
    map = null
  }
})

watch(
  () => props.geojsonUrl,
  async (newUrl) => {
    if (!map) return
    if (geojsonLayer) {
      geojsonLayer.remove()
      geojsonLayer = null
    }

    if (newUrl) {
      await loadGeoJSON(newUrl)
    } else {
      map.setView([37.7749, -122.4194], 10)
    }
  }
)

async function loadGeoJSON(url) {
  try {
    const res = await fetch(url)
    const data = await res.json()

    if (geojsonLayer) {
      geojsonLayer.remove()
      geojsonLayer = null
    }

    geojsonLayer = L.geoJSON(data, {
      pointToLayer: (feature, latlng) => {
        const icon = getIcon(feature.properties?.prediction)
        return L.marker(latlng, { icon })
      },
      onEachFeature: (feature, layer) => {
        const { classification = 'N/A', prediction = 'N/A' } = feature.properties || {}
        const [lng, lat] = feature.geometry?.coordinates || []

        const probability = parseFloat(prediction?.replace('%', '')) || 0
        let bgClass = 'bg-green-100 text-green-900'
        if (probability >= 99.5) bgClass = 'bg-red-100 text-red-900'
        else if (probability >= 90) bgClass = 'bg-orange-100 text-orange-900'
        else if (probability >= 70) bgClass = 'bg-yellow-100 text-yellow-900'

        const popupContent = `
          <div class="${bgClass} text-sm p-3 rounded shadow-sm leading-snug">
          <strong>Condition: ${classification}</strong><br/>
            There is a <strong>${prediction}</strong> chance of Oak Wilt at<br/>
            the coordinates:<br/><strong>[${lat}, ${lng}]</strong>.
          </div>
        `

        layer.bindPopup(popupContent, {
          className: 'tailwind-popup'
        })
      },
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
  border: 2px solid #f3f4f6; /* light gray border */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
</style>

<style>
/* Optional: override default Leaflet popup style if needed */
.leaflet-popup-content-wrapper.tailwind-popup {
  background: transparent;
  box-shadow: none;
  border: none;
  padding: 0;
  border-radius: 0;
}
.leaflet-popup-content.tailwind-popup {
  margin: 0;
}
</style>

