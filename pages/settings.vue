<template>
  <Appear>
    <h1 class="text-center sm:font-normal leading-[0.9] text-green-950 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl mb-8 mt-12">
      Choose a Specification
    </h1>
    <!-- Controls and Map Container -->
    <div class="relative w-full flex justify-center px-4">
      <!-- Dropdown and Buttons Layer -->
      <div class="absolute top-0 w-full flex flex-wrap items-center justify-center gap-4 z-[1100] mt-4">
        <!-- Upload Button -->
        <div>
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            class="hidden"
            @change="handleFileUpload"
          />
          <button
            type="button"
            class="bg-green-900 hover:bg-green-800 text-white font-semibold py-3 px-6 rounded-3xl w-56"
            @click="triggerFileInput"
          >
            Upload Photos
          </button>
        </div>
         <!-- Dropdown 1: Disease -->
        <div class="relative w-56">
          <button
            @click="openDiseaseDropdown = !openDiseaseDropdown"
            class="w-full bg-green-900 text-white text-center px-6 py-3 rounded-3xl font-semibold hover:bg-green-700 transition flex items-center justify-between"
          >
            {{ selectedDiseaseLabel }}
            <svg class="ml-2 w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div
            v-if="openDiseaseDropdown"
            class="absolute left-0 mt-2 w-56 bg-white border border-gray-200 rounded-3xl shadow-lg z-10"
          >
            <button
              v-for="disease in diseases"
              :key="disease"
              @click="selectDiseaseDropdown(disease)"
              class="block w-full text-left px-6 py-3 rounded-3xl hover:bg-gray-200"
              :class="{ 'bg-green-900 text-white': selectedDiseaseDropdown === disease }"
            >
              {{ disease }}
            </button>
          </div>
        </div>
        <button
          type="button"
          class="bg-green-900 hover:bg-green-800 text-white font-semibold py-3 px-6 rounded-3xl w-56"
          @click="handleSeeResults"
        >
          See Results
        </button>

      </div>
      <!-- Map Layer -->
      <ClientOnly>
        <div class="w-full md:w-11/12 lg:w-4/5 2xl:w-1/2 pt-25">
          <Map v-if="showMap" />
        </div>
      </ClientOnly> 
    </div>
    <!-- Results Section -->
    <div>
      <!-- Title -->
      <h2 class="text-center sm:font-normal leading-[0.9] text-green-950 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl mb-8 mt-12">
        Results
      </h2>

      <div class="flex justify-center items-center gap-4">
        <div v-if="results.length === 0" class="text-green-950 font-medium text-center text-xl mt-4">
          No results to display.
        </div>  
        <!-- Dropdown 2: Probability -->
        <div v-else class="relative w-56">
          <button
            @click="openProbabilityDropdown = !openProbabilityDropdown"
            class="w-full bg-green-900 text-white text-center px-6 py-3 rounded-3xl font-semibold hover:bg-green-700 transition flex items-center justify-between"
          >
            {{ selectedProbabilityLabel }}
            <svg class="ml-2 w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
          </button>
          <div
            v-if="openProbabilityDropdown"
            class="absolute left-0 mt-2 w-56 bg-white border border-gray-200 rounded-3xl shadow-lg z-10"
          >
            <button
              v-for="probability in probabilities"
              :key="probability"
              @click="selectProbabilityDropdown(probability)"
              class="block w-full text-left px-6 py-3 rounded-3xl hover:bg-gray-200"
              :class="{ 'bg-green-900 text-white': selectedProbabilityDropdown === probability }"
            >
              {{ probability }}
            </button>
          </div>
        </div>
      </div>

      <div class="flex justify-center grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 flex-wrap gap-2">
        <ResultCard
          v-for="(result, index) in paginatedResults"
          :key="index"
          :fileName="result.fileName"
          :imageUrl="result.imageUrl"
          :probability="result.probability"
          :coordinates="result.coordinates"
        />
      </div>

      <div v-if="totalPages > 1" class="flex justify-center items-center gap-4 mt-6">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="px-3 py-1 bg-gray-100 rounded hover:bg-gray-200 disabled:opacity-50"
        >
          Prev
        </button>

        <span class="text-sm">Page {{ currentPage }} of {{ totalPages }}</span>

        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 bg-gray-100 rounded hover:bg-gray-200 disabled:opacity-50"
        >
          Next
        </button>
      </div>

    </div>
  </Appear>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import Appear from '~/components/Appear.vue'
import 'leaflet/dist/leaflet.css'
import Map from '/components/Map.vue'
import ResultCard from '~/components/resultCard.vue'

definePageMeta({
  middleware: ['auth'],
  requiresAuth: true
})

const results = ref([])

const openProbabilityDropdown = ref(false)
const selectedProbabilityDropdown = ref(null)

const openDiseaseDropdown = ref(false)
const selectedDiseaseDropdown = ref(null)

const selectedDisease = ref(null)
const fileInput = ref(null)
const uploadedFile = ref(null)
const loading = ref(false)
const result = ref(null)
const showMap = ref(true)

const probabilities = [
  'All',
  'No condition',
  'Low probability',
  'High probability',
  'Has Condition',
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
  currentPage.value = 1
}


function selectDiseaseDropdown(disease) {
  selectedDiseaseDropdown.value = disease
  openDiseaseDropdown.value = false
}

function handleClick(e) {
  if (!e.target.closest('.relative')) {
    openProbabilityDropdown.value = false
    openDiseaseDropdown.value = false
  }
}

function isWithinSelectedProbability(prob) {
  const label = selectedProbabilityDropdown.value

  if (!label || label === 'All') return true

  switch (label) {
    case 'No Condition':
      return prob < 0.70
    case 'Low Probability':
      return prob >= 0.70 && prob < 0.90
    case 'High Probability':
      return prob >= 0.90 && prob < 0.995
    case 'Has Condition':
      return prob >= 0.995
    default:
      return true
  }
}

async function handleSeeResults() {
  if (!uploadedFile.value || !selectedDiseaseDropdown.value) {
    alert('Please upload a file and select a disease type.')
    return
  }
  const formData = new FormData()
  formData.append('file', uploadedFile.value)
  formData.append('disease', selectedDiseaseDropdown.value)

  loading.value = true

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData
    })
    const data = await response.json()

    results.value = data.results
    currentPage.value = 1
  } catch (err) {
    console.error('Failed to analyze file:', err)
    alert('Error processing your file. Please try again.')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
window.addEventListener('click', handleClick)

results.value = [

  ]
  })

const currentPage = ref(1)
const itemsPerPage = 28

const totalPages = computed(() => {
  return Math.ceil(results.value.length / itemsPerPage)
})

const paginatedResults = computed(() => {
  const filtered = results.value.filter(result =>
    isWithinSelectedProbability(result.probability)
  )

  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filtered.slice(start, end)
})

onBeforeUnmount(() => window.removeEventListener('click', handleClick))

function triggerFileInput() {
  if (fileInput.value) fileInput.value.click()
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/jpg']

  if (file && allowedTypes.includes(file.type)) {
    console.log('Accepted image file:', file)
    uploadedFile.value = file
  } else {
    console.warn('Rejected file:', file?.name)
    alert('Only JPEG, JPG, PNG, or GIF files are allowed.')
    uploadedFile.value = null
  }
}

watch(selectedDisease, () => {
  if (fileInput.value) fileInput.value.value = ''
  selectedProbabilityDropdown.value = null
  showMap.value = false
  setTimeout(() => {
    showMap.value = true
  }, 0)
})


</script>

