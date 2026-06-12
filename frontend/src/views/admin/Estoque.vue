<!-- views/admin/Estoque.vue -->
<template>
  <div class="dashboard-container">
    <BotaoVoltarAdmin />
    <h1 class="dashboard-titulo fade-in" :class="{ visible: fadeInVisible }">
      <i class="fas fa-boxes"></i> Estoque
    </h1>
    <p class="dashboard-subtitulo fade-in" :class="{ visible: fadeInVisible }">
      Movimentações de estoque e saldo atual por produto
    </p>

    <!-- CARDS -->
    <div class="cards-estatisticas">
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon vendas"><i class="fas fa-arrow-circle-down"></i></div>
        <div class="card-info">
          <h3>Entradas</h3>
          <span class="card-valor">{{ contar('entrada') }}</span>
          <p>movimentações</p>
        </div>
      </div>
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon ticket"><i class="fas fa-arrow-circle-up"></i></div>
        <div class="card-info">
          <h3>Saídas</h3>
          <span class="card-valor">{{ contar('saida') }}</span>
          <p>movimentações</p>
        </div>
      </div>
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon faturamento"><i class="fas fa-sliders-h"></i></div>
        <div class="card-info">
          <h3>Ajustes</h3>
          <span class="card-valor">{{ contar('ajuste') }}</span>
          <p>movimentações</p>
        </div>
      </div>
      <div class="card-estatistica fade-in" :class="{ visible: fadeInVisible }">
        <div class="card-icon clientes"><i class="fas fa-layer-group"></i></div>
        <div class="card-info">
          <h3>Total</h3>
          <span class="card-valor">{{ movimentacoes.length }}</span>
          <p>registros</p>
        </div>
      </div>
    </div>

    <!-- NOVA MOVIMENTAÇÃO -->
    <div class="dashboard-card fade-in" :class="{ visible: fadeInVisible }">
      <h3><i class="fas fa-plus-circle"></i> Nova Movimentação</h3>
      <div class="form-movimentacao">
        <select v-model="form.tipo" class="input-form">
          <option value="entrada">Entrada</option>
          <option value="saida">Saída</option>
          <option value="ajuste">Ajuste</option>
        </select>
        <select v-model="form.id_produto" class="input-form">
          <option value="" disabled>Selecionar produto...</option>
          <option v-for="p in produtos" :key="p.id" :value="p.id">
            {{ p.nome }} (saldo: {{ saldoPorProduto[p.id] ?? 0 }})
          </option>
        </select>
        <input
          v-model.number="form.quantidade"
          type="number"
          min="1"
          class="input-form input-qtd"
          placeholder="Quantidade"
        />
        <input
          v-model="form.motivo"
          type="text"
          class="input-form"
          :placeholder="form.tipo === 'ajuste' ? 'Motivo do ajuste...' : 'Motivo (opcional)'"
        />
        <button
          class="btn-registrar"
          :class="form.tipo"
          :disabled="enviando || !form.id_produto || !form.quantidade"
          @click="registrar"
        >
          <i v-if="enviando" class="fas fa-spinner fa-spin"></i>
          <i v-else :class="iconeAcao(form.tipo)"></i>
          {{ labelAcao(form.tipo) }}
        </button>
      </div>
      <p v-if="erroForm" class="erro-form">{{ erroForm }}</p>
      <p v-if="successoForm" class="sucesso-form">{{ successoForm }}</p>
    </div>

    <!-- FILTROS -->
    <div class="dashboard-card fade-in" :class="{ visible: fadeInVisible }">
      <div class="filtros-row">
        <div class="filtros">
          <button
            v-for="op in tipoOpcoes"
            :key="op.valor"
            class="btn-filtro"
            :class="{ ativo: filtroTipo === op.valor }"
            @click="filtroTipo = op.valor"
          >{{ op.label }}</button>
        </div>
        <input
          v-model="busca"
          class="input-busca"
          placeholder="Buscar por produto..."
          type="text"
        />
      </div>
    </div>

    <!-- TABELA -->
    <div class="dashboard-card fade-in" :class="{ visible: fadeInVisible }">
      <h3><i class="fas fa-history"></i> Histórico de Movimentações</h3>
      <div v-if="carregando" class="estado-vazio">
        <i class="fas fa-spinner fa-spin"></i>
        <p>Carregando movimentações...</p>
      </div>
      <div v-else-if="movsFiltradas.length === 0" class="estado-vazio">
        <i class="fas fa-search"></i>
        <p>Nenhuma movimentação encontrada.</p>
      </div>
      <div v-else class="tabela-wrapper">
        <table class="tabela-vendas">
          <thead>
            <tr>
              <th>ID</th>
              <th>Produto</th>
              <th>Tipo</th>
              <th>Qtd</th>
              <th>Saldo Anterior</th>
              <th>Saldo Posterior</th>
              <th>Motivo</th>
              <th>Venda</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in movsFiltradas" :key="m.id">
              <td><span class="id-badge">#{{ m.id }}</span></td>
              <td class="nome-produto">{{ m.nome_produto ?? '—' }}</td>
              <td>
                <span class="badge-tipo" :class="m.tipo">
                  <i :class="iconeTipo(m.tipo)"></i>
                  {{ m.tipo }}
                </span>
              </td>
              <td>
                <span class="qtd-cell" :class="m.tipo">
                  {{ m.tipo === 'saida' ? '-' : m.tipo === 'entrada' ? '+' : '=' }}{{ m.quantidade }}
                </span>
              </td>
              <td class="saldo-cell">{{ m.saldo_anterior }}</td>
              <td>
                <span class="saldo-posterior" :class="{ baixo: m.saldo_posterior <= 3 }">
                  {{ m.saldo_posterior }}
                  <i v-if="m.saldo_posterior <= 3" class="fas fa-exclamation-triangle aviso-estoque" title="Estoque baixo"></i>
                </span>
              </td>
              <td class="motivo-cell">{{ m.motivo || '—' }}</td>
              <td>
                <router-link
                  v-if="m.id_venda"
                  :to="`/admin/vendas/${m.id_venda}`"
                  class="link-venda"
                >#{{ m.id_venda }}</router-link>
                <span v-else class="sem-dado">—</span>
              </td>
              <td>{{ formatarDataHora(m.criado_em) }}</td>
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
import { formatarDataHora } from '@/utils/formatters'
import BotaoVoltarAdmin from '@/components/BotaoVoltarAdmin.vue'

const movimentacoes = ref([])
const produtos = ref([])
const carregando = ref(true)
const fadeInVisible = ref(false)
const filtroTipo = ref('todos')
const busca = ref('')
const enviando = ref(false)
const erroForm = ref('')
const successoForm = ref('')

const form = ref({ tipo: 'entrada', id_produto: '', quantidade: null, motivo: '' })

const tipoOpcoes = [
  { valor: 'todos', label: 'Todos' },
  { valor: 'entrada', label: 'Entradas' },
  { valor: 'saida', label: 'Saídas' },
  { valor: 'ajuste', label: 'Ajustes' },
]

// Saldo derivado da última movimentação de cada produto (estoque não vive mais em Produto)
const saldoPorProduto = computed(() => {
  const mapa = {}
  for (const m of movimentacoes.value) {
    if (!(m.id_produto in mapa)) mapa[m.id_produto] = m.saldo_posterior
  }
  return mapa
})

const movsFiltradas = computed(() => {
  let lista = movimentacoes.value
  if (filtroTipo.value !== 'todos') lista = lista.filter(m => m.tipo === filtroTipo.value)
  if (busca.value.trim()) {
    const q = busca.value.trim().toLowerCase()
    lista = lista.filter(m => (m.nome_produto ?? '').toLowerCase().includes(q))
  }
  return lista
})

function contar(tipo) {
  return movimentacoes.value.filter(m => m.tipo === tipo).length
}

function iconeTipo(tipo) {
  return { entrada: 'fas fa-arrow-down', saida: 'fas fa-arrow-up', ajuste: 'fas fa-equals' }[tipo] ?? 'fas fa-circle'
}

function iconeAcao(tipo) {
  return { entrada: 'fas fa-plus', saida: 'fas fa-minus', ajuste: 'fas fa-edit' }[tipo] ?? 'fas fa-check'
}

function labelAcao(tipo) {
  return { entrada: 'Registrar Entrada', saida: 'Registrar Saída', ajuste: 'Aplicar Ajuste' }[tipo] ?? 'Registrar'
}

async function registrar() {
  erroForm.value = ''
  successoForm.value = ''
  if (!form.value.id_produto || !form.value.quantidade) return
  enviando.value = true
  try {
    const payload = {
      id_produto: form.value.id_produto,
      quantidade: form.value.quantidade,
      motivo: form.value.motivo || undefined,
    }
    await api.post(`/estoque/admin/${form.value.tipo}`, payload)
    successoForm.value = `${labelAcao(form.value.tipo)} registrada com sucesso.`
    form.value = { tipo: form.value.tipo, id_produto: '', quantidade: null, motivo: '' }
    // recarregar movimentações e produtos
    const [movs, prods] = await Promise.all([
      api.get('/estoque/admin'),
      api.get('/produtos/admin'),
    ])
    movimentacoes.value = movs.data
    produtos.value = prods.data
  } catch (err) {
    erroForm.value = err.response?.data?.detail ?? 'Erro ao registrar movimentação.'
  } finally {
    enviando.value = false
  }
}

onMounted(async () => {
  try {
    const [movs, prods] = await Promise.all([
      api.get('/estoque/admin'),
      api.get('/produtos/admin'),
    ])
    movimentacoes.value = movs.data
    produtos.value = prods.data
  } catch {
    console.error('Erro ao carregar estoque.')
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
.card-icon.vendas      { background: linear-gradient(135deg,rgba(76,175,80,.2),rgba(76,175,80,.4)); color:#4CAF50; border-color:#4CAF50; }
.card-icon.faturamento { background: linear-gradient(135deg,rgba(255,193,7,.2),rgba(255,193,7,.4)); color:#FFC107; border-color:#FFC107; }
.card-icon.clientes    { background: linear-gradient(135deg,rgba(33,150,243,.2),rgba(33,150,243,.4)); color:#2196F3; border-color:#2196F3; }
.card-icon.ticket      { background: linear-gradient(135deg,rgba(156,39,176,.2),rgba(156,39,176,.4)); color:#9C27B0; border-color:#9C27B0; }
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

.form-movimentacao {
  display: flex;
  flex-wrap: wrap;
  gap: var(--espacamento-sm);
  align-items: center;
}
.input-form {
  padding: .6rem 1rem;
  border-radius: var(--borda-radius-sm);
  border: 1px solid rgba(255,215,0,0.3);
  background: var(--cor-fundo);
  color: var(--cor-texto);
  font-size: .9rem;
  outline: none;
  transition: border-color .3s;
  flex: 1;
  min-width: 160px;
}
.input-form:focus { border-color: var(--cor-dourado); }
.input-qtd { max-width: 120px; flex: unset; }
.btn-registrar {
  padding: .6rem 1.4rem;
  border-radius: var(--borda-radius-lg);
  border: none;
  font-weight: 600;
  font-size: .9rem;
  cursor: pointer;
  transition: all .3s;
  display: inline-flex;
  align-items: center;
  gap: .5rem;
  flex-shrink: 0;
}
.btn-registrar:disabled { opacity: .5; cursor: not-allowed; }
.btn-registrar.entrada { background: linear-gradient(45deg,#2E7D32,#4CAF50); color: #fff; }
.btn-registrar.saida   { background: linear-gradient(45deg,#b71c1c,#f44336); color: #fff; }
.btn-registrar.ajuste  { background: var(--gradiente-botao); color: #000; }
.btn-registrar:not(:disabled):hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,.3); }

.erro-form    { color: #f44336; margin-top: var(--espacamento-sm); font-size: .9rem; }
.sucesso-form { color: #4CAF50; margin-top: var(--espacamento-sm); font-size: .9rem; }

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
.nome-produto { font-weight: 500; }
.sem-dado { color: var(--cor-texto-secundario); }

.badge-tipo {
  display: inline-flex;
  align-items: center;
  gap: .35rem;
  padding: .3rem .8rem;
  border-radius: var(--borda-radius-lg);
  font-size: .8rem;
  font-weight: 600;
  border: 1px solid;
  text-transform: capitalize;
}
.badge-tipo.entrada { background: rgba(76,175,80,.2);  color: #4CAF50; border-color: #4CAF50; }
.badge-tipo.saida   { background: rgba(244,67,54,.2);  color: #f44336; border-color: #f44336; }
.badge-tipo.ajuste  { background: rgba(255,193,7,.2);  color: #FFC107; border-color: #FFC107; }

.qtd-cell {
  font-family: monospace;
  font-weight: 700;
  font-size: 1rem;
}
.qtd-cell.entrada { color: #4CAF50; }
.qtd-cell.saida   { color: #f44336; }
.qtd-cell.ajuste  { color: #FFC107; }

.saldo-cell { color: var(--cor-texto-secundario); font-family: monospace; }
.saldo-posterior {
  font-family: monospace;
  font-weight: 600;
  color: var(--cor-texto);
  display: inline-flex;
  align-items: center;
  gap: .3rem;
}
.saldo-posterior.baixo { color: #f44336; }
.aviso-estoque { color: #f44336; font-size: .75rem; }

.motivo-cell { color: var(--cor-texto-secundario); font-size: .85rem; max-width: 180px; }
.link-venda { color: var(--cor-dourado); text-decoration: none; font-weight: 600; }
.link-venda:hover { text-decoration: underline; }

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
  .form-movimentacao { flex-direction: column; }
  .input-form, .input-qtd { min-width: 100%; max-width: 100%; }
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
.input-form,
.input-busca { background: #FFFFFF; border: 1px solid #D6D9DE; color: #1B1A19; font-family: inherit; }
.input-form:focus,
.input-busca:focus { border-color: #C9A84C; box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.15); }
.btn-filtro { background: #FFFFFF; border: 1px solid #D6D9DE; color: #4B5563; font-family: inherit; }
.btn-filtro:hover,
.btn-filtro.ativo { background: #FDF6E5; border-color: #C9A84C; color: #8A6520; }
.tabela-wrapper { border: 1px solid #E3E5E8; }
.tabela-vendas th { background: #F9FAFB; color: #6B7280; border-bottom: 1px solid #E3E5E8; font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; }
.tabela-vendas td { color: #1B1A19; border-bottom: 1px solid #F0F1F3; }
.tabela-vendas tr:hover td { background: #FAFAF8; }
.id-badge { background: #F0F1F3; color: #4B5563; }
.saldo-cell { color: #6B7280; }
.motivo-cell { color: #6B7280; }
.sem-dado { color: #9CA3AF; }
.link-venda { color: #8A6520; }
.estado-vazio { color: #9CA3AF; }
.estado-vazio i { color: #C9A84C; }
.erro-form { color: #DC2626; }
.sucesso-form { color: #2E8B57; }
</style>
