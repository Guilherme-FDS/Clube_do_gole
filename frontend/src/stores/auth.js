// stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, logout as apiLogout, oauthCallback, me as apiMe } from '@/services/auth'
import { useCarrinhoStore } from './carrinho'

const INATIVIDADE_MS = 30 * 60 * 1000 // 30 minutos

// Detecta dispositivo móvel — não aplica timeout em mobile
const _isMobile = () =>
  typeof navigator !== 'undefined' &&
  /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent)

export const useAuthStore = defineStore('auth', () => {
  const token  = ref(localStorage.getItem('token')   || null)
  const nome   = ref(localStorage.getItem('nome')    || null)
  const tipo   = ref(localStorage.getItem('tipo')    || null)
  const userId = ref(localStorage.getItem('user_id') || null)

  const logado = computed(() => !!token.value)

  // ── Inatividade ────────────────────────────────────────────────────────────
  let _inativTimer  = null
  let _inativSetup  = false

  function _resetarTimer() {
    if (_inativTimer) clearTimeout(_inativTimer)
    _inativTimer = setTimeout(() => sair(), INATIVIDADE_MS)
  }

  function _iniciarInatividade() {
    if (_isMobile() || _inativSetup) return
    _inativSetup = true
    const eventos = ['mousemove', 'keydown', 'click', 'scroll']
    eventos.forEach(ev => window.addEventListener(ev, _resetarTimer, { passive: true }))
    _resetarTimer()
  }

  function _pararInatividade() {
    if (_inativTimer) { clearTimeout(_inativTimer); _inativTimer = null }
    // Não remove os listeners (tornaria necessário guardar referência); chamar
    // sair() em estado deslogado é inofensivo.
  }
  // ───────────────────────────────────────────────────────────────────────────

  function _salvar(data) {
    token.value  = data.token
    nome.value   = data.nome
    tipo.value   = data.tipo
    userId.value = String(data.id || '')

    localStorage.setItem('token',   data.token)
    localStorage.setItem('nome',    data.nome)
    localStorage.setItem('tipo',    data.tipo)
    localStorage.setItem('user_id', userId.value)
    localStorage.removeItem('guest_id')

    _iniciarInatividade()
  }

  async function init() {
    if (token.value) {
      try {
        const { data } = await apiMe()
        nome.value   = data.nome
        tipo.value   = data.tipo
        userId.value = String(data.id || '')
        localStorage.setItem('nome',    data.nome)
        localStorage.setItem('tipo',    data.tipo)
        localStorage.setItem('user_id', userId.value)
        _iniciarInatividade()
      } catch (err) {
        // Só limpa auth em erros explícitos de autenticação (token inválido/expirado).
        // Erros de rede (backend dormindo) não invalidam o token — mantém o estado atual.
        const status = err?.response?.status
        if (status === 401 || status === 403) {
          token.value  = null
          nome.value   = null
          tipo.value   = null
          userId.value = null
          localStorage.removeItem('token')
          localStorage.removeItem('nome')
          localStorage.removeItem('tipo')
          localStorage.removeItem('user_id')
          _pararInatividade()
        }
      }
    }
  }

  async function entrar(email, senha) {
    const carrinho = useCarrinhoStore()
    const { data } = await apiLogin({
      email,
      senha,
      guest_carrinho: carrinho.itens || [],
    })
    _salvar(data)
    await carrinho.buscar()
    return data
  }

  async function entrarOAuth(code, provider) {
    const carrinho = useCarrinhoStore()
    const { data } = await oauthCallback(
      code,
      provider,
      carrinho.itens || [],
    )
    _salvar(data)
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
    _pararInatividade()
  }

  return { token, nome, tipo, userId, logado, init, entrar, entrarOAuth, sair }
})
