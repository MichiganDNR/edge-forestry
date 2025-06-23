import { useUserStore } from '@/stores/user'

export default defineNuxtRouteMiddleware(async (to) => {
  const userStore = useUserStore()

  if (import.meta.server) return

  const publicPages = ['/', '/login', '/signup','404']

  if (publicPages.includes(to.path)) return

  if (!userStore.user) {
    return navigateTo('/login')
  }
})
