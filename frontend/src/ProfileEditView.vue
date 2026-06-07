<script setup lang="ts">
import { ref, watch } from 'vue'
import { useQuery, useMutation, useQueryClient } from '@tanstack/vue-query'
import { fetchMyProfile, updateMyProfile, formatError } from '@/api'

const queryClient = useQueryClient()

const myProfileQuery = useQuery({
  queryKey: ['profile', 'me'],
  queryFn: fetchMyProfile,
})

const displayName = ref('')
const avatarUrl = ref('')

// myProfileQuery.data je Ref pa je validan watch izvor; callback prima odmotanu vrijednost
watch(myProfileQuery.data, (p) => {
  displayName.value = p?.display_name ?? ''
  avatarUrl.value = p?.avatar_url ?? ''
}, { immediate: true })

const saved = ref(false)

const updateMutation = useMutation({
  mutationKey: ['updateProfile'],
  mutationFn: () => updateMyProfile({
    display_name: displayName.value,
    avatar_url: avatarUrl.value,
  }),
  onSuccess: (updated) => {
    queryClient.setQueryData(['profile', 'me'], updated)
    saved.value = true
  },
})

const save = () => updateMutation.mutate()
</script>

<template>
  <v-container max-width="500">
    <h1 class="text-h5 mb-4">Uredi profil</h1>

    <v-progress-circular v-if="myProfileQuery.isLoading.value" indeterminate />

    <v-alert v-else-if="myProfileQuery.isError.value" type="error">
      Ne mogu dohvatiti profil.
    </v-alert>

    <template v-else>
      <div class="d-flex justify-center mb-4">
        <v-avatar size="96">
          <v-img v-if="avatarUrl" :src="avatarUrl" alt="Avatar" />
          <v-icon v-else size="96">mdi-account-circle</v-icon>
        </v-avatar>
      </div>

      <v-text-field
        v-model="displayName"
        label="Ime za prikaz"
        :counter="20"
        maxlength="20"
      />

      <v-text-field
        v-model="avatarUrl"
        label="URL profilne slike"
        placeholder="https://..."
      />

      <v-alert
        v-if="updateMutation.isError.value"
        type="error"
        class="mb-3"
        style="white-space: pre-line"
      >
        {{ formatError(updateMutation.error.value) }}
      </v-alert>

      <v-btn color="primary" :loading="updateMutation.isPending.value" @click="save()">
        Spremi
      </v-btn>
    </template>

    <v-snackbar v-model="saved" :timeout="2000" color="success">
      Profil spremljen.
    </v-snackbar>
  </v-container>
</template>
