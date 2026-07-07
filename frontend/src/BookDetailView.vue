<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useQuery, useQueryClient } from '@tanstack/vue-query'
import { fetchBookDetail, fetchBookReviews, fetchMyProfile, formatError } from '@/api'
import ShelfPicker from '@/ShelfPicker.vue'
import ReviewForm from '@/ReviewForm.vue'
import ReviewList from '@/ReviewList.vue'

const route = useRoute()
const externalId = route.params.id as string

const queryClient = useQueryClient()

const bookQuery = useQuery({
  queryKey: ['book', externalId],
  queryFn: () => fetchBookDetail(externalId),
})

const reviewsQuery = useQuery({
  queryKey: ['reviews', externalId],
  queryFn: () => fetchBookReviews(externalId),
})

const profileQuery = useQuery({
  queryKey: ['profile', 'me'],
  queryFn: fetchMyProfile,
})

// Nakon dodavanja/brisanja recenzije ponovno dohvati listu.
const refreshReviews = () => queryClient.invalidateQueries({ queryKey: ['reviews', externalId] })
</script>

<template>
  <v-container max-width="900">
    <v-progress-circular v-if="bookQuery.isLoading.value" indeterminate class="ma-4" />

    <v-alert v-else-if="bookQuery.isError.value" type="error" style="white-space: pre-line">
      {{ formatError(bookQuery.error.value) }}
    </v-alert>

    <template v-else-if="bookQuery.data.value">
      <v-row>
        <v-col cols="12" sm="4">
          <v-img
            :src="bookQuery.data.value.cover_url || 'https://placehold.co/300x450?text=Nema+Slike'"
            class="rounded"
            cover
          />
          <ShelfPicker :book-external-id="externalId" class="mt-4" />
        </v-col>

        <v-col cols="12" sm="8">
          <h1 class="text-h4 font-weight-bold">{{ bookQuery.data.value.title }}</h1>
          <div class="text-subtitle-1 text-medium-emphasis mb-2">{{ bookQuery.data.value.authors }}</div>
          <div v-if="bookQuery.data.value.published_year" class="text-caption text-grey mb-4">
            Godina izdanja: {{ bookQuery.data.value.published_year }}
          </div>
          <p v-if="bookQuery.data.value.description" class="text-body-1">
            {{ bookQuery.data.value.description }}
          </p>
        </v-col>
      </v-row>

      <v-divider class="my-6" />

      <ReviewForm :book-external-id="externalId" @review-added="refreshReviews" />

      <ReviewList
        :reviews="reviewsQuery.data.value ?? []"
        :current-user-id="profileQuery.data.value?.id ?? -1"
        @review-deleted="refreshReviews"
      />
    </template>
  </v-container>
</template>
