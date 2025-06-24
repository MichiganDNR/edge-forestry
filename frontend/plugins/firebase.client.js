// ~/plugins/firebase.client.js
import { initializeApp } from 'firebase/app'
import { getAuth, setPersistence, browserSessionPersistence, onAuthStateChanged } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'
import { useUserStore } from '@/stores/user'

export default defineNuxtPlugin(async (nuxtApp) => {
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

  const app = initializeApp(firebaseConfig)
  const auth = getAuth(app)
  const db = getFirestore(app)

  await setPersistence(auth, browserSessionPersistence)

  nuxtApp.provide('auth', auth)
  nuxtApp.provide('db', db)

  onAuthStateChanged(auth, (user) => {
    const userStore = useUserStore(nuxtApp.$pinia)
    userStore.setUser(user || null)
  })
})

