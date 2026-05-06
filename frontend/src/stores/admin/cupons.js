import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useCuponsAdminStore = defineStore('adminCupons', () => {
  const cupons = ref([])
  const loading = ref(false)

  async function fetchCupons() {
    loading.value = true
    try {
      const response = await api.get('/admin/cupons')
      cupons.value = response.data
      return cupons.value
    } catch (error) {
      console.error('Erro ao buscar cupons:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function adicionarCupom(dados) {
    try {
      const response = await api.post('/admin/cupons', dados)
      return response.data
    } catch (error) {
      console.error('Erro ao adicionar cupom:', error)
      throw error
    }
  }

  async function alterarStatus(id, novoStatus) {
    try {
      const response = await api.put(`/admin/cupons/${id}/status`, { status: novoStatus })
      return response.data
    } catch (error) {
      console.error('Erro ao alterar status:', error)
      throw error
    }
  }

  async function excluirCupom(id) {
    try {
      await api.delete(`/admin/cupons/${id}`)
    } catch (error) {
      console.error('Erro ao excluir cupom:', error)
      throw error
    }
  }

  return {
    cupons,
    loading,
    fetchCupons,
    adicionarCupom,
    alterarStatus,
    excluirCupom
  }
})