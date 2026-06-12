<template>
  <div class="checkout-page">
    <!-- Loading state -->
    <div v-if="carregando" class="checkout-loading">
      <div class="loading-spinner"></div>
      <p>Preparando seu pedido...</p>
    </div>

    <!-- Empty state -->
    <div v-else-if="itensSelecionados.length === 0" class="checkout-vazio">
      <div class="vazio-icon">🛒</div>
      <h2>Nenhum item selecionado</h2>
      <p>Volte ao carrinho e selecione os itens que deseja finalizar.</p>
      <button class="btn-voltar" @click="$router.push('/carrinho')">Ir ao Carrinho</button>
    </div>

    <!-- Checkout content -->
    <div v-else class="checkout-container">
      <!-- Header da página -->
      <div class="checkout-header">
        <button class="btn-back" @click="$router.push('/carrinho')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="m15 18-6-6 6-6"/>
          </svg>
          Carrinho
        </button>
        <div class="checkout-progress">
          <span class="step active">Endereço</span>
          <span class="step-divider">›</span>
          <span class="step">Pagamento</span>
          <span class="step-divider">›</span>
          <span class="step">Confirmação</span>
        </div>
      </div>

      <div class="checkout-grid">
        <!-- Coluna esquerda -->
        <div class="checkout-left">

          <!-- Itens selecionados -->
          <section class="checkout-section">
            <div class="section-eyebrow">
              <span class="eyebrow-badge">● Pedido</span>
            </div>
            <h2 class="section-title">Itens selecionados</h2>
            <div class="itens-lista">
              <div v-for="item in itensSelecionados" :key="item.id_carrinho" class="item-checkout">
                <div class="item-info">
                  <span class="item-nome">{{ item.nome_produto }}</span>
                  <span :class="['item-plano-badge', item.plano]">{{ formatarPlano(item.plano) }}</span>
                </div>
                <div class="item-preco">
                  <span class="item-qtd">{{ item.quantidade }}x</span>
                  <span class="item-valor">{{ formatarMoeda(item.valor_total) }}</span>
                </div>
              </div>
            </div>
          </section>

          <!-- Endereço de entrega -->
          <section class="checkout-section">
            <div class="section-eyebrow">
              <span class="eyebrow-badge">● Entrega</span>
            </div>
            <h2 class="section-title">Endereço de entrega</h2>

            <div v-if="carregandoEnderecos" class="loading-text">Carregando endereços...</div>

            <div v-else>
              <div v-if="enderecos.length > 0" class="enderecos-lista">
                <label
                  v-for="end in enderecos"
                  :key="end.id"
                  class="endereco-card"
                  :class="{ selected: enderecoSelecionado === end.id }"
                >
                  <input type="radio" :value="end.id" v-model="enderecoSelecionado" class="sr-only" />
                  <div class="endereco-radio">
                    <div class="radio-dot" :class="{ active: enderecoSelecionado === end.id }"></div>
                  </div>
                  <div class="endereco-info">
                    <div class="endereco-tipo">{{ end.tipo }}</div>
                    <div class="endereco-linha">{{ end.endereco }}, {{ end.numero }}<span v-if="end.complemento">, {{ end.complemento }}</span></div>
                    <div class="endereco-linha">{{ end.bairro }} — {{ end.cidade }}/{{ end.estado }}</div>
                    <div class="endereco-cep">CEP {{ formatarCEP(end.cep) }}</div>
                  </div>
                  <span v-if="end.principal" class="badge-principal">Principal</span>
                </label>
              </div>

              <button class="btn-novo-endereco" @click="abrirModalEndereco(null)">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M12 5v14M5 12h14"/>
                </svg>
                {{ enderecos.length === 0 ? 'Adicionar endereço de entrega' : 'Usar novo endereço' }}
              </button>
            </div>
          </section>

          <!-- Pagamento -->
          <section class="checkout-section">
            <div class="section-eyebrow">
              <span class="eyebrow-badge">● Pagamento</span>
            </div>
            <h2 class="section-title">Forma de pagamento</h2>
            <div class="pagamento-opcoes">
              <label class="pagamento-card" :class="{ selected: pagamento === 'cartao' }">
                <input type="radio" value="cartao" v-model="pagamento" class="sr-only" />
                <div class="radio-dot" :class="{ active: pagamento === 'cartao' }"></div>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/>
                </svg>
                <span>Cartão de crédito</span>
              </label>
              <label class="pagamento-card" :class="{ selected: pagamento === 'pix' }">
                <input type="radio" value="pix" v-model="pagamento" class="sr-only" />
                <div class="radio-dot" :class="{ active: pagamento === 'pix' }"></div>
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/>
                </svg>
                <span>Pix</span>
              </label>
            </div>

            <div v-if="pagamento === 'cartao'" class="cartao-form">
              <div class="form-group">
                <label>Número do cartão</label>
                <input type="text" v-model="cartao.numero" placeholder="0000 0000 0000 0000" class="form-input" maxlength="19" @input="formatarCartao" />
              </div>
              <div class="form-group">
                <label>Nome no cartão</label>
                <input type="text" v-model="cartao.nome" placeholder="Como está no cartão" class="form-input" />
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Validade</label>
                  <input type="text" v-model="cartao.validade" placeholder="MM/AA" class="form-input" maxlength="5" />
                </div>
                <div class="form-group">
                  <label>CVV</label>
                  <input type="text" v-model="cartao.cvv" placeholder="000" class="form-input" maxlength="4" />
                </div>
                <div class="form-group">
                  <label>Parcelas</label>
                  <select v-model="cartao.parcelas" class="form-input">
                    <option v-for="n in 12" :key="n" :value="n">{{ n }}x {{ formatarMoeda(totalFinal / n) }}</option>
                  </select>
                </div>
              </div>
            </div>

            <div v-if="pagamento === 'pix'" class="pix-info">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--cor-dourado)" stroke-width="1.5">
                <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
              </svg>
              <p>Após confirmar o pedido, você receberá o QR Code do Pix para pagamento.</p>
              <p class="pix-destaque">Aprovação instantânea após o pagamento.</p>
            </div>
          </section>
        </div>

        <!-- Resumo sticky -->
        <aside class="checkout-resumo">
          <div class="resumo-card">
            <h3 class="resumo-titulo">Resumo do pedido</h3>

            <div class="resumo-itens">
              <div v-for="item in itensSelecionados" :key="item.id_carrinho" class="resumo-item">
                <span class="resumo-item-nome">{{ item.nome_produto }} <span class="resumo-item-qtd">×{{ item.quantidade }}</span></span>
                <span class="resumo-item-valor">{{ formatarMoeda(item.valor_total) }}</span>
              </div>
            </div>

            <!-- Cupom -->
            <div class="cupom-form">
              <input
                v-model="cupom"
                type="text"
                placeholder="Cupom de desconto"
                class="input-cupom"
                :disabled="cupomAplicado"
                @keyup.enter="aplicarCupom"
              />
              <button v-if="!cupomAplicado" class="btn-cupom" @click="aplicarCupom" :disabled="!cupom.trim() || carregandoCupom">
                {{ carregandoCupom ? '...' : 'Aplicar' }}
              </button>
              <button v-else class="btn-cupom-remover" @click="removerCupom">✕</button>
            </div>
            <div v-if="mensagemCupom" class="cupom-feedback" :class="{ erro: !cupomAplicado }">
              {{ mensagemCupom }}
            </div>

            <div class="resumo-divider"></div>

            <div class="resumo-linha">
              <span>Subtotal</span>
              <span>{{ formatarMoeda(subtotal) }}</span>
            </div>
            <div v-if="desconto > 0" class="resumo-linha desconto">
              <span>Desconto ({{ cupom }})</span>
              <span>−{{ formatarMoeda(desconto) }}</span>
            </div>
            <div class="resumo-linha">
              <span>Frete</span>
              <span class="frete-gratis">Grátis</span>
            </div>

            <div class="resumo-divider"></div>

            <div class="resumo-total">
              <span>Total</span>
              <span>{{ formatarMoeda(totalFinal) }}</span>
            </div>

            <button class="btn-finalizar" @click="finalizarCompra" :disabled="finalizando || !enderecoSelecionado">
              <span v-if="finalizando">Processando...</span>
              <span v-else>Confirmar pedido</span>
            </button>

            <p v-if="!enderecoSelecionado" class="aviso-endereco">Selecione um endereço de entrega para continuar</p>

            <div class="resumo-seguranca">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
              </svg>
              <span>Compra 100% segura e criptografada</span>
            </div>
          </div>
        </aside>
      </div>
    </div>

    <!-- Modal Endereço -->
    <Teleport to="body">
      <div v-if="modalEndereco" class="modal-overlay" @click.self="fecharModalEndereco">
        <div class="modal-endereco">
          <div class="modal-header">
            <h3>{{ enderecoEditando ? 'Editar endereço' : 'Novo endereço' }}</h3>
            <button class="modal-close" @click="fecharModalEndereco">✕</button>
          </div>
          <div class="modal-body">
            <div class="form-row">
              <div class="form-group flex-2">
                <label>CEP *</label>
                <input v-model="form.cep" type="text" class="form-input" placeholder="00000-000" maxlength="9" @blur="buscarCEP" @input="formatarCEPInput" />
              </div>
              <div class="form-group flex-3">
                <label>Tipo</label>
                <select v-model="form.tipo" class="form-input">
                  <option value="Casa">Casa</option>
                  <option value="Apartamento">Apartamento</option>
                  <option value="Trabalho">Trabalho</option>
                  <option value="Outro">Outro</option>
                </select>
              </div>
            </div>
            <div class="form-group">
              <label>Endereço *</label>
              <input v-model="form.endereco" type="text" class="form-input" placeholder="Rua, Avenida..." />
            </div>
            <div class="form-row">
              <div class="form-group flex-1">
                <label>Número *</label>
                <input v-model="form.numero" type="text" class="form-input" placeholder="123" />
              </div>
              <div class="form-group flex-2">
                <label>Complemento</label>
                <input v-model="form.complemento" type="text" class="form-input" placeholder="Apto, Bloco..." />
              </div>
            </div>
            <div class="form-group">
              <label>Bairro *</label>
              <input v-model="form.bairro" type="text" class="form-input" placeholder="Bairro" />
            </div>
            <div class="form-row">
              <div class="form-group flex-2">
                <label>Cidade *</label>
                <input v-model="form.cidade" type="text" class="form-input" placeholder="Cidade" />
              </div>
              <div class="form-group flex-1">
                <label>Estado *</label>
                <input v-model="form.estado" type="text" class="form-input" placeholder="UF" maxlength="2" />
              </div>
            </div>
            <label class="checkbox-label">
              <input type="checkbox" v-model="form.principal" class="checkbox-input" />
              <span class="checkbox-mark"></span>
              Definir como endereço principal
            </label>
          </div>
          <div class="modal-footer">
            <button class="btn-cancelar" @click="fecharModalEndereco">Cancelar</button>
            <button class="btn-salvar" @click="salvarEndereco" :disabled="salvandoEndereco">
              {{ salvandoEndereco ? 'Salvando...' : 'Salvar endereço' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>

    <!-- Toast -->
    <div v-if="toast.visivel" class="toast" :class="toast.tipo">{{ toast.mensagem }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCarrinhoStore } from '@/stores/carrinho'
import api from '@/services/api'

const router = useRouter()
const carrinhoStore = useCarrinhoStore()

const carregando = ref(true)
const itensSelecionados = ref([])

const enderecos = ref([])
const carregandoEnderecos = ref(false)
const enderecoSelecionado = ref(null)

const cupom = ref('')
const cupomAplicado = ref(false)
const desconto = ref(0)
const carregandoCupom = ref(false)
const mensagemCupom = ref('')

const pagamento = ref('cartao')
const cartao = ref({ numero: '', nome: '', validade: '', cvv: '', parcelas: 1 })

const finalizando = ref(false)

const modalEndereco = ref(false)
const enderecoEditando = ref(null)
const salvandoEndereco = ref(false)
const form = ref(formVazio())

const toast = ref({ visivel: false, mensagem: '', tipo: 'success' })

const subtotal = computed(() => itensSelecionados.value.reduce((s, i) => s + parseFloat(i.valor_total), 0))
const totalFinal = computed(() => Math.max(0, subtotal.value - desconto.value))

onMounted(async () => {
  document.body.classList.add('pagina-clara')
  await carregarItens()
  await carregarEnderecos()
  carregando.value = false
})

onUnmounted(() => {
  document.body.classList.remove('pagina-clara')
})

function formVazio() {
  return { tipo: 'Casa', cep: '', endereco: '', numero: '', complemento: '', bairro: '', cidade: '', estado: '', pais: 'Brasil', principal: false }
}

function formatarMoeda(v) {
  return Number(v || 0).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' })
}

function formatarPlano(p) {
  return { mensal: 'Mensal', semestral: 'Semestral', anual: 'Anual' }[p] || p
}

function formatarCEP(cep) {
  return cep ? String(cep).replace(/(\d{5})(\d{3})/, '$1-$2') : ''
}

function formatarCEPInput(e) {
  let v = e.target.value.replace(/\D/g, '').slice(0, 8)
  if (v.length > 5) v = v.slice(0, 5) + '-' + v.slice(5)
  form.value.cep = v
}

function formatarCartao(e) {
  let v = e.target.value.replace(/\D/g, '').slice(0, 16)
  cartao.value.numero = v.replace(/(\d{4})(?=\d)/g, '$1 ')
}

async function carregarItens() {
  await carrinhoStore.buscar()
  const ids = JSON.parse(localStorage.getItem('checkoutItems') || '[]')
  if (!ids.length) return
  itensSelecionados.value = carrinhoStore.itens.filter(i => ids.includes(i.id_carrinho))
}

async function carregarEnderecos() {
  carregandoEnderecos.value = true
  try {
    const res = await api.get('/configuracoes/enderecos')
    enderecos.value = res.data
    const principal = enderecos.value.find(e => e.principal)
    enderecoSelecionado.value = principal?.id || enderecos.value[0]?.id || null
  } catch {
    mostrarToast('Erro ao carregar endereços', 'error')
  } finally {
    carregandoEnderecos.value = false
  }
}

function abrirModalEndereco(end) {
  enderecoEditando.value = end
  form.value = end ? { ...end } : formVazio()
  modalEndereco.value = true
}

function fecharModalEndereco() {
  modalEndereco.value = false
  enderecoEditando.value = null
}

async function buscarCEP() {
  const cep = form.value.cep.replace(/\D/g, '')
  if (cep.length !== 8) return
  try {
    const res = await fetch(`https://viacep.com.br/ws/${cep}/json/`)
    const data = await res.json()
    if (!data.erro) {
      form.value.endereco = data.logradouro
      form.value.bairro = data.bairro
      form.value.cidade = data.localidade
      form.value.estado = data.uf
    }
  } catch {}
}

async function salvarEndereco() {
  if (!form.value.cep || !form.value.endereco || !form.value.numero || !form.value.cidade) {
    mostrarToast('Preencha os campos obrigatórios', 'error')
    return
  }
  salvandoEndereco.value = true
  try {
    const payload = { ...form.value, cep: form.value.cep.replace(/\D/g, '') }
    if (enderecoEditando.value) {
      await api.put(`/configuracoes/enderecos/${enderecoEditando.value.id}`, payload)
    } else {
      await api.post('/configuracoes/enderecos', payload)
    }
    await carregarEnderecos()
    fecharModalEndereco()
    mostrarToast('Endereço salvo com sucesso!', 'success')
  } catch {
    mostrarToast('Erro ao salvar endereço', 'error')
  } finally {
    salvandoEndereco.value = false
  }
}

async function aplicarCupom() {
  if (!cupom.value.trim()) return
  carregandoCupom.value = true
  mensagemCupom.value = ''
  try {
    const res = await api.post('/carrinho/validar_cupom', { cupom: cupom.value })
    cupomAplicado.value = true
    desconto.value = res.data.desconto || 0
    mensagemCupom.value = `Cupom aplicado! Desconto de ${formatarMoeda(desconto.value)}`
  } catch (e) {
    cupomAplicado.value = false
    desconto.value = 0
    mensagemCupom.value = e.response?.data?.detail || 'Cupom inválido'
  } finally {
    carregandoCupom.value = false
  }
}

function removerCupom() {
  cupom.value = ''
  cupomAplicado.value = false
  desconto.value = 0
  mensagemCupom.value = ''
}

async function finalizarCompra() {
  if (!enderecoSelecionado.value) {
    mostrarToast('Selecione um endereço de entrega', 'error')
    return
  }
  const ids = itensSelecionados.value.map(i => i.id_carrinho)
  finalizando.value = true
  try {
    await api.post('/carrinho/finalizar', {
      ids,
      cupom: cupomAplicado.value ? cupom.value : null,
      desconto_cupom: desconto.value
    })
    localStorage.removeItem('checkoutItems')
    await carrinhoStore.buscar()
    mostrarToast('Pedido realizado com sucesso!', 'success')
    setTimeout(() => router.push('/pedidos'), 1500)
  } catch (e) {
    mostrarToast(e.response?.data?.detail || 'Erro ao finalizar pedido', 'error')
  } finally {
    finalizando.value = false
  }
}

function mostrarToast(mensagem, tipo = 'success') {
  toast.value = { visivel: true, mensagem, tipo }
  setTimeout(() => { toast.value.visivel = false }, 3500)
}
</script>

<style scoped>
/* ── Tokens de design ─────────────────────────────────────────────────── */
:root {
  --ck-bg: #EDECEA;
  --ck-card: #FFFFFF;
  --ck-border: #DDD9D0;
  --ck-text: #1B1A19;
  --ck-text2: #3D3A36;
  --ck-muted: #5A5650;
  --ck-subtle: #888480;
  --ck-gold: #C9A84C;
  --ck-gold-grad: linear-gradient(135deg, #9E7A2E 0%, #E2C06A 100%);
  --ck-radius: 14px;
  --ck-shadow: 0 2px 16px rgba(27,26,25,0.08);
}

/* ── Page ──────────────────────────────────────────────────────────────── */
.checkout-page {
  min-height: 100vh;
  background: var(--ck-bg);
  padding: 40px 0 100px;
  font-family: var(--fonte-ui);
  color: var(--ck-text);
}

/* ── Loading / Empty ──────────────────────────────────────────────────── */
.checkout-loading,
.checkout-vazio {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 20px;
  color: var(--ck-muted);
}

.loading-spinner {
  width: 44px;
  height: 44px;
  border: 3px solid var(--ck-border);
  border-top-color: var(--ck-gold);
  border-radius: 50%;
  animation: spin 0.75s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.vazio-icon { font-size: 52px; }
.checkout-vazio h2 {
  font-family: var(--fonte-principal);
  font-size: 30px;
  font-weight: 600;
  color: var(--ck-text);
  margin: 0;
}
.checkout-vazio p { color: var(--ck-muted); margin: 0; font-size: 16px; }

.btn-voltar {
  margin-top: 4px;
  padding: 13px 32px;
  background: var(--ck-gold-grad);
  color: var(--ck-text);
  font-family: var(--fonte-ui);
  font-weight: 600;
  font-size: 15px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  letter-spacing: 0.02em;
}

/* ── Container ─────────────────────────────────────────────────────────── */
.checkout-container {
  max-width: 1120px;
  margin: 0 auto;
  padding: 0 32px;
}

/* ── Header ────────────────────────────────────────────────────────────── */
.checkout-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 44px;
}

.btn-back {
  display: flex;
  align-items: center;
  gap: 7px;
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--fonte-ui);
  font-size: 14px;
  font-weight: 500;
  color: var(--ck-muted);
  padding: 0;
  transition: color 0.2s;
}
.btn-back:hover { color: var(--ck-text); }

.checkout-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 13px;
  font-weight: 500;
  color: var(--ck-subtle);
  letter-spacing: 0.02em;
}
.step.active { color: var(--ck-text); font-weight: 600; }
.step-divider { color: var(--ck-border); font-size: 16px; }

/* ── Grid ──────────────────────────────────────────────────────────────── */
.checkout-grid {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 28px;
  align-items: start;
}

/* ── Sections ──────────────────────────────────────────────────────────── */
.checkout-section {
  background: var(--ck-card);
  border: 1px solid var(--ck-border);
  border-radius: var(--ck-radius);
  padding: 32px 36px;
  margin-bottom: 20px;
  box-shadow: var(--ck-shadow);
}

.section-eyebrow { margin-bottom: 10px; }

.eyebrow-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--fonte-ui);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.28em;
  text-transform: uppercase;
  color: #7B2FE0;
  border: 1px solid rgba(123,47,224,0.35);
  border-radius: 30px;
  padding: 4px 14px;
  background: rgba(123,47,224,0.04);
}

.section-title {
  font-family: var(--fonte-principal);
  font-size: 24px;
  font-weight: 600;
  color: var(--ck-text);
  margin: 0 0 24px;
  line-height: 1.25;
}

/* ── Itens ─────────────────────────────────────────────────────────────── */
.itens-lista { display: flex; flex-direction: column; }

.item-checkout {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 0;
  border-bottom: 1px solid #F2EFE9;
}
.item-checkout:last-child { border-bottom: none; padding-bottom: 0; }
.item-checkout:first-child { padding-top: 0; }

.item-info { display: flex; flex-direction: column; gap: 6px; }
.item-nome {
  font-size: 15px;
  font-weight: 600;
  color: var(--ck-text);
  line-height: 1.3;
}

.item-plano-badge {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
  width: fit-content;
  letter-spacing: 0.04em;
}
.item-plano-badge.mensal  { background: rgba(201,168,76,0.13); color: #8A6520; }
.item-plano-badge.semestral { background: rgba(123,47,224,0.09); color: #6B25C9; }
.item-plano-badge.anual   { background: rgba(27,26,25,0.07); color: #3D3B39; }

.item-preco { display: flex; align-items: center; gap: 10px; }
.item-qtd { font-size: 13px; color: var(--ck-subtle); }
.item-valor { font-size: 16px; font-weight: 700; color: var(--ck-text); }

/* ── Endereços ─────────────────────────────────────────────────────────── */
.enderecos-lista { display: flex; flex-direction: column; gap: 12px; margin-bottom: 16px; }

.endereco-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 18px 20px;
  border: 1.5px solid var(--ck-border);
  border-radius: 12px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
  position: relative;
  background: var(--ck-card);
}
.endereco-card:hover { border-color: #D4B96A; box-shadow: 0 2px 10px rgba(201,168,76,0.12); }
.endereco-card.selected {
  border-color: var(--ck-gold);
  background: #FFFBF0;
  box-shadow: 0 2px 12px rgba(201,168,76,0.16);
}

.endereco-radio { padding-top: 3px; flex-shrink: 0; }

.radio-dot {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #D0CCC6;
  transition: border-color 0.2s;
  position: relative;
  background: #fff;
}
.radio-dot.active { border-color: var(--ck-gold); }
.radio-dot.active::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--ck-gold);
}

.endereco-info { flex: 1; }
.endereco-tipo {
  font-size: 11px;
  font-weight: 700;
  color: var(--ck-subtle);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 6px;
}
.endereco-linha { font-size: 15px; color: var(--ck-text2); line-height: 1.6; }
.endereco-cep { font-size: 13px; color: var(--ck-muted); margin-top: 3px; }

.badge-principal {
  font-size: 11px;
  font-weight: 600;
  background: rgba(201,168,76,0.15);
  color: #8A6520;
  padding: 4px 10px;
  border-radius: 20px;
  position: absolute;
  top: 14px;
  right: 16px;
}

.btn-novo-endereco {
  display: flex;
  align-items: center;
  gap: 10px;
  background: none;
  border: 1.5px dashed #D0CCC6;
  border-radius: 12px;
  padding: 15px 20px;
  width: 100%;
  cursor: pointer;
  font-family: var(--fonte-ui);
  font-size: 14px;
  font-weight: 500;
  color: var(--ck-muted);
  transition: border-color 0.2s, color 0.2s;
}
.btn-novo-endereco:hover { border-color: var(--ck-gold); color: #8A6520; }

.loading-text { font-size: 14px; color: var(--ck-subtle); padding: 8px 0; }

/* ── Cupom ─────────────────────────────────────────────────────────────── */
.cupom-form { display: flex; gap: 10px; }

.input-cupom {
  flex: 1;
  height: 48px;
  padding: 0 18px;
  border: 1.5px solid #C8C4BB;
  border-radius: 10px;
  font-family: var(--fonte-ui);
  font-size: 15px;
  color: var(--ck-text);
  background: #FFFFFF;
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.input-cupom:focus { border-color: var(--ck-gold); box-shadow: 0 0 0 3px rgba(201,168,76,0.15); }
.input-cupom::placeholder { color: #B0ABA4; }
.input-cupom:disabled { background: #F0EDE7; color: var(--ck-muted); }

.btn-cupom {
  padding: 0 24px;
  height: 48px;
  background: var(--ck-gold-grad);
  color: var(--ck-text);
  font-family: var(--fonte-ui);
  font-weight: 700;
  font-size: 14px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  letter-spacing: 0.03em;
  white-space: nowrap;
  transition: opacity 0.2s;
}
.btn-cupom:hover:not(:disabled) { opacity: 0.88; }
.btn-cupom:disabled { opacity: 0.45; cursor: not-allowed; }

.btn-cupom-remover {
  padding: 0 18px;
  height: 48px;
  background: #F2EFE9;
  border: 1px solid var(--ck-border);
  border-radius: 10px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: var(--ck-muted);
  font-family: var(--fonte-ui);
  transition: background 0.2s;
}
.btn-cupom-remover:hover { background: var(--ck-border); }

.cupom-feedback { margin-top: 10px; font-size: 14px; color: #3A7D52; font-weight: 500; }
.cupom-feedback.erro { color: #B83232; }

/* ── Pagamento ─────────────────────────────────────────────────────────── */
.pagamento-opcoes { display: flex; gap: 12px; margin-bottom: 24px; }

.pagamento-card {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border: 1.5px solid #C8C4BB;
  border-radius: 12px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s, box-shadow 0.2s;
  font-size: 15px;
  font-weight: 500;
  color: var(--ck-text2);
  flex: 1;
  background: var(--ck-card);
}
.pagamento-card:hover { border-color: #D4B96A; }
.pagamento-card.selected {
  border-color: var(--ck-gold);
  background: #FFFBF0;
  color: var(--ck-text);
  box-shadow: 0 2px 10px rgba(201,168,76,0.14);
}

.cartao-form { display: flex; flex-direction: column; gap: 18px; }

.form-row { display: flex; gap: 14px; }
.form-group { display: flex; flex-direction: column; gap: 7px; flex: 1; }
.form-group.flex-1 { flex: 1; }
.form-group.flex-2 { flex: 2; }
.form-group.flex-3 { flex: 3; }

.form-group label {
  font-size: 13px;
  font-weight: 600;
  color: var(--ck-text2);
}

.form-input {
  height: 48px;
  padding: 0 16px;
  border: 1.5px solid #C8C4BB;
  border-radius: 10px;
  font-family: var(--fonte-ui);
  font-size: 15px;
  color: var(--ck-text);
  outline: none;
  background: #FFFFFF;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.form-input:focus { border-color: var(--ck-gold); box-shadow: 0 0 0 3px rgba(201,168,76,0.15); }
.form-input::placeholder { color: #B0ABA4; }
select.form-input { cursor: pointer; }

.pix-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 10px;
  padding: 28px 20px;
  background: #FFFBF0;
  border: 1px dashed rgba(201,168,76,0.4);
  border-radius: 12px;
  font-size: 15px;
  color: var(--ck-muted);
  line-height: 1.6;
}
.pix-destaque { font-weight: 700; color: var(--ck-text); margin: 0; font-size: 15px; }
.pix-info p { margin: 0; }

/* ── Resumo sticky ─────────────────────────────────────────────────────── */
.checkout-resumo { position: sticky; top: 28px; }

.resumo-card {
  background: var(--ck-card);
  border: 1px solid var(--ck-border);
  border-radius: var(--ck-radius);
  padding: 28px 28px 32px;
  box-shadow: var(--ck-shadow);
}

.resumo-titulo {
  font-family: var(--fonte-principal);
  font-size: 22px;
  font-weight: 600;
  color: var(--ck-text);
  margin: 0 0 22px;
  padding-bottom: 18px;
  border-bottom: 1px solid #F2EFE9;
}

.resumo-itens { display: flex; flex-direction: column; gap: 12px; margin-bottom: 20px; }

.resumo-item { display: flex; justify-content: space-between; align-items: baseline; gap: 8px; }
.resumo-item-nome { font-size: 14px; color: var(--ck-text2); flex: 1; line-height: 1.4; }
.resumo-item-qtd { color: var(--ck-muted); font-size: 12px; }
.resumo-item-valor { font-size: 14px; font-weight: 700; color: var(--ck-text); white-space: nowrap; }

.resumo-divider { height: 1px; background: #F2EFE9; margin: 18px 0; }

.resumo-linha {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 14px;
  font-weight: 500;
  color: var(--ck-text2);
  margin-bottom: 10px;
}
.resumo-linha.desconto { color: #3A7D52; font-weight: 600; }
.frete-gratis { color: #3A7D52; font-weight: 600; }

.resumo-total {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  font-family: var(--fonte-principal);
  font-size: 26px;
  font-weight: 700;
  color: var(--ck-text);
  margin-bottom: 22px;
  padding-top: 4px;
}

.btn-finalizar {
  width: 100%;
  height: 54px;
  background: var(--ck-gold-grad);
  color: var(--ck-text);
  font-family: var(--fonte-ui);
  font-weight: 700;
  font-size: 16px;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: opacity 0.2s, transform 0.15s;
  letter-spacing: 0.03em;
  box-shadow: 0 4px 16px rgba(201,168,76,0.3);
}
.btn-finalizar:hover:not(:disabled) { opacity: 0.9; transform: translateY(-2px); box-shadow: 0 6px 22px rgba(201,168,76,0.38); }
.btn-finalizar:disabled { opacity: 0.45; cursor: not-allowed; transform: none; box-shadow: none; }

.aviso-endereco {
  text-align: center;
  font-size: 12px;
  font-weight: 500;
  color: #C07010;
  margin: 10px 0 0;
}

.resumo-seguranca {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  font-size: 12px;
  font-weight: 500;
  color: var(--ck-muted);
  margin-top: 18px;
}

/* ── Modal ─────────────────────────────────────────────────────────────── */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(27,26,25,0.5);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}

.modal-endereco {
  background: var(--ck-card);
  border-radius: 18px;
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(27,26,25,0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 28px 32px 0;
}
.modal-header h3 {
  font-family: var(--fonte-principal);
  font-size: 24px;
  font-weight: 600;
  color: var(--ck-text);
  margin: 0;
}

.modal-close {
  background: #F2EFE9;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: var(--ck-muted);
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, color 0.2s;
}
.modal-close:hover { background: var(--ck-border); color: var(--ck-text); }

.modal-body { padding: 24px 32px; display: flex; flex-direction: column; gap: 18px; }

.modal-footer {
  padding: 0 32px 28px;
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.btn-cancelar {
  padding: 11px 22px;
  background: #F2EFE9;
  border: 1px solid var(--ck-border);
  border-radius: 10px;
  cursor: pointer;
  font-family: var(--fonte-ui);
  font-size: 14px;
  font-weight: 500;
  color: var(--ck-muted);
  transition: background 0.2s;
}
.btn-cancelar:hover { background: var(--ck-border); }

.btn-salvar {
  padding: 11px 28px;
  background: var(--ck-gold-grad);
  color: var(--ck-text);
  font-family: var(--fonte-ui);
  font-weight: 700;
  font-size: 14px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: opacity 0.2s;
}
.btn-salvar:hover:not(:disabled) { opacity: 0.88; }
.btn-salvar:disabled { opacity: 0.45; cursor: not-allowed; }

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: var(--ck-text2);
}
.checkbox-input { display: none; }
.checkbox-mark {
  width: 20px;
  height: 20px;
  border: 1.5px solid #D0CCC6;
  border-radius: 6px;
  flex-shrink: 0;
  position: relative;
  transition: border-color 0.2s, background 0.2s;
  background: #fff;
}
.checkbox-input:checked + .checkbox-mark {
  background: var(--ck-gold-grad);
  border-color: var(--ck-gold);
}
.checkbox-input:checked + .checkbox-mark::after {
  content: '✓';
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: var(--ck-text);
  font-weight: 800;
}

/* ── Toast ─────────────────────────────────────────────────────────────── */
.toast {
  position: fixed;
  bottom: 36px;
  right: 36px;
  padding: 15px 24px;
  border-radius: 12px;
  font-family: var(--fonte-ui);
  font-size: 14px;
  font-weight: 600;
  z-index: 2000;
  animation: slideUp 0.3s ease;
  box-shadow: 0 8px 30px rgba(0,0,0,0.18);
}
.toast.success { background: #1B1A19; color: #C9A84C; }
.toast.error   { background: #B83232; color: #fff; }

@keyframes slideUp {
  from { transform: translateY(16px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}

/* ── Responsive ────────────────────────────────────────────────────────── */
@media (max-width: 880px) {
  .checkout-grid { grid-template-columns: 1fr; }
  .checkout-resumo { position: static; }
  .checkout-container { padding: 0 20px; }
  .checkout-header { flex-direction: column; align-items: flex-start; gap: 14px; }
  .form-row { flex-direction: column; }
  .pagamento-opcoes { flex-direction: column; }
  .checkout-section { padding: 24px 22px; }
}

.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }
</style>
