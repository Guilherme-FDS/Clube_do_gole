<template>
  <div class="reset-container">
    <div class="reset-box">
      <h2>Redefinir Senha</h2>

      <div v-if="sucesso" class="msg-sucesso">
        Senha redefinida com sucesso! <br />
        <router-link to="/login">Fazer login</router-link>
      </div>

      <div v-else-if="erro" class="msg-erro">{{ erro }}</div>

      <form v-else @submit.prevent="submeter">
        <input
          v-model="novaSenha"
          type="password"
          placeholder="Nova senha"
          required
          minlength="6"
        />
        <input
          v-model="confirmar"
          type="password"
          placeholder="Confirmar senha"
          required
        />
        <button type="submit" :disabled="carregando">
          {{ carregando ? 'Salvando...' : 'Redefinir senha' }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

const novaSenha = ref('')
const confirmar = ref('')
const carregando = ref(false)
const sucesso = ref(false)
const erro = ref('')
const token = ref('')

onMounted(() => {
  token.value = route.query.token
  if (!token.value) erro.value = 'Token inválido ou expirado.'
})

async function submeter() {
  if (novaSenha.value !== confirmar.value) {
    erro.value = 'As senhas não coincidem.'
    return
  }
  carregando.value = true
  try {
    await api.post('/auth/redefinir-senha', {
      token: token.value,
      nova_senha: novaSenha.value,
    })
    sucesso.value = true
  } catch (e) {
    erro.value = e?.response?.data?.detail || 'Erro ao redefinir senha.'
  } finally {
    carregando.value = false
  }
}
</script>

<style scoped>
.reset-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: var(--bg, #0e0e0e);
}
.reset-box {
  background: #1a1a1a;
  border: 1px solid #333;
  border-radius: 12px;
  padding: 2rem;
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
h2 { color: #c9a84c; margin: 0; }
input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid #444;
  background: #111;
  color: #fff;
  font-size: 0.95rem;
  box-sizing: border-box;
}
button {
  padding: 0.75rem;
  background: #c9a84c;
  color: #000;
  border: none;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
}
button:disabled { opacity: 0.6; cursor: not-allowed; }
.msg-sucesso { color: #4caf50; }
.msg-erro { color: #f44336; }
a { color: #c9a84c; }
</style>