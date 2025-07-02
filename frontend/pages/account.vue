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

    <div class="max-w-8xl mx-auto mt-12">
      <h2 class="text-2xl font-medium mb-4 text-green-950 text-center">Past Results</h2>

      <div v-if="loadingUploads" class="text-center text-gray-500">Loading past results...</div>
      <div v-else-if="pastUploads.length === 0" class="text-center text-gray-500">No uploads found.</div>

      <div v-else class="flex flex-row flex-wrap justify-center items-center gap-6">
        <PastResultsCard
          v-for="upload in pastUploads"
          :key="upload.id"
          :upload="upload"
          @see-results="handleSeeResults"
        />
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
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load data.'
  } finally {
    loading.value = false
    loadingUploads.value = false
  }
})

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
