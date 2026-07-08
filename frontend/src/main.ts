// src/main.ts
import { createApp } from 'vue'
import App from './App.vue'
import { initAuth } from './auth/useAuth'
import { registerPlugins } from '@/plugins'

async function bootstrap() {
  //await initAuth()
  console.log("Nešto")
  console.log(import.meta.VITE_TENANT_ID)
  const app = createApp(App)
  registerPlugins(app)
  app.mount('#app')
}

bootstrap()
