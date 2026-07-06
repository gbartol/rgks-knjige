<script setup lang="ts">
import { ref } from 'vue'
import { deleteReview as apiDeleteReview } from '@/api'
import type { Review } from '@/types'

const props = defineProps<{
  reviews: Review[]
  currentUserId: number
}>()

const emit = defineEmits(['review-deleted'])

const dialog = ref(false)
const reviewToDelete = ref<number | null>(null)
const deleting = ref(false)

const confirmDelete = (reviewId: number) => {
  reviewToDelete.value = reviewId
  dialog.value = true
}

const deleteReview = async () => {
  if (!reviewToDelete.value) return
  deleting.value = true
  
  try {
    await apiDeleteReview(reviewToDelete.value)
    emit('review-deleted', reviewToDelete.value)
    dialog.value = false
  } catch (error) {
    console.error('Greška pri brisanju recenzije', error)
  } finally {
    deleting.value = false
    reviewToDelete.value = null
  }
}
</script>

<template>
  <div class="mt-4">
    <div class="text-h6 mb-3">Recenzije korisnika ({{ reviews.length }})</div>
    
    <v-alert v-if="reviews.length === 0" type="info" variant="tonal">
      Još nema recenzija za ovu knjigu. Budi prvi!
    </v-alert>

    <v-list v-else lines="three" variant="flat">
      <v-list-item
        v-for="review in reviews"
        :key="review.id"
        class="border-b py-3 px-0"
      >
        <template v-slot:prepend>
          <v-avatar color="grey-lighten-2" class="mr-3">
            <v-img :src="review.user.avatar_url || 'https://placehold.co/40x40?text=U'"></v-img>
          </v-avatar>
        </template>

        <v-list-item-title class="font-weight-bold d-flex align-items-center">
          {{ review.user.display_name || review.user.username }}
          <v-rating
            :model-value="review.rating"
            readonly
            color="amber"
            density="compact"
            size="small"
            class="ml-3"
          ></v-rating>
        </v-list-item-title>

        <v-list-item-subtitle class="text-body-1 text-high-emphasis mt-1">
          {{ review.text }}
        </v-list-item-subtitle>

        <template v-slot:append>
          <v-btn
            v-if="review.user.id === currentUserId"
            icon="mdi-delete-outline"
            variant="text"
            color="error"
            @click="confirmDelete(review.id)"
          ></v-btn>
        </template>
      </v-list-item>
    </v-list>

    <v-dialog v-model="dialog" max-width="400">
      <v-card title="Brisanje recenzije">
        <v-card-text>
          Jeste li sigurni da želite obrisati ovu recenziju? Ova akcija je nepovratna.
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Odustani</v-btn>
          <v-btn color="error" :loading="deleting" @click="deleteReview">Obriši</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>