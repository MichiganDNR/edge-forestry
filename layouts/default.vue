<script setup>
import Navbar from '~/components/NavBar.vue'
import Footer from '~/components/Footer.vue'

const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <div class="flex flex-col min-h-screen bg-white">
    <div id="top"></div>

    <!-- Nav Bar -->
    <header class="bg-white p-2">
      <Navbar />
    </header>

    <!-- Page content injected here -->
    <main class="flex-1 p-6 space-y-12">
      <slot />
    </main>

    <!-- Footer -->
    <Footer />
  </div>
</template>

<style>
html, body {
  height: 100%;
  margin: 0;
}
</style>
