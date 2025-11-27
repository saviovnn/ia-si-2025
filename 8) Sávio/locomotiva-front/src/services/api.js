import axios from 'axios'

// Usar variável de ambiente ou fallback para localhost
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

if(API_BASE_URL === '') {
  console.error('API_BASE_URL is empty')
  throw new Error('API_BASE_URL is empty')
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Contador de requisições
let requestCount = 0
const requestLog = []

// Interceptor para contar requisições
api.interceptors.request.use(
  (config) => {
    requestCount++
    const requestInfo = {
      count: requestCount,
      method: config.method?.toUpperCase(),
      url: config.url,
      timestamp: new Date().toISOString()
    }
    requestLog.push(requestInfo)
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Interceptor para tratamento de erros
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.code === 'ECONNABORTED' || error.message.includes('Network Error')) {
      error.isConnectionError = true
    }
    console.error(`[ERROR #${requestCount}] ${error.config?.method?.toUpperCase()} ${error.config?.url} - ${error.message}`)
    return Promise.reject(error)
  }
)

// Função para obter estatísticas de requisições
export function getRequestStats() {
  const stats = {
    total: requestCount,
    byMethod: {},
    byUrl: {},
    log: requestLog
  }
  
  requestLog.forEach(req => {
    stats.byMethod[req.method] = (stats.byMethod[req.method] || 0) + 1
    stats.byUrl[req.url] = (stats.byUrl[req.url] || 0) + 1
  })
  
  return stats
}

// Expor função global para ver estatísticas
if (typeof window !== 'undefined') {
  window.getRequestStats = getRequestStats
}

export const apiService = {
  // Buscar rota
  async buscarRota(data) {
    const response = await api.post('/mapa-rota', data)
    return response.data
  },
  
  // Listar cidades por bitola
  async getCidades(bitola) {
    const response = await api.get(`/cidades/${bitola}`)
    return response.data.cidades
  },
  
  // Obter coordenadas de uma cidade
  async getCoordenadasCidade(cidade) {
    const response = await api.get(`/coordenadas-cidade/${encodeURIComponent(cidade)}`)
    return response.data
  },
  
  // Obter coordenadas de múltiplas cidades de uma vez
  async getCoordenadasCidades(cidades) {
    const response = await api.post('/coordenadas-cidades', { cidades })
    return response.data.coordenadas
  },
  
  // Obter todas as rotas de uma bitola
  async getRotas(bitola) {
    const response = await api.get(`/rotas/${bitola}`)
    return response.data
  },
  
  // Obter linhas ferroviárias (GeoJSON)
  async getLinhasFerroviarias() {
    const response = await api.get('/dados/linhas_ferroviarias.geojson')
    return response.data
  }
}

export default api

