
<!-- components/SectionWrapper.vue -->
<template>
  <section :id="id" class="relative w-screen min-h-screen overflow-hidden">
    <div class="relative z-10 scroll-mt-20 py-20 px-4 text-center">
      <Appear>
        <div v-if="tag" class="inline-block px-3 py-1 mb-4 text-sm font-medium rounded-lg border border-green-700 text-green-950">
          {{ tag }}
        </div>
        <h2 v-if="title" class="text-6xl font-medium text-green-950 mb-4">{{ title }}</h2>
        <p v-if="description" class="text-green-950 font-light max-w-xl mx-auto mb-6">{{ description }}</p>
        <slot />
      </Appear>
    </div>
  </section>
</template>

<script setup>
import Appear from './Appear.vue';
defineProps({
  id: String,
  tag: String,
  title: String,
  description: String,
});
</script>
