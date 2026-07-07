<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchShelves } from '@/api'
import type { Shelf } from '@/types'
import ShelfSection from './ShelfSection.vue'

const shelves = ref<Shelf[]>([])
const loading = ref(true)

const loadShelves = async () => {
  loading.value = true
  try {
    const data = await fetchShelves()
    shelves.value = data
  } catch (error) {
    console.error('Greška pri učitavanju polica', error)
  } finally {
    loading.value = false
  }
}

const handleBookRemoved = (payload: { shelfId: number; externalId: string }) => {
  const shelf = shelves.value.find(s => s.id === payload.shelfId)
  if (shelf && shelf.books) {
    shelf.books = shelf.books.filter(b => b.external_id !== payload.externalId)
    shelf.books_count = shelf.books.length
  }
}

onMounted(loadShelves)
</script>

<template>
  <v-container>
    <h1 class="text-h4 mb-6 font-weight-bold">Moje police</h1>
    
    <div v-if="loading" class="d-flex justify-center my-10">
      <v-progress-circular indeterminate color="primary" size="64"></v-progress-circular>
    </div>
    
    <template v-else>
      <v-alert v-if="shelves.length === 0" type="info" variant="tonal">
        Još nemate kreiranu nijednu policu.
      </v-alert>
      
      <div v-for="shelf in shelves" :key="shelf.id" class="mb-8">
        <ShelfSection 
        :shelf="shelf" 
        :books="shelf.books || []" 
        @book-removed="handleBookRemoved"
        />
        <v-divider class="mt-4"></v-divider>
      </div>
    </template>
  </v-container>
</template>