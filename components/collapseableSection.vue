<!-- components/ResultsHistory.vue -->
<template>
  <div class="p-6">
    <h2 class="text-2xl font-bold text-center mb-4">View Results History</h2>
    
    <div v-for="(entry, index) in paginatedEntries" :key="entry.id" class="mb-4">
      <div
        @click="toggle(index)"
        class="cursor-pointer flex justify-between items-center border py-2 px-4 bg-white shadow-sm rounded"
      >
        <div>
          <p class="font-medium">{{ entry.location }}</p>
          <p class="text-sm text-gray-500">{{ entry.date }}</p>
        </div>
        <span>{{ openIndex === index ? '▲' : '▼' }}</span>
      </div>

      <CollapsibleSection
        v-if="openIndex === index"
        :entry="entry"
        :files="entry.files"
        @selectProbability="handleProbability"
        @viewOnMap="handleMap"
      />
    </div>

    <div class="flex justify-center space-x-2 mt-6">
      <button @click="prevPage" :disabled="entryPage === 1" class="text-green-700">Prev</button>
      <span v-for="n in totalEntryPages" :key="n" @click="entryPage = n" :class="{ 'font-bold': entryPage === n }">
        {{ n }}
      </span>
      <button @click="nextPage" :disabled="entryPage === totalEntryPages" class="text-green-700">Next</button>
    </div>
  </div>
</template>

<script setup>
import CollapsibleSection from './CollapsibleSection.vue'

const props = defineProps({
  savedEntries: Array,
})

const openIndex = ref(null)
const entryPage = ref(1)
const entriesPerPage = 10

const paginatedEntries = computed(() => {
  const start = (entryPage.value - 1) * entriesPerPage
  return props.savedEntries.slice(start, start + entriesPerPage)
})
const totalEntryPages = computed(() => Math.ceil(props.savedEntries.length / entriesPerPage))

function toggle(index) {
  openIndex.value = openIndex.value === index ? null : index
}
function nextPage() {
  if (entryPage.value < totalEntryPages.value) entryPage.value++
}
function prevPage() {
  if (entryPage.value > 1) entryPage.value--
}
function handleProbability(entry) {
  console.log('Set probability for:', entry)
}
function handleMap(entry) {
  console.log('Refresh map with:', entry)
}
</script>
