<template>
  <v-app>
    <v-app-bar>
      <v-app-bar-title>Bookshelf</v-app-bar-title>
      <v-spacer />
      
      <template v-if="isAuthenticated">
        <template v-if="mobitel">
          <v-menu>
            <template v-slot:activator="{ props }">
              <v-btn
                color="primary"
                v-bind="props"
              >
                IZABERI OPCIJU
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                :to="{ name: 'feed' }"
              >Feed
              </v-list-item>
              <v-list-item
                :to="{ name: 'book-search' }"
              >Pretraga knjiga
              </v-list-item>
              <v-list-item
                :to="{ name: 'my-shelves' }"
              >Moje police
              </v-list-item>
              <v-list-item
                :to="{ name: 'users' }"
              >Korisnici
              </v-list-item>
              <v-list-item
                :to="{ name: 'profile' }"
              >Profil
              </v-list-item>
              <v-list-item
                @click="logout()"
              >Odjava
              </v-list-item>
            </v-list>
          </v-menu>
        </template>
        <template v-else>
          <v-btn :to="{ name: 'feed' }">Feed</v-btn>
          <v-btn :to="{ name: 'book-search' }">Pretraga knjiga</v-btn>
          <v-btn :to="{ name: 'my-shelves' }">Moje police</v-btn>
          <v-btn :to="{ name: 'users' }">Korisnici</v-btn>
          <v-btn :to="{ name: 'profile' }">Profil</v-btn>
          <v-btn @click="logout()">Odjava</v-btn>
        </template>
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
  import { onMounted } from 'vue'
  import { useDisplay } from 'vuetify'

  const { isAuthenticated, login, logout } = useAuth()
  const { mobile } = useDisplay()
  onMounted(() => {
    const mobitel = mobile.value
  })

  const items = ['FEED','PRETRAGA KNJIGA','MOJE POLICE', 'KORISNICI','PROFIL','ODJAVA']

  const snackbar = ref(false)
  const snackbarText = ref('')
  const snackbarColor = ref('success')

  const showNotification = (payload: { text: string; color?: string }) => {
    snackbarText.value = payload.text
    snackbarColor.value = payload.color || 'success'
    snackbar.value = true
  }
</script>
