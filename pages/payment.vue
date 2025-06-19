<template>
  <div class="min-h-screen flex items-center justify-center px-4">
    <div class="bg-white p-8 rounded-xl shadow-lg max-w-md w-full">
      <h2 class="text-3xl font-medium text-green-950 mb-6 text-center">Payment Processing</h2>

      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-green-950 mb-1">Full Name</label>
          <input v-model="name" type="text" class="w-full p-2 border rounded" required />
        </div>

        <div>
          <label class="block text-green-950 mb-1">Email</label>
          <input v-model="email" type="email" class="w-full p-2 border rounded" required />
        </div>

        <div>
          <label class="block text-green-950 mb-1">Card Number</label>
          <input v-model="card" type="text" class="w-full p-2 border rounded" placeholder="1234 5678 9012 3456" required />
        </div>

        <div class="flex space-x-4 gap-2">
          <div class="w-1/2">
            <label class="block text-green-950 mb-1">Expiration</label>
            <input v-model="expiry" type="text" class="w-full p-2 border rounded" placeholder="MM/YY" required />
          </div>
          <div class="w-1/2">
            <label class="block text-green-950 mb-1">CVC</label>
            <input v-model="cvc" type="text" class="w-full p-2 border rounded" placeholder="123" required />
          </div>
        </div>

        <button
          type="submit"
          class="w-full bg-green-700 text-white py-2 px-4 rounded-2xl hover:bg-green-800 transition"
          :disabled="loading"
        >
          {{ loading ? 'Processing...' : 'Pay Now' }}
        </button>
      </form>

      <div v-if="success" class="mt-4 text-green-700 font-medium text-center">
        Payment successful! 🎉
      </div>

      <div v-if="error" class="mt-4 text-red-600 text-center">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const card = ref('')
const expiry = ref('')
const cvc = ref('')
const loading = ref(false)
const success = ref(false)
const error = ref('')

definePageMeta({
  middleware: ['auth'],
  requiresAuth: true
})

const handleSubmit = async () => {
  loading.value = true
  error.value = ''
  success.value = false

  try {
    // Simulate payment processing delay
    await new Promise(resolve => setTimeout(resolve, 2000))

    // Simulated success
    success.value = true
  } catch (err) {
    error.value = 'Payment failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
