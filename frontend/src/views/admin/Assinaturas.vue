<template>
  <div class="dashboard-container">
    <BotaoVoltarAdmin />
    <h1 class="dashboard-titulo fade-in" :class="{ visible: fadeInVisible }">
      <i class="fas fa-repeat"></i> Assinaturas
    </h1>
    <p class="dashboard-subtitulo fade-in" :class="{ visible: fadeInVisible }">
      Gerencie as assinaturas ativas dos clientes
    </p>

    <!-- CARDS -->
    <div class="cards-estatisticas">
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon vendas"><i class="fas fa-check-circle"></i></div>
        <div class="card-info">
          <h3>Ativas</h3>
          <span class="card-valor">{{ contarStatus('ativa') }}</span>
          <p>Assinaturas em dia</p>
        </div>
      </div>
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon faturamento"><i class="fas fa-pause-circle"></i></div>
        <div class="card-info">
          <h3>Pausadas</h3>
          <span class="card-valor">{{ contarStatus('pausada') }}</span>
          <p>Temporariamente paradas</p>
        </div>
      </div>
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon ticket"><i class="fas fa-times-circle"></i></div>
        <div class="card-info">
          <h3>Canceladas</h3>
          <span class="card-valor">{{ contarStatus('cancelada') }}</span>
          <p>Encerradas</p>
        </div>
      </div>
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon clientes"><i class="fas fa-list"></i></div>
        <div class="card-info">
          <h3>Total</h3>
          <span class="card-valor">{{ assinaturas.length }}</span>
          <p>Todas as assinaturas</p>
        </div>
      </div>
    </div>

    <!-- FILTRO -->
    <div class="dashboard-card fade-in" :class="{ visible: fadeInVisible }">
      <div class="filtros">
        <button v-for="s in statusOpcoes" :key="s.valor" class="btn-filtro"
          :class="{ ativo: filtroStatus === s.valor }" @click="filtroStatus = s.valor">
          {{ s.label }}
        </button>
      </div>
    </div>

    <!-- TABELA -->
    <div class="dashboard-card full-width fade-in" :class="{ visible: fadeInVisible }">
      <h3><i class="fas fa-table"></i> Lista de Assinaturas</h3>
      <div class="tabela-wrapper">
        <table class="tabela-vendas">
          <thead>
            <tr>
              <th>#</th>
              <th>Cliente ID</th>
              <th>Produto ID</th>
              <th>Plano</th>
              <th>Status</th>
              <th>Início</th>
              <th>Próximo Ciclo</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="a in assinaturasFiltradas" :key="a.id">
              <td>{{ a.id }}</td>
              <td>{{ a.id_cliente }}</td>
              <td>{{ a.id_produto ?? '—' }}</td>
              <td><span class="badge-plano" :class="a.plano">{{ a.plano }}</span></td>
              <td><span class="badge-status" :class="a.status">{{ a.status }}</span></td>
              <td>{{ formatarData(a.data_inicio) }}</td>
              <td>{{ a.proximo_ciclo ? formatarData(a.proximo_ciclo) : '—' }}</td>
              <td>
                <div class="acoes">
                  <button v-if="a.status === 'ativa'" class="btn-acao pausar"
                    @click="alterarStatus(a, 'pausada')" title="Pausar">
                    <i class="fas fa-pause"></i>
                  </button>
                  <button v-if="a.status === 'pausada'" class="btn-acao reativar"
                    @click="alterarStatus(a, 'ativa')" title="Reativar">
                    <i class="fas fa-play"></i>
                  </button>
                  <button v-if="a.status !== 'cancelada'" class="btn-acao cancelar"
                    @click="alterarStatus(a, 'cancelada')" title="Cancelar">
                    <i class="fas fa-ban"></i>
                  </button>
                  <span v-if="a.status === 'cancelada'" class="sem-acao">—</span>
                </div>
              </td>
            </tr>
            <tr v-if="assinaturasFiltradas.length === 0">
              <td colspan="8" class="sem-dados">Nenhuma assinatura encontrada.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import BotaoVoltarAdmin from '@/components/BotaoVoltarAdmin.vue'

const assinaturas = ref([])
const fadeInVisible = ref(false)
const filtroStatus = ref('todos')

const statusOpcoes = [
  { valor: 'todos',     label: 'Todos' },
  { valor: 'ativa',     label: 'Ativas' },
  { valor: 'pausada',   label: 'Pausadas' },
  { valor: 'cancelada', label: 'Canceladas' },
  { valor: 'expirada',  label: 'Expiradas' },
]

const assinaturasFiltradas = computed(() => {
  if (filtroStatus.value === 'todos') return assinaturas.value
  return assinaturas.value.filter(a => a.status === filtroStatus.value)
})

function contarStatus(status) {
  return assinaturas.value.filter(a => a.status === status).length
}

function formatarData(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('pt-BR')
}

async function alterarStatus(assinatura, novoStatus) {
  const mensagens = {
    pausada:   'Pausar esta assinatura?',
    ativa:     'Reativar esta assinatura?',
    cancelada: 'Cancelar esta assinatura? Esta ação não pode ser desfeita.',
  }
  if (!confirm(mensagens[novoStatus])) return
  try {
    await api.patch(`/assinaturas/admin/${assinatura.id}/status`, { status: novoStatus })
    assinatura.status = novoStatus
  } catch {
    alert('Erro ao atualizar status da assinatura.')
  }
}

onMounted(async () => {
  try {
    const { data } = await api.get('/assinaturas/admin')
    assinaturas.value = data
  } catch {
    console.error('Erro ao carregar assinaturas.')
  }
  setTimeout(() => { fadeInVisible.value = true }, 100)
})
</script>

<style scoped>
.dashboard-container {
  max-width: 1400px;
  margin: 100px auto 0;
  padding: 0 var(--espacamento-sm);
}
.dashboard-titulo {
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 600;
  color: var(--cor-dourado);
  text-align: center;
  margin-bottom: var(--espacamento-xs);
}
.dashboard-subtitulo {
  font-size: 1.125rem;
  color: var(--cor-texto-secundario);
  text-align: center;
  margin-bottom: var(--espacamento-lg);
}
.cards-estatisticas {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--espacamento-md);
  margin-bottom: var(--espacamento-lg);
}
.card-estatistica {
  background: var(--cor-fundo-secundario);
  border: 1px solid rgba(255,215,0,0.2);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  display: flex;
  align-items: center;
  gap: var(--espacamento-sm);
  transition: all 0.3s ease;
}
.card-estatistica:hover {
  transform: translateY(-8px);
  box-shadow: var(--sombra-destaque);
  border-color: var(--cor-dourado);
}
.card-icon {
  width: 80px; height: 80px;
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 2rem; flex-shrink: 0; border: 2px solid;
}
.card-icon.vendas    { background: linear-gradient(135deg,rgba(76,175,80,.2),rgba(76,175,80,.4));   color:#4CAF50; border-color:#4CAF50; }
.card-icon.faturamento { background: linear-gradient(135deg,rgba(255,193,7,.2),rgba(255,193,7,.4)); color:#FFC107; border-color:#FFC107; }
.card-icon.clientes  { background: linear-gradient(135deg,rgba(33,150,243,.2),rgba(33,150,243,.4)); color:#2196F3; border-color:#2196F3; }
.card-icon.ticket    { background: linear-gradient(135deg,rgba(156,39,176,.2),rgba(156,39,176,.4)); color:#9C27B0; border-color:#9C27B0; }
.card-info h3 { color:var(--cor-texto); margin-bottom:var(--espacamento-xs); font-size:1rem; font-weight:600; text-transform:uppercase; }
.card-valor { font-size:2.2rem; font-weight:bold; color:var(--cor-dourado); display:block; margin-bottom:var(--espacamento-xs); }
.card-info p { color:var(--cor-texto-secundario); font-size:.9rem; margin:0; }

.dashboard-card {
  background: var(--cor-fundo-secundario);
  border: 1px solid rgba(255,215,0,0.1);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  margin-bottom: var(--espacamento-md);
}
.dashboard-card h3 { color:var(--cor-dourado); margin-bottom:var(--espacamento-md); font-size:1.4rem; font-weight:600; display:flex; align-items:center; gap:var(--espacamento-xs); }

.filtros { display:flex; gap:var(--espacamento-sm); flex-wrap:wrap; }
.btn-filtro {
  padding: .5rem 1.2rem;
  border-radius: var(--borda-radius-lg);
  border: 1px solid rgba(255,215,0,0.3);
  background: transparent;
  color: var(--cor-texto-secundario);
  cursor: pointer;
  transition: all .3s;
  font-size: .9rem;
}
.btn-filtro:hover, .btn-filtro.ativo {
  background: var(--gradiente-botao);
  color: #000;
  border-color: var(--cor-dourado);
  font-weight: 600;
}

.tabela-wrapper { overflow-x:auto; border-radius:var(--borda-radius-sm); border:1px solid rgba(255,215,0,.2); }
.tabela-vendas { width:100%; border-collapse:collapse; min-width:800px; }
.tabela-vendas th { background:var(--cor-fundo-secundario); color:var(--cor-dourado); padding:var(--espacamento-sm); text-align:left; font-weight:600; text-transform:uppercase; font-size:.9rem; border-bottom:2px solid var(--cor-dourado); }
.tabela-vendas td { padding:var(--espacamento-sm); border-bottom:1px solid rgba(255,215,0,.1); color:var(--cor-texto); }
.tabela-vendas tr:hover td { background:rgba(255,215,0,.05); }

.badge-status, .badge-plano {
  padding:.3rem .8rem; border-radius:var(--borda-radius-lg);
  font-size:.8rem; font-weight:bold; text-transform:uppercase; border:1px solid;
}
.badge-status.ativa     { background:rgba(76,175,80,.2);  color:#4CAF50; border-color:#4CAF50; }
.badge-status.pausada   { background:rgba(255,193,7,.2);  color:#FFC107; border-color:#FFC107; }
.badge-status.cancelada { background:rgba(244,67,54,.2);  color:#f44336; border-color:#f44336; }
.badge-status.expirada  { background:rgba(158,158,158,.2);color:#9e9e9e; border-color:#9e9e9e; }
.badge-plano.mensal    { background:rgba(33,150,243,.2);  color:#2196F3; border-color:#2196F3; }
.badge-plano.semestral { background:rgba(156,39,176,.2);  color:#9C27B0; border-color:#9C27B0; }
.badge-plano.anual     { background:rgba(255,215,0,.2);   color:#FFD700; border-color:#FFD700; }

.acoes { display:flex; gap:.5rem; align-items:center; }
.btn-acao {
  width: 32px; height: 32px;
  border-radius: 50%;
  border: 1px solid;
  cursor: pointer;
  font-size: .8rem;
  display: flex; align-items: center; justify-content: center;
  transition: all .25s;
}
.btn-acao.pausar   { background:rgba(255,193,7,.15);  color:#FFC107; border-color:#FFC107; }
.btn-acao.reativar { background:rgba(76,175,80,.15);  color:#4CAF50; border-color:#4CAF50; }
.btn-acao.cancelar { background:rgba(244,67,54,.15);  color:#f44336; border-color:#f44336; }
.btn-acao:hover { transform:scale(1.15); opacity:.85; }
.sem-acao { color:var(--cor-texto-secundario); }
.sem-dados { text-align:center; color:var(--cor-texto-secundario); font-style:italic; padding:var(--espacamento-lg); }

.fade-in { opacity:0; transform:translateY(30px); transition:all .6s ease; }
.fade-in.visible { opacity:1; transform:translateY(0); }

@media (max-width:768px) {
  .dashboard-container { margin-top:120px; }
  .cards-estatisticas { grid-template-columns:1fr; }
  .card-estatistica { flex-direction:column; text-align:center; }
}

/* ===== ERP LIGHT THEME (sobrescreve o tema escuro acima) ===== */
.dashboard-container {
  max-width: none;
  margin: 80px 0 0;
  padding: 30px max(24px, calc((100% - 1100px) / 2)) 60px;
  background: #F4F5F7;
  min-height: 100vh;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
}
.dashboard-titulo { font-family: 'DM Sans', 'Segoe UI', sans-serif; font-size: 22px; color: #1B1A19; text-align: left; font-weight: 700; margin-bottom: 2px; }
.dashboard-titulo i { color: #C9A84C; font-size: 18px; margin-right: 6px; }
.dashboard-subtitulo { font-family: inherit; font-size: 13px; color: #6B7280; text-align: left; margin-bottom: 24px; }
.dashboard-card,
.card-estatistica { background: #FFFFFF; border: 1px solid #E3E5E8; border-radius: 10px; box-shadow: none; }
.dashboard-card:hover,
.card-estatistica:hover { transform: none; box-shadow: 0 4px 14px rgba(27, 26, 25, 0.07); border-color: #C9A84C; }
.dashboard-card h3 { color: #1B1A19; font-family: inherit; font-size: 14px; font-weight: 600; }
.dashboard-card h3 i { color: #C9A84C; }
.card-icon { width: 52px; height: 52px; font-size: 1.2rem; border-width: 1px; }
.card-info h3 { color: #6B7280; font-size: 12px; letter-spacing: 0.05em; }
.card-valor { color: #1B1A19; font-size: 1.5rem; font-weight: 700; }
.card-info p { color: #9CA3AF; font-size: 12px; }
.btn-filtro { background: #FFFFFF; border: 1px solid #D6D9DE; color: #4B5563; font-family: inherit; }
.btn-filtro:hover,
.btn-filtro.ativo { background: #FDF6E5; border-color: #C9A84C; color: #8A6520; }
.tabela-wrapper { border: 1px solid #E3E5E8; }
.tabela-vendas th { background: #F9FAFB; color: #6B7280; border-bottom: 1px solid #E3E5E8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; }
.tabela-vendas td { color: #1B1A19; border-bottom: 1px solid #F0F1F3; }
.tabela-vendas tr:hover td { background: #FAFAF8; }
.badge-status.ativa { background: #EBF8F0; color: #2E8B57; border-color: #2E8B57; }
.badge-status.pausada { background: #FFF8E5; color: #B8860B; border-color: #B8860B; }
.badge-status.cancelada { background: #FEF2F2; color: #DC2626; border-color: #DC2626; }
.badge-status.expirada { background: #F0F1F3; color: #6B7280; border-color: #9CA3AF; }
.badge-plano.mensal { background: #FDF6E5; color: #8A6520; border-color: #C9A84C; }
.badge-plano.semestral { background: #F3EEFD; color: #7B2FE0; border-color: #7B2FE0; }
.badge-plano.anual { background: #EBEBEA; color: #1B1A19; border-color: #1B1A19; }
.btn-acao.pausar { background: #FFF8E5; color: #B8860B; border-color: #B8860B; }
.btn-acao.reativar { background: #EBF8F0; color: #2E8B57; border-color: #2E8B57; }
.btn-acao.cancelar { background: #FEF2F2; color: #DC2626; border-color: #DC2626; }
.sem-acao { color: #9CA3AF; }
.sem-dados { color: #9CA3AF; }
</style>