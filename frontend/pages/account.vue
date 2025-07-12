<template>
  <Appear>
    <h1 class="text-center sm:font-normal leading-[0.9] text-green-950 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl mb-8 mt-12">
      Account
    </h1>

    <h2 class="text-2xl font-medium text-green-950 text-center mt-10">
      Profile Information
    </h2>
    <div class="max-w-xl mx-auto mt-4 bg-white p-6 rounded-xl shadow">
      <div v-if="loading" class="text-center text-gray-500">Loading...</div>
      <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
      <div v-else class="space-y-4 text-lg text-green-950">
        <div><span class="font-semibold">Email:</span> {{ profileData.email }}</div>
        <div><span class="font-semibold">Membership:</span> {{ profileData.membership }}</div>
        <div><span class="font-semibold">Credits:</span> {{ profileData.credit }}</div>
        <button @click="handleLogout" class="bg-green-700 rounded-2xl w-1/4 text-white hover:bg-green-800 py-2">
          Log Out
        </button>
      </div>
    </div>

    <div class="max-w-8xl mx-auto mt-12 px-4">
      <h2 class="text-2xl font-medium mb-4 text-green-950 text-center">Past Results</h2>

      <div v-if="loadingUploads" class="text-center text-gray-500">Loading past results...</div>
      <div v-else-if="pastUploads.length === 0" class="text-center text-gray-500">No uploads found.</div>

      <div v-else>
        <!-- Sorting Dropdown -->
        <div class="text-left mb-4 ml-50">
          <label class="text-green-950 mr-2 font-medium">Sort by:</label>
          <select
            v-model="sortOption"
            @change="applySortOption"
            class="border border-gray-300 rounded-md px-2 py-1 text-sm"
          >
            <option value="nameAsc">Entry Name (A-Z)</option>
            <option value="nameDesc">Entry Name (Z-A)</option>
            <option value="dateDesc">Newest First</option>
            <option value="dateAsc">Oldest First</option>
          </select>
        </div>

        <!-- Results Table -->
        <div class="flex justify-center overflow-x-auto">
          <table class="min-w-3/4 border-collapse border border-gray-300 rounded-lg overflow-hidden">
            <thead class="bg-gray-100">
              <tr>
                <th class="border border-gray-300 px-4 py-2 text-left">Entry Name</th>
                <th class="border border-gray-300 px-4 py-2 text-left">Disease</th>
                <th class="border border-gray-300 px-4 py-2 text-left">Date</th>
                <th class="border border-gray-300 px-4 py-2 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              <PastResultsCard
                v-for="upload in paginatedUploads"
                :key="upload.id"
                :upload="upload"
                @see-results="handleSeeResults"
              />
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="flex justify-center mt-4 space-x-2">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-1 rounded-md"
            :class="currentPage === 1 ? 'bg-gray-200 text-gray-500' : 'bg-green-700 text-white hover:bg-green-800'"
          >
            Previous
          </button>
          <button
            v-for="page in totalPages"
            :key="page"
            @click="changePage(page)"
            class="px-3 py-1 rounded-md"
            :class="page === currentPage ? 'bg-green-800 text-white' : 'bg-green-700 text-white hover:bg-green-800'"
          >
            {{ page }}
          </button>
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-1 rounded-md"
            :class="currentPage === totalPages ? 'bg-gray-200 text-gray-500' : 'bg-green-700 text-white hover:bg-green-800'"
          >
            Next
          </button>
        </div>
      </div>
    </div>
  </Appear>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import Appear from '@/components/Appear.vue'
import PastResultsCard from '@/components/PastResultsCard.vue'
import { useUserStore } from '@/stores/user'
import { doc, getDoc, collection, getDocs } from 'firebase/firestore'
import { signOut } from 'firebase/auth'

const { $auth, $db } = useNuxtApp()
const userStore = useUserStore()
const router = useRouter()

const profileData = ref({ email: '', credit: 0, membership: 'Free' })
const pastUploads = ref([])
const loading = ref(true)
const loadingUploads = ref(true)
const error = ref('')

// Sort state
const sortOption = ref('dateDesc') // default to newest first

// Pagination
const currentPage = ref(1)
const itemsPerPage = 25

onMounted(async () => {
  try {
    const user = $auth.currentUser
    if (!user) throw new Error('Not logged in')

    // Profile Info
    const userDocRef = doc($db, 'users', user.uid)
    const userSnap = await getDoc(userDocRef)
    if (userSnap.exists()) {
      const data = userSnap.data()
      profileData.value = {
        email: data.email,
        credit: data.credit,
        membership: data.membership || 'Free',
      }
    }

    // Past Uploads
    const uploadsSnap = await getDocs(collection($db, 'users', user.uid, 'uploads'))
    pastUploads.value = uploadsSnap.docs.map(doc => ({ id: doc.id, ...doc.data() }))

    // Convert Firestore Timestamp to JS Date
    pastUploads.value.forEach(upload => {
      if (upload.timestamp && typeof upload.timestamp.toDate === 'function') {
        upload.timestamp = upload.timestamp.toDate()
      } else if (!(upload.timestamp instanceof Date)) {
        upload.timestamp = null
      }
    })
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load data.'
  } finally {
    loading.value = false
    loadingUploads.value = false
  }
})

const sortedUploads = computed(() => {
  const uploadsToSort = [...pastUploads.value]
  switch (sortOption.value) {
    case 'nameAsc':
      return uploadsToSort.sort((a, b) => a.entryName?.localeCompare(b.entryName))
    case 'nameDesc':
      return uploadsToSort.sort((a, b) => b.entryName?.localeCompare(a.entryName))
    case 'dateAsc':
      return uploadsToSort.sort((a, b) => {
        const tA = a.timestamp ? a.timestamp.getTime() : 0
        const tB = b.timestamp ? b.timestamp.getTime() : 0
        return tA - tB
      })
    case 'dateDesc':
    default:
      return uploadsToSort.sort((a, b) => {
        const tA = a.timestamp ? a.timestamp.getTime() : 0
        const tB = b.timestamp ? b.timestamp.getTime() : 0
        return tB - tA
      })
  }
})

const paginatedUploads = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sortedUploads.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() => Math.ceil(sortedUploads.value.length / itemsPerPage))

const changePage = (page) => {
  if (page >= 1 && page <= totalPages.value) currentPage.value = page
}

const applySortOption = () => {
  currentPage.value = 1 // Reset to page 1 when sorting changes
}

const handleLogout = async () => {
  try {
    await signOut($auth)
    userStore.logout()
    router.push('/')
  } catch (err) {
    error.value = 'Failed to log out.'
  }
}

const handleSeeResults = (upload) => {
  router.push({
    name: 'results',
    query: {
      id: upload.id,
      uid: $auth.currentUser.uid,
      fromHistory: 'true'
    }
  })
}
</script>
