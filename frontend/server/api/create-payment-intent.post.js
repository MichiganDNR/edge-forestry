// server/api/create-payment-intent.post.js
import Stripe from 'stripe'

const config = useRuntimeConfig()
const stripe = new Stripe(config.stripeSecretKey)

export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  const paymentIntent = await stripe.paymentIntents.create({
    amount: body.amount || 2000, // in cents
    currency: 'usd',
  })

  return { clientSecret: paymentIntent.client_secret }
})

