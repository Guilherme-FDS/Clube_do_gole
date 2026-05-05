<template>
  <div class="produto-container">
    <!-- Produto Principal -->
    <div class="produto-hero">
      <!-- COLUNA DA IMAGEM -->
      <div class="produto-imagem">
        <img :src="produto.imagem || '/img/sem_imagem.png'" :alt="produto.nome" class="imagem-principal-premium">
        <div v-if="produto.estoque <= 0" class="badge-esgotado">Esgotado</div>
        <div v-else-if="produto.estoque <= 5" class="badge-estoque">Últimas unidades!</div>
      </div>

      <!-- COLUNA DAS INFORMAÇÕES -->
      <div class="produto-info">
        <h1 class="titulo-produto">{{ produto.nome }}</h1>
        <p class="descricao-produto">{{ produto.descricao }}</p>

        <div class="produto-info-linha">
          <!-- Estoque -->
          <div class="info-estoque">
            <i class="fas fa-box"></i>
            <span>{{ produto.estoque }} unidades disponíveis</span>
          </div>

          <!-- Preço Base -->
          <div class="preco-base">
            <span class="preco-original">{{ formatarMoeda(produto.preco) }}</span>
            <span class="periodo">/mês</span>
          </div>

          <!-- Quantidade -->
          <div class="quantidade-group">
            <label class="quantidade-label">Quantidade:</label>
            <div class="quantidade-controles">
              <button type="button" class="btn-quantidade" @click="alterarQuantidade(-1)" :disabled="produto.estoque <= 0">
                <i class="fas fa-minus"></i>
              </button>
              <input type="number" v-model.number="quantidade" min="1" :max="produto.estoque" class="quantidade-input">
              <button type="button" class="btn-quantidade" @click="alterarQuantidade(1)" :disabled="quantidade >= produto.estoque || produto.estoque <= 0">
                <i class="fas fa-plus"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- SEÇÃO DE PLANOS -->
    <div class="planos-section">
      <h2 class="titulo-planos">Escolha seu plano</h2>
      <p class="subtitulo-planos">Economize mais com planos de longo prazo</p>

      <div class="planos-grid">
        <!-- Plano Mensal -->
        <div class="plano-card" :class="{ selecionado: planoSelecionado === 'mensal' }" data-plano="mensal">
          <div class="plano-header">
            <h3>Mensal</h3>
            <span class="plano-badge popular">Mais Popular</span>
          </div>
          <div class="plano-preco">
            <span class="valor">{{ formatarMoeda(produto.preco) }}</span>
            <span class="periodo">/mês</span>
          </div>
          <ul class="plano-beneficios">
            <li><i class="fas fa-check"></i> Flexibilidade total</li>
            <li><i class="fas fa-check"></i> Renovação mensal</li>
            <li><i class="fas fa-check"></i> Sem compromisso</li>
          </ul>
          <button type="button" class="btn-plano" @click="selecionarPlano('mensal')" :disabled="produto.estoque <= 0">
            <i class="fas fa-shopping-cart"></i> Assinar Mensal
          </button>
        </div>

        <!-- Plano Semestral (5% desconto) -->
        <div class="plano-card" :class="{ selecionado: planoSelecionado === 'semestral' }" data-plano="semestral">
          <div class="plano-header">
            <h3>Semestral</h3>
            <span class="plano-badge economize">Economize 5%</span>
          </div>
          <div class="plano-preco">
            <span class="valor">{{ formatarMoeda(precoComDesconto(produto.preco, 6, 0.05)) }}</span>
            <span class="periodo">/semestre</span>
          </div>
          <div class="economia-info">
            <span class="economia-valor">Economize {{ formatarMoeda(produto.preco * 6 * 0.05) }}</span>
          </div>
          <ul class="plano-beneficios">
            <li><i class="fas fa-check"></i> 5% de desconto</li>
            <li><i class="fas fa-check"></i> 6 meses de acesso</li>
            <li><i class="fas fa-check"></i> Melhor custo-benefício</li>
          </ul>
          <button type="button" class="btn-plano" @click="selecionarPlano('semestral')" :disabled="produto.estoque <= 0">
            <i class="fas fa-shopping-cart"></i> Assinar Semestral
          </button>
        </div>

        <!-- Plano Anual (10% desconto) -->
        <div class="plano-card" :class="{ selecionado: planoSelecionado === 'anual' }" data-plano="anual">
          <div class="plano-header">
            <h3>Anual</h3>
            <span class="plano-badge melhor">Melhor Oferta</span>
          </div>
          <div class="plano-preco">
            <span class="valor">{{ formatarMoeda(precoComDesconto(produto.preco, 12, 0.10)) }}</span>
            <span class="periodo">/ano</span>
          </div>
          <div class="economia-info">
            <span class="economia-valor">Economize {{ formatarMoeda(produto.preco * 12 * 0.10) }}</span>
          </div>
          <ul class="plano-beneficios">
            <li><i class="fas fa-check"></i> 10% de desconto</li>
            <li><i class="fas fa-check"></i> 12 meses de acesso</li>
            <li><i class="fas fa-check"></i> Maior economia</li>
          </ul>
          <button type="button" class="btn-plano" @click="selecionarPlano('anual')" :disabled="produto.estoque <= 0">
            <i class="fas fa-shopping-cart"></i> Assinar Anual
          </button>
        </div>
      </div>
    </div>

    <!-- Seção de Benefícios -->
    <section class="beneficios-section">
      <div class="container">
        <h2 class="titulo-lg">Por que escolher o Clube do Gole?</h2>
        <div class="beneficios-grid">
          <div class="beneficio-card">
            <div class="beneficio-icone"><i class="fas fa-shipping-fast"></i></div>
            <h3>Entrega Rápida</h3>
            <p>Receba seus produtos em todo o Brasil com agilidade e segurança</p>
          </div>
          <div class="beneficio-card">
            <div class="beneficio-icone"><i class="fas fa-lock"></i></div>
            <h3>Compra Segura</h3>
            <p>Seus dados protegidos com criptografia de última geração</p>
          </div>
          <div class="beneficio-card">
            <div class="beneficio-icone"><i class="fas fa-headset"></i></div>
            <h3>Suporte Premium</h3>
            <p>Atendimento especializado para tirar todas suas dúvidas</p>
          </div>
          <div class="beneficio-card">
            <div class="beneficio-icone"><i class="fas fa-undo"></i></div>
            <h3>Garantia Total</h3>
            <p>Satisfação garantida ou seu dinheiro de volta em 7 dias</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Toast Container -->
    <div id="toast-container"></div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCarrinhoStore } from '@/stores/carrinho'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const carrinhoStore = useCarrinhoStore()

// Dados do produto
const produto = reactive({
  id: null,
  nome: '',
  descricao: '',
  preco: 0,
  estoque: 0,
  imagem: ''
})

const quantidade = ref(1)
const planoSelecionado = ref('mensal')
const carregando = ref(false)

// Formatação
const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor || 0)
}

// Calcular preço com desconto para plano (total)
const precoComDesconto = (precoUnitario, meses, descontoPercentual) => {
  const totalSemDesconto = precoUnitario * meses
  const totalComDesconto = totalSemDesconto * (1 - descontoPercentual)
  return totalComDesconto
}

// Carregar produto da API
const carregarProduto = async () => {
  const id = route.params.id
  if (!id) {
    router.push('/')
    return
  }
  carregando.value = true
  try {
    const response = await fetch(`/api/produtos/${id}`)
    if (!response.ok) throw new Error('Produto não encontrado')
    const data = await response.json()
    Object.assign(produto, data)
  } catch (error) {
    console.error(error)
    mostrarToast('Produto não encontrado', 'error')
    router.push('/')
  } finally {
    carregando.value = false
  }
}

// Alterar quantidade (com validação)
const alterarQuantidade = (delta) => {
  let nova = quantidade.value + delta
  if (nova < 1) nova = 1
  if (nova > produto.estoque) nova = produto.estoque
  quantidade.value = nova
}

// Selecionar plano e adicionar ao carrinho
const selecionarPlano = async (plano) => {
  planoSelecionado.value = plano
  await adicionarAoCarrinho()
}

// Adicionar ao carrinho via store
const adicionarAoCarrinho = async () => {
  if (produto.estoque <= 0) {
    mostrarToast('Produto esgotado', 'error')
    return
  }

  // Preparar dados no formato esperado pelo store
  const dadosProduto = {
    produto_id: produto.id,
    plano: planoSelecionado.value,
    quantidade: quantidade.value
  }

  try {
    // Usa o método add do store carrinho
    await carrinhoStore.add(produto.id, planoSelecionado.value, quantidade.value)
    mostrarToast('Produto adicionado ao carrinho!', 'success')
  } catch (error) {
    console.error('Erro ao adicionar:', error)
    mostrarToast('Erro ao adicionar ao carrinho', 'error')
  }
}

// Toast personalizado
const mostrarToast = (mensagem, tipo = 'success') => {
  const container = document.getElementById('toast-container')
  if (!container) return

  const toast = document.createElement('div')
  toast.className = `toast-message toast-${tipo}`
  toast.innerHTML = `
    <div class="toast-content">
      <i class="fas ${tipo === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
      <span>${mensagem}</span>
      <button class="toast-close" onclick="this.parentElement.parentElement.remove()">
        <i class="fas fa-times"></i>
      </button>
    </div>
  `
  container.appendChild(toast)
  setTimeout(() => toast.classList.add('show'), 10)
  setTimeout(() => {
    toast.classList.remove('show')
    setTimeout(() => toast.remove(), 300)
  }, 5000)
}

// Carregar dados ao montar
onMounted(() => {
  carregarProduto()
})
</script>

<style scoped>
/* ===== ESTILOS ESPECÍFICOS DO PRODUTO DETALHE ===== */
/* (Os estilos globais já trazem header, footer, variáveis, tipografia, etc.) */

.produto-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: calc(var(--espacamento-xl) + var(--espacamento-md)) var(--espacamento-md) var(--espacamento-xl);
}

.produto-hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--espacamento-lg);
  align-items: start;
  margin-bottom: var(--espacamento-xl);
}

.produto-imagem {
  position: relative;
  border-radius: var(--borda-radius-lg);
  overflow: hidden;
  box-shadow: var(--sombra-destaque);
}

.imagem-principal-premium {
  width: 100%;
  height: auto;
  object-fit: contain;
  display: block;
  transition: transform 0.3s ease;
}

.produto-imagem:hover .imagem-principal-premium {
  transform: scale(1.05);
}

.badge-esgotado, .badge-estoque {
  position: absolute;
  top: var(--espacamento-sm);
  right: var(--espacamento-sm);
  padding: var(--espacamento-xs) var(--espacamento-sm);
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  font-size: 0.875rem;
  z-index: 2;
}
.badge-esgotado {
  background: linear-gradient(45deg, #ff4444, #cc0000);
  color: var(--cor-texto);
}
.badge-estoque {
  background: var(--gradiente-dourado);
  color: var(--cor-fundo);
}

.produto-info {
  padding: var(--espacamento-md);
}
.titulo-produto {
  font-family: var(--fonte-secundaria);
  font-size: clamp(2rem, 4vw, 3rem);
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-sm);
}
.descricao-produto {
  font-size: 1.125rem;
  color: var(--cor-texto-secundario);
  margin-bottom: var(--espacamento-md);
}
.info-estoque {
  display: flex;
  align-items: center;
  gap: var(--espacamento-xs);
  margin-bottom: var(--espacamento-md);
  padding: var(--espacamento-sm);
  background: rgba(255, 215, 0, 0.1);
  border-radius: var(--borda-radius-md);
  border: 1px solid rgba(255, 215, 0, 0.2);
}
.preco-base {
  margin-bottom: var(--espacamento-lg);
  padding: var(--espacamento-md);
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-md);
  border: 1px solid rgba(255, 215, 0, 0.2);
}
.preco-original {
  font-family: var(--fonte-secundaria);
  font-size: 2rem;
  color: var(--cor-dourado);
  font-weight: 600;
}
.quantidade-group {
  margin-bottom: var(--espacamento-lg);
}
.quantidade-label {
  display: block;
  margin-bottom: var(--espacamento-sm);
  font-weight: 600;
  font-size: 1.125rem;
}
.quantidade-controles {
  display: flex;
  align-items: center;
  gap: var(--espacamento-sm);
  max-width: 200px;
}
.btn-quantidade {
  background: var(--gradiente-botao);
  color: var(--cor-fundo);
  border: none;
  border-radius: var(--borda-radius-sm);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}
.btn-quantidade:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--sombra-suave);
}
.btn-quantidade:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.quantidade-input {
  width: 80px;
  padding: var(--espacamento-sm);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: var(--borda-radius-sm);
  background: var(--cor-fundo-secundario);
  color: var(--cor-texto);
  text-align: center;
  font-size: 1.125rem;
  font-weight: 600;
  -moz-appearance: textfield;
  appearance: textfield;
}
.quantidade-input:focus {
  outline: none;
  border-color: var(--cor-dourado);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

/* Planos */
.planos-section {
  margin-top: var(--espacamento-lg);
}
.titulo-planos {
  font-family: var(--fonte-secundaria);
  font-size: clamp(1.5rem, 3vw, 2rem);
  color: var(--cor-dourado);
  text-align: center;
  margin-bottom: var(--espacamento-xs);
}
.subtitulo-planos {
  text-align: center;
  margin-bottom: var(--espacamento-lg);
}
.planos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--espacamento-md);
  margin-top: var(--espacamento-md);
}
.plano-card {
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-lg);
  border: 1px solid rgba(255, 215, 0, 0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}
.plano-card::before {
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
.plano-card:hover::before,
.plano-card.selecionado::before {
  transform: scaleX(1);
}
.plano-card:hover,
.plano-card.selecionado {
  transform: translateY(-5px);
  box-shadow: var(--sombra-destaque);
  border-color: var(--cor-dourado);
}
.plano-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--espacamento-md);
}
.plano-header h3 {
  font-family: var(--fonte-secundaria);
  font-size: 1.5rem;
}
.plano-badge {
  padding: 0.25rem 0.75rem;
  border-radius: var(--borda-radius-lg);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}
.plano-badge.popular { background: var(--gradiente-dourado); color: var(--cor-fundo); }
.plano-badge.economize { background: linear-gradient(45deg, var(--cor-roxo-principal), var(--cor-roxo-claro)); color: var(--cor-texto); }
.plano-badge.melhor { background: linear-gradient(45deg, var(--cor-roxo-escuro), var(--cor-roxo-principal)); color: var(--cor-texto); }
.plano-preco {
  text-align: center;
  margin-bottom: var(--espacamento-sm);
}
.plano-preco .valor {
  font-family: var(--fonte-secundaria);
  font-size: 2rem;
  color: var(--cor-dourado);
  font-weight: 600;
}
.economia-info {
  text-align: center;
  margin-bottom: var(--espacamento-md);
}
.economia-valor {
  background: rgba(0, 255, 136, 0.1);
  color: #00ff88;
  padding: 0.5rem 1rem;
  border-radius: var(--borda-radius-lg);
  font-size: 0.875rem;
  font-weight: 600;
}
.plano-beneficios {
  list-style: none;
  margin-bottom: var(--espacamento-lg);
}
.plano-beneficios li {
  display: flex;
  align-items: center;
  gap: var(--espacamento-xs);
  margin-bottom: var(--espacamento-xs);
  color: var(--cor-texto-secundario);
}
.plano-beneficios i {
  color: var(--cor-dourado);
}
.btn-plano {
  width: 100%;
  background: var(--gradiente-botao);
  color: var(--cor-fundo);
  border: none;
  padding: 1rem 2rem;
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 1.1rem;
}
.btn-plano:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: var(--sombra-destaque);
}
.btn-plano:disabled {
  background: #666;
  cursor: not-allowed;
  opacity: 0.6;
}

/* Benefícios */
.beneficios-section {
  background: var(--cor-fundo-secundario);
  padding: var(--espacamento-xl) 0;
  border-top: 2px solid var(--cor-dourado);
  border-bottom: 2px solid var(--cor-dourado);
  margin-top: var(--espacamento-xl);
}
.beneficios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--espacamento-md);
}
.beneficio-card {
  background: var(--cor-fundo);
  padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-md);
  text-align: center;
  border: 1px solid rgba(255, 215, 0, 0.2);
  transition: all 0.3s ease;
}
.beneficio-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--sombra-destaque);
  border-color: var(--cor-dourado);
}
.beneficio-icone {
  width: 80px;
  height: 80px;
  background: var(--gradiente-botao);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto var(--espacamento-md);
  font-size: 2rem;
  color: var(--cor-fundo);
}
.beneficio-card h3 {
  color: var(--cor-texto);
  margin-bottom: var(--espacamento-sm);
}
.beneficio-card p {
  color: var(--cor-texto-secundario);
}

/* Toast container e mensagens */
#toast-container {
  position: fixed;
  top: 100px;
  right: var(--espacamento-md);
  z-index: 10000;
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-xs);
}
.toast-message {
  opacity: 0;
  transform: translateX(100%);
  padding: var(--espacamento-sm) var(--espacamento-md);
  border-radius: var(--borda-radius-md);
  background: var(--cor-fundo-secundario);
  color: var(--cor-texto);
  font-weight: 600;
  box-shadow: var(--sombra-destaque);
  transition: all 0.3s ease;
  min-width: 300px;
  backdrop-filter: blur(10px);
}
.toast-message.show {
  opacity: 1;
  transform: translateX(0);
}
.toast-message.toast-success {
  background: linear-gradient(135deg, #00ff88, #00cc66);
  color: var(--cor-fundo);
}
.toast-message.toast-error {
  background: linear-gradient(135deg, #ff4444, #cc0000);
  color: var(--cor-texto);
}
.toast-content {
  display: flex;
  align-items: center;
  gap: var(--espacamento-sm);
}
.toast-content span {
  flex: 1;
}
.toast-close {
  background: none;
  border: none;
  color: inherit;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s;
}
.toast-close:hover {
  opacity: 1;
}

/* Responsividade */
@media (max-width: 1024px) {
  .produto-hero {
    grid-template-columns: 1fr;
  }
}
@media (max-width: 768px) {
  .planos-grid, .beneficios-grid {
    grid-template-columns: 1fr;
  }
  .quantidade-controles {
    max-width: 100%;
  }
}
@media (max-width: 480px) {
  .produto-container {
    padding: calc(var(--espacamento-xl) + var(--espacamento-xs)) var(--espacamento-xs) var(--espacamento-lg);
  }
  .toast-message {
    min-width: 250px;
  }
}
</style>