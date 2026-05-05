<template>
  <div class="dashboard-container">
    <h1 class="dashboard-titulo fade-in" :class="{ visible: fadeInVisible }">
      <i class="fas fa-chart-line"></i> Dashboard de Vendas
    </h1>
    <p class="dashboard-subtitulo fade-in" :class="{ visible: fadeInVisible }">
      Análise completa das vendas do Clube do Gole
    </p>

    <!-- CARDS DE ESTATÍSTICAS -->
    <div class="cards-estatisticas">
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon vendas">
          <i class="fas fa-shopping-cart"></i>
        </div>
        <div class="card-info">
          <h3>Total de Vendas</h3>
          <span class="card-valor">{{ estatisticas.total_vendas }}</span>
          <p>Pedidos realizados</p>
        </div>
      </div>

      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon faturamento">
          <i class="fas fa-money-bill-wave"></i>
        </div>
        <div class="card-info">
          <h3>Faturamento Total</h3>
          <span class="card-valor">{{ formatarMoeda(estatisticas.faturamento_total) }}</span>
          <p>Receita gerada</p>
        </div>
      </div>

      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon clientes">
          <i class="fas fa-users"></i>
        </div>
        <div class="card-info">
          <h3>Clientes Únicos</h3>
          <span class="card-valor">{{ estatisticas.clientes_unicos }}</span>
          <p>Compradores ativos</p>
        </div>
      </div>

      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon ticket">
          <i class="fas fa-receipt"></i>
        </div>
        <div class="card-info">
          <h3>Ticket Médio</h3>
          <span class="card-valor">{{ formatarMoeda(estatisticas.ticket_medio) }}</span>
          <p>Por venda</p>
        </div>
      </div>
    </div>

    <!-- GRÁFICO E PRODUTOS MAIS VENDIDOS -->
    <div class="dashboard-grid">
      <!-- PRODUTOS MAIS VENDIDOS -->
      <div class="dashboard-card fade-in" :class="{ visible: fadeInVisible }">
        <h3><i class="fas fa-trophy"></i> Produtos Mais Vendidos</h3>
        <div class="lista-produtos">
          <div v-for="(dados, produto) in produtosMaisVendidos" :key="produto" class="item-produto">
            <div class="produto-info">
              <strong>{{ produto }}</strong>
              <span>{{ dados.quantidade }} unidades</span>
            </div>
            <div class="produto-valor">
              {{ formatarMoeda(dados.faturamento) }}
            </div>
          </div>
          <p v-if="Object.keys(produtosMaisVendidos).length === 0" class="sem-dados">
            Nenhuma venda registrada ainda.
          </p>
        </div>
      </div>

      <!-- VENDAS POR MÊS -->
      <div class="dashboard-card fade-in" :class="{ visible: fadeInVisible }">
        <h3><i class="fas fa-calendar"></i> Vendas por Mês</h3>
        <div class="lista-meses">
          <div v-for="(dados, mes) in vendasPorMesOrdenadas" :key="mes" class="item-mes">
            <div class="mes-info">
              <strong>{{ formatarMes(mes) }}</strong>
              <span>{{ dados.vendas }} vendas</span>
            </div>
            <div class="mes-valor">
              {{ formatarMoeda(dados.faturamento) }}
            </div>
          </div>
          <p v-if="Object.keys(vendasPorMes).length === 0" class="sem-dados">
            Nenhuma venda por mês registrada.
          </p>
        </div>
      </div>
    </div>

    <!-- ÚLTIMAS VENDAS -->
    <div class="dashboard-card full-width fade-in" :class="{ visible: fadeInVisible }">
      <h3><i class="fas fa-clock"></i> Últimas Vendas</h3>
      <div class="tabela-wrapper">
        <table class="tabela-vendas">
          <thead>
            <tr>
              <th @click="ordenarTabela('data')">Data</th>
              <th @click="ordenarTabela('produto')">Produto</th>
              <th @click="ordenarTabela('tipo')">Tipo</th>
              <th @click="ordenarTabela('quantidade')">Quantidade</th>
              <th @click="ordenarTabela('valor')">Valor</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="venda in ultimasVendasOrdenadas" :key="venda.id_compra">
              <td>{{ formatarData(venda.data) }}</td>
              <td>{{ venda.nome_produto }}</td>
              <td>
                <span :class="['badge-tipo', venda.tipo_produto.toLowerCase()]">
                  {{ venda.tipo_produto }}
                </span>
              </td>
              <td>{{ venda.quantidade }}</td>
              <td>{{ formatarMoeda(venda.valor_total) }}</td>
              <td>
                <router-link :to="`/admin/vendas/${venda.id_compra}`" class="btn-detalhes" title="Ver Detalhes">
                  <i class="fas fa-eye"></i> Detalhes
                </router-link>
              </td>
            </tr>
            <tr v-if="ultimasVendas.length === 0">
              <td colspan="6" class="sem-dados">Nenhuma venda registrada.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- RESUMO POR TIPO DE PRODUTO -->
    <div class="dashboard-card full-width fade-in" :class="{ visible: fadeInVisible }">
      <h3><i class="fas fa-wine-bottle"></i> Resumo por Tipo de Produto</h3>
      <div class="resumo-tipos">
        <div v-for="(dados, tipo) in resumoPorTipo" :key="tipo" class="item-tipo">
          <div class="tipo-info">
            <strong>{{ tipo }}</strong>
            <span>{{ dados.quantidade }} unidades vendidas</span>
          </div>
          <div class="tipo-valor">
            {{ formatarMoeda(dados.faturamento) }}
          </div>
        </div>
        <p v-if="Object.keys(resumoPorTipo).length === 0" class="sem-dados">
          Nenhum dado por tipo disponível.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useDashboardStore } from '@/stores/admin/dashboard'

const dashboardStore = useDashboardStore()

// Estados
const fadeInVisible = ref(false)
const ordenacaoTabela = ref({ coluna: 'data', ordem: 'desc' })

// Dados
const estatisticas = ref({
  total_vendas: 0,
  faturamento_total: 0,
  clientes_unicos: 0,
  ticket_medio: 0
})

const produtosMaisVendidos = ref({})
const vendasPorMes = ref({})
const ultimasVendas = ref([])
const resumoPorTipo = ref({})

// Computed
const vendasPorMesOrdenadas = computed(() => {
  const entries = Object.entries(vendasPorMes.value)
  return Object.fromEntries(entries.sort((a, b) => b[0].localeCompare(a[0])))
})

const ultimasVendasOrdenadas = computed(() => {
  const vendas = [...ultimasVendas.value]
  const { coluna, ordem } = ordenacaoTabela.value
  
  vendas.sort((a, b) => {
    let aValor, bValor
    
    switch (coluna) {
      case 'data':
        aValor = new Date(a.data)
        bValor = new Date(b.data)
        break
      case 'produto':
        aValor = a.nome_produto
        bValor = b.nome_produto
        break
      case 'tipo':
        aValor = a.tipo_produto
        bValor = b.tipo_produto
        break
      case 'quantidade':
        aValor = a.quantidade
        bValor = b.quantidade
        break
      case 'valor':
        aValor = a.valor_total
        bValor = b.valor_total
        break
      default:
        return 0
    }
    
    if (ordem === 'asc') {
      return aValor > bValor ? 1 : -1
    } else {
      return aValor < bValor ? 1 : -1
    }
  })
  
  return vendas
})

// Métodos
const carregarDados = async () => {
  try {
    const data = await dashboardStore.fetchDashboardData()
    estatisticas.value = data.estatisticas
    produtosMaisVendidos.value = data.produtos_mais_vendidos
    vendasPorMes.value = data.vendas_por_mes
    ultimasVendas.value = data.ultimas_vendas
    resumoPorTipo.value = data.resumo_por_tipo
  } catch (error) {
    console.error('Erro ao carregar dashboard:', error)
  }
}

const ordenarTabela = (coluna) => {
  if (ordenacaoTabela.value.coluna === coluna) {
    ordenacaoTabela.value.ordem = ordenacaoTabela.value.ordem === 'asc' ? 'desc' : 'asc'
  } else {
    ordenacaoTabela.value.coluna = coluna
    ordenacaoTabela.value.ordem = 'desc'
  }
}

const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor || 0)
}

const formatarData = (dataString) => {
  if (!dataString) return ''
  const data = new Date(dataString)
  return data.toLocaleDateString('pt-BR') + ' ' + data.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
}

const formatarMes = (mesAno) => {
  const [ano, mes] = mesAno.split('-')
  const data = new Date(ano, parseInt(mes) - 1)
  return data.toLocaleDateString('pt-BR', { month: 'short', year: 'numeric' })
}

// Lifecycle
onMounted(async () => {
  await carregarDados()
  
  setTimeout(() => {
    fadeInVisible.value = true
  }, 100)
})
</script>

<style scoped>
/* ===== LAYOUT DO DASHBOARD ===== */
.dashboard-container {
  max-width: 1400px;
  margin: 100px auto 0;
  padding: 0 var(--espacamento-sm);
}

.dashboard-titulo {
  font-family: var(--fonte-secundaria);
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 600;
  color: var(--cor-dourado);
  text-align: center;
  margin-bottom: var(--espacamento-xs);
}

.dashboard-subtitulo {
  font-family: var(--fonte-principal);
  font-size: 1.125rem;
  color: var(--cor-texto-secundario);
  text-align: center;
  margin-bottom: var(--espacamento-lg);
}

/* ===== CARDS DE ESTATÍSTICAS ===== */
.cards-estatisticas {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--espacamento-md);
  margin-bottom: var(--espacamento-lg);
}

.card-estatistica {
  background: var(--cor-fundo-secundario);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  display: flex;
  align-items: center;
  gap: var(--espacamento-sm);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.card-estatistica::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.1), transparent);
  transition: left 0.5s;
}

.card-estatistica:hover::before {
  left: 100%;
}

.card-estatistica:hover {
  transform: translateY(-8px);
  box-shadow: var(--sombra-destaque);
  border-color: var(--cor-dourado);
}

.card-icon {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  flex-shrink: 0;
  border: 2px solid;
}

.card-icon.vendas { 
  background: linear-gradient(135deg, rgba(76, 175, 80, 0.2) 0%, rgba(76, 175, 80, 0.4) 100%); 
  color: #4CAF50; 
  border-color: #4CAF50;
}

.card-icon.faturamento { 
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.2) 0%, rgba(255, 193, 7, 0.4) 100%); 
  color: #FFC107; 
  border-color: #FFC107;
}

.card-icon.clientes { 
  background: linear-gradient(135deg, rgba(33, 150, 243, 0.2) 0%, rgba(33, 150, 243, 0.4) 100%); 
  color: #2196F3; 
  border-color: #2196F3;
}

.card-icon.ticket { 
  background: linear-gradient(135deg, rgba(156, 39, 176, 0.2) 0%, rgba(156, 39, 176, 0.4) 100%); 
  color: #9C27B0; 
  border-color: #9C27B0;
}

.card-info h3 {
  color: var(--cor-texto);
  margin-bottom: var(--espacamento-xs);
  font-size: 1rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-valor {
  font-size: 2.2rem;
  font-weight: bold;
  color: var(--cor-dourado);
  display: block;
  margin-bottom: var(--espacamento-xs);
  transition: all 0.3s ease-out;
}

.card-info p {
  color: var(--cor-texto-secundario);
  font-size: 0.9rem;
  margin: 0;
  font-weight: 300;
}

/* ===== GRID DO DASHBOARD ===== */
.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--espacamento-md);
  margin-bottom: var(--espacamento-lg);
}

.dashboard-card {
  background: var(--cor-fundo-secundario);
  border: 1px solid rgba(255, 215, 0, 0.1);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  transition: all 0.3s ease;
  position: relative;
}

.dashboard-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradiente-botao);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.dashboard-card:hover::before {
  transform: scaleX(1);
}

.dashboard-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--sombra-destaque);
  border-color: var(--cor-dourado);
}

.dashboard-card.full-width {
  grid-column: 1 / -1;
}

.dashboard-card h3 {
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-md);
  font-size: 1.4rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: var(--espacamento-xs);
}

/* ===== LISTAS E ITENS ===== */
.lista-produtos,
.lista-meses,
.resumo-tipos {
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-sm);
}

.item-produto,
.item-mes,
.item-tipo {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--espacamento-sm);
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-sm);
  border-left: 4px solid var(--cor-dourado);
  transition: all 0.3s ease;
}

.item-produto:hover,
.item-mes:hover,
.item-tipo:hover {
  background: rgba(255, 215, 0, 0.1);
  transform: translateX(5px);
}

.produto-info,
.mes-info,
.tipo-info {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.produto-info strong,
.mes-info strong,
.tipo-info strong {
  color: var(--cor-texto);
  font-weight: 600;
}

.produto-info span,
.mes-info span,
.tipo-info span {
  color: var(--cor-texto-secundario);
  font-size: 0.85rem;
}

.produto-valor,
.mes-valor,
.tipo-valor {
  color: var(--cor-dourado);
  font-weight: bold;
  font-size: 1.1rem;
}

/* ===== TABELA DE VENDAS ===== */
.tabela-wrapper {
  overflow-x: auto;
  border-radius: var(--borda-radius-sm);
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.tabela-vendas {
  width: 100%;
  border-collapse: collapse;
  min-width: 800px;
}

.tabela-vendas th {
  background: linear-gradient(135deg, var(--cor-fundo-secundario) 0%, var(--cor-fundo) 100%);
  color: var(--cor-dourado);
  padding: var(--espacamento-sm);
  text-align: left;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  font-size: 0.9rem;
  border-bottom: 2px solid var(--cor-dourado);
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.tabela-vendas th:hover {
  background: linear-gradient(135deg, var(--cor-fundo) 0%, var(--cor-fundo-secundario) 100%);
}

.tabela-vendas td {
  padding: var(--espacamento-sm);
  border-bottom: 1px solid rgba(255, 215, 0, 0.1);
  color: var(--cor-texto);
}

.tabela-vendas tr:hover td {
  background: rgba(255, 215, 0, 0.05);
}

/* ===== BADGES ===== */
.badge-tipo {
  padding: 0.4rem 1rem;
  border-radius: var(--borda-radius-lg);
  font-size: 0.8rem;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border: 1px solid;
}

.badge-tipo.gold {
  background: linear-gradient(135deg, rgba(255, 215, 0, 0.2) 0%, rgba(255, 215, 0, 0.4) 100%);
  color: #FFD700;
  border-color: #FFD700;
}

.badge-tipo.premium {
  background: linear-gradient(135deg, rgba(138, 43, 226, 0.2) 0%, rgba(138, 43, 226, 0.4) 100%);
  color: #8A2BE2;
  border-color: #8A2BE2;
}

/* ===== BOTÕES ===== */
.btn-detalhes {
  background: var(--gradiente-botao-dourado-claro-escuro);
  color: var(--cor-fundo) !important;
  padding: 0.6rem 1.2rem;
  border-radius: var(--borda-radius-lg);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-detalhes:hover {
  background: var(--gradiente-botao-roxo);
  transform: translateY(-2px);
  box-shadow: var(--sombra-destaque);
}

/* ===== MENSAGENS ===== */
.sem-dados {
  text-align: center;
  color: var(--cor-texto-secundario);
  font-style: italic;
  padding: var(--espacamento-lg);
  font-size: 1.1rem;
}

/* ===== ANIMAÇÕES ===== */
.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease;
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* ===== RESPONSIVIDADE ===== */
@media (max-width: 1024px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .cards-estatisticas {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .dashboard-container {
    margin-top: 120px;
    padding: 0 var(--espacamento-xs);
  }
  
  .cards-estatisticas {
    grid-template-columns: 1fr;
  }
  
  .card-estatistica {
    flex-direction: column;
    text-align: center;
  }
  
  .card-icon {
    width: 70px;
    height: 70px;
    font-size: 1.5rem;
  }
  
  .card-valor {
    font-size: 1.8rem;
  }
}

@media (max-width: 480px) {
  .dashboard-titulo {
    font-size: 1.8rem;
  }
  
  .item-produto,
  .item-mes,
  .item-tipo {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .produto-valor,
  .mes-valor,
  .tipo-valor {
    align-self: flex-end;
  }
}
</style>