<template>
  <DefaultLayout>
    <div class="checkout-container">
      <h1 class="checkout-title titulo-lg">Finalizar Compra</h1>

      <div v-if="notificacao" :class="`checkout-notification ${notificacao.tipo}`">
        <div class="notification-content">
          <i :class="notificacao.tipo === 'success' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
          <span>{{ notificacao.msg }}</span>
        </div>
      </div>

      <div class="checkout-content">
        <!-- ESQUERDA -->
        <div class="checkout-left">

          <!-- Endereços -->
          <section class="address-section">
            <div class="section-header">
              <h2>Endereço de Entrega</h2>
              <p>Selecione ou adicione um endereço de entrega</p>
            </div>

            <div class="enderecos-container" v-if="enderecos.length">
              <div v-for="e in enderecos" :key="e.id"
                class="endereco-card"
                :class="{ principal: e.principal === 'sim', selected: enderecoSelecionado?.id === e.id }"
                @click="enderecoSelecionado = e">
                <div class="endereco-header">
                  <h3>{{ e.principal === 'sim' ? 'Endereço Principal' : 'Endereço' }}</h3>
                  <span v-if="e.principal === 'sim'" class="badge-principal">Principal</span>
                </div>
                <div class="endereco-info">
                  <p><strong>{{ e.endereco }}, {{ e.numero }}</strong></p>
                  <p v-if="e.complemento">{{ e.complemento }}</p>
                  <p>{{ e.bairro }} - {{ e.cidade }}/{{ e.estado }}</p>
                  <p>CEP: {{ e.cep }}</p>
                </div>
              </div>

              <div class="add-endereco-card" @click="abrirModal()">
                <div class="add-endereco-content">
                  <i class="fas fa-plus-circle"></i>
                  <h3>Adicionar Endereço</h3>
                  <p>Clique para cadastrar um novo endereço</p>
                </div>
              </div>
            </div>

            <div v-else class="empty-address">
              <i class="fas fa-map-marker-alt"></i>
              <h3>Nenhum endereço cadastrado</h3>
              <p>Adicione um endereço de entrega para continuar.</p>
              <div class="address-actions">
                <button class="btn-confirm-payment" @click="abrirModal()">
                  <i class="fas fa-plus"></i> Adicionar Endereço
                </button>
              </div>
            </div>
          </section>

          <!-- Pagamento -->
          <section class="payment-section">
            <h2>Forma de Pagamento</h2>
            <div class="payment-options">
              <div class="payment-option">
                <input type="radio" id="pix" name="payment" value="pix" v-model="pagamento" />
                <label for="pix">
                  <i class="fas fa-qrcode"></i>
                  <div><strong>Pix</strong><span class="payment-info">Aprovação imediata</span></div>
                </label>
              </div>
              <div class="payment-option">
                <input type="radio" id="cartao" name="payment" value="cartao" v-model="pagamento" />
                <label for="cartao">
                  <i class="fas fa-credit-card"></i>
                  <div><strong>Cartão de Crédito</strong><span class="payment-info">Parcelamento disponível</span></div>
                </label>
              </div>
              <div class="payment-option">
                <input type="radio" id="boleto" name="payment" value="boleto" v-model="pagamento" />
                <label for="boleto">
                  <i class="fas fa-barcode"></i>
                  <div><strong>Boleto Bancário</strong><span class="payment-info">Vencimento em 3 dias úteis</span></div>
                </label>
              </div>
            </div>

            <div v-if="pagamento === 'cartao'" class="card-data">
              <h3>Dados do Cartão</h3>
              <div class="form-group">
                <label>Número do Cartão</label>
                <input v-model="cartao.numero" type="text" placeholder="0000 0000 0000 0000" maxlength="19" />
              </div>
              <div class="form-group">
                <label>Nome no Cartão</label>
                <input v-model="cartao.nome" type="text" placeholder="Nome como está no cartão" />
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>Validade</label>
                  <input v-model="cartao.validade" type="text" placeholder="MM/AA" maxlength="5" />
                </div>
                <div class="form-group">
                  <label>CVV</label>
                  <input v-model="cartao.cvv" type="text" placeholder="000" maxlength="4" />
                </div>
              </div>
            </div>
          </section>
        </div>

        <!-- DIREITA - Resumo -->
        <div class="checkout-right">
          <section class="order-summary">
            <h2>Resumo do Pedido</h2>

            <div class="order-items">
              <div v-if="itensPedido.length" v-for="item in itensPedido" :key="item.id_carrinho" class="order-item">
                <div class="item-info">
                  <h4>{{ item.nome_produto }}</h4>
                  <span class="price">{{ item.plano }}</span>
                </div>
                <span class="item-quantity">x{{ item.quantidade }}</span>
                <span class="item-total">R$ {{ fmt(item.valor_total) }}</span>
              </div>
              <div v-else class="empty-cart">
                <i class="fas fa-shopping-cart"></i>
                <p>Nenhum item selecionado</p>
              </div>
            </div>

            <div class="coupon-section">
              <input v-model="cupomCodigo" type="text" placeholder="Código do cupom" />
              <button class="btn-coupon" @click="aplicarCupom" :disabled="loadingCupom">
                {{ loadingCupom ? '...' : 'Aplicar' }}
              </button>
            </div>

            <div class="order-totals">
              <div class="total-line">
                <span>Subtotal</span>
                <span>R$ {{ fmt(subtotal) }}</span>
              </div>
              <div v-if="desconto > 0" class="total-line discount">
                <span>Desconto</span>
                <span>- R$ {{ fmt(desconto) }}</span>
              </div>
              <div class="total-line final">
                <span>Total</span>
                <span>R$ {{ fmt(subtotal - desconto) }}</span>
              </div>
            </div>

            <button class="btn-confirm-payment" @click="confirmarPagamento" :disabled="loading || !enderecoSelecionado">
              <i class="fas fa-lock"></i>
              {{ loading ? 'Processando...' : 'Confirmar Pagamento' }}
            </button>
            <p class="security-note"><i class="fas fa-shield-alt"></i> Pagamento 100% seguro</p>
          </section>
        </div>
      </div>
    </div>

    <ModalEndereco
      :aberto="modalAberto"
      :endereco="enderecoEditando"
      @fechar="fecharModal"
      @salvo="onEnderecoSalvo"
    />
  </DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import ModalEndereco from '@/components/ModalEndereco.vue'
import api from '@/services/api'

const router            = useRouter()
const enderecos         = ref([])
const enderecoSelecionado = ref(null)
const itensPedido       = ref([])
const pagamento         = ref('pix')
const cupomCodigo       = ref('')
const desconto          = ref(0)
const loading           = ref(false)
const loadingCupom      = ref(false)
const modalAberto       = ref(false)
const enderecoEditando  = ref(null)
const notificacao       = ref(null)
const cartao            = ref({ numero: '', nome: '', validade: '', cvv: '' })

const subtotal = computed(() => itensPedido.value.reduce((s, i) => s + parseFloat(i.valor_total || 0), 0))
function fmt(v) { return parseFloat(v || 0).toFixed(2).replace('.', ',') }

function mostrarNotificacao(msg, tipo = 'success') {
  notificacao.value = { msg, tipo }
  setTimeout(() => notificacao.value = null, 4000)
}

function abrirModal(e = null) { enderecoEditando.value = e; modalAberto.value = true }
function fecharModal()        { modalAberto.value = false; enderecoEditando.value = null }

async function onEnderecoSalvo(dados) {
  if (enderecoEditando.value?.id)
    await api.put(`/configuracoes/enderecos/${enderecoEditando.value.id}`, dados)
  else
    await api.post('/configuracoes/enderecos', dados)
  await carregarDados()
  fecharModal()
}

async function aplicarCupom() {
  if (!cupomCodigo.value.trim()) return
  loadingCupom.value = true
  try {
    const { data } = await api.post('/cupons/validar', { codigo: cupomCodigo.value, total: subtotal.value })
    desconto.value = data.desconto || 0
    mostrarNotificacao(`Cupom aplicado! Desconto: R$ ${fmt(desconto.value)}`)
  } catch (e) {
    mostrarNotificacao(e.response?.data?.error || 'Cupom inválido', 'error')
  } finally {
    loadingCupom.value = false
  }
}

async function confirmarPagamento() {
  if (!enderecoSelecionado.value) { mostrarNotificacao('Selecione um endereço.', 'error'); return }
  if (!itensPedido.value.length)  { mostrarNotificacao('Nenhum item selecionado.', 'error'); return }
  loading.value = true
  try {
    const ids = JSON.parse(sessionStorage.getItem('checkout_ids') || '[]')
    await api.post('/carrinho/finalizar', {
      itens_ids: ids,
      forma_pagamento: pagamento.value,
      endereco_id: enderecoSelecionado.value.id,
      cupom: cupomCodigo.value || null,
    })
    sessionStorage.removeItem('checkout_ids')
    mostrarNotificacao('Pedido realizado com sucesso!')
    setTimeout(() => router.push('/configuracoes'), 2000)
  } catch (e) {
    mostrarNotificacao(e.response?.data?.error || 'Erro ao finalizar pedido.', 'error')
  } finally {
    loading.value = false
  }
}

async function carregarDados() {
  const [resEnd, resCart] = await Promise.all([
    api.get('/configuracoes/perfil'),
    (async () => {
      const ids = JSON.parse(sessionStorage.getItem('checkout_ids') || '[]')
      if (!ids.length) return { data: { itens: [] } }
      return api.post('/carrinho/itens_selecionados', { itens_selecionados: ids })
    })()
  ])
  enderecos.value       = resEnd.data.enderecos || []
  enderecoSelecionado.value = enderecos.value.find(e => e.principal === 'sim') || enderecos.value[0] || null
  itensPedido.value     = resCart.data.itens || []
}

onMounted(carregarDados)
</script>

<style scoped>
.checkout-container {
  max-width: 1200px;
  margin: 120px auto var(--espacamento-lg);
  padding: 0 var(--espacamento-sm);
  animation: fadeInUp 0.6s ease-out;
}

.checkout-title {
  text-align: center;
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-lg);
  position: relative;
}
.checkout-title::after {
  content: '';
  position: absolute;
  bottom: -10px; left: 50%;
  transform: translateX(-50%);
  width: 100px; height: 3px;
  background: var(--gradiente-botao);
  border-radius: var(--borda-radius-sm);
}

.checkout-content { display: flex; gap: var(--espacamento-lg); align-items: flex-start; }

.checkout-left {
  flex: 1;
  background: var(--cor-fundo-secundario);
  padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-lg);
  border: 1px solid rgba(255, 215, 0, 0.2);
  box-shadow: var(--sombra-card);
  position: relative; overflow: hidden;
  display: flex; flex-direction: column; gap: var(--espacamento-lg);
}
.checkout-left::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0;
  height: 3px; background: var(--gradiente-botao);
}

.checkout-right {
  flex: 0 0 400px;
  background: var(--cor-fundo-secundario);
  padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-lg);
  border: 1px solid rgba(255, 215, 0, 0.2);
  box-shadow: var(--sombra-card);
  height: fit-content; position: sticky; top: 120px;
  overflow: hidden; display: flex; flex-direction: column;
}
.checkout-right::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0;
  height: 3px; background: var(--gradiente-botao);
}

/* Seções */
.section-header h2, .payment-section h2, .order-summary h2 {
  color: var(--cor-dourado);
  font-family: var(--fonte-secundaria);
  border-left: 3px solid var(--cor-dourado);
  padding-left: var(--espacamento-sm);
  margin-bottom: var(--espacamento-sm);
}
.section-header p { color: var(--cor-texto-secundario); font-size: 0.9rem; margin-bottom: var(--espacamento-md); }

/* Endereços */
.enderecos-container { display: grid; gap: var(--espacamento-md); margin-bottom: var(--espacamento-md); }

.endereco-card {
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-md);
  border: 2px solid transparent;
  transition: all 0.3s; cursor: pointer; position: relative;
}
.endereco-card.principal { border-color: var(--cor-dourado); background: rgba(255,215,0,0.05); }
.endereco-card.selected  { border-color: var(--cor-dourado); background: rgba(255,215,0,0.1); box-shadow: 0 0 20px rgba(255,215,0,0.2); }
.endereco-card.selected::before {
  content: '✓'; position: absolute; top: -10px; right: -10px;
  background: var(--cor-dourado); color: var(--cor-fundo);
  width: 24px; height: 24px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-weight: bold; font-size: 0.8rem;
}
.endereco-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--espacamento-sm); }
.endereco-header h3 { margin: 0; color: var(--cor-texto); font-weight: 600; }
.badge-principal {
  background: var(--cor-dourado); color: var(--cor-fundo);
  padding: var(--espacamento-xs) 0.75rem;
  border-radius: var(--borda-radius-lg); font-size: 0.75rem; font-weight: 500;
}
.endereco-info p { margin: 0.5rem 0; color: var(--cor-texto-secundario); font-size: 0.9rem; }
.endereco-info p strong { color: var(--cor-texto); }

.add-endereco-card {
  background: var(--cor-fundo); border: 2px dashed rgba(255,215,0,0.3);
  border-radius: var(--borda-radius-lg); padding: var(--espacamento-lg);
  text-align: center; cursor: pointer; transition: all 0.3s;
}
.add-endereco-card:hover { border-color: var(--cor-dourado); }
.add-endereco-content i { font-size: 2rem; color: var(--cor-dourado); margin-bottom: var(--espacamento-sm); display: block; }
.add-endereco-content h3 { color: var(--cor-texto); margin-bottom: 0.25rem; }
.add-endereco-content p  { color: var(--cor-texto-secundario); margin: 0; }

.empty-address {
  text-align: center; padding: var(--espacamento-xl);
  border: 2px dashed rgba(255,215,0,0.3); border-radius: var(--borda-radius-lg);
  color: var(--cor-texto-secundario);
}
.empty-address i { font-size: 3rem; color: var(--cor-dourado); margin-bottom: var(--espacamento-sm); display: block; }
.empty-address h3 { color: var(--cor-texto); margin-bottom: var(--espacamento-xs); }
.empty-address p  { margin-bottom: var(--espacamento-lg); }
.address-actions  { display: flex; justify-content: center; }

/* Pagamento */
.payment-options { display: flex; flex-direction: column; gap: var(--espacamento-sm); }

.payment-option { display: flex; align-items: center; }
.payment-option input[type="radio"] { display: none; }
.payment-option label {
  display: flex; align-items: center; gap: var(--espacamento-sm);
  padding: var(--espacamento-md);
  border: 2px solid rgba(255,255,255,0.1);
  border-radius: var(--borda-radius-md); cursor: pointer;
  transition: all 0.3s; flex: 1;
  background: var(--cor-fundo); position: relative; overflow: hidden;
}
.payment-option label::before {
  content: ''; position: absolute; top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,215,0,0.1), transparent);
  transition: left 0.5s;
}
.payment-option label:hover::before { left: 100%; }
.payment-option input[type="radio"]:checked + label {
  border-color: var(--cor-dourado); background: rgba(255,215,0,0.05);
  box-shadow: 0 0 20px rgba(255,215,0,0.2);
}
.payment-option label i { font-size: 1.5rem; color: var(--cor-dourado); width: 30px; text-align: center; }
.payment-option label div { display: flex; flex-direction: column; }
.payment-option label strong { color: var(--cor-texto); font-weight: 600; margin-bottom: 0.25rem; }
.payment-info { font-size: 0.9rem; color: var(--cor-texto-secundario); }

/* Card data */
.card-data {
  margin-top: var(--espacamento-lg); padding-top: var(--espacamento-lg);
  border-top: 1px solid rgba(255,215,0,0.2); animation: slideDown 0.3s ease-out;
}
.card-data h3 {
  color: var(--cor-dourado); font-family: var(--fonte-secundaria);
  border-left: 3px solid var(--cor-roxo-principal);
  padding-left: var(--espacamento-sm); margin-bottom: var(--espacamento-md);
}
.form-group { margin-bottom: var(--espacamento-md); }
.form-group label { display: block; color: var(--cor-texto); margin-bottom: var(--espacamento-xs); font-weight: 500; font-size: 0.9rem; }
.form-group input {
  width: 100%; padding: 0.875rem 1rem;
  border: 1px solid rgba(255,255,255,0.1); border-radius: var(--borda-radius-md);
  background: var(--cor-fundo); color: var(--cor-texto); font-size: 1rem;
  transition: all 0.3s; font-family: var(--fonte-principal);
}
.form-group input::placeholder { color: var(--cor-texto-secundario); opacity: 0.7; }
.form-group input:focus { outline: none; border-color: var(--cor-dourado); box-shadow: 0 0 0 3px rgba(255,215,0,0.1); }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: var(--espacamento-md); }

/* Order summary */
.order-items { margin-bottom: var(--espacamento-md); max-height: 400px; overflow-y: auto; }
.order-items::-webkit-scrollbar { width: 6px; }
.order-items::-webkit-scrollbar-track { background: var(--cor-fundo); }
.order-items::-webkit-scrollbar-thumb { background: var(--cor-dourado); border-radius: var(--borda-radius-sm); }

.order-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: var(--espacamento-sm) 0; border-bottom: 1px solid rgba(255,255,255,0.1);
}
.order-item:last-child { border-bottom: none; }
.item-info h4 { color: var(--cor-texto); margin-bottom: 0.25rem; font-weight: 500; }
.item-info .price { color: var(--cor-dourado); font-size: 0.9rem; }
.item-quantity { color: var(--cor-texto-secundario); font-size: 0.9rem; background: rgba(255,215,0,0.1); padding: 0.25rem 0.5rem; border-radius: var(--borda-radius-sm); }
.item-total { color: var(--cor-dourado); font-weight: bold; }

.empty-cart { text-align: center; color: var(--cor-texto-secundario); padding: var(--espacamento-lg); border: 2px dashed rgba(255,215,0,0.3); border-radius: var(--borda-radius-md); }
.empty-cart i { font-size: 3rem; color: var(--cor-dourado); margin-bottom: var(--espacamento-sm); display: block; }

/* Cupom */
.coupon-section {
  display: flex; gap: var(--espacamento-xs);
  margin: var(--espacamento-lg) 0;
  background: var(--cor-fundo); padding: var(--espacamento-sm);
  border-radius: var(--borda-radius-md); border: 1px solid rgba(255,215,0,0.2);
}
.coupon-section input {
  flex: 1; padding: 0.875rem 1rem;
  border: 1px solid rgba(255,255,255,0.1); border-radius: var(--borda-radius-md);
  background: var(--cor-fundo-secundario); color: var(--cor-texto); font-family: var(--fonte-principal);
}
.coupon-section input:focus { outline: none; border-color: var(--cor-dourado); }
.btn-coupon {
  padding: 0.875rem 1.5rem; background: var(--gradiente-botao);
  color: var(--cor-fundo); border: none; border-radius: var(--borda-radius-md);
  cursor: pointer; transition: all 0.3s; font-weight: 600; white-space: nowrap;
}
.btn-coupon:hover { transform: translateY(-2px); box-shadow: var(--sombra-destaque); }
.btn-coupon:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }

/* Totais */
.order-totals { border-top: 1px solid rgba(255,215,0,0.2); padding-top: var(--espacamento-md); }
.total-line { display: flex; justify-content: space-between; margin-bottom: var(--espacamento-sm); color: var(--cor-texto); }
.total-line.discount { color: #00ff88; background: rgba(0,255,136,0.1); padding: var(--espacamento-xs) var(--espacamento-sm); border-radius: var(--borda-radius-sm); }
.total-line.final { border-top: 1px solid rgba(255,215,0,0.2); padding-top: var(--espacamento-sm); font-size: 1.25rem; color: var(--cor-dourado); }

.btn-confirm-payment {
  width: 100%; padding: 1rem 2rem;
  background: var(--gradiente-botao); color: var(--cor-fundo); border: none;
  border-radius: var(--borda-radius-lg); font-size: 1.1rem; font-weight: 600;
  cursor: pointer; transition: all 0.3s; margin-top: var(--espacamento-md);
  position: relative; overflow: hidden;
  display: flex; align-items: center; justify-content: center; gap: var(--espacamento-xs);
}
.btn-confirm-payment::before {
  content: ''; position: absolute; top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}
.btn-confirm-payment:hover::before { left: 100%; }
.btn-confirm-payment:hover:not(:disabled) { transform: translateY(-3px); box-shadow: var(--sombra-destaque); }
.btn-confirm-payment:disabled { background: #666; cursor: not-allowed; }

.security-note { text-align: center; color: var(--cor-texto-secundario); font-size: 0.8rem; margin-top: var(--espacamento-sm); display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
.security-note i { color: var(--cor-dourado); }

/* Notificação */
.checkout-notification {
  position: fixed; top: 120px; right: 20px;
  background: var(--cor-roxo-principal); color: white;
  padding: 1rem 1.5rem; border-radius: var(--borda-radius-md);
  box-shadow: var(--sombra-destaque); z-index: 10000;
  animation: slideInRight 0.3s ease-out;
  max-width: 400px; border: 1px solid var(--cor-dourado);
}
.checkout-notification.error { background: #ff4444; border-color: #cc0000; }
.notification-content { display: flex; align-items: center; gap: 0.5rem; }

@keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideDown { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
@keyframes slideInRight { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }

@media (max-width: 1024px) {
  .checkout-content { flex-direction: column; }
  .checkout-right { flex: 1; width: 100%; position: static; }
}

@media (max-width: 768px) {
  .checkout-container { margin: 100px auto var(--espacamento-md); padding: 0 var(--espacamento-xs); }
  .checkout-left, .checkout-right { padding: var(--espacamento-md); }
  .form-row { grid-template-columns: 1fr; }
  .coupon-section { flex-direction: column; }
  .checkout-notification { right: 10px; left: 10px; max-width: none; }
}

@media (max-width: 480px) {
  .checkout-left, .checkout-right { padding: var(--espacamento-sm); }
}
</style>