<!-- views/admin/Pagamentos.vue -->
<template>
  <div class="dashboard-container">
    <BotaoVoltarAdmin />
    <h1 class="dashboard-titulo fade-in" :class="{ visible: fadeInVisible }">
      <i class="fas fa-credit-card"></i> Pagamentos
    </h1>
    <p class="dashboard-subtitulo fade-in" :class="{ visible: fadeInVisible }">
      Histórico e status dos pagamentos — gateway Stripe
    </p>

    <!-- CARDS DE ESTATÍSTICAS -->
    <div class="cards-estatisticas">
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon vendas"><i class="fas fa-check-circle"></i></div>
        <div class="card-info">
          <h3>Aprovados</h3>
          <span class="card-valor">{{ contar('aprovado') }}</span>
          <p>{{ formatarMoeda(somarStatus('aprovado')) }}</p>
        </div>
      </div>
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon faturamento"><i class="fas fa-clock"></i></div>
        <div class="card-info">
          <h3>Pendentes</h3>
          <span class="card-valor">{{ contar('pendente') }}</span>
          <p>{{ formatarMoeda(somarStatus('pendente')) }}</p>
        </div>
      </div>
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon ticket"><i class="fas fa-times-circle"></i></div>
        <div class="card-info">
          <h3>Recusados</h3>
          <span class="card-valor">{{ contar('recusado') }}</span>
          <p>{{ formatarMoeda(somarStatus('recusado')) }}</p>
        </div>
      </div>
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon clientes"><i class="fas fa-undo-alt"></i></div>
        <div class="card-info">
          <h3>Estornados</h3>
          <span class="card-valor">{{ contar('estornado') }}</span>
          <p>{{ formatarMoeda(somarStatus('estornado')) }}</p>
        </div>
      </div>
    </div>

    <!-- FILTROS + BUSCA -->
    <div class="dashboard-card fade-in" :class="{ visible: fadeInVisible }">
      <div class="filtros-row">
        <div class="filtros">
          <button
            v-for="op in statusOpcoes"
            :key="op.valor"
            class="btn-filtro"
            :class="{ ativo: filtroStatus === op.valor }"
            @click="filtroStatus = op.valor"
          >{{ op.label }}</button>
        </div>
        <div class="filtros">
          <button
            v-for="op in metodoOpcoes"
            :key="op.valor"
            class="btn-filtro btn-filtro-sm"
            :class="{ ativo: filtroMetodo === op.valor }"
            @click="filtroMetodo = op.valor"
          >{{ op.label }}</button>
        </div>
        <input
          v-model="busca"
          class="input-busca"
          placeholder="Buscar por ID, venda ou gateway ID..."
          type="text"
        />
      </div>
    </div>

    <!-- TABELA -->
    <div class="dashboard-card fade-in" :class="{ visible: fadeInVisible }">
      <h3><i class="fas fa-list"></i> Transações</h3>
      <div v-if="carregando" class="estado-vazio">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Carregando pagamentos...</p>
      </div>
      <div v-else-if="pagamentosFiltrados.length === 0" class="estado-vazio">
        <i class="fas fa-search"></i>
        <p>Nenhum pagamento encontrado.</p>
      </div>
      <div v-else class="tabela-wrapper">
        <table class="tabela-vendas">
          <thead>
            <tr>
              <th>ID</th>
              <th>Venda</th>
              <th>Assinatura</th>
              <th>Método</th>
              <th>Status</th>
              <th>Valor</th>
              <th>Gateway ID</th>
              <th>Pago em</th>
              <th>Criado em</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in pagamentosFiltrados" :key="p.id">
              <td><span class="id-badge">#{{ p.id }}</span></td>
              <td>
                <router-link
                  v-if="p.id_venda"
                  :to="`/admin/vendas/${p.id_venda}`"
                  class="link-venda"
                >#{{ p.id_venda }}</router-link>
                <span v-else class="sem-dado">—</span>
              </td>
              <td>
                <span v-if="p.id_assinatura" class="badge-assinatura">#{{ p.id_assinatura }}</span>
                <span v-else class="sem-dado">—</span>
              </td>
              <td>
                <span class="badge-metodo" :class="p.metodo">
                  <i :class="iconeMetodo(p.metodo)"></i>
                  {{ labelMetodo(p.metodo) }}
                </span>
              </td>
              <td>
                <span class="badge-status" :class="p.status">{{ p.status }}</span>
              </td>
              <td class="valor-cell">{{ formatarMoeda(p.valor) }}</td>
              <td>
                <span v-if="p.gateway_id" class="gateway-id" :title="p.gateway_id">
                  {{ p.gateway_id.length > 20 ? p.gateway_id.slice(0, 20) + '…' : p.gateway_id }}
                  <a
                    :href="`https://dashboard.stripe.com/payments/${p.gateway_id}`"
                    target="_blank"
                    rel="noopener"
                    class="link-stripe"
                    title="Ver no Stripe"
                  ><i class="fas fa-external-link-alt"></i></a>
                </span>
                <span v-else class="sem-dado">—</span>
              </td>
              <td>{{ p.pago_em ? formatarDataHora(p.pago_em) : '—' }}</td>
              <td>{{ formatarDataHora(p.criado_em) }}</td>
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
import { formatarMoeda, formatarDataHora } from '@/utils/formatters'
import BotaoVoltarAdmin from '@/components/BotaoVoltarAdmin.vue'

const pagamentos = ref([])
const carregando = ref(true)
const fadeInVisible = ref(false)
const filtroStatus = ref('todos')
const filtroMetodo = ref('todos')
const busca = ref('')

const statusOpcoes = [
  { valor: 'todos', label: 'Todos' },
  { valor: 'aprovado', label: 'Aprovados' },
  { valor: 'pendente', label: 'Pendentes' },
  { valor: 'recusado', label: 'Recusados' },
  { valor: 'estornado', label: 'Estornados' },
]

const metodoOpcoes = [
  { valor: 'todos', label: 'Todos' },
  { valor: 'cartao_credito', label: 'Cartão' },
  { valor: 'pix', label: 'PIX' },
  { valor: 'boleto', label: 'Boleto' },
  { valor: 'outro', label: 'Outro' },
]

const pagamentosFiltrados = computed(() => {
  let lista = pagamentos.value
  if (filtroStatus.value !== 'todos') lista = lista.filter(p => p.status === filtroStatus.value)
  if (filtroMetodo.value !== 'todos') lista = lista.filter(p => p.metodo === filtroMetodo.value)
  if (busca.value.trim()) {
    const q = busca.value.trim().toLowerCase()
    lista = lista.filter(p =>
      String(p.id).includes(q) ||
      String(p.id_venda ?? '').includes(q) ||
      (p.gateway_id ?? '').toLowerCase().includes(q)
    )
  }
  return lista
})

function contar(status) {
  return pagamentos.value.filter(p => p.status === status).length
}

function somarStatus(status) {
  return pagamentos.value.filter(p => p.status === status).reduce((acc, p) => acc + parseFloat(p.valor), 0)
}

function iconeMetodo(metodo) {
  const map = { cartao_credito: 'fas fa-credit-card', pix: 'fas fa-qrcode', boleto: 'fas fa-barcode', outro: 'fas fa-ellipsis-h' }
  return map[metodo] ?? 'fas fa-money-bill'
}

function labelMetodo(metodo) {
  const map = { cartao_credito: 'Cartão', pix: 'PIX', boleto: 'Boleto', outro: 'Outro' }
  return map[metodo] ?? metodo
}

onMounted(async () => {
  try {
    const { data } = await api.get('/pagamentos/admin')
    pagamentos.value = data
  } catch {
    console.error('Erro ao carregar pagamentos.')
  } finally {
    carregando.value = false
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
  font-family: var(--fonte-principal);
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
.card-icon.vendas   { background: linear-gradient(135deg,rgba(76,175,80,.2),rgba(76,175,80,.4)); color:#4CAF50; border-color:#4CAF50; }
.card-icon.faturamento { background: linear-gradient(135deg,rgba(255,193,7,.2),rgba(255,193,7,.4)); color:#FFC107; border-color:#FFC107; }
.card-icon.clientes { background: linear-gradient(135deg,rgba(33,150,243,.2),rgba(33,150,243,.4)); color:#2196F3; border-color:#2196F3; }
.card-icon.ticket   { background: linear-gradient(135deg,rgba(156,39,176,.2),rgba(156,39,176,.4)); color:#9C27B0; border-color:#9C27B0; }
.card-info h3  { color: var(--cor-texto); margin-bottom: var(--espacamento-xs); font-size: 1rem; font-weight: 600; text-transform: uppercase; }
.card-valor    { font-size: 2.2rem; font-weight: bold; color: var(--cor-dourado); display: block; margin-bottom: var(--espacamento-xs); }
.card-info p   { color: var(--cor-texto-secundario); font-size: .9rem; margin: 0; }

.dashboard-card {
  background: var(--cor-fundo-secundario);
  border: 1px solid rgba(255,215,0,0.1);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  margin-bottom: var(--espacamento-md);
  transition: all 0.3s ease;
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

.filtros-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--espacamento-sm);
  align-items: center;
}
.filtros { display: flex; gap: 0.5rem; flex-wrap: wrap; }
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
.btn-filtro-sm { padding: .4rem .9rem; font-size: .8rem; }
.btn-filtro:hover, .btn-filtro.ativo {
  background: var(--gradiente-botao);
  color: #000;
  border-color: var(--cor-dourado);
  font-weight: 600;
}
.input-busca {
  flex: 1;
  min-width: 220px;
  padding: .5rem 1rem;
  border-radius: var(--borda-radius-lg);
  border: 1px solid rgba(255,215,0,0.3);
  background: var(--cor-fundo);
  color: var(--cor-texto);
  font-size: .9rem;
  outline: none;
  transition: border-color .3s;
}
.input-busca:focus { border-color: var(--cor-dourado); }

.tabela-wrapper { overflow-x: auto; border-radius: var(--borda-radius-sm); border: 1px solid rgba(255,215,0,.2); }
.tabela-vendas { width: 100%; border-collapse: collapse; min-width: 900px; }
.tabela-vendas th {
  background: var(--cor-fundo-secundario);
  color: var(--cor-dourado);
  padding: var(--espacamento-sm);
  text-align: left;
  font-weight: 600;
  text-transform: uppercase;
  font-size: .85rem;
  border-bottom: 2px solid var(--cor-dourado);
}
.tabela-vendas td { padding: var(--espacamento-sm); border-bottom: 1px solid rgba(255,215,0,.1); color: var(--cor-texto); vertical-align: middle; }
.tabela-vendas tr:hover td { background: rgba(255,215,0,.05); }

.id-badge {
  font-family: monospace;
  background: rgba(201,168,76,.15);
  color: var(--cor-dourado);
  padding: .2rem .6rem;
  border-radius: var(--borda-radius-sm);
  font-size: .85rem;
}
.link-venda {
  color: var(--cor-dourado);
  text-decoration: none;
  font-weight: 600;
}
.link-venda:hover { text-decoration: underline; }
.badge-assinatura {
  background: rgba(156,39,176,.2);
  color: #CE93D8;
  padding: .2rem .6rem;
  border-radius: var(--borda-radius-sm);
  font-size: .8rem;
  font-family: monospace;
}
.sem-dado { color: var(--cor-texto-secundario); }

.badge-metodo {
  display: inline-flex;
  align-items: center;
  gap: .35rem;
  padding: .3rem .8rem;
  border-radius: var(--borda-radius-lg);
  font-size: .8rem;
  font-weight: 600;
  border: 1px solid;
}
.badge-metodo.cartao_credito { background: rgba(33,150,243,.2); color: #64B5F6; border-color: #2196F3; }
.badge-metodo.pix            { background: rgba(0,191,165,.2); color: #80CBC4; border-color: #00BFA5; }
.badge-metodo.boleto         { background: rgba(255,152,0,.2); color: #FFCC80; border-color: #FF9800; }
.badge-metodo.outro          { background: rgba(158,158,158,.2); color: #BDBDBD; border-color: #9E9E9E; }

.badge-status {
  padding: .3rem .8rem;
  border-radius: var(--borda-radius-lg);
  font-size: .8rem;
  font-weight: bold;
  text-transform: uppercase;
  border: 1px solid;
}
.badge-status.aprovado  { background: rgba(76,175,80,.2);  color: #4CAF50; border-color: #4CAF50; }
.badge-status.pendente  { background: rgba(255,193,7,.2);  color: #FFC107; border-color: #FFC107; }
.badge-status.recusado  { background: rgba(244,67,54,.2);  color: #f44336; border-color: #f44336; }
.badge-status.estornado { background: rgba(33,150,243,.2); color: #2196F3; border-color: #2196F3; }

.valor-cell { font-weight: 600; color: var(--cor-dourado-claro); font-family: monospace; }

.gateway-id {
  font-family: monospace;
  font-size: .8rem;
  color: var(--cor-texto-secundario);
  display: inline-flex;
  align-items: center;
  gap: .4rem;
}
.link-stripe {
  color: #635BFF;
  font-size: .75rem;
  text-decoration: none;
  transition: color .2s;
}
.link-stripe:hover { color: #9B97FF; }

.estado-vazio {
  text-align: center;
  padding: var(--espacamento-lg);
  color: var(--cor-texto-secundario);
}
.estado-vazio i { font-size: 2.5rem; margin-bottom: var(--espacamento-sm); color: var(--cor-dourado); opacity: .5; }
.estado-vazio p { font-size: 1rem; }

.fade-in { opacity: 0; transform: translateY(30px); transition: all .6s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }

@media (max-width: 768px) {
  .filtros-row { flex-direction: column; align-items: flex-start; }
  .input-busca { min-width: 100%; }
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
.input-busca { background: #FFFFFF; border: 1px solid #D6D9DE; color: #1B1A19; font-family: inherit; }
.input-busca:focus { border-color: #C9A84C; box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.15); }
.tabela-wrapper { border: 1px solid #E3E5E8; }
.tabela-vendas th { background: #F9FAFB; color: #6B7280; border-bottom: 1px solid #E3E5E8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; }
.tabela-vendas td { color: #1B1A19; border-bottom: 1px solid #F0F1F3; }
.tabela-vendas tr:hover td { background: #FAFAF8; }
.id-badge { background: #F0F1F3; color: #4B5563; }
.link-venda { color: #8A6520; }
.valor-cell { color: #1B1A19; }
.sem-dado { color: #9CA3AF; }
.gateway-id { color: #6B7280; }
.badge-metodo.cartao_credito { background: #EEF4FF; color: #3B6FD4; border-color: #3B6FD4; }
.badge-metodo.pix { background: #E8F7F4; color: #0E8C75; border-color: #0E8C75; }
.badge-metodo.boleto { background: #FFF4E5; color: #C07010; border-color: #C07010; }
.badge-metodo.outro { background: #F0F1F3; color: #6B7280; border-color: #9CA3AF; }
.badge-status.aprovado { background: #EBF8F0; color: #2E8B57; border-color: #2E8B57; }
.badge-status.pendente { background: #FFF8E5; color: #B8860B; border-color: #B8860B; }
.badge-status.recusado { background: #FEF2F2; color: #DC2626; border-color: #DC2626; }
.badge-status.estornado { background: #EEF4FF; color: #3B6FD4; border-color: #3B6FD4; }
.estado-vazio { color: #9CA3AF; }
.estado-vazio i { color: #C9A84C; }
</style>
