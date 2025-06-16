// ~/plugins/firebase.client.js
import { initializeApp } from 'firebase/app'
import { getAuth, onAuthStateChanged } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'
import { useUserStore } from '@/stores/user'

export default defineNuxtPlugin((nuxtApp) => {
  const firebaseConfig = {
    apiKey: "AIzaSyCshHqp6lSreG77Qgy3-eQyT9Xw_Bh6aKE",
    authDomain: "edgeforestryai.firebaseapp.com",
    databaseURL: "https://edgeforestryai-default-rtdb.firebaseio.com",
    projectId: "edgeforestryai",
    storageBucket: "edgeforestryai.firebasestorage.app",
    messagingSenderId: "984192259272",
    appId: "1:984192259272:web:cb3abeb0c1604541ae01fd",
    measurementId: "G-LNY1RL87S3"
  }

  // Initialize Firebase app and services
  const app = initializeApp(firebaseConfig)
  const auth = getAuth(app)
  const db = getFirestore(app)
  

  nuxtApp.provide('auth', auth)
  nuxtApp.provide('db', db)

  // Setup auth state listener to update pinia store reactively
  onAuthStateChanged(auth, (user) => {
    const userStore = useUserStore(nuxtApp.$pinia) 
    if (user) {
      userStore.setUser(user)
    } else {
      userStore.setUser(null)
    }
  })
})

