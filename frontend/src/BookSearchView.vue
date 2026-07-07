<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { searchBooks } from '@/api'

const router = useRouter()
const searchInput = ref('')
const items = ref<any[]>([])
const loading = ref(false)

let debounceTimer: ReturnType<typeof setTimeout> | null = null

watch(searchInput, (newVal) => {
  if (!newVal || newVal.length < 3) {
    items.value = []
    return
  }
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(async () => {
    loading.value = true
    try {
      const data = await searchBooks(newVal)
      items.value = data
    } catch (error) {
      console.error('Pretraga nije uspjela', error)
    } finally {
      loading.value = false
    }
  }, 500)
})

const onBookSelect = (book: any) => {
  if (book) {
    router.push({ name: 'book-details', params: { id: book.external_id } })
  }
}
</script>

<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <h1 class="text-h4 mb-6 text-center font-weight-bold">Pronađi svoju sljedeću knjigu</h1>
        
        <v-autocomplete
          v-model:search="searchInput"
          :items="items"
          :loading="loading"
          no-filter
          item-title="title"
          item-value="external_id"
          label="Unesi naslov knjige ili autora..."
          prepend-inner-icon="mdi-magnify"
          variant="solo-filled"
          flat
          hide-no-data
          return-object
          @update:model-value="onBookSelect"
        >
          <template v-slot:item="{ props, item }">
            <v-list-item
              v-bind="props"
              :prepend-avatar="(item.raw ?? item)?.cover_url || 'https://placehold.co/40x60?text=No+Cover'"
              :title="(item.raw ?? item)?.title"
              :subtitle="(item.raw ?? item)?.authors"
            ></v-list-item>
          </template>
        </v-autocomplete>
      </v-col>
    </v-row>
  </v-container>
</template>
