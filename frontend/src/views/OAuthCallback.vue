<template>
  <div class="oauth-wrap">
    <div class="oauth-card">
      <div v-if="!erro">
        <div class="spinner"></div>
        <p class="msg">Autenticando com {{ providerNome }}…</p>
        <p class="sub">Aguarde, isso pode levar alguns instantes.</p>
      </div>
      <div v-else class="erro-box">
        <p class="msg erro-txt">Falha ao autenticar</p>
        <p class="sub">{{ erro }}</p>
        <button class="btn-voltar" @click="$router.push('/login')">Voltar ao login</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const route  = useRoute()
const auth   = useAuthStore()

const erro = ref('')
const provider = route.path.includes('google') ? 'google' : 'facebook'
const providerNome = computed(() => provider === 'google' ? 'Google' : 'Facebook')

onMounted(async () => {
  const code = route.query.code

  if (!code) {
    erro.value = 'Código de autorização ausente. Tente novamente.'
    return
  }

  try {
    const { data } = await api.post('/auth/oauth/callback', { provider, code })
    auth.setAuth(data.token, data.tipo, data.nome)
    router.push(data.tipo === 'admin' ? '/admin' : '/')
  } catch (e) {
    const msg = e?.response?.data?.detail
    erro.value = msg || 'Não foi possível completar o login. Tente novamente.'
  }
})
</script>

<style scoped>
.oauth-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #0d0d0d;
}
.oauth-card {
  background: #1a1a1a;
  border: 1px solid #2a2a2a;
  border-radius: 12px;
  padding: 48px 40px;
  text-align: center;
  min-width: 300px;
}
.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #333;
  border-top-color: #c9a84c;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 24px;
}
@keyframes spin { to { transform: rotate(360deg); } }
.msg {
  color: #f0e6d0;
  font-size: 1.1rem;
  font-weight: 600;
  margin: 0 0 8px;
}
.sub {
  color: #888;
  font-size: 0.875rem;
  margin: 0;
}
.erro-box { display: flex; flex-direction: column; align-items: center; gap: 12px; }
.erro-txt { color: #e57373; }
.btn-voltar {
  margin-top: 8px;
  padding: 10px 24px;
  background: #c9a84c;
  color: #0d0d0d;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  font-size: 0.9rem;
}
.btn-voltar:hover { background: #b8963e; }
</style>
