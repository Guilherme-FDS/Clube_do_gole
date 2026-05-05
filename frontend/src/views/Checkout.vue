<template>
  <div class="checkout-container">
    <h1 class="checkout-title titulo-lg">Finalizar Compra</h1>

    <div class="checkout-content">
      <!-- COLUNA ESQUERDA - ENDEREÇOS E PAGAMENTO -->
      <div class="checkout-left">
        <!-- SEÇÃO DE ENDEREÇO -->
        <section class="address-section">
          <div class="section-header">
            <h2 class="titulo-md">Endereço de Entrega</h2>
            <p>Selecione ou adicione um endereço para entrega</p>
          </div>

          <div class="enderecos-container" id="enderecosContainer">
            <div v-if="enderecos.length === 0" class="empty-address">
              <i class="fas fa-map-marker-alt"></i>
              <h3>Nenhum endereço cadastrado</h3>
              <p>Você precisa cadastrar um endereço para continuar com a compra</p>
              <button class="btn-primary" @click="abrirModalEndereco">
                <i class="fas fa-plus"></i> Adicionar Primeiro Endereço
              </button>
            </div>

            <div v-for="endereco in enderecos" :key="endereco.id" class="endereco-card"
                 :class="{ principal: endereco.principal === 'sim', selected: enderecoSelecionado === endereco.id }"
                 @click="selecionarEndereco(endereco.id)">
              <div class="endereco-header">
                <h3>{{ endereco.principal === 'sim' ? 'Endereço Principal' : `Endereço` }}</h3>
                <span v-if="endereco.principal === 'sim'" class="badge-principal">Principal</span>
              </div>
              <div class="endereco-info">
                <p><strong>{{ endereco.endereco }}, {{ endereco.numero }}</strong></p>
                <p v-if="endereco.complemento">Complemento: {{ endereco.complemento }}</p>
                <p>{{ endereco.bairro }} - {{ endereco.cidade }}/{{ endereco.estado }}</p>
                <p>CEP: {{ endereco.cep }}</p>
              </div>
              <div class="endereco-actions">
                <button type="button" class="btn-edit" @click.stop="editarEndereco(endereco)">
                  <i class="fas fa-edit"></i> Editar
                </button>
                <button v-if="endereco.principal !== 'sim'" type="button" class="btn-set-primary"
                        @click.stop="definirComoPrincipal(endereco.id)">
                  <i class="fas fa-star"></i> Tornar Principal
                </button>
                <button v-if="enderecos.length > 1" type="button" class="btn-delete"
                        @click.stop="excluirEndereco(endereco.id)">
                  <i class="fas fa-trash"></i> Excluir
                </button>
              </div>
              <div class="endereco-selecao">
                <label class="checkbox-label">
                  <input type="radio" name="endereco_entrega" :value="endereco.id"
                         :checked="enderecoSelecionado === endereco.id"
                         @change="selecionarEndereco(endereco.id)">
                  <span class="checkmark"></span>
                  Usar este endereço para entrega
                </label>
              </div>
            </div>
          </div>

          <div class="address-actions">
            <button class="btn-secondary" @click="abrirModalEndereco">
              <i class="fas fa-plus"></i> Adicionar Novo Endereço
            </button>
          </div>
        </section>

        <!-- SEÇÃO DE PAGAMENTO -->
        <section class="payment-section">
          <h2 class="titulo-md">Forma de Pagamento</h2>
          <div class="payment-options">
            <div class="payment-option">
              <input type="radio" id="pix" value="pix" v-model="metodoPagamento">
              <label for="pix">
                <i class="fas fa-qrcode"></i>
                <div>
                  <strong>Pix</strong>
                  <span class="payment-info">Aprovação imediata</span>
                </div>
              </label>
            </div>
            <div class="payment-option">
              <input type="radio" id="cartao" value="cartao" v-model="metodoPagamento">
              <label for="cartao">
                <i class="fas fa-credit-card"></i>
                <div>
                  <strong>Cartão de Crédito</strong>
                  <span class="payment-info">Parcele em até 12x</span>
                </div>
              </label>
            </div>
            <div class="payment-option">
              <input type="radio" id="boleto" value="boleto" v-model="metodoPagamento">
              <label for="boleto">
                <i class="fas fa-barcode"></i>
                <div>
                  <strong>Boleto Bancário</strong>
                  <span class="payment-info">Aprovação em 1 a 2 dias úteis</span>
                </div>
              </label>
            </div>
          </div>
        </section>

        <!-- DADOS DO CARTÃO (exibe apenas se cartão selecionado) -->
        <div v-if="metodoPagamento === 'cartao'" class="card-data">
          <h3 class="titulo-md">Dados do Cartão</h3>
          <div class="form-group">
            <label for="cardNumber">Número do Cartão</label>
            <input type="text" id="cardNumber" v-model="cartao.numero" placeholder="0000 0000 0000 0000" maxlength="19">
          </div>
          <div class="form-row">
            <div class="form-group">
              <label for="cardExpiry">Validade</label>
              <input type="text" id="cardExpiry" v-model="cartao.validade" placeholder="MM/AA" maxlength="5">
            </div>
            <div class="form-group">
              <label for="cardCVC">CVV</label>
              <input type="text" id="cardCVC" v-model="cartao.cvv" placeholder="000" maxlength="3">
            </div>
          </div>
          <div class="form-group">
            <label for="cardName">Nome no Cartão</label>
            <input type="text" id="cardName" v-model="cartao.nome" placeholder="Como está no cartão">
          </div>
        </div>
      </div>

      <!-- COLUNA DIREITA - RESUMO DA COMPRA -->
      <div class="checkout-right">
        <section class="order-summary">
          <h2 class="titulo-md">Resumo do Pedido</h2>

          <div class="order-items" v-if="itens.length">
            <div v-for="item in itens" :key="item.id_carrinho" class="order-item">
              <div class="item-info">
                <h4>{{ item.nome_produto }}</h4>
                <span class="price">{{ formatarMoeda(item.valor_unitario) }}</span>
              </div>
              <div class="item-quantity">{{ item.quantidade }}x</div>
              <div class="item-total">{{ formatarMoeda(item.valor_total) }}</div>
            </div>
          </div>
          <div v-else class="empty-cart">
            <i class="fas fa-shopping-cart"></i>
            <p>Carregando itens...</p>
          </div>

          <div class="coupon-section">
            <input type="text" v-model="codigoCupom" placeholder="Digite o código do cupom">
            <button class="btn-coupon" @click="aplicarCupom" :disabled="aplicandoCupom">
              {{ aplicandoCupom ? 'Aplicando...' : 'Aplicar' }}
            </button>
          </div>

          <div class="order-totals">
            <div class="total-line">
              <span>Subtotal</span>
              <span>{{ formatarMoeda(subtotal) }}</span>
            </div>
            <div class="total-line">
              <span>Frete</span>
              <span>Grátis</span>
            </div>
            <div v-if="desconto > 0" class="total-line discount">
              <span>Desconto</span>
              <span>- {{ formatarMoeda(desconto) }}</span>
            </div>
            <div class="total-line final">
              <strong>Total</strong>
              <strong>{{ formatarMoeda(total) }}</strong>
            </div>
          </div>

          <button class="btn-confirm-payment" @click="finalizarCompra" :disabled="!enderecoSelecionado || processando">
            <i class="fas fa-lock"></i>
            {{ processando ? 'Processando...' : (enderecoSelecionado ? 'Confirmar Pagamento' : 'Selecione um endereço para continuar') }}
          </button>

          <p class="security-note">
            <i class="fas fa-shield-alt"></i>
            Sua informação está segura e criptografada
          </p>
        </section>
      </div>
    </div>

    <!-- MODAL DE ENDEREÇO -->
    <div v-if="modalEnderecoAberto" class="modal" @click.self="fecharModalEndereco">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editandoEndereco ? 'Editar Endereço' : 'Adicionar Novo Endereço' }}</h3>
          <button class="modal-close" @click="fecharModalEndereco">
            <i class="fas fa-times"></i>
          </button>
        </div>

        <form class="endereco-form" @submit.prevent="salvarEndereco">
          <input type="hidden" v-model="enderecoForm.id">

          <div class="form-group">
            <label for="cep">CEP *</label>
            <input type="text" id="cep" v-model="enderecoForm.cep" required maxlength="9" @blur="buscarCep">
          </div>

          <div class="form-grid">
            <div class="form-group">
              <label for="endereco">Endereço *</label>
              <input type="text" id="endereco" v-model="enderecoForm.endereco" required>
            </div>
            <div class="form-group">
              <label for="numero">Número *</label>
              <input type="text" id="numero" v-model="enderecoForm.numero" required>
            </div>
          </div>

          <div class="form-group">
            <label for="complemento">Complemento</label>
            <input type="text" id="complemento" v-model="enderecoForm.complemento" placeholder="Apartamento, bloco, etc.">
          </div>

          <div class="form-grid">
            <div class="form-group">
              <label for="bairro">Bairro *</label>
              <input type="text" id="bairro" v-model="enderecoForm.bairro" required>
            </div>
            <div class="form-group">
              <label for="cidade">Cidade *</label>
              <input type="text" id="cidade" v-model="enderecoForm.cidade" required>
            </div>
          </div>

          <div class="form-grid">
            <div class="form-group">
              <label for="estado">Estado *</label>
              <select v-model="enderecoForm.estado" required>
                <option value="">Selecione</option>
                <option value="AC">Acre</option>
                <option value="AL">Alagoas</option>
                <option value="AP">Amapá</option>
                <option value="AM">Amazonas</option>
                <option value="BA">Bahia</option>
                <option value="CE">Ceará</option>
                <option value="DF">Distrito Federal</option>
                <option value="ES">Espírito Santo</option>
                <option value="GO">Goiás</option>
                <option value="MA">Maranhão</option>
                <option value="MT">Mato Grosso</option>
                <option value="MS">Mato Grosso do Sul</option>
                <option value="MG">Minas Gerais</option>
                <option value="PA">Pará</option>
                <option value="PB">Paraíba</option>
                <option value="PR">Paraná</option>
                <option value="PE">Pernambuco</option>
                <option value="PI">Piauí</option>
                <option value="RJ">Rio de Janeiro</option>
                <option value="RN">Rio Grande do Norte</option>
                <option value="RS">Rio Grande do Sul</option>
                <option value="RO">Rondônia</option>
                <option value="RR">Roraima</option>
                <option value="SC">Santa Catarina</option>
                <option value="SP">São Paulo</option>
                <option value="SE">Sergipe</option>
                <option value="TO">Tocantins</option>
              </select>
            </div>
            <div class="form-group">
              <label for="pais">País *</label>
              <input type="text" id="pais" v-model="enderecoForm.pais" required>
            </div>
          </div>

          <div class="form-group checkbox-group">
            <input type="checkbox" id="endereco_principal" v-model="enderecoForm.principal">
            <label for="endereco_principal">Tornar este endereço principal</label>
          </div>

          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="fecharModalEndereco">Cancelar</button>
            <button type="submit" class="btn-primary">
              <i class="fas fa-save"></i> {{ editandoEndereco ? 'Atualizar Endereço' : 'Salvar Endereço' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCarrinhoStore } from '@/stores/carrinho'

const router = useRouter()
const authStore = useAuthStore()
const carrinhoStore = useCarrinhoStore()

// Dados do checkout
const itens = ref([])
const enderecos = ref([])
const enderecoSelecionado = ref(null)
const metodoPagamento = ref('pix')
const codigoCupom = ref('')
const desconto = ref(0)
const cupomId = ref(null)
const aplicandoCupom = ref(false)
const processando = ref(false)

// Dados do cartão
const cartao = ref({
  numero: '',
  validade: '',
  cvv: '',
  nome: ''
})

// Modal de endereço
const modalEnderecoAberto = ref(false)
const editandoEndereco = ref(false)
const enderecoForm = ref({
  id: null,
  cep: '',
  endereco: '',
  numero: '',
  complemento: '',
  bairro: '',
  cidade: '',
  estado: '',
  pais: 'Brasil',
  principal: false
})

// Computed
const subtotal = computed(() => {
  return itens.value.reduce((sum, item) => sum + (item.valor_total || 0), 0)
})

const total = computed(() => subtotal.value - desconto.value)

// Formatação
const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor || 0)
}

// Máscaras de cartão
const aplicarMascaraCartao = () => {
  // Número do cartão: adiciona espaço a cada 4 dígitos
  let num = cartao.value.numero.replace(/\D/g, '')
  num = num.replace(/(\d{4})(?=\d)/g, '$1 ')
  cartao.value.numero = num.substring(0, 19)

  // Validade: MM/AA
  let val = cartao.value.validade.replace(/\D/g, '')
  if (val.length >= 2) {
    val = val.substring(0, 2) + '/' + val.substring(2, 4)
  }
  cartao.value.validade = val.substring(0, 5)

  // CVV: apenas números, máximo 3
  cartao.value.cvv = cartao.value.cvv.replace(/\D/g, '').substring(0, 3)
}

// Máscara de CEP no modal
const aplicarMascaraCep = () => {
  let cep = enderecoForm.value.cep.replace(/\D/g, '')
  if (cep.length > 5) {
    cep = cep.substring(0, 5) + '-' + cep.substring(5, 8)
  }
  enderecoForm.value.cep = cep.substring(0, 9)
}

// Buscar CEP via ViaCEP
const buscarCep = async () => {
  const cepLimpo = enderecoForm.value.cep.replace(/\D/g, '')
  if (cepLimpo.length !== 8) return

  try {
    const response = await fetch(`https://viacep.com.br/ws/${cepLimpo}/json/`)
    const data = await response.json()
    if (!data.erro) {
      enderecoForm.value.endereco = data.logradouro || ''
      enderecoForm.value.bairro = data.bairro || ''
      enderecoForm.value.cidade = data.localidade || ''
      enderecoForm.value.estado = data.uf || ''
    } else {
      alert('CEP não encontrado. Verifique o número.')
    }
  } catch (error) {
    console.error('Erro ao buscar CEP:', error)
    alert('Erro ao buscar CEP. Tente novamente.')
  }
}

// Carregar itens selecionados do carrinho
const carregarItensSelecionados = async () => {
  const selectedItems = JSON.parse(localStorage.getItem('checkoutItems') || '[]')
  if (selectedItems.length === 0) {
    alert('Nenhum item selecionado. Redirecionando para o carrinho.')
    router.push('/carrinho')
    return
  }

  try {
    const response = await fetch('/api/carrinho/itens_selecionados', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ itens_selecionados: selectedItems })
    })
    const data = await response.json()
    if (data.itens && data.itens.length) {
      itens.value = data.itens
    } else {
      throw new Error('Itens não encontrados')
    }
  } catch (error) {
    console.error(error)
    alert('Erro ao carregar itens. Redirecionando.')
    router.push('/carrinho')
  }
}

// Carregar endereços do usuário
const carregarEnderecos = async () => {
  try {
    const response = await fetch('/api/enderecos')
    const data = await response.json()
    enderecos.value = data.enderecos || []
    // Selecionar automaticamente o endereço principal, se existir
    const principal = enderecos.value.find(e => e.principal === 'sim')
    if (principal) {
      enderecoSelecionado.value = principal.id
    } else if (enderecos.value.length > 0) {
      enderecoSelecionado.value = enderecos.value[0].id
    }
  } catch (error) {
    console.error('Erro ao carregar endereços:', error)
  }
}

// Selecionar endereço
const selecionarEndereco = (id) => {
  enderecoSelecionado.value = id
}

// Abrir modal de endereço
const abrirModalEndereco = (endereco = null) => {
  if (endereco) {
    editandoEndereco.value = true
    enderecoForm.value = {
      id: endereco.id,
      cep: endereco.cep || '',
      endereco: endereco.endereco || '',
      numero: endereco.numero || '',
      complemento: endereco.complemento || '',
      bairro: endereco.bairro || '',
      cidade: endereco.cidade || '',
      estado: endereco.estado || '',
      pais: endereco.pais || 'Brasil',
      principal: endereco.principal === 'sim'
    }
  } else {
    editandoEndereco.value = false
    enderecoForm.value = {
      id: null,
      cep: '',
      endereco: '',
      numero: '',
      complemento: '',
      bairro: '',
      cidade: '',
      estado: '',
      pais: 'Brasil',
      principal: false
    }
  }
  modalEnderecoAberto.value = true
}

const fecharModalEndereco = () => {
  modalEnderecoAberto.value = false
  editandoEndereco.value = false
}

// Salvar endereço (adicionar ou editar)
const salvarEndereco = async () => {
  const url = enderecoForm.value.id
    ? `/editar_endereco/${enderecoForm.value.id}`
    : '/adicionar_endereco'

  const formData = new FormData()
  Object.keys(enderecoForm.value).forEach(key => {
    let value = enderecoForm.value[key]
    if (key === 'principal') value = value ? 'sim' : 'nao'
    formData.append(key, value)
  })

  try {
    const response = await fetch(url, { method: 'POST', body: formData })
    const data = await response.json()
    if (data.success) {
      await carregarEnderecos()
      fecharModalEndereco()
    } else {
      alert(data.message || 'Erro ao salvar endereço')
    }
  } catch (error) {
    console.error(error)
    alert('Erro ao salvar endereço. Tente novamente.')
  }
}

// Excluir endereço
const excluirEndereco = async (id) => {
  if (!confirm('Tem certeza que deseja excluir este endereço?')) return
  try {
    const response = await fetch(`/excluir_endereco/${id}`, { method: 'POST' })
    const data = await response.json()
    if (data.success) {
      await carregarEnderecos()
      if (enderecoSelecionado.value === id) enderecoSelecionado.value = null
    } else {
      alert(data.message)
    }
  } catch (error) {
    console.error(error)
    alert('Erro ao excluir endereço.')
  }
}

// Definir endereço como principal
const definirComoPrincipal = async (id) => {
  try {
    const response = await fetch(`/definir_endereco_principal/${id}`, { method: 'POST' })
    const data = await response.json()
    if (data.success) {
      await carregarEnderecos()
    } else {
      alert(data.message)
    }
  } catch (error) {
    console.error(error)
    alert('Erro ao definir endereço principal.')
  }
}

// Aplicar cupom
const aplicarCupom = async () => {
  if (!codigoCupom.value.trim()) {
    alert('Digite um código de cupom.')
    return
  }
  aplicandoCupom.value = true
  try {
    const response = await fetch('/api/cupons/validar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ codigo: codigoCupom.value.toUpperCase() })
    })
    const data = await response.json()
    if (data.valido) {
      desconto.value = subtotal.value * (data.desconto / 100)
      cupomId.value = data.id_cupom
      alert(data.mensagem)
    } else {
      alert(data.mensagem)
      desconto.value = 0
      cupomId.value = null
    }
  } catch (error) {
    console.error(error)
    alert('Erro ao validar cupom.')
  } finally {
    aplicandoCupom.value = false
  }
}

// Finalizar compra
const finalizarCompra = async () => {
  if (!enderecoSelecionado.value) {
    alert('Selecione um endereço de entrega.')
    return
  }

  if (metodoPagamento.value === 'cartao') {
    if (!cartao.value.numero || !cartao.value.validade || !cartao.value.cvv || !cartao.value.nome) {
      alert('Preencha todos os dados do cartão.')
      return
    }
  }

  processando.value = true
  try {
    const formData = new FormData()
    // Adicionar itens selecionados (IDs do carrinho)
    itens.value.forEach(item => {
      formData.append('selecionar_item', item.id_carrinho)
    })
    formData.append('endereco_id', enderecoSelecionado.value)
    formData.append('pagamento', metodoPagamento.value)
    if (cupomId.value) {
      formData.append('cupom_aplicado', codigoCupom.value)
      formData.append('desconto_cupom', desconto.value.toString())
    }

    const response = await fetch('/finalizar_compra', { method: 'POST', body: formData })
    if (response.ok) {
      // Limpar localStorage e redirecionar
      localStorage.removeItem('checkoutItems')
      localStorage.removeItem('cupomAplicado')
      alert('Compra finalizada com sucesso! Obrigado.')
      router.push('/')
    } else {
      throw new Error('Erro no servidor')
    }
  } catch (error) {
    console.error(error)
    alert('Erro ao processar pagamento. Tente novamente.')
  } finally {
    processando.value = false
  }
}

// Inicialização
onMounted(async () => {
  // Verificar se usuário está logado (o store já cuida, mas redirecionar se não estiver)
  if (!authStore.logado) {
    router.push('/login?redirect=checkout')
    return
  }
  await carregarItensSelecionados()
  await carregarEnderecos()

  // Recuperar cupom salvo (se houver)
  const cupomSalvo = localStorage.getItem('cupomAplicado')
  if (cupomSalvo) {
    const { codigo, desconto: descSalvo } = JSON.parse(cupomSalvo)
    codigoCupom.value = codigo
    desconto.value = descSalvo
  }
})
</script>

<style scoped>
/* ===== CHECKOUT - ESTILOS ESPECÍFICOS ===== */
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
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: var(--gradiente-botao);
  border-radius: var(--borda-radius-sm);
}

.checkout-content {
  display: flex;
  gap: var(--espacamento-lg);
  align-items: flex-start;
}

.checkout-left {
  flex: 1;
  background: var(--cor-fundo-secundario);
  padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-lg);
  border: 1px solid rgba(255, 215, 0, 0.2);
  box-shadow: var(--sombra-card);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-lg);
}

.checkout-left::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradiente-botao);
}

.checkout-right {
  flex: 0 0 400px;
  background: var(--cor-fundo-secundario);
  padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-lg);
  border: 1px solid rgba(255, 215, 0, 0.2);
  box-shadow: var(--sombra-card);
  height: fit-content;
  position: sticky;
  top: 120px;
}

.checkout-right::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradiente-botao);
}

.section-header h2,
.payment-section h2,
.order-summary h2,
.card-data h3 {
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-md);
  font-family: var(--fonte-secundaria);
  border-left: 3px solid var(--cor-dourado);
  padding-left: var(--espacamento-sm);
}

.enderecos-container {
  display: grid;
  gap: var(--espacamento-md);
  margin-bottom: var(--espacamento-md);
}

.endereco-card {
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-md);
  border: 2px solid transparent;
  transition: all 0.3s ease;
  cursor: pointer;
  position: relative;
}

.endereco-card.principal {
  border-color: var(--cor-dourado);
  background: rgba(255, 215, 0, 0.05);
}

.endereco-card.selected {
  border-color: var(--cor-dourado);
  background: rgba(255, 215, 0, 0.1);
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
}

.endereco-card.selected::before {
  content: '✓';
  position: absolute;
  top: -10px;
  right: -10px;
  background: var(--cor-dourado);
  color: var(--cor-fundo);
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.8rem;
}

.endereco-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--espacamento-sm);
}

.badge-principal {
  background: var(--cor-dourado);
  color: var(--cor-fundo);
  padding: var(--espacamento-xs) 0.75rem;
  border-radius: var(--borda-radius-xl);
  font-size: 0.8rem;
  font-weight: 500;
}

.endereco-info p {
  margin: 0.5rem 0;
  color: var(--cor-texto-secundario);
  font-size: 0.9rem;
}

.endereco-actions {
  margin-top: var(--espacamento-sm);
  display: flex;
  gap: var(--espacamento-sm);
  flex-wrap: wrap;
}

.btn-edit, .btn-delete, .btn-set-primary {
  border: none;
  padding: var(--espacamento-xs) var(--espacamento-sm);
  border-radius: var(--borda-radius-sm);
  cursor: pointer;
  font-size: 0.85rem;
  display: inline-flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s ease;
}

.btn-edit { background: #2196F3; color: white; }
.btn-delete { background: #f44336; color: white; }
.btn-set-primary { background: #4caf50; color: white; }
.btn-edit:hover, .btn-delete:hover, .btn-set-primary:hover { transform: translateY(-2px); filter: brightness(0.9); }

.endereco-selecao {
  margin-top: var(--espacamento-sm);
  display: flex;
  align-items: center;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.empty-address {
  text-align: center;
  padding: var(--espacamento-xl);
  border: 2px dashed rgba(255, 215, 0, 0.3);
  border-radius: var(--borda-radius-lg);
}
.empty-address i { font-size: 3rem; color: var(--cor-dourado); margin-bottom: 1rem; }
.empty-address h3 { color: var(--cor-texto); margin-bottom: 0.5rem; }
.empty-address p { margin-bottom: 1.5rem; }

.btn-primary, .btn-secondary {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--borda-radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
.btn-primary { background: var(--gradiente-botao-dourado-claro-escuro); color: var(--cor-fundo); }
.btn-secondary { background: var(--cor-fundo); color: var(--cor-texto); border: 1px solid var(--cor-dourado); }
.btn-primary:hover, .btn-secondary:hover { transform: translateY(-2px); box-shadow: var(--sombra-destaque); }

.payment-options {
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-sm);
}
.payment-option input[type="radio"] { display: none; }
.payment-option label {
  display: flex;
  align-items: center;
  gap: var(--espacamento-sm);
  padding: var(--espacamento-md);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--borda-radius-md);
  cursor: pointer;
  transition: all 0.3s ease;
  background: var(--cor-fundo);
}
.payment-option input[type="radio"]:checked + label {
  border-color: var(--cor-dourado);
  background: rgba(255, 215, 0, 0.05);
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.2);
}
.payment-option label i { font-size: 1.5rem; color: var(--cor-dourado); }
.payment-option label strong { color: var(--cor-texto); }
.payment-info { font-size: 0.8rem; color: var(--cor-texto-secundario); }

.card-data {
  animation: slideDown 0.3s ease-out;
}
.form-group { margin-bottom: var(--espacamento-md); }
.form-group label { display: block; color: var(--cor-texto); margin-bottom: 0.25rem; font-weight: 500; }
.form-group input, .form-group select {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--borda-radius-md);
  background: var(--cor-fundo);
  color: var(--cor-texto);
}
.form-group input:focus, .form-group select:focus {
  outline: none;
  border-color: var(--cor-dourado);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: var(--espacamento-md); }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--espacamento-sm); }
.checkbox-group { display: flex; align-items: center; gap: 0.5rem; }
.checkbox-group input { width: auto; }

.order-items { max-height: 400px; overflow-y: auto; margin-bottom: 1rem; }
.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}
.item-info h4 { margin-bottom: 0.25rem; }
.item-info .price { color: var(--cor-dourado); font-weight: 600; font-size: 0.9rem; }
.item-quantity { background: rgba(255, 215, 0, 0.1); padding: 0.25rem 0.5rem; border-radius: var(--borda-radius-sm); }
.item-total { color: var(--cor-dourado); font-weight: bold; }

.coupon-section {
  display: flex;
  gap: 0.5rem;
  margin: 1.5rem 0;
  background: var(--cor-fundo);
  padding: 0.5rem;
  border-radius: var(--borda-radius-md);
  border: 1px solid rgba(255, 215, 0, 0.2);
}
.coupon-section input { flex: 1; padding: 0.75rem; background: var(--cor-fundo-secundario); border: 1px solid rgba(255,215,0,0.2); border-radius: var(--borda-radius-md); color: var(--cor-texto); }
.btn-coupon { padding: 0.75rem 1.5rem; background: var(--gradiente-botao); color: var(--cor-fundo); border: none; border-radius: var(--borda-radius-md); cursor: pointer; font-weight: bold; transition: all 0.3s; }
.btn-coupon:hover { transform: translateY(-2px); box-shadow: var(--sombra-destaque); }
.btn-coupon:disabled { opacity: 0.6; cursor: not-allowed; }

.order-totals .total-line {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}
.total-line.discount { color: #00ff88; background: rgba(0,255,136,0.1); padding: 0.5rem; border-radius: 8px; margin: 0.5rem 0; }
.total-line.final { border-top: 1px solid rgba(255,215,0,0.2); padding-top: 1rem; margin-top: 0.5rem; font-size: 1.2rem; color: var(--cor-dourado); }

.btn-confirm-payment {
  width: 100%;
  padding: 1rem;
  background: var(--gradiente-botao);
  color: var(--cor-fundo);
  border: none;
  border-radius: var(--borda-radius-lg);
  font-weight: bold;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s;
  margin-top: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
.btn-confirm-payment:hover:not(:disabled) { transform: translateY(-3px); box-shadow: var(--sombra-destaque); }
.btn-confirm-payment:disabled { background: #666; cursor: not-allowed; transform: none; }

.security-note { text-align: center; color: var(--cor-texto-secundario); font-size: 0.8rem; margin-top: 1rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem; }
.security-note i { color: var(--cor-dourado); }

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.modal-content {
  background: var(--cor-fundo-secundario);
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: var(--borda-radius-lg);
  border: 1px solid var(--cor-dourado);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255,215,0,0.2);
}
.modal-close { background: none; border: none; color: var(--cor-texto); font-size: 1.5rem; cursor: pointer; transition: all 0.3s; }
.modal-close:hover { color: var(--cor-dourado); transform: rotate(90deg); }
.endereco-form { padding: 1.5rem; }
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255,215,0,0.2);
}

@keyframes slideDown {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 1024px) {
  .checkout-content { flex-direction: column; }
  .checkout-right { flex: 1; width: 100%; position: static; }
}
@media (max-width: 768px) {
  .checkout-left, .checkout-right { padding: 1rem; }
  .form-row, .form-grid { grid-template-columns: 1fr; }
  .endereco-actions { flex-direction: column; }
  .coupon-section { flex-direction: column; }
}
</style>