<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'
import { Shelf, Book } from '@/types'
import BookCard from './BookCard.vue'

const props = defineProps<{
  shelf: Shelf
  books: Book[]
}>()

const emit = defineEmits(['book-removed'])
const removingBookId = ref<string | null>(null)

const removeBook = async (externalId: string) => {
  removingBookId.value = externalId
  try {
    await axios.post(`/api/shelves/${props.shelf.id}/remove/`, {
      external_id: externalId
    })
    emit('book-removed', { shelfId: props.shelf.id, externalId })
  } catch (error) {
    console.error('Greška pri micanju knjige s police', error)
  } finally {
    removingBookId.value = null
  }
}
</script>

<template>
  <v-container class="px-0 py-4">
    <div class="d-flex align-center mb-4">
      <h2 class="text-h5 font-weight-bold">{{ shelf.name }}</h2>
      <v-chip class="ml-3" size="small" variant="outlined">
        {{ shelf.is_public ? 'Javna' : 'Privatna' }}
      </v-chip>
    </div>

    <v-alert v-if="books.length === 0" type="info" variant="tonal" class="ma-2">
      Ova polica je još prazna. Pregledaj knjige i dodaj ih ovdje!
    </v-alert>

    <v-row v-else>
      <v-col
        v-for="book in books"
        :key="book.id"
        cols="12"
        sm="6"
        md="4"
        lg="3"
        class="position-relative"
      >
        <BookCard :book="book" />
        
        <v-btn
          icon="mdi-close-circle"
          size="x-small"
          color="error"
          variant="flat"
          class="position-absolute"
          style="top: 10px; right: 20px; z-index: 2;"
          :loading="removingBookId === book.external_id"
          @click="removeBook(book.external_id)"
        ></v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>