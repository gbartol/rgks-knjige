<script setup lang="ts">
import { ref } from 'vue'
import { addReview, formatError } from '@/api'

const props = defineProps<{
  bookExternalId: string
}>()

const emit = defineEmits(['review-added'])

const rating = ref(5)
const text = ref('')
const loading = ref(false)
const errorMessage = ref('')

const submitReview = async () => {
  if (!rating.value) {
    errorMessage.value = 'Molimo odaberite ocjenu.'
    return
  }
  
  loading.value = true
  errorMessage.value = ''
  
  try {
    const data = await addReview(props.bookExternalId, {
      rating: rating.value,
      text: text.value
    })
    
    emit('review-added', data)
    text.value = ''
  } catch (error: any) {
    errorMessage.value = formatError(error) || 'Došlo je do greške.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <v-card class="pa-4" variant="flat">
    <v-card-title class="px-0">Napiši recenziju</v-card-title>
    
    <div class="mb-3">
      <span class="text-body-2 mr-2">Tvoja ocjena:</span>
      <v-rating
        v-model="rating"
        color="amber"
        density="compact"
        :half-increments="false"
      ></v-rating>
    </div>

    <v-textarea
      v-model="text"
      label="Što misliš o ovoj knjizi?"
      variant="outlined"
      rows="3"
      auto-grow
    ></v-textarea>

    <v-alert v-if="errorMessage" type="error" variant="tonal" class="mb-3" density="compact">
      {{ errorMessage }}
    </v-alert>

    <v-btn
      color="primary"
      :loading="loading"
      block
      @click="submitReview"
    >
      Objavi recenziju
    </v-btn>
  </v-card>
</template>