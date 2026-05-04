<template>
  <DefaultLayout>
    <div class="container" style="margin-top: 120px; min-height: 60vh;">
      <h1 class="titulo-lg">Meus Pedidos</h1>

      <div v-if="carregando" class="texto-centro">Carregando...</div>

      <div v-else-if="vendas.length" class="pedidos-lista">
        <div class="pedido-card" v-for="venda in vendas" :key="venda.id">
          <div class="pedido-info">
            <h3>{{ venda.nome_produto }}</h3>
            <p>Quantidade: {{ venda.quantidade }}</p>
            <p>Total: R$ {{ fmt(venda.valor_total) }}</p>
            <p>Data: {{ venda.data }}</p>
          </div>
        </div>
      </div>

      <div v-else class="texto-centro">
        <p>Você ainda não fez nenhum pedido.</p>
        <router-link to="/#planos" class="btn-modern">Conhecer Planos</router-link>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { meusPedidos } from '@/services/carrinho'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const vendas    = ref([])
const carregando = ref(true)

function fmt(v) { return parseFloat(v || 0).toFixed(2).replace('.', ',') }

onMounted(async () => {
  try {
    const { data } = await meusPedidos()
    vendas.value = data
  } finally {
    carregando.value = false
  }
})
</script>