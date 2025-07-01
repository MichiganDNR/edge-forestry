<template>
  <Appear>
    <h1 class="text-center text-green-950 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl mb-8 mt-12">
      Choose a Specification
    </h1>

    <div class="relative w-full flex justify-center px-4">
      <div class="absolute top-0 w-full flex flex-wrap items-center justify-center gap-4 z-[1100] mt-4">

        <div>
          <input ref="fileInput" type="file" accept="image/*" multiple class="hidden" @change="handleFileUpload" />
          <button type="button" class="bg-green-900 hover:bg-green-800 text-white font-semibold py-3 px-6 rounded-3xl w-56" @click="triggerFileInput">
            Upload Photos
          </button>
        </div>
        <div class="relative w-56">
          <button @click="openDiseaseDropdown = !openDiseaseDropdown" class="w-full bg-green-900 text-white text-center px-6 py-3 rounded-3xl font-semibold hover:bg-green-700 transition flex items-center justify-between">
            {{ selectedDiseaseLabel }}
            <svg class="ml-2 w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div v-if="openDiseaseDropdown" class="absolute left-0 mt-2 w-56 bg-white border border-gray-200 rounded-3xl shadow-lg z-10">
            <button v-for="disease in diseases" :key="disease" @click="selectDiseaseDropdown(disease)" class="block w-full text-left px-6 py-3 rounded-3xl hover:bg-gray-200" :class="{ 'bg-green-900 text-white': selectedDiseaseDropdown === disease }">
              {{ disease }}
            </button>
          </div>
        </div>
        <button type="button" class="bg-green-900 hover:bg-green-800 text-white font-semibold py-3 px-6 rounded-3xl w-56" @click="handleSeeResults">
          See Results
        </button>
        <p class="text-green-950 font-medium" v-if="uploadedFiles.length > 0">
          {{ uploadedFiles.length }} uploaded {{ uploadedFiles.length === 1 ? 'photo' : 'photos' }}.
        </p>
      </div>

      <!-- Map Layer -->
      <ClientOnly>
        <div class="w-full md:w-11/12 lg:w-4/5 2xl:w-1/2 pt-25">
          <Map v-if="showMap" :geojson-url="geojsonLink" />
        </div>
      </ClientOnly>
    </div>

    <!-- Centered Login Button Below Map -->
    <NuxtLink to="/login">
      <div class="flex justify-center mt-8">
        <button
          type="button"
          class="bg-green-700 hover:bg-green-800 text-white border-3 border-green-900 font-semibold py-3 px-6 rounded-3xl w-56"
        >
          Log in for full features
        </button>
      </div>
    </NuxtLink>
  </Appear>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import Appear from '~/components/Appear.vue'
import 'leaflet/dist/leaflet.css'
import Map from '/components/Map.vue'
import axios from 'axios'

const openProbabilityDropdown = ref(false)
const selectedProbabilityDropdown = ref(null)

const openDiseaseDropdown = ref(false)
const selectedDiseaseDropdown = ref(null)

const results = ref([])
const loading = ref(false)
const fileInput = ref(null)
const showMap = ref(true)
const uploadedFiles = ref([])
const apiURL = 'http://localhost:5001'
const geojsonLink = ref(null)


const probabilities = [
  'No condition',
  'Low probability',
  'Medium probability',
  'High probability',
]

const diseases = [
  'Oak Wilt',
  'Hemlock Woolly Adelgid',
  'Beech Bark Disease',
  'Beech Leaf Disease',
]

const selectedProbabilityLabel = computed(() => selectedProbabilityDropdown.value || 'Choose Probability')
const selectedDiseaseLabel = computed(() => selectedDiseaseDropdown.value || 'Choose Disease')

function selectProbabilityDropdown(probability) {
  selectedProbabilityDropdown.value = probability
  openProbabilityDropdown.value = false
}

function selectDiseaseDropdown(disease) {
  if (disease !== 'Oak Wilt') {
    alert('Only Oak Wilt is available at this time.')
    return
  }

  selectedDiseaseDropdown.value = disease
  openDiseaseDropdown.value = false
}

function triggerFileInput() {
  if (fileInput.value) fileInput.value.click()
}

function handleFileUpload(event) {
  const files = Array.from(event.target.files)
  uploadedFiles.value = files
}

function handleClick(e) {
  if (!e.target.closest('.relative')) {
    openProbabilityDropdown.value = false
    openDiseaseDropdown.value = false
  }
}

onMounted(() => window.addEventListener('click', handleClick))
onBeforeUnmount(() => window.removeEventListener('click', handleClick))

async function handleSeeResults() {
  if (uploadedFiles.value.length === 0 || !selectedDiseaseDropdown.value) {
    alert('Please upload a file and select a disease type')
    return
  }

  const formData = new FormData()
  uploadedFiles.value.forEach(file => {
    formData.append('file', file)
  })
  formData.append('disease', selectedDiseaseDropdown.value)

  loading.value = true
  try {
    // Upload to backend and get predictions
    const response = await axios.post(`${apiURL}/upload-images`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })

    // Process backend results
    results.value = Object.values(response.data.results).flat().map(result => ({
      ...result,
      imageUrl: `${apiURL}/images/${result.filename}`,
      coordinates: [result.latitude, result.longitude],
      fileName: result.filename,
      probability: parseFloat(result.prediction) / 100,
    }))

    geojsonLink.value = `${apiURL}/results.geojson`

    // Force map to reload
    showMap.value = false
    setTimeout(() => {
      showMap.value = true
    }, 0)

  } catch (error) {
    console.error('Error during analysis:', error)
    alert('Error processing your file or fetching results. Please try again.')
  } finally {
    loading.value = false
  }
}

</script>
