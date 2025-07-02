<template>
  <div class="p-8">
    <h1 class="text-center text-5xl font-semibold mb-8 mt-8 text-green-950">Make a Payment</h1>
    <StripePaymentForm />
  </div>
</template>

<script setup>
import StripePaymentForm from '~/components/StripePaymentForm.vue'
</script>
