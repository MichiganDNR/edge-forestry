// ~/plugins/firebase.client.js
import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'

export default defineNuxtPlugin(nuxtApp => {
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

  const firebaseApp = initializeApp(firebaseConfig)
  const auth = getAuth(firebaseApp)

  nuxtApp.provide('auth', auth)
})
