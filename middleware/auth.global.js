export default defineNuxtRouteMiddleware((to) => {
  const { $auth } = useNuxtApp()

  if (import.meta.server) return

  // Only protect pages that ask for auth
  if (to.meta.requiresAuth && !$auth.currentUser) {
    return navigateTo('/login')
  }
})
