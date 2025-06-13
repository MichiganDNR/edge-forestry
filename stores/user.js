// stores/user.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const user = ref(null)        // Firebase user object
  const credits = ref(0)        // Credits from your database

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

  return {
    user,
    credits,
    setUser,
    setCredits,
    incrementCredits,
    decrementCredits,
  }
})
