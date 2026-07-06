<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchShelves as apiFetchShelves, modifyShelfBooks } from '@/api'
import type { Shelf } from '@/types'

const props = defineProps<{
  bookExternalId: string
}>()

const shelves = ref<Shelf[]>([])
const selectedShelfId = ref<number | null>(null)
const loading = ref(false)

const fetchShelves = async () => {
  try {
    const data = await apiFetchShelves()
    shelves.value = data
  } catch (error) {
    console.error('Greška pri dohvaćanju polica', error)
  }
}

const handleShelfChange = async (shelfId: number) => {
  if (loading.value) return
  loading.value = true
  
  try {
    await modifyShelfBooks(shelfId, 'add', props.bookExternalId)
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