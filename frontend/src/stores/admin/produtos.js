import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useProdutosAdminStore = defineStore('adminProdutos', () => {
  const produtos = ref([])
  const loading = ref(false)

  // ── Produtos ──────────────────────────────────────────────────────────
  async function fetchProdutos() {
    loading.value = true
    try {
      const { data } = await api.get('/admin/produtos')
      produtos.value = data
      return data
    } finally {
      loading.value = false
    }
  }

  async function adicionarProduto(dados) {
    const { data } = await api.post('/admin/produtos', dados)
    return data
  }

  async function atualizarProduto(id, dados) {
    const { data } = await api.put(`/admin/produtos/${id}`, dados)
    return data
  }

  async function excluirProduto(id) {
    await api.delete(`/admin/produtos/${id}`)
  }

  async function alterarStatusProduto(id, ativo) {
    const { data } = await api.patch(`/admin/produtos/${id}/status`, { ativo })
    return data
  }

  // ── Planos ────────────────────────────────────────────────────────────
  async function fetchPlanos(produtoId) {
    const { data } = await api.get(`/admin/produtos/${produtoId}/planos`)
    return data
  }

  async function adicionarPlano(produtoId, dados) {
    const { data } = await api.post(`/admin/produtos/${produtoId}/planos`, dados)
    return data
  }

  async function atualizarPlano(planoId, dados) {
    const { data } = await api.put(`/admin/planos/${planoId}`, dados)
    return data
  }

  async function excluirPlano(planoId) {
    await api.delete(`/admin/planos/${planoId}`)
  }

  async function alterarStatusPlano(planoId, ativo) {
    const { data } = await api.patch(`/admin/planos/${planoId}/status`, { ativo })
    return data
  }

  return {
    produtos,
    loading,
    fetchProdutos,
    adicionarProduto,
    atualizarProduto,
    excluirProduto,
    alterarStatusProduto,
    fetchPlanos,
    adicionarPlano,
    atualizarPlano,
    excluirPlano,
    alterarStatusPlano,
  }
})
