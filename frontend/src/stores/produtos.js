// src/stores/produtos.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
// import { getProdutos } from '@/services/produtos' // se tiver API

export const useProdutosStore = defineStore('produtos', () => {
  const produtosGold = ref([])
  const produtosPremium = ref([])
  const loading = ref(false)

  async function fetchProdutos() {
    loading.value = true
    try {
      // 🔁 Substitua pela sua API real quando tiver
      // const { data } = await getProdutos({ categoria: 'gold' })
      // produtosGold.value = data
      
      // Mock para teste (substitua depois)
      produtosGold.value = [
        { 
          id: 1, 
          nome: 'Box Gold - Edição Especial', 
          descricao: 'Seleção premium com 3 bebidas exclusivas', 
          preco: 199.90, 
          imagem: null 
        },
        { 
          id: 2, 
          nome: 'Box Gold - Coleção Clássica', 
          descricao: 'Os melhores rótulos selecionados para você', 
          preco: 249.90, 
          imagem: null 
        }
      ]
      
      produtosPremium.value = [
        { 
          id: 3, 
          nome: 'Box Premium - Coleção Master', 
          descricao: 'Experiência única com 5 bebidas selecionadas', 
          preco: 399.90, 
          imagem: null 
        },
        { 
          id: 4, 
          nome: 'Box Premium - Edição Limitada', 
          descricao: 'Garrafas exclusivas e brinde especial', 
          preco: 499.90, 
          imagem: null 
        }
      ]
    } catch (error) {
      console.error('Erro ao carregar produtos:', error)
    } finally {
      loading.value = false
    }
  }

  return { produtosGold, produtosPremium, loading, fetchProdutos }
})