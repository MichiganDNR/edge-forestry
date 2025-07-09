<template>
  <Appear>
    <div class="min-h-screen flex flex-col items-center p-4">
      <h1 class="text-center sm:font-normal leading-[0.9] text-green-950 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl mb-12 mt-12">
        Login
      </h1>

      <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
        <h1 class="text-3xl font-semibold mb-6 text-green-950 text-center">Welcome Back</h1>

        <form @submit.prevent="handleLogin" class="flex flex-col gap-4">
          <input
            v-model="email"
            type="email"
            placeholder="Email"
            required
            class="border border-gray-300 rounded p-2 w-full"
          />
          <input
            v-model="password"
            type="password"
            placeholder="Password"
            required
            class="border border-gray-300 rounded p-2 w-full"
          />

          <button
            type="submit"
            class="bg-green-600 text-white rounded-2xl p-2 hover:bg-green-700"
          >
            Log In
          </button>

          <p v-if="error" class="text-red-500 text-sm mt-2 text-center">{{ error }}</p>
        </form>

        <!-- Create Account Link -->
        <div class="text-center mt-6">
          <p class="text-gray-600">
            Don’t have an account?
            <NuxtLink to="/signup" class="text-green-700 font-semibold hover:underline">
              Create Account
            </NuxtLink>
          </p>
        </div>
      </div>
    </div>
  </Appear>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router' 
import Appear from '/components/Appear'
import { signInWithEmailAndPassword } from 'firebase/auth'
import { doc, getDoc } from 'firebase/firestore'
import { useUserStore } from '@/stores/user'

const email = ref('')
const password = ref('')
const error = ref('')

const { $auth, $db } = useNuxtApp()
const userStore = useUserStore()
const router = useRouter()

const handleLogin = async () => {
  error.value = ''

  try {
    const userCredential = await signInWithEmailAndPassword($auth, email.value, password.value)
    const user = userCredential.user

    const userDocRef = doc($db, 'users', user.uid)
    const userSnap = await getDoc(userDocRef)

    if (userSnap.exists()) {
      const data = userSnap.data()
      userStore.setUser(user)
      userStore.setCredits(data.credit)
      router.push('/results') 
    } else {
      error.value = 'No profile found for this user.'
    }
  } catch (err) {
    if (err.code === 'auth/user-not-found') {
      error.value = 'No user found with that email.'
    } else if (err.code === 'auth/wrong-password') {
      error.value = 'Incorrect password.'
    } else {
      error.value = err.message
    }
  }
}
</script>
