import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ver, adicionar, remover, atualizarQtd, contador } from '@/services/carrinho'

export const useCarrinhoStore = defineStore('carrinho', () => {
  const itens   = ref([])
  const total   = ref(0)
  const count   = ref(0)
  const guestId = ref(localStorage.getItem('guest_id') || null)

  function _ensureGuest() {
    if (!guestId.value) {
      guestId.value = crypto.randomUUID()
      localStorage.setItem('guest_id', guestId.value)
    }
  }

  async function init() {
    _ensureGuest()
    await buscar()
  }

  async function buscar() {
    try {
      const { data } = await ver()
      itens.value = data.itens
      total.value = data.total
      count.value = data.itens.length
    } catch {}
  }

  async function add(produto_id, plano, quantidade = 1) {
    _ensureGuest()
    const { data } = await adicionar({ produto_id, plano, quantidade })
    count.value = data.count
    await buscar()
    return data
  }

  async function remove(ids) {
    await remover(Array.isArray(ids) ? ids : [ids])
    await buscar()
  }

  async function atualizarQuantidade(item_id, quantidade) {
    const { data } = await atualizarQtd({ item_id, quantidade })
    await buscar()
    return data
  }

  const isEmpty = computed(() => itens.value.length === 0)

  return { itens, total, count, guestId, isEmpty, init, buscar, add, remove, atualizarQuantidade }
})