<template>
  <div style="display:flex;align-items:center;justify-content:center;height:100vh;">
    <p style="color:#fff;">Autenticando...</p>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

onMounted(async () => {
  const code = route.query.code
  const provider = route.path.includes('google') ? 'google' : 'facebook'

  if (!code) {
    router.push('/login')
    return
  }

  try {
    const { data } = await api.post('/auth/oauth/callback', { provider, code })
    auth.setAuth(data.token, data.tipo, data.nome)
    router.push(data.tipo === 'admin' ? '/admin' : '/')
  } catch {
    router.push('/login')
  }
})
</script>