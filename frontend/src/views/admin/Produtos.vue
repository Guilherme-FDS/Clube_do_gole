<template>
  <main class="prod-admin">
    <div class="prod-container">
      <BotaoVoltarAdmin />

      <header class="prod-header">
        <div>
          <h1>Produtos & Planos</h1>
          <p>Catálogo e planos de assinatura</p>
        </div>
        <button class="btn-primario" @click="abrirModalProduto(null)">
          <i class="fas fa-plus"></i> Novo Produto
        </button>
      </header>

      <!-- Tabela de produtos -->
      <div class="card-tabela">
        <div v-if="carregando" class="estado-vazio">
          <i class="fas fa-spinner fa-spin"></i> Carregando...
        </div>
        <div v-else-if="produtos.length === 0" class="estado-vazio">
          Nenhum produto cadastrado. Clique em "Novo Produto" para começar.
        </div>

        <table v-else>
          <thead>
            <tr>
              <th style="width:36px"></th>
              <th>Produto</th>
              <th>Descrição</th>
              <th class="centro">Planos</th>
              <th class="centro">Status</th>
              <th class="centro">Ações</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="p in produtos" :key="p.id">
              <tr class="linha-produto" :class="{ expandida: expandido === p.id }">
                <td class="centro">
                  <button class="btn-expandir" @click="toggleExpandir(p.id)" :title="expandido === p.id ? 'Fechar' : 'Ver planos'">
                    <i :class="expandido === p.id ? 'fas fa-chevron-down' : 'fas fa-chevron-right'"></i>
                  </button>
                </td>
                <td class="nome-produto">{{ p.nome }}</td>
                <td class="desc-produto">{{ p.descricao || '—' }}</td>
                <td class="centro">
                  <span class="badge-planos">{{ planosCount[p.id] ?? '...' }}</span>
                </td>
                <td class="centro">
                  <button
                    class="toggle-status"
                    :class="{ ativo: p.ativo }"
                    @click="toggleStatusProduto(p)"
                    :title="p.ativo ? 'Clique para desativar' : 'Clique para ativar'"
                  >
                    <span class="toggle-bola"></span>
                  </button>
                </td>
                <td class="centro acoes">
                  <button class="btn-icone" @click="abrirModalProduto(p)" title="Editar">
                    <i class="fas fa-pen"></i>
                  </button>
                  <button class="btn-icone perigo" @click="confirmarExclusaoProduto(p)" title="Excluir">
                    <i class="fas fa-trash"></i>
                  </button>
                </td>
              </tr>

              <!-- Linha expandida: planos -->
              <tr v-if="expandido === p.id" class="linha-planos">
                <td colspan="6">
                  <div class="planos-painel">
                    <div class="planos-header">
                      <h3>Planos de assinatura — {{ p.nome }}</h3>
                      <button class="btn-secundario" @click="abrirModalPlano(p, null)">
                        <i class="fas fa-plus"></i> Adicionar Plano
                      </button>
                    </div>

                    <div v-if="carregandoPlanos" class="estado-vazio pequeno">
                      <i class="fas fa-spinner fa-spin"></i> Carregando planos...
                    </div>
                    <div v-else-if="!planos.length" class="estado-vazio pequeno">
                      Nenhum plano cadastrado para este produto.
                    </div>

                    <table v-else class="tabela-planos">
                      <thead>
                        <tr>
                          <th>Recorrência</th>
                          <th class="direita">Preço base</th>
                          <th class="centro">Desconto</th>
                          <th class="direita">Preço final</th>
                          <th class="direita">Economia</th>
                          <th class="centro">Status</th>
                          <th class="centro">Ações</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="pl in planos" :key="pl.id">
                          <td>
                            <span :class="['badge-rec', pl.recorrencia]">{{ formatarRec(pl.recorrencia) }}</span>
                          </td>
                          <td class="direita">{{ formatarMoeda(pl.preco_base) }}</td>
                          <td class="centro">{{ Number(pl.desconto_pct) }}%</td>
                          <td class="direita destaque">{{ formatarMoeda(pl.preco_total) }}</td>
                          <td class="direita economia">{{ Number(pl.economia) > 0 ? formatarMoeda(pl.economia) : '—' }}</td>
                          <td class="centro">
                            <button
                              class="toggle-status mini"
                              :class="{ ativo: pl.ativo }"
                              @click="toggleStatusPlano(p, pl)"
                            >
                              <span class="toggle-bola"></span>
                            </button>
                          </td>
                          <td class="centro acoes">
                            <button class="btn-icone" @click="abrirModalPlano(p, pl)" title="Editar">
                              <i class="fas fa-pen"></i>
                            </button>
                            <button class="btn-icone perigo" @click="confirmarExclusaoPlano(p, pl)" title="Excluir">
                              <i class="fas fa-trash"></i>
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal Produto -->
    <Teleport to="body">
      <div v-if="modalProduto" class="modal-fundo" @click.self="fecharModalProduto">
        <div class="modal-caixa">
          <h2>{{ produtoEditando ? 'Editar Produto' : 'Novo Produto' }}</h2>
          <form @submit.prevent="salvarProduto">
            <div class="campo">
              <label>Nome *</label>
              <input v-model="formProduto.nome" type="text" placeholder="Ex: Clube do Gole — Linha Gold" required />
            </div>
            <div class="campo">
              <label>Descrição</label>
              <textarea v-model="formProduto.descricao" rows="3" placeholder="Descrição do produto"></textarea>
            </div>
            <label class="campo-check">
              <input type="checkbox" v-model="formProduto.ativo" />
              Produto ativo (visível no site)
            </label>
            <div class="modal-botoes">
              <button type="button" class="btn-cancelar" @click="fecharModalProduto">Cancelar</button>
              <button type="submit" class="btn-primario" :disabled="salvando">
                {{ salvando ? 'Salvando...' : 'Salvar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Modal Plano -->
    <Teleport to="body">
      <div v-if="modalPlano" class="modal-fundo" @click.self="fecharModalPlano">
        <div class="modal-caixa">
          <h2>{{ planoEditando ? 'Editar Plano' : 'Novo Plano' }} — {{ produtoDoPlano?.nome }}</h2>
          <form @submit.prevent="salvarPlano">
            <div class="campo">
              <label>Recorrência *</label>
              <select v-model="formPlano.recorrencia" required :disabled="!!planoEditando">
                <option value="mensal">Mensal</option>
                <option value="semestral">Semestral</option>
                <option value="anual">Anual</option>
              </select>
            </div>
            <div class="campo-linha">
              <div class="campo">
                <label>Preço base (R$) *</label>
                <input v-model.number="formPlano.preco_base" type="number" step="0.01" min="0.01" placeholder="649.00" required />
              </div>
              <div class="campo">
                <label>Desconto (%)</label>
                <input v-model.number="formPlano.desconto_pct" type="number" step="0.01" min="0" max="100" placeholder="0" />
              </div>
            </div>
            <div v-if="formPlano.preco_base > 0" class="preview-preco">
              Preço final: <strong>{{ formatarMoeda(precoFinalPreview) }}</strong>
              <span v-if="formPlano.desconto_pct > 0" class="economia">
                (economia de {{ formatarMoeda(formPlano.preco_base - precoFinalPreview) }})
              </span>
            </div>
            <label class="campo-check">
              <input type="checkbox" v-model="formPlano.ativo" />
              Plano ativo
            </label>
            <div class="modal-botoes">
              <button type="button" class="btn-cancelar" @click="fecharModalPlano">Cancelar</button>
              <button type="submit" class="btn-primario" :disabled="salvando">
                {{ salvando ? 'Salvando...' : 'Salvar' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </Teleport>

    <!-- Toast -->
    <div v-if="toast.visivel" class="toast" :class="toast.tipo">{{ toast.mensagem }}</div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useProdutosAdminStore } from '@/stores/admin/produtos'
import BotaoVoltarAdmin from '@/components/BotaoVoltarAdmin.vue'

const store = useProdutosAdminStore()

// ── Estado ────────────────────────────────────────────────────────────
const produtos = ref([])
const carregando = ref(false)
const planosCount = ref({})

const expandido = ref(null)
const planos = ref([])
const carregandoPlanos = ref(false)

const modalProduto = ref(false)
const produtoEditando = ref(null)
const formProduto = ref(formProdutoVazio())

const modalPlano = ref(false)
const planoEditando = ref(null)
const produtoDoPlano = ref(null)
const formPlano = ref(formPlanoVazio())

const salvando = ref(false)
const toast = ref({ visivel: false, mensagem: '', tipo: 'success' })

const precoFinalPreview = computed(() => {
  const base = Number(formPlano.value.preco_base) || 0
  const desc = Number(formPlano.value.desconto_pct) || 0
  return base * (1 - desc / 100)
})

// ── Helpers ───────────────────────────────────────────────────────────
function formProdutoVazio() {
  return { nome: '', descricao: '', ativo: true }
}

function formPlanoVazio() {
  return { recorrencia: 'mensal', preco_base: '', desconto_pct: 0, ativo: true }
}

function formatarMoeda(v) {
  return Number(v || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatarRec(r) {
  return { mensal: 'Mensal', semestral: 'Semestral', anual: 'Anual' }[r] || r
}

function mostrarToast(mensagem, tipo = 'success') {
  toast.value = { visivel: true, mensagem, tipo }
  setTimeout(() => { toast.value.visivel = false }, 3500)
}

// ── Produtos ──────────────────────────────────────────────────────────
async function carregar() {
  carregando.value = true
  try {
    produtos.value = await store.fetchProdutos()
    carregarContagens()
  } catch {
    mostrarToast('Erro ao carregar produtos', 'error')
  } finally {
    carregando.value = false
  }
}

async function carregarContagens() {
  for (const p of produtos.value) {
    try {
      const pls = await store.fetchPlanos(p.id)
      planosCount.value[p.id] = pls.length
    } catch {
      planosCount.value[p.id] = 0
    }
  }
}

function abrirModalProduto(p) {
  produtoEditando.value = p
  formProduto.value = p
    ? { nome: p.nome, descricao: p.descricao || '', ativo: p.ativo }
    : formProdutoVazio()
  modalProduto.value = true
}

function fecharModalProduto() {
  modalProduto.value = false
  produtoEditando.value = null
}

async function salvarProduto() {
  if (!formProduto.value.nome.trim()) return
  salvando.value = true
  try {
    if (produtoEditando.value) {
      await store.atualizarProduto(produtoEditando.value.id, formProduto.value)
      mostrarToast('Produto atualizado!')
    } else {
      await store.adicionarProduto(formProduto.value)
      mostrarToast('Produto criado!')
    }
    fecharModalProduto()
    await carregar()
  } catch (e) {
    mostrarToast(e.response?.data?.detail || 'Erro ao salvar produto', 'error')
  } finally {
    salvando.value = false
  }
}

async function toggleStatusProduto(p) {
  try {
    await store.alterarStatusProduto(p.id, !p.ativo)
    p.ativo = !p.ativo
    mostrarToast(p.ativo ? 'Produto ativado' : 'Produto desativado')
  } catch {
    mostrarToast('Erro ao alterar status', 'error')
  }
}

async function confirmarExclusaoProduto(p) {
  if (!confirm(`Excluir "${p.nome}"? Os planos vinculados também serão removidos.`)) return
  try {
    await store.excluirProduto(p.id)
    mostrarToast('Produto excluído')
    if (expandido.value === p.id) expandido.value = null
    await carregar()
  } catch (e) {
    mostrarToast(e.response?.data?.detail || 'Erro ao excluir', 'error')
  }
}

// ── Planos ────────────────────────────────────────────────────────────
async function toggleExpandir(produtoId) {
  if (expandido.value === produtoId) {
    expandido.value = null
    return
  }
  expandido.value = produtoId
  await carregarPlanos(produtoId)
}

async function carregarPlanos(produtoId) {
  carregandoPlanos.value = true
  try {
    planos.value = await store.fetchPlanos(produtoId)
    planosCount.value[produtoId] = planos.value.length
  } catch {
    mostrarToast('Erro ao carregar planos', 'error')
    planos.value = []
  } finally {
    carregandoPlanos.value = false
  }
}

function abrirModalPlano(produto, plano) {
  produtoDoPlano.value = produto
  planoEditando.value = plano
  formPlano.value = plano
    ? {
        recorrencia: plano.recorrencia,
        preco_base: Number(plano.preco_base),
        desconto_pct: Number(plano.desconto_pct),
        ativo: plano.ativo
      }
    : formPlanoVazio()
  modalPlano.value = true
}

function fecharModalPlano() {
  modalPlano.value = false
  planoEditando.value = null
  produtoDoPlano.value = null
}

async function salvarPlano() {
  if (!formPlano.value.preco_base || formPlano.value.preco_base <= 0) {
    mostrarToast('Preço base deve ser maior que zero', 'error')
    return
  }
  salvando.value = true
  try {
    const dados = {
      recorrencia: formPlano.value.recorrencia,
      preco_base: formPlano.value.preco_base,
      desconto_pct: formPlano.value.desconto_pct || 0,
      ativo: formPlano.value.ativo
    }
    if (planoEditando.value) {
      await store.atualizarPlano(planoEditando.value.id, dados)
      mostrarToast('Plano atualizado!')
    } else {
      await store.adicionarPlano(produtoDoPlano.value.id, dados)
      mostrarToast('Plano criado!')
    }
    const pid = produtoDoPlano.value.id
    fecharModalPlano()
    await carregarPlanos(pid)
  } catch (e) {
    mostrarToast(e.response?.data?.detail || 'Erro ao salvar plano', 'error')
  } finally {
    salvando.value = false
  }
}

async function toggleStatusPlano(produto, plano) {
  try {
    await store.alterarStatusPlano(plano.id, !plano.ativo)
    await carregarPlanos(produto.id)
    mostrarToast('Status do plano alterado')
  } catch {
    mostrarToast('Erro ao alterar status do plano', 'error')
  }
}

async function confirmarExclusaoPlano(produto, plano) {
  if (!confirm(`Excluir plano ${formatarRec(plano.recorrencia)} de "${produto.nome}"?`)) return
  try {
    await store.excluirPlano(plano.id)
    mostrarToast('Plano excluído')
    await carregarPlanos(produto.id)
  } catch (e) {
    mostrarToast(e.response?.data?.detail || 'Erro ao excluir plano', 'error')
  }
}

onMounted(carregar)
</script>

<style scoped>
.prod-admin {
  min-height: 100vh;
  background: #F4F5F7;
  padding: 110px 0 60px;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
}

.prod-container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Header */
.prod-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.prod-header h1 {
  font-size: 22px;
  font-weight: 700;
  color: #1B1A19;
  margin: 0 0 2px;
}

.prod-header p {
  font-size: 13px;
  color: #6B7280;
  margin: 0;
}

/* Botões */
.btn-primario {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: linear-gradient(135deg, #9E7A2E, #E2C06A);
  color: #1B1A19;
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  padding: 10px 18px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: opacity 0.15s;
}
.btn-primario:hover:not(:disabled) { opacity: 0.88; }
.btn-primario:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-secundario {
  display: inline-flex;
  align-items: center;
  gap: 7px;
  background: #FFFFFF;
  border: 1px solid #C9A84C;
  color: #8A6520;
  font-family: inherit;
  font-size: 12px;
  font-weight: 600;
  padding: 7px 14px;
  border-radius: 7px;
  cursor: pointer;
  transition: background 0.15s;
}
.btn-secundario:hover { background: #FDF6E5; }

.btn-cancelar {
  background: #F0F1F3;
  border: 1px solid #E3E5E8;
  color: #4B5563;
  font-family: inherit;
  font-size: 13px;
  font-weight: 500;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
}

/* Card / tabela */
.card-tabela {
  background: #FFFFFF;
  border: 1px solid #E3E5E8;
  border-radius: 10px;
  overflow: hidden;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

th {
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #6B7280;
  background: #F9FAFB;
  padding: 11px 14px;
  border-bottom: 1px solid #E3E5E8;
}

td {
  padding: 12px 14px;
  border-bottom: 1px solid #F0F1F3;
  color: #1B1A19;
  vertical-align: middle;
}

.linha-produto:hover { background: #FAFAF8; }
.linha-produto.expandida { background: #FDF9EF; }

.centro { text-align: center; }
.direita { text-align: right; }

.nome-produto { font-weight: 600; }
.desc-produto {
  color: #6B7280;
  max-width: 320px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.badge-planos {
  display: inline-block;
  min-width: 24px;
  background: #EEF4FF;
  color: #3B6FD4;
  font-weight: 600;
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 12px;
}

/* Expandir */
.btn-expandir {
  background: none;
  border: none;
  color: #9CA3AF;
  cursor: pointer;
  font-size: 12px;
  padding: 4px 6px;
  transition: color 0.15s;
}
.btn-expandir:hover { color: #C9A84C; }

/* Toggle status */
.toggle-status {
  width: 38px;
  height: 21px;
  background: #D6D9DE;
  border: none;
  border-radius: 11px;
  cursor: pointer;
  position: relative;
  transition: background 0.2s;
  padding: 0;
}
.toggle-status.ativo { background: #2E8B57; }
.toggle-bola {
  position: absolute;
  top: 2.5px;
  left: 3px;
  width: 16px;
  height: 16px;
  background: #fff;
  border-radius: 50%;
  transition: transform 0.2s;
}
.toggle-status.ativo .toggle-bola { transform: translateX(16px); }
.toggle-status.mini { width: 32px; height: 18px; }
.toggle-status.mini .toggle-bola { width: 13px; height: 13px; top: 2.5px; }
.toggle-status.mini.ativo .toggle-bola { transform: translateX(14px); }

/* Ações */
.acoes { white-space: nowrap; }

.btn-icone {
  background: none;
  border: 1px solid #E3E5E8;
  color: #6B7280;
  width: 30px;
  height: 30px;
  border-radius: 7px;
  cursor: pointer;
  font-size: 12px;
  margin: 0 2px;
  transition: all 0.15s;
}
.btn-icone:hover { border-color: #C9A84C; color: #8A6520; background: #FDF6E5; }
.btn-icone.perigo:hover { border-color: #DC2626; color: #DC2626; background: #FEF2F2; }

/* Painel de planos */
.linha-planos td { padding: 0; background: #FBFBF9; }

.planos-painel { padding: 16px 20px 20px; }

.planos-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.planos-header h3 {
  font-size: 13px;
  font-weight: 600;
  color: #4B5563;
  margin: 0;
}

.tabela-planos {
  background: #FFFFFF;
  border: 1px solid #E8E9EB;
  border-radius: 8px;
  overflow: hidden;
}

.tabela-planos th { background: #F4F5F7; }

.badge-rec {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 12px;
}
.badge-rec.mensal { background: #FDF6E5; color: #8A6520; }
.badge-rec.semestral { background: #F3EEFD; color: #7B2FE0; }
.badge-rec.anual { background: #EBEBEA; color: #1B1A19; }

.destaque { font-weight: 700; }
.economia { color: #2E8B57; font-weight: 500; }

/* Estados */
.estado-vazio {
  padding: 40px;
  text-align: center;
  color: #9CA3AF;
  font-size: 14px;
}
.estado-vazio.pequeno { padding: 20px; }

/* Modais */
.modal-fundo {
  position: fixed;
  inset: 0;
  background: rgba(27, 26, 25, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-caixa {
  background: #FFFFFF;
  border-radius: 12px;
  padding: 26px 28px;
  width: 100%;
  max-width: 460px;
  max-height: 90vh;
  overflow-y: auto;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
}

.modal-caixa h2 {
  font-size: 17px;
  font-weight: 700;
  color: #1B1A19;
  margin: 0 0 20px;
}

.campo { margin-bottom: 14px; display: flex; flex-direction: column; gap: 5px; flex: 1; }
.campo-linha { display: flex; gap: 12px; }

.campo label {
  font-size: 12px;
  font-weight: 600;
  color: #4B5563;
}

.campo input,
.campo select,
.campo textarea {
  font-family: inherit;
  font-size: 14px;
  color: #1B1A19;
  background: #FFFFFF;
  border: 1px solid #D6D9DE;
  border-radius: 8px;
  padding: 9px 12px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
  resize: vertical;
}
.campo input:focus,
.campo select:focus,
.campo textarea:focus {
  border-color: #C9A84C;
  box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.15);
}
.campo select:disabled { background: #F4F5F7; color: #9CA3AF; }

.campo-check {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #4B5563;
  cursor: pointer;
  margin-bottom: 6px;
}
.campo-check input { accent-color: #C9A84C; width: 16px; height: 16px; }

.preview-preco {
  background: #FDF6E5;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 13px;
  color: #4B5563;
  margin-bottom: 14px;
}
.preview-preco strong { color: #1B1A19; }
.preview-preco .economia { margin-left: 6px; font-size: 12px; }

.modal-botoes {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 18px;
}

/* Toast */
.toast {
  position: fixed;
  bottom: 30px;
  right: 30px;
  padding: 13px 22px;
  border-radius: 10px;
  font-size: 13px;
  font-weight: 600;
  z-index: 2000;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.18);
  animation: subir 0.25s ease;
}
.toast.success { background: #1B1A19; color: #C9A84C; }
.toast.error { background: #DC2626; color: #fff; }

@keyframes subir {
  from { transform: translateY(14px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Responsivo */
@media (max-width: 760px) {
  .prod-header { flex-direction: column; align-items: flex-start; gap: 12px; }
  .desc-produto { display: none; }
  .campo-linha { flex-direction: column; gap: 0; }
}
</style>
