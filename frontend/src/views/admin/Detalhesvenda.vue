<template>
  <DefaultLayout>
    <main class="detalhes-container">
      <h1 class="detalhes-titulo"><i class="fas fa-receipt"></i> Detalhes da Venda</h1>

      <div v-if="!venda" class="texto-centro">Carregando...</div>

      <div v-else class="detalhes-grid">
        <!-- Info da Venda -->
        <div class="detalhes-card">
          <h3><i class="fas fa-info-circle"></i> Informações da Venda</h3>
          <div class="info-list">
            <div class="info-item"><strong>ID da Venda:</strong><span>{{ venda.id_compra }}</span></div>
            <div class="info-item"><strong>Data e Hora:</strong><span>{{ venda.data }}</span></div>
            <div class="info-item"><strong>Produto:</strong><span>{{ venda.nome_produto }}</span></div>
            <div class="info-item">
              <strong>Tipo:</strong>
              <span :class="`badge-tipo ${venda.tipo_produto?.toLowerCase()}`">{{ venda.tipo_produto }}</span>
            </div>
            <div class="info-item"><strong>Quantidade:</strong><span>{{ venda.quantidade }} unidades</span></div>
            <div class="info-item"><strong>Preço Unitário:</strong><span>R$ {{ fmt(venda.preco_unitario) }}</span></div>
            <div class="info-item total"><strong>Valor Total:</strong><span class="valor-total">R$ {{ fmt(venda.valor_total) }}</span></div>
          </div>
        </div>

        <!-- Info do Cliente -->
        <div class="detalhes-card">
          <h3><i class="fas fa-user"></i> Informações do Cliente</h3>
          <div class="info-list">
            <div class="info-item"><strong>Nome:</strong><span>{{ venda.nome_usuario }}</span></div>
            <div class="info-item"><strong>Email:</strong><span>{{ venda.email_usuario }}</span></div>
          </div>
        </div>
      </div>

      <div style="margin-top:24px">
        <router-link to="/admin/dashboard" class="btn-secondary">
          <i class="fas fa-arrow-left"></i> Voltar ao Dashboard
        </router-link>
      </div>
    </main>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

const route = useRoute()
const venda = ref(null)
const fmt   = v => parseFloat(v || 0).toFixed(2).replace('.', ',')

onMounted(async () => {
  const { data } = await api.get(`/admin/vendas/${route.params.id}`)
  venda.value = data
})
</script>