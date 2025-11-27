// Serviço para gerenciar IndexedDB
const DB_NAME = 'LocomotivaDB'
const DB_VERSION = 2

const STORES = {
  CIDADES: 'cidades',
  COORDENADAS: 'coordenadas',
  LINHAS_FERROVIARIAS: 'linhas_ferroviarias'
}

let db = null

// Inicializar banco de dados
export async function initDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB_NAME, DB_VERSION)
    
    request.onerror = () => {
      console.error('Erro ao abrir IndexedDB:', request.error)
      reject(request.error)
    }
    
    request.onsuccess = () => {
      db = request.result
      resolve(db)
    }
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result
      
      // Store para cidades por bitola
      if (!db.objectStoreNames.contains(STORES.CIDADES)) {
        const cidadesStore = db.createObjectStore(STORES.CIDADES, { keyPath: 'bitola' })
        cidadesStore.createIndex('bitola', 'bitola', { unique: true })
      }
      
      // Store para coordenadas de cidades
      if (!db.objectStoreNames.contains(STORES.COORDENADAS)) {
        const coordenadasStore = db.createObjectStore(STORES.COORDENADAS, { keyPath: 'cidade' })
        coordenadasStore.createIndex('cidade', 'cidade', { unique: true })
      }
      
      // Store para linhas ferroviárias (GeoJSON)
      if (!db.objectStoreNames.contains(STORES.LINHAS_FERROVIARIAS)) {
        db.createObjectStore(STORES.LINHAS_FERROVIARIAS, { keyPath: 'id' })
      }
    }
  })
}

// Obter instância do banco
async function getDB() {
  if (!db) {
    await initDB()
  }
  return db
}

// Salvar cidades por bitola
export async function saveCidades(bitola, cidades) {
  try {
    const database = await getDB()
    const transaction = database.transaction([STORES.CIDADES], 'readwrite')
    const store = transaction.objectStore(STORES.CIDADES)
    
    return new Promise((resolve, reject) => {
      const request = store.put({
        bitola,
        cidades,
        timestamp: Date.now()
      })
      
      request.onsuccess = () => resolve(true)
      request.onerror = () => {
        console.error('Erro ao salvar cidades no IndexedDB:', request.error)
        reject(request.error)
      }
    })
  } catch (error) {
    console.error('Erro ao salvar cidades no IndexedDB:', error)
    return false
  }
}

// Obter cidades por bitola
export async function getCidades(bitola) {
  try {
    const database = await getDB()
    const transaction = database.transaction([STORES.CIDADES], 'readonly')
    const store = transaction.objectStore(STORES.CIDADES)
    
    return new Promise((resolve, reject) => {
      const request = store.get(bitola)
      
      request.onsuccess = () => {
        const result = request.result
        if (result && result.cidades) {
          // Verificar se o cache não está muito antigo (30 dias - dados estáticos)
          const cacheAge = Date.now() - result.timestamp
          const maxAge = 30 * 24 * 60 * 60 * 1000 // 30 dias
          
          // Verificar se os dados parecem estar incompletos (apenas SP)
          // Se mais de 50% das cidades são de SP, provavelmente é cache antigo
          const spCities = result.cidades.filter(c => c.endsWith('_SP'))
          const spPercentage = result.cidades.length > 0 ? (spCities.length / result.cidades.length) * 100 : 0
          
          // Se mais de 50% são de SP e há menos de 500 cidades, provavelmente é cache antigo
          // (para bitola Larga esperamos ~851 cidades, Metrica ~1127)
          const isLikelyIncomplete = spPercentage > 50 && result.cidades.length < 500
          
          // Se o cache é válido e não está incompleto, sempre usar
          if (cacheAge < maxAge && !isLikelyIncomplete && result.cidades.length > 0) {
            resolve(result.cidades)
          } else {
            // Cache expirado ou incompleto - limpar e buscar novamente
            if (isLikelyIncomplete) {
              console.log('Cache parece incompleto (muitas cidades de SP), forçando atualização...')
              // Limpar cache para esta bitola
              clearCidadesCacheForBitola(bitola)
            }
            resolve(null)
          }
        } else {
          resolve(null)
        }
      }
      
      request.onerror = () => {
        reject(request.error)
      }
    })
  } catch (error) {
    console.error('Erro ao obter cidades do IndexedDB:', error)
    return null
  }
}

// Limpar cache de cidades para uma bitola específica
export async function clearCidadesCacheForBitola(bitola) {
  try {
    const database = await getDB()
    const transaction = database.transaction([STORES.CIDADES], 'readwrite')
    const store = transaction.objectStore(STORES.CIDADES)
    
    return new Promise((resolve, reject) => {
      const request = store.delete(bitola)
      
      request.onsuccess = () => resolve(true)
      request.onerror = () => {
        console.error('Erro ao limpar cache de cidades para bitola:', request.error)
        reject(request.error)
      }
    })
  } catch (error) {
    console.error('Erro ao limpar cache de cidades para bitola:', error)
    return false
  }
}

// Salvar coordenadas de uma cidade
export async function saveCoordenadas(cidade, coordenadas) {
  try {
    const database = await getDB()
    const transaction = database.transaction([STORES.COORDENADAS], 'readwrite')
    const store = transaction.objectStore(STORES.COORDENADAS)
    
    return new Promise((resolve, reject) => {
      const request = store.put({
        cidade,
        ...coordenadas,
        timestamp: Date.now()
      })
      
      request.onsuccess = () => resolve(true)
      request.onerror = () => {
        console.error('Erro ao salvar coordenadas no IndexedDB:', request.error)
        reject(request.error)
      }
    })
  } catch (error) {
    console.error('Erro ao salvar coordenadas no IndexedDB:', error)
    return false
  }
}

// Obter coordenadas de uma cidade
export async function getCoordenadas(cidade) {
  try {
    const database = await getDB()
    const transaction = database.transaction([STORES.COORDENADAS], 'readonly')
    const store = transaction.objectStore(STORES.COORDENADAS)
    
    return new Promise((resolve, reject) => {
      const request = store.get(cidade)
      
      request.onsuccess = () => {
        const result = request.result
        if (result) {
          // Coordenadas não expiram (são dados estáticos)
          const { cidade: _, timestamp: __, ...coordenadas } = result
          resolve(coordenadas)
        } else {
          resolve(null)
        }
      }
      
      request.onerror = () => {
        reject(request.error)
      }
    })
  } catch (error) {
    console.error('Erro ao obter coordenadas do IndexedDB:', error)
    return null
  }
}

// Limpar cache de cidades
export async function clearCidadesCache() {
  try {
    const database = await getDB()
    const transaction = database.transaction([STORES.CIDADES], 'readwrite')
    const store = transaction.objectStore(STORES.CIDADES)
    
    return new Promise((resolve, reject) => {
      const request = store.clear()
      
      request.onsuccess = () => resolve(true)
      request.onerror = () => {
        console.error('Erro ao limpar cache de cidades:', request.error)
        reject(request.error)
      }
    })
  } catch (error) {
    console.error('Erro ao limpar cache de cidades:', error)
    return false
  }
}

// Limpar cache de coordenadas
export async function clearCoordenadasCache() {
  try {
    const database = await getDB()
    const transaction = database.transaction([STORES.COORDENADAS], 'readwrite')
    const store = transaction.objectStore(STORES.COORDENADAS)
    
    return new Promise((resolve, reject) => {
      const request = store.clear()
      
      request.onsuccess = () => resolve(true)
      request.onerror = () => {
        console.error('Erro ao limpar cache de coordenadas:', request.error)
        reject(request.error)
      }
    })
  } catch (error) {
    console.error('Erro ao limpar cache de coordenadas:', error)
    return false
  }
}

// Salvar linhas ferroviárias (GeoJSON)
export async function saveLinhasFerroviarias(geojson) {
  try {
    const database = await getDB()
    const transaction = database.transaction([STORES.LINHAS_FERROVIARIAS], 'readwrite')
    const store = transaction.objectStore(STORES.LINHAS_FERROVIARIAS)
    
    return new Promise((resolve, reject) => {
      const request = store.put({
        id: 'linhas_ferroviarias',
        geojson,
        timestamp: Date.now()
      })
      
      request.onsuccess = () => resolve(true)
      request.onerror = () => {
        console.error('Erro ao salvar linhas ferroviárias no IndexedDB:', request.error)
        reject(request.error)
      }
    })
  } catch (error) {
    console.error('Erro ao salvar linhas ferroviárias no IndexedDB:', error)
    return false
  }
}

// Obter linhas ferroviárias (GeoJSON)
export async function getLinhasFerroviarias() {
  try {
    const database = await getDB()
    const transaction = database.transaction([STORES.LINHAS_FERROVIARIAS], 'readonly')
    const store = transaction.objectStore(STORES.LINHAS_FERROVIARIAS)
    
    return new Promise((resolve, reject) => {
      const request = store.get('linhas_ferroviarias')
      
      request.onsuccess = () => {
        const result = request.result
        if (result && result.geojson) {
          // Verificar se o cache não está muito antigo (7 dias - dados estáticos)
          const cacheAge = Date.now() - result.timestamp
          const maxAge = 7 * 24 * 60 * 60 * 1000 // 7 dias
          
          if (cacheAge < maxAge) {
            resolve(result.geojson)
          } else {
            // Cache expirado
            resolve(null)
          }
        } else {
          resolve(null)
        }
      }
      
      request.onerror = () => {
        reject(request.error)
      }
    })
  } catch (error) {
    console.error('Erro ao obter linhas ferroviárias do IndexedDB:', error)
    return null
  }
}

// Limpar cache de linhas ferroviárias
export async function clearLinhasFerroviariasCache() {
  try {
    const database = await getDB()
    const transaction = database.transaction([STORES.LINHAS_FERROVIARIAS], 'readwrite')
    const store = transaction.objectStore(STORES.LINHAS_FERROVIARIAS)
    
    return new Promise((resolve, reject) => {
      const request = store.clear()
      
      request.onsuccess = () => resolve(true)
      request.onerror = () => {
        console.error('Erro ao limpar cache de linhas ferroviárias:', request.error)
        reject(request.error)
      }
    })
  } catch (error) {
    console.error('Erro ao limpar cache de linhas ferroviárias:', error)
    return false
  }
}

// Limpar todo o cache
export async function clearAllCache() {
  try {
    await clearCidadesCache()
    await clearCoordenadasCache()
    await clearLinhasFerroviariasCache()
    return true
  } catch (error) {
    console.error('Erro ao limpar todo o cache:', error)
    return false
  }
}

