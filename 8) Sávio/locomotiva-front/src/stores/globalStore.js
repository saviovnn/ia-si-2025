import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useGlobalStore = defineStore('global', () => {
  // Estado
  const bitola = ref('Larga')
  const algoritmo = ref('a_estrela')
  const origem = ref('')
  const destino = ref('')
  const profundidade = ref(20)
  
  const cidades = ref([])
  
  const rotaAtual = ref(null)
  const loading = ref(false)
  const error = ref(null)
  
  const railwayVisible = ref(true)
  
  // Triggers para ações (substituem emits)
  const buscarRotaTrigger = ref(0)
  const verTodasRotasTrigger = ref({ bitola: null, trigger: 0 })
  const limparMapaTrigger = ref(0)
  const apiError = ref(null)
  const mapReady = ref(false)
  
  // Constantes
  const BITOLA_COLORS = {
    Larga: '#f59e0b',
    Metrica: '#3b82f6',
    Mista: '#8b5cf6',
    Standard: '#10b981',
    Standart: '#10b981' // Mesma cor do Standard
  }
  
  const ALGORITMOS = [
    { value: 'amplitude', label: 'Amplitude' },
    { value: 'bidirecional', label: 'Bidirecional' },
    { value: 'profundidade', label: 'Profundidade' },
    { value: 'prof_limitada', label: 'Prof. Limitada' },
    { value: 'aprofundamento_iterativo', label: 'Aprof. Iterativo' },
    { value: 'custo_uniforme', label: 'Custo Uniforme' },
    { value: 'greedy', label: 'Greedy' },
    { value: 'a_estrela', label: 'A* (A Estrela)' },
    { value: 'aia_estrela', label: 'AIA* (A* Iterativo)' }
  ]
  
  // Computed
  const precisaProfundidade = computed(() => {
    return algoritmo.value === 'prof_limitada' || algoritmo.value === 'aprofundamento_iterativo'
  })
  
  const corBitola = computed(() => {
    return BITOLA_COLORS[bitola.value] || BITOLA_COLORS.Mista
  })
  
  // Actions
  function setBitola(value) {
    bitola.value = value
  }
  
  function setAlgoritmo(value) {
    algoritmo.value = value
  }
  
  function setOrigem(value) {
    origem.value = value
  }
  
  function setDestino(value) {
    destino.value = value
  }
  
  function setProfundidade(value) {
    profundidade.value = value
  }
  
  function setCidades(value) {
    cidades.value = value
  }
  
  function setRotaAtual(rota) {
    rotaAtual.value = rota
  }
  
  function setLoading(value) {
    loading.value = value
  }
  
  function setError(value) {
    error.value = value
  }
  
  function toggleRailwayVisible() {
    railwayVisible.value = !railwayVisible.value
  }
  
  function clearRota() {
    rotaAtual.value = null
    origem.value = ''
    destino.value = ''
  }
  
  // Actions para triggers
  function triggerBuscarRota() {
    buscarRotaTrigger.value++
  }
  
  function triggerVerTodasRotas(bitola) {
    verTodasRotasTrigger.value = {
      bitola,
      trigger: verTodasRotasTrigger.value.trigger + 1
    }
  }
  
  function triggerLimparMapa() {
    limparMapaTrigger.value++
  }
  
  function setApiError(error) {
    apiError.value = error
  }
  
  function clearApiError() {
    apiError.value = null
  }
  
  function setMapReady(value) {
    mapReady.value = value
  }
  
  return {
    // State
    bitola,
    algoritmo,
    origem,
    destino,
    profundidade,
    cidades,
    rotaAtual,
    loading,
    error,
    railwayVisible,
    
    // Triggers
    buscarRotaTrigger,
    verTodasRotasTrigger,
    limparMapaTrigger,
    apiError,
    mapReady,
    
    // Constants
    BITOLA_COLORS,
    ALGORITMOS,
    
    // Computed
    precisaProfundidade,
    corBitola,
    
    // Actions
    setBitola,
    setAlgoritmo,
    setOrigem,
    setDestino,
    setProfundidade,
    setCidades,
    setRotaAtual,
    setLoading,
    setError,
    toggleRailwayVisible,
    clearRota,
    
    // Trigger actions
    triggerBuscarRota,
    triggerVerTodasRotas,
    triggerLimparMapa,
    setApiError,
    clearApiError,
    setMapReady
  }
})

