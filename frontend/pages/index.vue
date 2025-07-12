<template>
  <div class="space-y-12 bg-white">
    <Appear>
      <section class="relative w-screen min-h-screen overflow-hidden">
        <div class="relative z-10 scroll-mt-20 py-20 px-4 text-center">
          <div class="w-full max-w-7xl mx-auto">
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-y-12 gap-x-8 lg:gap-x-16 items-center">
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

              <div class="lg:col-span-6 flex justify-center">
                <div class="w-full aspect-[3/4] max-w-sm sm:max-w-md md:max-w-lg lg:max-w-xl xl:max-w-2xl 2xl:max-w-3xl 2xl:max-h-[700px] max-h-[600px] overflow-hidden rounded-2xl sm:rounded-3xl shadow-xl relative">
                  <img
                    :key="currentImageIndex"
                    :src="currentImageSrc"
                    alt="Aerial view of forest canopy showing healthy trees"
                    class="w-full h-full object-cover object-center"
                  />

                  <button
                    @click="prevImage"
                    class="absolute left-4 top-1/2 -translate-y-1/2 bg-white bg-opacity-50 text-green-800 p-2 rounded-full z-10 hover:bg-opacity-75 focus:outline-none"
                  >
                    &#10094; </button>
                  <button
                    @click="nextImage"
                    class="absolute right-4 top-1/2 -translate-y-1/2 bg-white bg-opacity-50 text-green-800 p-2 rounded-full z-10 hover:bg-opacity-75 focus:outline-none"
                  >
                    &#10095; </button>

                  <div class="absolute bottom-4 flex space-x-2 z-10 w-full justify-center">
                    <span
                      v-for="(image, index) in heroImages"
                      :key="index"
                      @click="goToImage(index)"
                      class="block w-3 h-3 rounded-full cursor-pointer transition-colors duration-300"
                      :class="{ 'bg-white': index === currentImageIndex, 'bg-gray-400': index !== currentImageIndex }"
                      aria-label="Go to slide"
                    ></span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </Appear>

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

    <SectionWrapper id="packages" tag="Packages" title="Pay by needs." class="flex justify-center">
      <div class="w-full max-w-md m-8 h-[300px] 2xl:max-w-2xl 2xl:h-[500px] bg-white rounded-2xl shadow-md border border-green-700
    hover:scale-105 transform transition-all duration-300">
        <p class="text-xl text-green-950 m-12">
          If you have any questions on packaging, services, or pricing, please click to button below to send us a contact form.
        </p>
        <Button label="Contact Us." :scrollTo="'contact-us'"/>
      </div>
    </SectionWrapper>

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

    <SectionWrapper
      id="about-us"
      tag="About Us"
      title="Meet the Team"
      description="Edge Forestry is redefining how we detect and manage plant conditions using AI."
    >
      <div class="w-full flex justify-center mb-7">
        <div class="flex flex-row gap-4">
          <div class="flex flex-col items-center w-64 h-[400px] 2xl:w-80 2xl:h-[500px] bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden">
            <a href="https://www.linkedin.com/in/rahatibnrafiq/">
              <img
                src="public/images/Rahat.png"
                class="w-full h-[350px] 2xl:h-[450px] object-cover object-center"
              />
            </a>
            <p class="mt-2 text-center text-green-950 font-medium">Rahat Rafiq</p>
          </div>

          <div class="flex flex-col items-center w-64 h-[400px] 2xl:w-80 2xl:h-[500px] bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden">
            <a href="https://www.linkedin.com/in/muttaki-bismoy/">
              <img
                src="public/images/Muttaki.png"
                class="w-full h-[350px] 2xl:h-[450px] object-cover object-center"
              />
            </a>
            <p class="mt-2 text-center text-green-950 font-medium">Muttaki Bismoy</p>
          </div>

          <div class="flex flex-col items-center w-64 h-[400px] 2xl:w-80 2xl:h-[500px] bg-white rounded-2xl shadow-md border border-gray-200 overflow-hidden">
            <a href="https://www.linkedin.com/in/collin-brennan-078407273/">
              <img
                src="public/images/Collin.png"
                class="w-full h-[350px] 2xl:h-[450px] object-cover object-center"
              />
          </a>
            <p class="mt-2 text-center text-green-950 font-medium">Collin Brennan</p>
          </div>
        </div>
      </div>

      <div class="flex justify-center">
        <Button class="mt-7" label="Learn More" href="https://www.gvsu.edu/bluenucleus/" external />
      </div>
    </SectionWrapper>

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
import { ref, computed } from 'vue' 
import Button from '~/components/MainButton.vue'
import Appear from '~/components/Appear.vue'
import SectionWrapper from '~/components/SectionWrapper.vue'
import Service from '~/components/PackagesContainer.vue'
import emailjs from '@emailjs/browser'
import { useRouter } from 'vue-router'

const router = useRouter()

const goToPage = () => {
    router.push('/results')
}

const heroImages = ref([
  '/images/pic.webp', 
  '/images/pic2.webp', 
  '/images/pic3.webp',
]);

const currentImageIndex = ref(0);

const currentImageSrc = computed(() => heroImages.value[currentImageIndex.value]);

const nextImage = () => {
  currentImageIndex.value = (currentImageIndex.value + 1) % heroImages.value.length;
};


const prevImage = () => {

  currentImageIndex.value = (currentImageIndex.value - 1 + heroImages.value.length) % heroImages.value.length;
};

const goToImage = (index) => {
  currentImageIndex.value = index;
};


const EMAILJS_CONFIG = {
  serviceId: 'service_817br4o',
  templateId: 'template_1unsqk9',
  publicKey: 'aRFiTIS1dQnPwbGDs'
}

const formState = ref({
  name: '',
  email: '',
  message: '',
  isSent: false,
  error: null,
  isLoading: false,
  validationErrors: {}
})

const faqState = ref({
  items: [
    {
      question: 'How does the AI analyze tree photos?',
      answer: `Our system uses artificial intelligence to detect oak wilt from aerial images taken by drones.
               When you upload the images, our AI model analyzes patterns in tree color, canopy texture, and spatial changes that are invisible to the human eye.
               It compares this data to thousands of known cases to determine the likelihood of infection. As our users submit more feedback, the model continuously improves.
               The result is a fast, accurate assessment that helps prioritize on-the-ground action.
              `,
      open: false,
    },
    {
      question: 'What image formats are supported?',
      answer: `We support standard image formats such as JPG, JPEG, PNG, and GIF because they are widely used in drone imaging and preserve essential visual data for analysis. These formats ensure compatibility across devices while maintaining the resolution needed for accurate oak wilt detection by our AI model.`,
      open: false,
    },
    {
      question: 'Can I use this service for commercial forestry?',
      answer: `The platform is designed for both individual and commercial forestry as oak wilt poses a serious threat at every scale—from single property owners to large land managers. By offering accessible, high-accuracy detection, we empower everyone from private landowners to forestry professionals to act early and make informed decisions to protect their trees and investments.`,
      open: false,
    },
    {
      question: 'Can this be used remotely?',
      answer: 'In order to enable the best user experience for offline use, Edge Forestry is in the process of curating a proprietary device with our ai model and software. This device will allow for optimal remote use of our model and eliminate back and forth between sites.',
      open: false,
    },
  ]
})

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
