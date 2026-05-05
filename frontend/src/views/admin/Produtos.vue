import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useProdutosAdminStore = defineStore('adminProdutos', () => {
  const produtos = ref([])
  const loading = ref(false)

  async function fetchProdutos() {
    loading.value = true
    try {
      const response = await api.get('/admin/produtos')
      produtos.value = response.data
      return produtos.value
    } catch (error) {
      console.error('Erro ao buscar produtos:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function adicionarProduto(dados) {
    try {
      const response = await api.post('/admin/produtos', dados)
      return response.data
    } catch (error) {
      console.error('Erro ao adicionar produto:', error)
      throw error
    }
  }

  async function atualizarProduto(id, dados) {
    try {
      const response = await api.put(`/admin/produtos/${id}`, dados)
      return response.data
    } catch (error) {
      console.error('Erro ao atualizar produto:', error)
      throw error
    }
  }

  async function excluirProduto(id) {
    try {
      await api.delete(`/admin/produtos/${id}`)
    } catch (error) {
      console.error('Erro ao excluir produto:', error)
      throw error
    }
  }

  return {
    produtos,
    loading,
    fetchProdutos,
    adicionarProduto,
    atualizarProduto,
    excluirProduto
  }
})