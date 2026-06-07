<script setup lang="ts">
import { ref } from 'vue'
import { useQuery } from '@tanstack/vue-query'
import { userSearch, formatError } from '@/api'
import UserCard from '@/components/UserCard.vue'

const search = ref('')

const usersQuery = useQuery({
  queryKey: ['users', search],
  queryFn: () => userSearch(search.value),
})
</script>

<template>
  <v-container max-width="600">
    <h1 class="text-h5 mb-4">Pretraga korisnika</h1>

    <v-text-field
      v-model="search"
      label="Pretraži po imenu"
      prepend-inner-icon="mdi-magnify"
      clearable
      :loading="usersQuery.isFetching.value"
    />

    <v-alert v-if="usersQuery.isError.value" type="error" style="white-space: pre-line">
      {{ formatError(usersQuery.error.value) }}
    </v-alert>

    <template v-else>
      <v-alert
        v-if="!usersQuery.isLoading.value && (usersQuery.data.value?.length ?? 0) === 0"
        type="info"
        variant="tonal"
      >
        Nema rezultata.
      </v-alert>

      <UserCard
        v-for="user in usersQuery.data.value ?? []"
        :key="user.id"
        :user="user"
      />
    </template>
  </v-container>
</template>
