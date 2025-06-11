<template>
  <section class="relative w-screen overflow-hidden bg-white border-t border-gray-200 mt-4 2xl:mt-10">
    <div class="relative z-10 scroll-mt-20 py-10 px-4 text-center">
      <div class="max-w-3xl mx-auto">
        <div class="flex flex-col sm:flex-row justify-center sm:justify-between items-center gap-6">
          <!-- Left Side: Logo + Copyright -->
          <div class=" space-y-2 text-center  sm:text-left">
            <button class="flex ml-8 sm:ml-0 items-center space-x-2" @click="scrollToTop">
              <img src="/images/leaves.png" alt="Logo" class="w-8 h-8 object-contain" />
              <span class="text-xl font-medium text-gray-800">Edge Forestry</span>
            </button>
            <p class="text-xs text-gray-500">&copy; {{ new Date().getFullYear() }} Edge Forestry. All rights reserved.</p>
          </div>

          <!-- Right Side: Nav Links + Buttons -->
          <div class="flex flex-col items-center gap-2 sm:flex-row sm:flex-wrap sm:justify-center sm:gap-4 text-sm text-green-950 transition">
            <NuxtLink to="/account" class="hover:text-green-800">Account</NuxtLink>
            <button @click="scrollToSection('how-it-works')" class="hover:text-green-800">How It Works</button>
            <button @click="scrollToSection('packages')" class="hover:text-green-800">Packages</button>
            <button @click="scrollToSection('faqs')" class="hover:text-green-800">FAQs</button>
            <button @click="scrollToSection('about-us')" class="hover:text-green-800">About Us</button>
            <button @click="scrollToSection('contact-us')" class="hover:text-green-800">Contact</button>
            <NuxtLink to="/interactive" class="hover:text-green-800">Upload</NuxtLink>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const scrollToSection = (id) => {
  const el = document.getElementById(id)
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

const scrollToTop = () => {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>
