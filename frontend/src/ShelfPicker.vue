<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { Shelf } from '@/types'

const props = defineProps<{
  bookExternalId: string
}>()

const shelves = ref<Shelf[]>([])
const selectedShelfId = ref<number | null>(null)
const loading = ref(false)

// Dohvati sve police korisnika pri učitavanju
const fetchShelves = async () => {
  try {
    const response = await axios.get('/api/shelves/')
    shelves.value = response.data
  } catch (error) {
    console.error('Greška pri dohvaćanju polica', error)
  }
}

// Premjesti knjigu na odabranu policu
const handleShelfChange = async (shelfId: number) => {
  if (loading.value) return
  loading.value = true
  
  try {
    await axios.post(`/api/shelves/${shelfId}/add/`, {
      external_id: props.bookExternalId
    })
    selectedShelfId.value = shelfId
  } catch (error) {
    console.error('Greška pri spremanju na policu', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchShelves)
</script>

<template>
  <v-card class="pa-4" variant="outlined">
    <div class="text-subtitle-1 mb-2 font-weight-bold">Spremi na policu:</div>
    
    <v-progress-circular v-if="loading" indeterminate color="primary" class="ma-2"></v-progress-circular>
    
    <v-chip-group v-else v-model="selectedShelfId" column>
      <v-chip
        v-for="shelf in shelves"
        :key="shelf.id"
        :value="shelf.id"
        filter
        variant="tonal"
        color="primary"
        @click="handleShelfChange(shelf.id)"
      >
        {{ shelf.name }}
      </v-chip>
    </v-chip-group>
  </v-card>
</template>