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
            class="w-full bg-green-900 text-white px-6 py-3 rounded-3xl font-semibold hover:bg-green-700 transition flex items-center justify-between"
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
        <!-- Dropdown 2: Probability -->
        <div class="relative w-56">
          <button
            @click="openProbabilityDropdown = !openProbabilityDropdown"
            class="w-full bg-green-900 text-white px-6 py-3 rounded-3xl font-semibold hover:bg-green-700 transition flex items-center justify-between"
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
      <!-- Map Layer -->
      <ClientOnly>
        <div class="w-full md:w-11/12 lg:w-4/5 2xl:w-1/2 pt-25">
          <Map v-if="showMap" />
        </div>
      </ClientOnly>
      
    </div>
    <!-- Centered Login Button Below Map -->
    <div class="flex justify-center mt-8">
      <button
        type="button"
        class="bg-green-700 hover:bg-green-800 text-white border-3 border-green-900 font-semibold py-3 px-6 rounded-3xl w-56"
      >
        Log in to view results
      </button>
    </div>
  </Appear>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import Appear from '~/components/Appear.vue'
import 'leaflet/dist/leaflet.css'
import Map from '/components/Map.vue'

const openProbabilityDropdown = ref(false)
const selectedProbabilityDropdown = ref(null)

const openDiseaseDropdown = ref(false)
const selectedDiseaseDropdown = ref(null)

const selectedDisease = ref(null)
const fileInput = ref(null)
const showMap = ref(true)

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
  selectedDiseaseDropdown.value = disease
  openDiseaseDropdown.value = false
}

function handleClick(e) {
  if (!e.target.closest('.relative')) {
    openProbabilityDropdown.value = false
    openDiseaseDropdown.value = false
  }
}

onMounted(() => window.addEventListener('click', handleClick))
onBeforeUnmount(() => window.removeEventListener('click', handleClick))

function triggerFileInput() {
  if (fileInput.value) fileInput.value.click()
}

const handleFileUpload = (event) => {
  const file = event.target.files[0]
  if (file) console.log('Selected file:', file)
}

function toggleDisease(disease) {
  selectedDisease.value = selectedDisease.value === disease ? null : disease
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

