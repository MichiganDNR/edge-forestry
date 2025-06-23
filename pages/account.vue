<template>
  <Appear>
    <h1
    class="text-center sm:font-normal leading-[0.9] text-green-950 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl mb-8 mt-12"
  >
    Account
    </h1>

    <div class="max-w-xl mx-auto mt-10 bg-white p-6 rounded-xl shadow">
      <h2 class="text-2xl font-medium mb-6 text-green-950 text-center">
        Profile Information
      </h2>

      <div v-if="loading" class="text-center text-gray-500">Loading...</div>
      <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
      <div v-else class="space-y-4 text-lg text-green-950">
        <div>
          <span class="font-semibold text-green-950">Email:</span>
          {{ profileData.email }}
        </div>
        <div>
          <span class="font-semibold text-green-950">Membership:</span>
          {{ profileData.membership }}
        </div>
        <div>
          <span class="font-semibold text-green-950">Credits:</span>
          {{ profileData.credit }}
        </div>
        <button
          @click="handleLogout"
          class="bg-green-700 rounded-2xl w-1/4 text-white hover:bg-green-800 py-2"
        >
          Log Out
        </button>
      </div>
    </div>


  </Appear>
  
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Appear from "/components/Appear"
import { useUserStore } from '@/stores/user'
import { doc, getDoc } from 'firebase/firestore'
import { signOut } from 'firebase/auth'

const { $auth, $db } = useNuxtApp()
const router = useRouter()
const userStore = useUserStore()

const profileData = ref({
  email: '',
  credit: 0,
  membership: 'Free',
})

const loading = ref(true)
const error = ref('')


onMounted(async () => {
  try {
    const user = $auth.currentUser
    const userDocRef = doc($db, 'users', user.uid)
    const userSnap = await getDoc(userDocRef)

    if (userSnap.exists()) {
      const data = userSnap.data()
      profileData.value.email = data.email
      profileData.value.credit = data.credit
      profileData.value.membership = data.membership || 'Free'
    } else {
      error.value = 'User data not found.'
    }
  } catch (err) {
    error.value = 'Failed to load profile data.'
    console.error(err)
  } finally {
    loading.value = false
  }
})

const handleLogout = async () => {
  try {
    await signOut($auth)
    userStore.logout()
    router.push('/')
  } catch (err) {
    console.error('Logout error:', err)
    error.value = 'Failed to log out.'
  }
}
</script>
