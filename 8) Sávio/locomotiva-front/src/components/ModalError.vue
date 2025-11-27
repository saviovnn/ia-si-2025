<template>
  <Transition name="modal">
    <div v-if="visible" class="modal-error" @click.self="close">
      <div class="modal-error-content">
        <div class="modal-error-header">
          <h3 class="modal-error-title">API Fora do Ar</h3>
          <button class="modal-error-close" @click="close">&times;</button>
        </div>
        <div class="modal-error-body">
          <p>A API da Locomotiva não está respondendo. Siga as instruções abaixo para iniciar o servidor:</p>
          
          <h3>Instruções de Instalação e Execução</h3>
          <p><strong>PRÉ-REQUISITOS:</strong></p>
          <ul>
            <li>Python 3.8+ instalado</li>
            <li>Terminal/Command Prompt</li>
          </ul>
          
          <p><strong>INSTALAÇÃO:</strong></p>
          <ol>
            <li>Abra o terminal na pasta do prototipo</li>
            <li>Execute: <code>python -m venv venv</code></li>
            <li>Execute: <code>venv\\Scripts\\activate</code> (Windows) ou <code>source venv/bin/activate</code> (Mac/Linux)</li>
            <li>Execute: <code>pip install -r requirements.txt</code></li>
          </ol>
          
          <p><strong>EXECUÇÃO:</strong></p>
          <ol>
            <li>Abra um terminal na pasta raiz do projeto</li>
            <li>Execute a API: <code>uvicorn main:app --reload</code> (na pasta locomotiva-api)</li>
            <li>Abra outro terminal na pasta <code>locomotiva-front</code></li>
            <li>Execute o frontend: <code>npm run dev</code></li>
            <li>Abra o navegador em: <code>http://localhost:5173</code></li>
          </ol>
          
          <p><strong>NOTAS:</strong></p>
          <ul>
            <li>A API roda na porta 8000</li>
            <li>O frontend roda na porta 5173</li>
            <li>API info: http://localhost:8000 (opcional)</li>
            <li>Frontend: http://localhost:5173</li>
            <li>Para parar os servidores, pressione Ctrl+C nos terminais</li>
          </ul>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { watch, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible', 'close'])

function close() {
  emit('update:visible', false)
  emit('close')
}

function handleEscape(e) {
  if (e.key === 'Escape' && props.visible) {
    close()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleEscape)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleEscape)
})
</script>

<style scoped>
.modal-error {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10001;
}

.modal-error-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  max-width: 500px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  position: relative;
}

.modal-error-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #e2e8f0;
}

.modal-error-title {
  font-size: 18px;
  font-weight: 600;
  color: #dc2626;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.modal-error-close {
  background: none;
  border: none;
  font-size: 24px;
  color: #6b7280;
  cursor: pointer;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-error-close:hover {
  color: #374151;
}

.modal-error-body {
  color: #374151;
  line-height: 1.6;
}

.modal-error-body h3 {
  color: #1e293b;
  font-size: 16px;
  font-weight: 600;
  margin: 16px 0 8px 0;
}

.modal-error-body h3:first-child {
  margin-top: 0;
}

.modal-error-body p {
  margin: 0 0 12px 0;
}

.modal-error-body p:last-child {
  margin-bottom: 0;
}

.modal-error-body code {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  color: #1e293b;
}

.modal-error-body ul,
.modal-error-body ol {
  margin: 8px 0;
  padding-left: 20px;
}

.modal-error-body li {
  margin: 4px 0;
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>

