import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

export const useProdutosStore = defineStore('produtos', () => {
  const produtos = ref([])
  const loading = ref(false)

  async function fetchProdutos() {
    loading.value = true
    try {
      const response = await api.get('/produtos/')
      produtos.value = response.data
    } catch (error) {
      console.error('Erro ao buscar produtos:', error)
      produtos.value = []
    } finally {
      loading.value = false
    }
  }

  const produtosGold = computed(() =>
    produtos.value.filter(p => p.tipo?.toLowerCase() === 'gold')
  )

  const produtosPremium = computed(() =>
    produtos.value.filter(p => p.tipo?.toLowerCase() === 'premium')
  )

  return { produtos, loading, fetchProdutos, produtosGold, produtosPremium }
})