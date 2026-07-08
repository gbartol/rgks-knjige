<script setup lang="ts">
import { fetchBookDetailById } from '@/api';
import type { Review } from '@/types'
import { useRouter } from 'vue-router'

const router = useRouter()

defineProps<{ review: Review }>()

const formatDate = (iso: string) => new Date(iso).toLocaleDateString('hr-HR')

const onBookSelect = async (bookSummary: any) => {
  const book = await fetchBookDetailById(bookSummary.id)
  if (book) {
    router.push({ name: 'book-details', params: { id: book.external_id } })
  }
}


</script>

<template>
  <v-card class="mb-3" variant="tonal">
    <v-card-item>
      <template #prepend>
        <v-avatar color="grey-lighten-1">
          <v-img
            v-if="review.user.avatar_url"
            :src="review.user.avatar_url"
            :alt="review.user.display_name"
          />
          <v-icon v-else>mdi-account-circle</v-icon>
        </v-avatar>
      </template>
      <v-card-title>{{ review.user.display_name }}</v-card-title>
      <v-card-subtitle>{{ formatDate(review.created_at) }}</v-card-subtitle>
    </v-card-item>

    <v-card-text>
      <div class="d-flex ga-3">
        <v-img
          v-if="review.book.cover_url"
          :src="review.book.cover_url"
          :alt="review.book.title"
          width="60"
          max-width="60"
          class="flex-grow-0 rounded"
        />
        <div>
          <div class="font-weight-medium">
            <v-btn @click="onBookSelect(review.book)">{{ review.book.title }}</v-btn>
          </div>
          <div class="text-caption text-medium-emphasis mb-1">{{ review.book.authors }}</div>
          <v-rating :model-value="review.rating" density="compact" size="small" readonly />
          <p v-if="review.text" class="mt-2">{{ review.text }}</p>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>
