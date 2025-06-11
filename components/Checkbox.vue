<template>
  <div class="flex flex-col gap-3">
    <label
      v-for="disease in diseases"
      :key="disease"
      class="flex items-center gap-3 text-green-900 font-medium cursor-pointer"
    >
      <input
        type="checkbox"
        :checked="modelValue === disease"
        @change="toggle(disease)"
        class="w-5 h-5 text-green-900 border-gray-300 rounded focus:ring-green-600"
      />
      {{ disease }}
    </label>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: String,
  diseases: {
    type: Array,
    default: () => ['Oak Wilt', 'Hemlock Woolly Adelgid', 'Beech Bark Disease', 'Beech Leaf Disease']
  }
})

const emit = defineEmits(['update:modelValue'])

function toggle(disease) {
  emit('update:modelValue', props.modelValue === disease ? null : disease)
}
</script>

