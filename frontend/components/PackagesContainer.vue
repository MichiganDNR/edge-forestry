<!-- components/Service.vue -->
<template>
    <div class="w-full max-w-sm m-8 h-[500px] 2xl:max-w-lg 2xl:h-[700px] bg-white rounded-2xl shadow-md border border-green-700
    hover:scale-105 transform transition-all duration-300">
        <h1 class="font-medium text-green-950 text-left m-8 mb-2 text-5xl xl:text-5xl 2xl:text-7xl">{{ title }}</h1>
        <h1 class="font-medium text-green-950 text-left m-8 mb-2 text-4xl xl:text-5xl 2xl:text-7xl">${{ price }}</h1>
        <p class="text-gray-500 text-left ml-8">{{ description }}</p>
        <div class="text-left m-8"><BuyNowButton label="Coming Soon."></BuyNowButton></div>
        <div class=" text-green-950 text-left m-4 ml-8 text-2xl 2xl:text-3xl">
            <div class="font-medium">Includes</div>
            <div v-for="(perk, index) in perks" :key="index">
                - {{ perk }}<br>
            </div>
        </div>
    </div>
</template>

<script setup>
import BuyNowButton from "./BuyNowButton.vue"

defineProps({
title: String,
price: Number,
description: String,
perks: Array
});
</script>
