// pinia store: allows us to access and modify data dynamically across the website
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)        // Firebase user object
  const credits = ref(0)    

  function setUser(newUser) {
    user.value = newUser
  }

  function setCredits(amount) {
    credits.value = amount
  }

  function incrementCredits(amount = 1) {
    credits.value += amount
  }

  function decrementCredits(amount = 1) {
    credits.value = Math.max(0, credits.value - amount)
  }

  function logout() {
    user.value = null
    credits.value = 0
  }

  const isAuthenticated = computed(() => !!user.value)

  return {
    user,
    credits,
    setUser,
    setCredits,
    incrementCredits,
    decrementCredits,
    logout,
    isAuthenticated,
  }
})