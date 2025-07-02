<template>
  <form @submit.prevent="handleSubmit" class="max-w-md mx-auto space-y-6 p-4 border border-green-950 rounded shadow">

    <!-- Package Selection -->
    <div class="flex justify-between mb-6">
      <label
        v-for="pkg in packages"
        :key="pkg.id"
        class="cursor-pointer p-3 m-3 border border-green-950 rounded-xl w-1/3 text-center"
        :class="selectedPackage.id === pkg.id ? 'bg-green-700 text-white' : 'bg-white text-green-950 hover:bg-gray-100'"
      >
        <input
          type="radio"
          :value="pkg"
          v-model="selectedPackage"
          class="hidden"
        />
        <div class="font-semibold text-lg">{{ pkg.name }}</div>
        <div class="text-sm text-green-500">{{ pkg.description }}</div>
        <div class="mt-2 font-bold">${{ (pkg.amount / 100).toFixed(2) }}</div>
      </label>
    </div>

    <!-- Billing Info -->
    <div class="space-y-4">
      <div>
        <label class="block mb-1 text-green-950 font-medium">Name</label>
        <input v-model="billingDetails.name" required type="text" class="w-full p-2 border  border-green-950 rounded" placeholder="Full Name" />
      </div>
      <div>
        <label class="block mb-1 text-green-950 font-medium">Email</label>
        <input v-model="billingDetails.email" required type="email" class="w-full p-2 border  border-green-950 rounded" placeholder="Email address" />
      </div>
      <div>
        <label class="block mb-1 text-green-950 font-medium">Address</label>
        <input v-model="billingDetails.address.line1" required type="text" class="w-full p-2 border  border-green-950 rounded" placeholder="Street address" />
      </div>
      <div class="flex space-x-2">
        <input v-model="billingDetails.address.city" required type="text" class="flex-1 p-2 border  border-green-950 rounded" placeholder="City" />
        <input v-model="billingDetails.address.state" required type="text" class="w-20 p-2 border  border-green-950 rounded" placeholder="State" />
        <input v-model="billingDetails.address.postal_code" required type="text" class="w-24 p-2 border  border-green-950 rounded" placeholder="Zip" />
      </div>
      <div>
        <label class="block mb-1 text-green-950 font-medium">Country</label>
        <input v-model="billingDetails.address.country" required type="text" class="w-full p-2 border  border-green-950 rounded" placeholder="Country" />
      </div>
    </div>

    <!-- Card Element -->
    <div id="card-element" class="p-4 border border-green-950 rounded"></div>

    <!-- Submit -->
    <button
      type="submit"
      class="w-full bg-green-700 text-white py-3 rounded hover:bg-green-800 disabled:opacity-50"
      :disabled="loading"
    >
      {{ loading ? 'Processing...' : `Pay $${(selectedPackage.amount / 100).toFixed(2)}` }}
    </button>

    <!-- Error Message -->
    <p class="text-red-500 mt-2 min-h-[1.25rem]">{{ errorMessage }}</p>
  </form>
</template>

<script setup>
import { onMounted, ref, reactive } from 'vue'
import { loadStripe } from '@stripe/stripe-js'

const packages = [
  { id: 'basic', name: 'Basic', description: 'For starters', amount: 500 },
  { id: 'standard', name: 'Standard', description: 'Most popular', amount: 2000 },
  { id: 'premium', name: 'Premium', description: 'All the extras', amount: 5000 },
]

const selectedPackage = ref(packages[0])
const billingDetails = reactive({
  name: '',
  email: '',
  address: {
    line1: '',
    city: '',
    state: '',
    postal_code: '',
    country: '',
  },
})

const loading = ref(false)
const errorMessage = ref('')

let stripe
let elements
let card

const stripePromise = loadStripe('pk_test_...') // Replace with your publishable key

onMounted(async () => {
  stripe = await stripePromise
  elements = stripe.elements()
  card = elements.create('card')
  card.mount('#card-element')
})

async function handleSubmit() {
  loading.value = true
  errorMessage.value = ''

  try {
    // Call backend to create PaymentIntent with selected package amount
    const { clientSecret } = await $fetch('/api/create-payment-intent', {
      method: 'POST',
      body: { amount: selectedPackage.value.amount },
    })

    // Confirm card payment with billing details
    const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
      payment_method: {
        card,
        billing_details: {
          name: billingDetails.name,
          email: billingDetails.email,
          address: billingDetails.address,
        },
      },
    })

    if (error) {
      errorMessage.value = error.message
    } else if (paymentIntent.status === 'succeeded') {
      errorMessage.value = 'Payment successful!'
      // You can reset form or route user as needed here
    }
  } catch (err) {
    errorMessage.value = 'Something went wrong. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>
