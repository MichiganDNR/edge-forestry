<template>
  <div class="flex flex-col items-center justify-center p-2">
    <!-- Flip Container -->
    <div
      class="relative w-[300px] md:w-[300px] h-[450px] cursor-pointer"
      @click="flipped = !flipped"
    >
      <!-- Inner Flip Element -->
      <div
        class="absolute inset-0 transition-transform duration-700 [transform-style:preserve-3d]"
        :class="{ '[transform:rotateY(180deg)]': flipped }"
      >
        <!-- FRONT SIDE -->
        <div
          class="absolute inset-0 flex flex-col items-center justify-start text-center
                 backdrop-blur-md bg-green-950 border border-green-900 rounded-2xl shadow-lg
                 [backface-visibility:hidden] p-6 space-y-4 hover:scale-[1.02] hover-pulse-green transition-all duration-300"
        >
          <!-- Profile Image -->
            <div class="flex flex-col">
                <div class="w-36 h-36 rounded-full border-4 border-white overflow-hidden mx-auto mt-4">
                    <img :src="image" :alt="`${name} profile`" class="w-full h-full object-cover" />
                </div>

                <!-- Name -->
                <h2 class="text-2xl font-semibold text-white mt-4">{{ name }}</h2>
            </div>
          

          <!-- Contact Methods -->
          <div class="w-full flex flex-col space-y-4">
            <!-- Email -->
            <a
              :href="`mailto:${email}`"
              class="flex items-center justify-start px-4 py-2 bg-white/5 hover:bg-white/10
                     rounded-xl border border-white/10 transition-all duration-300 hover:translate-x-1"
            >
              <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center mr-3 shadow-md">
                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="M3 8l7.89 7.89a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <div class="text-white font-medium">Email</div>
                <div class="text-white/60 text-xs truncate">{{ email }}</div>
              </div>
            </a>

            <!-- LinkedIn -->
            <a
              :href="linkedin"
              target="_blank"
              rel="noopener noreferrer"
              class="flex items-center justify-start px-4 py-2 bg-white/5 hover:bg-white/10
                     rounded-xl border border-white/10 transition-all duration-300 hover:translate-x-1"
            >
              <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-700 rounded-lg flex items-center justify-center mr-3 shadow-md">
                <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452z"/>
                </svg>
              </div>
              <div>
                <div class="text-white font-medium">LinkedIn</div>
                <div class="text-white/60 text-xs">Connect professionally</div>
              </div>
            </a>
          </div>

          <!-- Flip hint -->
          <p class="text-sm font-semibold text-gray-400 mt-4">(Click to view bio)</p>
        </div>

        <!-- BACK SIDE -->
        <div
          class="absolute inset-0 flex flex-col items-center justify-center text-center
                 backdrop-blur-md bg-green-800/90 border border-green-900 rounded-2xl shadow-lg
                 [transform:rotateY(180deg)] [backface-visibility:hidden] p-8 hover:scale[1.02] hover-pulse-green transition-all duration-300"
        >
          <h3 class="text-white text-xl font-semibold mb-4">About Me</h3>
          <p class="text-white/90 text-sm leading-relaxed max-w-xs">
            {{ bio }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

defineProps({
  name: String,
  email: String,
  bio: String,
  image: String,
  linkedin: String,
});

const flipped = ref(false);
</script>

<style scoped>
@keyframes pulse-green {
  0%, 100% {
    box-shadow: 0 0 10px rgba(34,197,94,0.7), 0 0 20px rgba(34,197,94,0.5);
  }
  50% {
    box-shadow: 0 0 25px rgba(34,197,94,1), 0 0 40px rgba(34,197,94,0.9);
  }
}

.hover-pulse-green:hover {
  animation: pulse-green 2s infinite;
}
</style>
