// src/main.ts
import { createApp } from 'vue'
import App from './App.vue'
import { initAuth } from './auth/useAuth'
import { registerPlugins } from '@/plugins'

async function bootstrap() {
  await initAuth()
  const app = createApp(App)
  registerPlugins(app)
  app.mount('#app')
}

bootstrap()
