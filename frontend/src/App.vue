<template>
  <v-app>
    <v-app-bar>
      <v-app-bar-title>Bookshelf</v-app-bar-title>
      <v-spacer />
      
      <template v-if="isAuthenticated">
        <v-btn :to="{ name: 'book-search' }">Pretraga knjiga</v-btn>

        <v-btn :to="{ name: 'users' }">Korisnici</v-btn>
        <v-btn :to="{ name: 'profile' }">Profil</v-btn>
        <v-btn @click="logout()">Odjava</v-btn>
      </template>
      
      <v-btn v-else @click="login()">Prijava</v-btn>
    </v-app-bar>

    <v-main>
      <router-view @notify="showNotification" />
    </v-main>

    <v-snackbar
      v-model="snackbar"
      :color="snackbarColor"
      :timeout="3000"
      location="bottom right"
    >
      {{ snackbarText }}
      <template v-slot:actions>
        <v-btn variant="text" @click="snackbar = false">Zatvori</v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script lang="ts" setup>
  import { ref } from 'vue'
  import { useAuth } from '@/auth/useAuth'

  const { isAuthenticated, login, logout } = useAuth()

  const snackbar = ref(false)
  const snackbarText = ref('')
  const snackbarColor = ref('success')

  const showNotification = (payload: { text: string; color?: string }) => {
    snackbarText.value = payload.text
    snackbarColor.value = payload.color || 'success'
    snackbar.value = true
  }
</script>