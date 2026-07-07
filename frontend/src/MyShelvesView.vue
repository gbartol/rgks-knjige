<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchShelves, createShelf, formatError } from '@/api'
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

// kreiranje nove police
const dialog = ref(false)
const newName = ref('')
const newPublic = ref(true)
const creating = ref(false)
const createError = ref('')

const createNewShelf = async () => {
  if (!newName.value.trim()) return
  creating.value = true
  createError.value = ''
  try {
    await createShelf({ name: newName.value.trim(), is_public: newPublic.value })
    dialog.value = false
    newName.value = ''
    newPublic.value = true
    await loadShelves()
  } catch (error) {
    createError.value = formatError(error)
  } finally {
    creating.value = false
  }
}

onMounted(loadShelves)
</script>

<template>
  <v-container>
    <div class="d-flex align-center mb-6">
      <h1 class="text-h4 font-weight-bold">Moje police</h1>
      <v-spacer />
      <v-btn color="primary" prepend-icon="mdi-plus" @click="dialog = true">
        Nova polica
      </v-btn>
    </div>
    
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

    <v-dialog v-model="dialog" max-width="420">
      <v-card title="Nova polica">
        <v-card-text>
          <v-text-field v-model="newName" label="Naziv police" autofocus />
          <v-switch v-model="newPublic" label="Javna polica" color="primary" hide-details />

          <v-alert
            v-if="createError"
            type="error"
            variant="tonal"
            class="mt-2"
            style="white-space: pre-line"
          >
            {{ createError }}
          </v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="text" @click="dialog = false">Odustani</v-btn>
          <v-btn
            color="primary"
            :loading="creating"
            :disabled="!newName.trim()"
            @click="createNewShelf"
          >
            Spremi
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>