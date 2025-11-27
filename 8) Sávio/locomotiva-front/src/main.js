import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import './style.css'
import { initDB } from './services/indexedDB'

// Inicializar IndexedDB antes de montar a aplicação
initDB().then(() => {
  const app = createApp(App)
  const pinia = createPinia()

  app.use(pinia)
  app.mount('#app')
}).catch((error) => {
  console.error('Erro ao inicializar IndexedDB:', error)
  // Montar app mesmo se IndexedDB falhar
  const app = createApp(App)
  const pinia = createPinia()

  app.use(pinia)
  app.mount('#app')
})

