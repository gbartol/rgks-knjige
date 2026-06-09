<script setup lang="ts">
import { useRouter } from 'vue-router'
import { Book } from '@/types'

const props = defineProps<{
  book: Book
}>()

const router = useRouter()

const goToDetails = () => {
  router.push({ name: 'book-details', params: { id: props.book.external_id } })
}
</script>

<template>
  <v-card class="mx-auto my-2" max-width="342" variant="outlined" @click="goToDetails">
    <v-img
      :src="book.cover_url || 'https://placehold.co/150x220?text=Nema+Slike'"
      height="220"
      cover
      class="align-end text-white"
    ></v-img>

    <v-card-item>
      <v-card-title class="text-subtitle-1 font-weight-bold text-truncate">
        {{ book.title }}
      </v-card-title>
      <v-card-subtitle class="text-truncate">
        {{ book.authors }}
      </v-card-subtitle>
    </v-card-item>

    <v-card-text v-if="book.published_year" class="text-caption text-grey">
      Godina izdanja: {{ book.published_year }}
    </v-card-text>
  </v-card>
</template>