<script setup lang="ts">
import type { UserSummary } from '@/types'

defineProps<{ user: UserSummary }>()

</script>

<template>
  <v-card class="mb-2" variant="tonal">
    <v-card-item>
      <template #prepend>
        <v-avatar color="grey-lighten-1">
          <v-img
            v-if="user.avatar_url"
            :src="user.avatar_url"
            :alt="user.display_name"
          />
          <v-icon v-else>mdi-account-circle</v-icon>
        </v-avatar>
      </template>

      <v-card-title>{{ user.display_name }}</v-card-title>
    </v-card-item>
  </v-card>
</template>
