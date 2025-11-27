<template>
  <Transition name="toast">
    <div v-if="visible" :class="['toast', type]">
      <div class="toast-content">
        <div class="toast-title">{{ title }}</div>
        <div class="toast-message">{{ message }}</div>
      </div>
      <button class="toast-close" @click="close">&times;</button>
    </div>
  </Transition>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

const props = defineProps({
  type: {
    type: String,
    default: 'error',
    validator: (value) => ['success', 'error', 'warning', 'info'].includes(value)
  },
  title: {
    type: String,
    required: true
  },
  message: {
    type: String,
    required: true
  },
  duration: {
    type: Number,
    default: 5000
  }
})

const emit = defineEmits(['close'])

const visible = ref(false)

onMounted(() => {
  visible.value = true
  
  if (props.duration > 0) {
    setTimeout(() => {
      close()
    }, props.duration)
  }
})

function close() {
  visible.value = false
  setTimeout(() => {
    emit('close')
  }, 300)
}
</script>

<style scoped>
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #dc2626;
  color: white;
  padding: 16px 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 10000;
  max-width: 400px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.toast.success {
  background: #059669;
}

.toast.warning {
  background: #d97706;
}

.toast.info {
  background: #06b6d4;
}

.toast-content {
  flex: 1;
}

.toast-title {
  font-weight: 600;
  margin-bottom: 4px;
}

.toast-message {
  font-size: 14px;
  opacity: 0.9;
}

.toast-close {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 0;
  margin-left: 8px;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.toast-close:hover {
  opacity: 1;
}

.toast-enter-active {
  transition: transform 0.3s ease-in-out;
}

.toast-leave-active {
  transition: transform 0.3s ease-in-out;
}

.toast-enter-from {
  transform: translateX(100%);
}

.toast-enter-to {
  transform: translateX(0);
}

.toast-leave-from {
  transform: translateX(0);
}

.toast-leave-to {
  transform: translateX(100%);
}
</style>

