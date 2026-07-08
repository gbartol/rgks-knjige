<template>
  <v-app>
    <v-app-bar>
      <v-app-bar-title>Bookshelf</v-app-bar-title>
      <v-spacer />
      
      <v-navigation-drawer v-model="drawer" temporary>
        <v-list v-if="isAuthenticated">
          <v-list-item title="Feed" :to="{ name: 'feed' }" />
          <v-list-item title="Pretraga knjiga" :to="{ name: 'book-search' }" />
          <v-list-item title="Moje police" :to="{ name: 'my-shelves' }" />
          <v-list-item title="Korisnici" :to="{ name: 'users' }" />
          <v-list-item title="Profil" :to="{ name: 'profile' }" />
          <v-divider />
          <v-list-item title="Odjava" @click="logout()" />
        </v-list>
      </v-navigation-drawer>
      
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
