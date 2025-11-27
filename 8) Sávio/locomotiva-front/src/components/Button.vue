<template>
  <button
    :class="['btn', variant, size, { disabled: disabled, loading: loading }]"
    :disabled="disabled || loading"
    @click="$emit('click', $event)"
  >
    <span v-if="loading" class="loading-spinner"></span>
    <slot></slot>
  </button>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'danger', 'info'].includes(value)
  },
  size: {
    type: String,
    default: 'medium',
    validator: (value) => ['small', 'medium', 'large'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])
</script>

<style scoped>
.btn {
  background: #3b82f6;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background-color 0.2s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.btn:hover:not(.disabled):not(:disabled) {
  background: #2563eb;
}

.btn.disabled,
.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Variantes */
.btn.secondary {
  background: #6b7280;
}

.btn.secondary:hover:not(.disabled):not(:disabled) {
  background: #4b5563;
}

.btn.success {
  background: #10b981;
}

.btn.success:hover:not(.disabled):not(:disabled) {
  background: #059669;
}

.btn.danger {
  background: #ef4444;
}

.btn.danger:hover:not(.disabled):not(:disabled) {
  background: #dc2626;
}

.btn.info {
  background: #06b6d4;
}

.btn.info:hover:not(.disabled):not(:disabled) {
  background: #0891b2;
}

/* Tamanhos */
.btn.small {
  padding: 6px 8px;
  font-size: 12px;
}

.btn.medium {
  padding: 8px 16px;
  font-size: 14px;
}

.btn.large {
  padding: 12px 24px;
  font-size: 16px;
  font-weight: 600;
}

.btn.full {
  width: 100%;
}
</style>

