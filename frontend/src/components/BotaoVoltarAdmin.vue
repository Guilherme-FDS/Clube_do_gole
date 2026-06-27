<template>
  <button class="btn-voltar-admin" @click="voltar">
    <i class="fas fa-arrow-left"></i>
    {{ label }}
  </button>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  to: { type: String, default: '/admin' },
  label: { type: String, default: 'Voltar' }
})

const router = useRouter()
const voltar = () => router.push(props.to)
</script>

<style scoped>
.btn-voltar-admin {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: #FDF6E5;
  border: 1px solid #C9A84C;
  color: #8A6520;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
  margin-bottom: 16px;
}

.btn-voltar-admin:hover {
  background: #8A6520;
  border-color: #8A6520;
  color: #FFFFFF;
}
</style>
