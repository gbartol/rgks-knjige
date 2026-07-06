<script setup lang="ts">
import type { UserSummary } from '@/types'
import { useMutation, useQueryClient } from '@tanstack/vue-query'
import { followUser, unfollowUser } from '@/api'

const props = defineProps<{ user: UserSummary }>()

const queryClient = useQueryClient()

const followMutation = useMutation({
  mutationFn: () =>
    props.user.is_following ? unfollowUser(props.user.id) : followUser(props.user.id),
  // Osvježi rezultate pretrage da se is_following (i gumb) ažuriraju.
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
})

const toggleFollow = () => followMutation.mutate()
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

      <template #append>
        <v-btn
          :color="user.is_following ? undefined : 'primary'"
          :variant="user.is_following ? 'outlined' : 'flat'"
          :loading="followMutation.isPending.value"
          size="small"
          @click="toggleFollow()"
        >
          {{ user.is_following ? 'Otprati' : 'Prati' }}
        </v-btn>
      </template>
    </v-card-item>
  </v-card>
</template>
