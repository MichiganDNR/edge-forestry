<template>
  <div class="min-h-screen flex flex-col items-center p-4">
    <h1 class="text-center sm:font-normal leading-[0.9] text-green-950 text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl 2xl:text-8xl mb-12 mt-12">
      Sign Up
    </h1>
    <div class="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
      <h1 class="text-3xl font-semibold mb-6 text-green-950 text-center">Create an Account</h1>

      <form @submit.prevent="handleSignUp" class="flex flex-col gap-4">
        <input
          v-model="name"
          type="name"
          placeholder="Full Name"
          required
          class="border border-gray-300 rounded p-2 w-full"
        />
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
          Sign Up
        </button>
        <p v-if="error" class="text-red-500 text-sm mt-2 text-center">{{ error }}</p>
        <p v-if="success" class="text-green-700 text-sm mt-2 text-center">Account created! 🎉</p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createUserWithEmailAndPassword } from 'firebase/auth'

const email = ref('')
const password = ref('')
const error = ref('')
const success = ref(false)

const { $auth } = useNuxtApp()

const handleSignUp = async () => {
  error.value = ''
  success.value = false
  try {
    await createUserWithEmailAndPassword($auth, email.value, password.value)
    success.value = true
    email.value = ''
    password.value = ''
  } catch (err) {
    error.value = err.message
  }
}
</script>

