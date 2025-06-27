<template>
  <div class="space-y-12 bg-white">
    <!-- Hero Section -->
    <Appear>
      <section class="relative w-screen min-h-screen overflow-hidden">
        <div class="relative z-10 scroll-mt-20 py-20 px-4 text-center">
          <div class="w-full max-w-7xl mx-auto">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-y-12 gap-x-8 lg:gap-x-16 items-center">
              <!-- Left Content -->
              <div class="lg:col-span-6 text-center space-y-6 flex flex-col items-center">
                <h1 class="font-semibold sm:font-normal leading-[0.9] text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-8xl 2xl:text-9xl">
                  <span>AI Powered</span><br>
                  <span class="text-green-900">Tree<br>Diagnosis</span>
                </h1>

                <p class="text-green-950 text-sm sm:text-base lg:text-lg leading-relaxed font-light max-w-xl">
                  Upload a photo — We'll analyze the pictures for probability of a variety of diseases and map them for you.
                </p>

                <div class="w-full sm:w-auto">
                  <Button @click="goToPage" class="w-full sm:w-auto" label="Click To Upload" />
                </div>
              </div>

              <!-- Right Image -->
              <div class="lg:col-span-6 flex justify-center">
                <div class="w-full aspect-[3/4] max-w-sm sm:max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl 2xl:max-w-3xl 2xl:max-h-[700px] max-h-[600px] overflow-hidden rounded-2xl sm:rounded-3xl shadow-xl">
                  <img 
                    src="/images/pic.webp" 
                    alt="Aerial view of forest canopy showing healthy trees"
                    class="w-full h-full object-cover object-center"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </Appear>

    <!-- How It Works -->
    <SectionWrapper
      id="how-it-works"
      tag="How It Works"
      title="See the Process"
      description="Upload pictures of trees for instant analysis. Our AI predicts disease probability."
    >
      <div class="w-full max-w-2xl mx-auto h-[350px] mb-7 2xl:max-w-4xl 2xl:h-[550px] bg-white rounded-2xl shadow-md border border-gray-200">
        <video
          src="/video/OakWiltDemoV1.mp4"
          controls
          class="w-full h-auto rounded-2xl"
        >
      Your browser does not support the video tag.
    </video>
      </div>
      <div class="flex justify-center">
        <Button class="mt-7" label="Learn More" :scrollTo="'faqs'" />
      </div>
    </SectionWrapper>

    <!-- Packages -->
    <SectionWrapper id="packages" tag="Packages" title="Pay by needs.">
      <div class="flex flex-wrap justify-center gap-4">
        <Service title="Basic" price="5" description="One time" :perks="['100 uploads']" />
        <Service title="Pro" price="25" description="Monthly" :perks="['1000 uploads']" />
        <Service title="Premium" price="50" description="Monthly" :perks="['Unlimited uploads']" />
      </div>
    </SectionWrapper>

    <!-- FAQ -->
    <SectionWrapper id="faqs" tag="FAQs" title="Frequently Asked Questions">
      <div class="max-w-3xl mx-auto space-y-4 2xl:space-y-8 2xl:mt-10">
        <div v-for="(faq, index) in faqState.items" :key="index" class="border p-4 rounded-xl shadow-sm">
          <button @click="toggleFaq(index)" class="w-full text-left flex justify-between items-center text-green-950 font-medium text-lg">
            {{ faq.question }}
            <span class="text-xl">{{ faq.open ? '−' : '+' }}</span>
          </button>
          <div v-show="faq.open" class="mt-3 text-gray-700 text-sm">
            {{ faq.answer }}
          </div>
        </div>
      </div>
    </SectionWrapper>

    <!-- About -->
    <SectionWrapper
      id="about-us"
      tag="About Us"
      title="Meet the Team"
      description="Edge Forestry is redefining how we detect and manage plant conditions using AI."
    >
      <div class="w-full flex justify-center mb-7">
        <div class="flex flex-row gap-4">
          <!-- Rahat -->
          <div class="flex flex-col items-center w-64 h-[400px] 2xl:w-80 2xl:h-[500px] bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden">
            <img 
              src="/images/Rahat.png" 
              class="w-full h-[350px] 2xl:h-[450px] object-cover object-center"
            />
            <p class="mt-2 text-center text-green-950 font-medium">Rahat Rafiq</p>
          </div>

          <!-- Muttaki -->
          <div class="flex flex-col items-center w-64 h-[400px] 2xl:w-80 2xl:h-[500px] bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden">
            <img 
              src="/images/Muttaki.png" 
              class="w-full h-[350px] 2xl:h-[450px] object-cover object-center"
            />
            <p class="mt-2 text-center text-green-950 font-medium">Muttaki Bismoy</p>
          </div>

          <!-- Collin -->
          <div class="flex flex-col items-center w-64 h-[400px] 2xl:w-80 2xl:h-[500px] bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden">
            <img 
              src="/images/Collin.png" 
              class="w-full h-[350px] 2xl:h-[450px] object-cover object-center"
            />
            <p class="mt-2 text-center text-green-950 font-medium">Collin Brennan</p>
          </div>
        </div>
      </div>

      <div class="flex justify-center">
        <Button class="mt-7" label="Learn More" href="https://www.gvsu.edu/bluenucleus/" external />
      </div>
    </SectionWrapper>

    <!-- Contact -->
    <SectionWrapper
      id="contact-us"
      tag="Contact Us"
      title="Get in Touch"
      description="Have a question? We're here to help."
    >
      <form @submit.prevent="sendEmail" class="max-w-2xl mx-auto space-y-6 text-green-950">
        <div>
          <label for="name" class="block text-center sm:text-left">Name</label>
          <input
            v-model="formState.name"
            type="text"
            id="name"
            class="mt-1 block w-full p-3 border rounded-xl shadow-sm"
            :class="{ 'border-red-500': formState.validationErrors.name }"
          />
          <p v-if="formState.validationErrors.name" class="text-red-500 text-sm text-center sm:text-left">{{ formState.validationErrors.name }}</p>
        </div>
        <div>
          <label for="email" class="block text-center sm:text-left">Email</label>
          <input
            v-model="formState.email"
            type="email"
            id="email"
            class="mt-1 block w-full p-3 border rounded-xl shadow-sm"
            :class="{ 'border-red-500': formState.validationErrors.email }"
          />
          <p v-if="formState.validationErrors.email" class="text-red-500 text-sm text-center sm:text-left">{{ formState.validationErrors.email }}</p>
        </div>
        <div>
          <label for="message" class="block text-center sm:text-left">Message</label>
          <textarea
            v-model="formState.message"
            id="message"
            rows="4"
            class="mt-1 block w-full p-3 border rounded-xl shadow-sm"
            :class="{ 'border-red-500': formState.validationErrors.message }"
          ></textarea>
          <p v-if="formState.validationErrors.message" class="text-red-500 text-sm text-center sm:text-left">{{ formState.validationErrors.message }}</p>
        </div>
        <button
          type="submit"
          class="bg-green-700 hover:bg-green-800 text-white font-semibold py-3 px-6 rounded-2xl w-full flex items-center justify-center"
          :disabled="formState.isLoading"
        >
          <span v-if="formState.isLoading" class="animate-spin rounded-full h-5 w-5 border-t-2 border-white mr-2"></span>
          {{ formState.isLoading ? 'Sending...' : 'Send Message' }}
        </button>
        <p
          v-if="formState.isSent"
          class="text-center text-green-700 text-sm mt-2"
        >
          Message sent successfully!
        </p>
        <p
          v-if="formState.error"
          class="text-center text-red-600 text-sm mt-2"
        >
          {{ formState.error }}
        </p>

      </form>
    </SectionWrapper>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import Button from '~/components/MainButton.vue'
import Appear from '~/components/Appear.vue'
import SectionWrapper from '~/components/SectionWrapper.vue'
import Service from '~/components/PackagesContainer.vue'
import emailjs from '@emailjs/browser'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { storeToRefs } from 'pinia'  

const router = useRouter()
const userStore = useUserStore()
const { user } = storeToRefs(userStore) // makes user a ref

const goToPage = () => {
  if (!user.value) {
    router.push('/interactive')
  } else {
    router.push('/results')
  }
}

// Constants
const EMAILJS_CONFIG = {
  serviceId: 'service_817br4o',
  templateId: 'template_1unsqk9',
  publicKey: 'aRFiTIS1dQnPwbGDs'
}

// Form state
const formState = ref({
  name: '',
  email: '',
  message: '',
  isSent: false,
  error: null,
  isLoading: false,
  validationErrors: {}
})

// FAQ state
const faqState = ref({
  items: [
    {
      question: 'How does the AI analyze tree photos?',
      answer: 'Our model uses image classification and segmentation to detect disease symptoms based on trained patterns.',
      open: false,
    },
    {
      question: 'What image formats are supported?',
      answer: 'We support JPEG, PNG, and WebP formats. High-resolution images yield better results.',
      open: false,
    },
    {
      question: 'Can I use this service for commercial forestry?',
      answer: 'Yes, our platform is designed for both individuals and forestry professionals.',
      open: false,
    }
  ]
})

// Methods
const scrollToSection = (id) => {
  if (id === 'top') {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  const el = document.getElementById(id)
  if (el) {
    window.scrollTo({
      top: el.offsetTop - 40,
      behavior: 'smooth'
    })
  }
}

const validateForm = () => {
  const errors = {}
  const { name, email, message } = formState.value
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!name.trim()) errors.name = 'Name is required.'
  if (!email.trim()) {
    errors.email = 'Email is required.'
  } else if (!emailPattern.test(email)) {
    errors.email = 'Invalid email format.'
  }
  if (!message.trim()) errors.message = 'Message is required.'

  formState.value.validationErrors = errors
  return Object.keys(errors).length === 0
}

const sendEmail = async () => {
  formState.value.error = null
  formState.value.isSent = false
  
  if (!validateForm()) return

  formState.value.isLoading = true

  try {
    const templateParams = {
      from_name: formState.value.name,
      reply_to: formState.value.email,
      message: formState.value.message,
    }

    await emailjs.send(
      EMAILJS_CONFIG.serviceId,
      EMAILJS_CONFIG.templateId,
      templateParams,
      EMAILJS_CONFIG.publicKey
    )

    formState.value.isSent = true
    formState.value.name = ''
    formState.value.email = ''
    formState.value.message = ''
  } catch (err) {
    formState.value.error = 'Failed to send message. Please try again.'
    console.error(err)
  } finally {
    formState.value.isLoading = false
    setTimeout(() => {
      formState.value.isSent = false
    }, 3000)
  }
}

const toggleFaq = (index) => {
  faqState.value.items[index].open = !faqState.value.items[index].open
}
</script>