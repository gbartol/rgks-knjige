<template>
  <v-app>
    <v-app-bar>
      <v-app-bar-title>Bookshelf</v-app-bar-title>
      <v-spacer />
      <template v-if="isAuthenticated">
        <v-btn :to="{ name: 'profile' }">Profil</v-btn>
        <v-btn @click="logout()">Odjava</v-btn>
      </template>
      <v-btn v-else @click="login()">Prijava</v-btn>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script lang="ts" setup>
  import { useAuth } from '@/auth/useAuth'

  const { isAuthenticated, login, logout } = useAuth()
</script>
