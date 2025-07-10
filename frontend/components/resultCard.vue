<template>
  <div v-if="showModal" class="fixed inset-0 bg-white bg-opacity-90 z-5000 flex items-center justify-center mt-20">
    <button
      @click="closeModal"
      class="absolute top-65 right-50 text-green-950 text-4xl font-bold z-5000"
      aria-label="Close"
    >
      &times;
    </button>

    <img
      :src="imageUrl"
      alt="Fullscreen image"
      class="w-2/3 h-2/3 object-contain"
    />
  </div>
  <div :class="['rounded-2xl p-4 flex flex-col gap-2 w-1/8 mt-8', bgClass]">
    <!-- Image/File Name -->
    <div class="text-sm font-medium">
      <img
        :src="imageUrl"
        alt="Result image"
        class="w-full h-32 object-contain rounded-md border border-green-950 mb-2"
        @click="openModal"
      />
        There is a <strong>{{ (probability * 100).toFixed(2) }}%</strong><br>chance this section<br>has Oak Wilt.
    </div>

    <!-- Coordinates -->
    <div class="text-green-950 text-sm">
      <strong>Coordinates:</strong><br> {{ coordinates[0] }}, {{ coordinates[1] }}
    </div>

    <!-- Probability 
    <div class="text-green-950 text-sm">
      <strong>Probability:</strong><br> {{ (probability * 100).toFixed(2) }}%
    </div> -->

    <!-- Feedback Buttons -->
    <div class="flex flex-row gap-2 mt-2">
      <button
        class="bg-green-100 text-green-800 px-4 py-1 rounded-full text-sm hover:bg-green-200 border-2 border-green-800"
        @click="$emit('feedback', fileName, 'Healthy')"
      >
        <img src="public/images/tu.png"/>
      </button>
      <button
        class="bg-red-100 text-red-800 px-4 py-1 rounded-full text-sm hover:bg-red-200 border-2 border-red-800"
        @click="$emit('feedback', fileName, 'Healthy')"
      >
        <img src="public/images/td.png"/>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ref } from 'vue'

const showModal = ref(false)
const openModal = () => showModal.value = true
const closeModal = () => showModal.value = false

const props = defineProps({
  imageUrl: String,
  probability: Number,
  fileName: String,
  coordinates: Array,
  onFeedback: Function,
  selectedDiseaseDropdown: String 
})

const bgClass = computed(() => {
  const prob = props.probability
  if (prob < 0.7) return 'bg-green-100'
  if (prob >= 0.7 && prob < 0.9) return 'bg-yellow-100'
  if (prob >= 0.9 && prob < 0.995) return 'bg-orange-100'
  if (prob >= 0.995) return 'bg-red-100'
  return 'bg-white'
})
</script>


<!--const sendFeedback = async (feedbackType) => {
  try {
    await fetch('/api/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        fileName,
        probability,
        coordinates,
        feedback: feedbackType,
        disease: selectedDiseaseDropdown
      })
    })
    alert('Feedback sent!')
  } catch (err) {
    console.error('Feedback failed:', err)
    alert('Failed to send feedback.')
  }
} -->