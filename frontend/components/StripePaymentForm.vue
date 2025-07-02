<template>
  <form @submit.prevent="handleSubmit" class="max-w-md mx-auto space-y-4">
    <div id="card-element" class="p-4 border rounded-md"></div>
    <button
      type="submit"
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      :disabled="loading"
    >
      {{ loading ? 'Processing...' : 'Pay $20' }}
    </button>
    <p class="text-red-500 mt-2">{{ errorMessage }}</p>
  </form>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { loadStripe } from '@stripe/stripe-js'

const stripePromise = loadStripe('pk_test_51Rg84bQM39Vu9mP8DE1EARE1Gk5xAzkOtFRJ4yBEyAonoz7LNLBSSeOYT4D8Zln73RzcfpWnpkk0N5rfGGutNy8z00pdHsreTo')

let stripe
let elements
let card
const loading = ref(false)
const errorMessage = ref('')

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
    const { clientSecret } = await $fetch('/api/create-payment-intent', {
      method: 'POST',
      body: { amount: 2000 }, //in cents
    })

    const result = await stripe.confirmCardPayment(clientSecret, {
      payment_method: { card },
    })

    if (result.error) {
      errorMessage.value = result.error.message
    } else if (result.paymentIntent.status === 'succeeded') {
      errorMessage.value = 'Payment successful!'
    }
  } catch (err) {
    errorMessage.value = 'Something went wrong.'
  } finally {
    loading.value = false
  }
}
</script>
