<template>
  <div class="min-h-screen flex flex-col items-center p-4">
    <h1 class="text-center sm:font-normal leading-[0.9] text-green-950 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl mb-12 mt-12">
      Sign Up
    </h1>
    <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
      <h1 class="text-3xl font-semibold mb-6 text-green-950 text-center">Create an Account</h1>

      <form @submit.prevent="handleSignUp" class="flex flex-col gap-4">
        <!--
        <input
          v-model="name"
          type="name"
          placeholder="FullName"
          required
          class="border border-gray-300 rounded p-2 w-full"
        />
      -->
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
        <input
          v-model="confirmPassword"
          type="password"
          placeholder="Confirm Password"
          required
          class="border border-gray-300 rounded p-2 w-full"
        />

        <button
          type="submit"
          :disabled="loading"
          class="bg-green-600 text-white rounded-2xl p-2 hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ loading ? 'Creating...' : 'Sign Up' }}
        </button>
        <p v-if="error" class="text-red-500 text-sm mt-2 text-center">{{ error }}</p>
        <p v-if="success" class="text-green-700 text-sm mt-2 text-center">Account created!</p>
      </form>

      <div class="text-center mt-6">
        <p class="text-gray-600">
          Have an account?
          <NuxtLink to="/login" class="text-green-700 font-semibold hover:underline">
            Log in
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useNuxtApp } from '#app'
import { createUserWithEmailAndPassword } from 'firebase/auth'
import { doc, setDoc, serverTimestamp } from 'firebase/firestore'
import { useUserStore } from '@/stores/user'

const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref(null)
const success = ref(false)
const loading = ref(false)

const { $auth, $db } = useNuxtApp()
const router = useRouter()
const userStore = useUserStore()

const errorMessages = {
  'auth/email-already-in-use': 'Email is already in use.',
  'auth/invalid-email': 'Invalid email address.',
  'auth/weak-password': 'Password is too weak.',
}

const handleSignUp = async () => {
  if (loading.value) return
  loading.value = true
  error.value = ''
  success.value = false

  if (password.value.length < 5) {
    error.value = 'Password must be at least 5 characters long.'
    loading.value = false
    return
  }

  if (password.value !== confirmPassword.value) {
    error.value = 'Passwords do not match.'
    loading.value = false
    return
  }

  try {
    //Create user in Firebase Auth
    const userCredential = await createUserWithEmailAndPassword($auth, email.value, password.value)
    const user = userCredential.user

    try {
      //Create user doc in Firestore
      await setDoc(doc($db, 'users', user.uid), {
        email: email.value,
        credit: 0,
        createdAt: serverTimestamp()
      })

      //Update store and UI state **only if Firestore write succeeds**
      userStore.setUser(user)
      userStore.setCredits(0)
      success.value = true
      router.push('/settings')
    } catch (firestoreErr) {
      console.error('Failed to create Firestore user doc:', firestoreErr)
      error.value = 'Account created, but failed to save user data. Please contact support.'
    }

  } catch (err) {
    console.error('Firebase Auth error:', err)
    error.value = errorMessages[err.code] || 'Something went wrong. Try again.'
  } finally {
    loading.value = false
  }
}
</script>