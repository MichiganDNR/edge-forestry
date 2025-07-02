import stripe from 'stripe'


const config = useRuntimeConfig()
const stripe = require('stripe')(config.stripeSecretKey)

export default defineEventHandler(async (event) => {
  const body = await readBody(event)

  const paymentIntent = await stripe.paymentIntents.create({
    amount: body.amount || 2000, //in cents
    currency: 'usd',
  })

  return { clientSecret: paymentIntent.client_secret }
})
