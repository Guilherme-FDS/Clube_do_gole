import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/services/api'

export const useDashboardStore = defineStore('adminDashboard', () => {
  const loading = ref(false)
  const error = ref(null)

  async function fetchDashboardData() {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/admin/dashboard')
      return response.data
    } catch (err) {
      error.value = err.message
      console.error('Erro ao buscar dados do dashboard:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  async function fetchVendasPorPeriodo(inicio, fim) {
    loading.value = true
    
    try {
      const response = await api.get('/admin/dashboard/vendas', {
        params: { inicio, fim }
      })
      return response.data
    } catch (err) {
      console.error('Erro ao buscar vendas por período:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    error,
    fetchDashboardData,
    fetchVendasPorPeriodo
  }
})