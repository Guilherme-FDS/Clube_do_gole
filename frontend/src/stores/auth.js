import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, logout as apiLogout } from '@/services/auth'
import { useCarrinhoStore } from './carrinho'

export const useAuthStore = defineStore('auth', () => {
  const token  = ref(localStorage.getItem('token') || null)
  const nome   = ref(localStorage.getItem('nome')  || null)
  const tipo   = ref(localStorage.getItem('tipo')  || null)
  const userId = ref(localStorage.getItem('user_id') || null)

  const logado = computed(() => !!token.value)

  function init() {
    // já carregado do localStorage acima
  }

  async function entrar(email, senha) {
    const carrinho = useCarrinhoStore()
    const { data } = await apiLogin({ email, senha, guest_id: carrinho.guestId })

    token.value  = data.token
    nome.value   = data.nome
    tipo.value   = data.tipo
    userId.value = String(data.id || '')

    localStorage.setItem('token',   data.token)
    localStorage.setItem('nome',    data.nome)
    localStorage.setItem('tipo',    data.tipo)
    localStorage.setItem('user_id', userId.value)
    localStorage.removeItem('guest_id')

    await carrinho.buscar()
    return data
  }

  async function sair() {
    try { await apiLogout() } catch {}
    token.value  = null
    nome.value   = null
    tipo.value   = null
    userId.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('nome')
    localStorage.removeItem('tipo')
    localStorage.removeItem('user_id')
  }

  return { token, nome, tipo, userId, logado, init, entrar, sair }
})