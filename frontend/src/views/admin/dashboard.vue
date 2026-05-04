<template>
  <DefaultLayout>
    <main class="dashboard-container">
      <h1 class="dashboard-titulo fade-in"><i class="fas fa-chart-line"></i> Dashboard de Vendas</h1>
      <p class="dashboard-subtitulo fade-in">Análise completa das vendas do Clube do Gole</p>

      <div v-if="carregando" class="texto-centro">Carregando...</div>

      <template v-else>
        <!-- Cards -->
        <div class="cards-estatisticas">
          <div class="card-estatistica fade-in" v-for="card in cards" :key="card.titulo">
            <div :class="`card-icon ${card.cls}`"><i :class="card.icone"></i></div>
            <div class="card-info">
              <h3>{{ card.titulo }}</h3>
              <span class="card-valor">{{ card.valor }}</span>
              <p>{{ card.sub }}</p>
            </div>
          </div>
        </div>

        <!-- Grid -->
        <div class="dashboard-grid">
          <div class="dashboard-card fade-in">
            <h3><i class="fas fa-trophy"></i> Produtos Mais Vendidos</h3>
            <div class="lista-produtos">
              <div v-if="dados.produtos_mais_vendidos?.length" v-for="[nome, d] in dados.produtos_mais_vendidos" :key="nome" class="item-produto">
                <div class="produto-info"><strong>{{ nome }}</strong><span>{{ d.quantidade }} unidades</span></div>
                <div class="produto-valor">R$ {{ fmt(d.faturamento) }}</div>
              </div>
              <p v-else class="sem-dados">Nenhuma venda registrada ainda.</p>
            </div>
          </div>

          <div class="dashboard-card fade-in">
            <h3><i class="fas fa-calendar"></i> Vendas por Mês</h3>
            <div class="lista-meses">
              <div v-if="mesesOrdenados.length" v-for="[mes, d] in mesesOrdenados" :key="mes" class="item-mes">
                <div class="mes-info"><strong>{{ mes.slice(5,7) }}/{{ mes.slice(0,4) }}</strong><span>{{ d.vendas }} vendas</span></div>
                <div class="mes-valor">R$ {{ fmt(d.faturamento) }}</div>
              </div>
              <p v-else class="sem-dados">Nenhuma venda por mês registrada.</p>
            </div>
          </div>
        </div>

        <!-- Últimas vendas -->
        <div class="dashboard-card full-width fade-in">
          <h3><i class="fas fa-clock"></i> Últimas Vendas</h3>
          <div class="tabela-wrapper">
            <table class="tabela-vendas">
              <thead>
                <tr><th>Data</th><th>Produto</th><th>Tipo</th><th>Quantidade</th><th>Valor</th><th>Ações</th></tr>
              </thead>
              <tbody>
                <tr v-if="!dados.ultimas_vendas?.length"><td colspan="6" class="sem-dados">Nenhuma venda registrada.</td></tr>
                <tr v-for="v in dados.ultimas_vendas" :key="v.id_compra">
                  <td>{{ v.data?.slice(0,16) }}</td>
                  <td>{{ v.nome_produto }}</td>
                  <td><span :class="`badge-tipo ${v.tipo_produto?.toLowerCase()}`">{{ v.tipo_produto }}</span></td>
                  <td>{{ v.quantidade }}</td>
                  <td>R$ {{ fmt(v.valor_total) }}</td>
                  <td>
                    <router-link :to="`/admin/vendas/${v.id_compra}`" class="btn-detalhes">
                      <i class="fas fa-eye"></i> Detalhes
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Resumo por tipo -->
        <div class="dashboard-card full-width fade-in">
          <h3><i class="fas fa-wine-bottle"></i> Resumo por Tipo de Produto</h3>
          <div class="resumo-tipos">
            <div v-if="resumoTipos.length" v-for="[tipo, d] in resumoTipos" :key="tipo" class="item-tipo">
              <div class="tipo-info"><strong>{{ tipo }}</strong><span>{{ d.quantidade }} unidades vendidas</span></div>
              <div class="tipo-valor">R$ {{ fmt(d.faturamento) }}</div>
            </div>
            <p v-else class="sem-dados">Nenhum dado por tipo disponível.</p>
          </div>
        </div>
      </template>
    </main>
  </DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

const dados     = ref({})
const carregando = ref(true)

const fmt = v => parseFloat(v || 0).toFixed(2).replace('.', ',')

const ticketMedio = computed(() => {
  const t = dados.value.total_vendas
  return t > 0 ? dados.value.faturamento_total / t : 0
})

const cards = computed(() => [
  { titulo: 'Total de Vendas',    cls: 'vendas',    icone: 'fas fa-shopping-cart',   valor: dados.value.total_vendas || 0,                sub: 'Pedidos realizados' },
  { titulo: 'Faturamento Total',  cls: 'faturamento', icone: 'fas fa-money-bill-wave', valor: `R$ ${fmt(dados.value.faturamento_total)}`, sub: 'Receita gerada' },
  { titulo: 'Clientes Únicos',    cls: 'clientes',  icone: 'fas fa-users',           valor: dados.value.clientes_unicos || 0,             sub: 'Compradores ativos' },
  { titulo: 'Ticket Médio',       cls: 'ticket',    icone: 'fas fa-receipt',         valor: `R$ ${fmt(ticketMedio.value)}`,               sub: 'Por venda' },
])

const mesesOrdenados = computed(() => {
  if (!dados.value.vendas_por_mes) return []
  return Object.entries(dados.value.vendas_por_mes).sort(([a], [b]) => b.localeCompare(a))
})

const resumoTipos = computed(() => {
  const vendas = dados.value.ultimas_vendas || []
  const mapa = {}
  vendas.forEach(v => {
    const t = v.tipo_produto
    if (!mapa[t]) mapa[t] = { quantidade: 0, faturamento: 0 }
    mapa[t].quantidade  += parseInt(v.quantidade || 0)
    mapa[t].faturamento += parseFloat(v.valor_total || 0)
  })
  return Object.entries(mapa)
})

onMounted(async () => {
  const { data } = await api.get('/admin/dashboard')
  dados.value = data
  carregando.value = false
})
</script>