<template>
  <Appear>
    <h1 class="text-center text-green-950 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl mb-8 mt-12">
      Choose a Specification
    </h1>

    <div class="relative w-full flex justify-center px-4">
      <div class="absolute top-0 w-full flex flex-wrap items-center justify-center gap-4 z-[1100] mt-4">
        <input v-model="entryName" placeholder="Enter Entry Name" class="w-56 px-4 py-2 rounded-3xl border border-gray-300" />
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

      <ClientOnly>
        <div class="w-full md:w-11/12 lg:w-4/5 2xl:w-1/2 pt-25">
          <Map v-if="showMap" :geojson-url="geojsonLink"/>
        </div>
      </ClientOnly>
    </div>

    <div>
      <!-- 
      <h2 v-if="isPastUpload" class="text-center sm:font-normal leading-[0.9] text-green-950 text-xl sm:text-2xl md:text-3xl lg:text-4xl xl:text-5xl 2xl:text-6xl mb-8 mt-12">
        Viewing saved results from {{ entryTitle }}.
      </h2> -->

      <h2 class="text-center sm:font-normal leading-[0.9] text-green-950 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl mb-8 mt-12">
        Results
      </h2>

      
      <div class="flex justify-center items-start gap-6 mb-6">
        <div class="flex flex-col gap-2">
          <a v-if="csvLink" :href="csvLink" class="underline text-green-800 font-semibold" @click="handleDownload" download>
            Download CSV
          </a>
          <a v-if="geojsonLink" :href="geojsonLink" class="underline text-green-800 font-semibold" @click="handleDownload" download>
            Download GeoJSON
          </a>
        </div>

        <div class="relative w-56">
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

      <div v-if="paginatedResults.length === 0" class="text-green-950 font-medium text-center text-xl mt-20 mb-35">
        No results to display.
      </div>

      <div v-else class="flex justify-center flex-wrap gap-4 mt-6">
        <ResultCard
          v-for="(result, index) in paginatedResults"
          :key="index"
          :fileName="result.fileName"
          :imageUrl="result.imageUrl"
          :probability="result.probability"
          :coordinates="result.coordinates"
          @feedback="handleFeedback"
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
import { onBeforeRouteLeave } from 'vue-router'
import { useNuxtApp } from '#app'
import Appear from '~/components/Appear.vue'
import 'leaflet/dist/leaflet.css'
import Map from '/components/Map.vue'
import ResultCard from '~/components/resultCard.vue'
import axios from 'axios'
import { getStorage, ref as storageRef, uploadBytes, getDownloadURL, listAll } from 'firebase/storage'
import { getAuth } from 'firebase/auth'
import { collection, addDoc, serverTimestamp } from 'firebase/firestore'
import { useUserStore } from '@/stores/user'
import { doc, getDoc } from 'firebase/firestore'

const userStore = useUserStore()
const user = userStore.user  // reactive user object

if (user) {
  const uid = user.uid
  // use uid in Firestore paths or Storage uploads
}

// Grab Nuxt app context to get db instance
const nuxtApp = useNuxtApp()
const db = nuxtApp.$db

const fileInput = ref(null)
const uploadedFiles = ref([])
const uploads = ref([])
const entryName = ref("")
const entryTitle = ref('')
const loading = ref(false)
const results = ref([])
const showMap = ref(true)
const currentPage = ref(1)
const itemsPerPage = 28
const apiURL = 'http://localhost:5001'
const csvLink= ref(null)
const geojsonLink = ref(null)
const route = useRoute()
const isPastUpload = route.query.fromHistory === 'true'
const uploadId = route.query.id
const uid = route.query.uid


const openProbabilityDropdown = ref(false)
const selectedProbabilityDropdown = ref(null)
const openDiseaseDropdown = ref(false)
const selectedDiseaseDropdown = ref(null)
const selectedDisease = ref(null)

const probabilities = ['All','No Condition: <70%','Possibility: 70-90%','High Chance: 90-99.5%','Has Condition: >99.5%']
const diseases = ['Oak Wilt','Hemlock Woolly Adelgid','Beech Bark Disease','Beech Leaf Disease']

const selectedProbabilityLabel = computed(() => selectedProbabilityDropdown.value || 'Choose Probability')
const selectedDiseaseLabel = computed(() => selectedDiseaseDropdown.value || 'Choose Disease')

const totalPages = computed(() => Math.ceil(results.value.length / itemsPerPage))

const paginatedResults = computed(() => {
  const filtered = results.value.filter(result => isWithinSelectedProbability(result.probability))
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filtered.slice(start, end)
})

watch(selectedDisease, () => {
  if (fileInput.value) fileInput.value.value = ''
  selectedProbabilityDropdown.value = null
  showMap.value = false
  setTimeout(() => { showMap.value = true }, 0)
})

onMounted(() => {
  window.addEventListener('click', handleClick)
  window.addEventListener('beforeunload', handleBeforeUnload)
  results.value = []

  if (isPastUpload) {
    loadPastUpload()
  }
})


onBeforeUnmount(() => window.removeEventListener('click', handleClick))

function handleClick(e) {
  if (!e.target.closest('.relative')) {
    openProbabilityDropdown.value = false
    openDiseaseDropdown.value = false
  }
}

function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileUpload(event) {
  const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/jpg']
  const files = Array.from(event.target.files)
  const validFiles = files.filter(file => allowedTypes.includes(file.type))

  if (validFiles.length === 0) {
    alert('Only JPEG, JPG, PNG, or GIF files are allowed.')
    uploadedFiles.value = []
  } else {
    uploadedFiles.value = validFiles
  }
}


function selectProbabilityDropdown(probability) {
  selectedProbabilityDropdown.value = probability
  openProbabilityDropdown.value = false
  currentPage.value = 1
}

function selectDiseaseDropdown(disease) {
  if (disease !== 'Oak Wilt') {
    alert('Only Oak Wilt is available at this time.')
    return
  }

  selectedDiseaseDropdown.value = disease
  openDiseaseDropdown.value = false
}

function isWithinSelectedProbability(prob) {
  const label = selectedProbabilityDropdown.value
  if (!label || label === 'All') return true
  switch (label) {
    case 'No Condition: <70%': return prob < 0.70
    case 'Possibility: 70-90%': return prob >= 0.70 && prob < 0.90
    case 'High Chance: 90-99.5%': return prob >= 0.90 && prob < 0.995
    case 'Has Condition: >99.5%': return prob >= 0.995
    default: return true
  }
}

onMounted(() => {
  window.addEventListener('beforeunload', handleBeforeUnload)
})

onBeforeUnmount(() => {
  window.removeEventListener('beforeunload', handleBeforeUnload)
})

let isDownloading = false

function handleBeforeUnload(event) {
  if (isDownloading) return 

  if (results.value.length > 0) {
    event.preventDefault()
    event.returnValue = ''
  }
}

onBeforeRouteLeave((to, from, next) => {
  if (results.value.length > 0) {
    const answer = window.confirm('Are you sure you want to leave this page? Your results will be lost on this page.')
    if (answer) {
      next()
    } else {
      next(false)
    }
  } else {
    next()
  }
})

async function handleSeeResults() {
  if (uploadedFiles.value == 0|| !selectedDiseaseDropdown.value || !entryName.value) {
    alert('Please upload a file, select a disease type, and enter an entry name.')
    return
  }

  const confirmed = confirm('Are you sure you want to analyze and view results for this entry?')
  if (!confirmed) return

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

    const [csvBlob, geojsonBlob] = await Promise.all([
    axios.get(`${apiURL}/results.csv`, { responseType: 'blob' }),
    axios.get(`${apiURL}/results.geojson`, { responseType: 'blob' })
    ])


    csvLink.value = `${apiURL}/results.csv`
    geojsonLink.value = `${apiURL}/results.geojson`
    currentPage.value = 1

    // Upload metadata and image URLs to Firestore
    await uploadFiles(
    uploadedFiles.value,
    entryName.value,
    selectedDiseaseDropdown.value,
    results.value,
    csvBlob.data,
    geojsonBlob.data
  )

    alert('Entry saved successfully!')
    showMap.value = false
    setTimeout(() => {
      showMap.value = true
    }, 0)

  } catch (err) {
    console.error('Error during analysis:', err)
    alert('Error processing your file or saving the entry.')
  } finally {
    loading.value = false
  }
}

async function loadPastUpload() {
  try {
    if (!uid || !uploadId) throw new Error('Missing upload info.')

    const uploadDocRef = doc(db, 'users', uid, 'uploads', uploadId)
    const uploadSnap = await getDoc(uploadDocRef)

    if (!uploadSnap.exists()) throw new Error('Upload not found.')

    const data = uploadSnap.data()

    entryTitle.value = data.entryName
    selectedDiseaseDropdown.value = data.disease
    results.value = data.predictions || []

    csvLink.value = data.csvLink ?? null
    geojsonLink.value = data.geojsonLink ?? null

    showMap.value = false
    setTimeout(() => {
      showMap.value = true
    }, 0)
  } catch (err) {
    console.error('Failed to load past upload:', err)
    alert('Failed to load saved entry.')
  }
}

function handleDownload() {
  isDownloading = true
  setTimeout(() => {
    isDownloading = false
  }, 1000) 
}

async function handleFeedback(fileName, isCorrect) {
  try {
    await axios.post(`${apiURL}/submit-feedback`, {
      filename: fileName,
      isCorrect: isCorrect
    })
    alert('Feedback submitted successfully!')
  } catch (err) {
    console.error('Error submitting feedback:', err)
    alert('Failed to send feedback.')
  }
}


async function uploadFiles(uploadedFiles, entryName, disease, backendResults, csvBlob, geojsonBlob) {
  loading.value = true
  try {
    const user = getAuth().currentUser
    if (!user) throw new Error('User not logged in')

    const storage = getStorage()
    const timestamp = Date.now()

    const fileUrls = await Promise.all(
      uploadedFiles.map(async (file) => {
        const fileRef = storageRef(storage, `uploads/${user.uid}/${timestamp}_${file.name}`)
        await uploadBytes(fileRef, file)
        return await getDownloadURL(fileRef)
      })
    )

    const csvRef = storageRef(storage, `uploads/${user.uid}/${timestamp}_results.csv`)
    await uploadBytes(csvRef, csvBlob)
    const csvDownloadUrl = await getDownloadURL(csvRef)

    const geojsonRef = storageRef(storage, `uploads/${user.uid}/${timestamp}_results.geojson`)
    await uploadBytes(geojsonRef, geojsonBlob)
    const geojsonDownloadUrl = await getDownloadURL(geojsonRef)

    const docRef = await addDoc(collection(db, 'users', user.uid, 'uploads'), {
      entryName,
      disease,
      timestamp: serverTimestamp(),
      csvLink: csvDownloadUrl,
      geojsonLink: geojsonDownloadUrl,
      predictions: backendResults.map((res, i) => ({
        ...res,
        imageUrl: fileUrls[i]
      }))
    })

    uploads.value.unshift({
      id: docRef.id,
      entryName,
      disease,
      timestamp: new Date(),
      predictions: backendResults
    })

  } catch (e) {
    console.error(e)
  } finally {
    loading.value = false
  }
}

</script>