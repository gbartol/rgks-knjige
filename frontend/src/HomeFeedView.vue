<script setup lang="ts">
import { useQuery } from '@tanstack/vue-query'
import { fetchFeed, formatError } from '@/api'
import FeedItem from '@/components/FeedItem.vue'

const feedQuery = useQuery({
  queryKey: ['feed'],
  queryFn: fetchFeed,
})
</script>

<template>
  <v-container max-width="700">
    <h1 class="text-h5 mb-4">Feed</h1>

    <v-progress-circular v-if="feedQuery.isLoading.value" indeterminate />

    <v-alert v-else-if="feedQuery.isError.value" type="error" style="white-space: pre-line">
      {{ formatError(feedQuery.error.value) }}
    </v-alert>

    <template v-else>
      <v-alert
        v-if="(feedQuery.data.value?.length ?? 0) === 0"
        type="info"
        variant="tonal"
      >
        Nema aktivnosti. Zaprati nekoga da vidiš njihove recenzije.
      </v-alert>

      <FeedItem
        v-for="review in feedQuery.data.value ?? []"
        :key="review.id"
        :review="review"
      />
    </template>
  </v-container>
</template>
