// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  app: {
    head: {
      link: [
        { rel: 'icon', type: 'image/png', href: '/favicon.png' },
      ]
    } 
  },
  compatibilityDate: '2025-05-15',
  devtools: { enabled: true },
  ssr: false,
  modules: ['@nuxtjs/tailwindcss', '@pinia/nuxt'],
  plugins: ['~/plugins/firebase.client.js'],
  ssr: false,
  tailwindcss: {
    exposeConfig: true,
    viewer: true,
  }
})