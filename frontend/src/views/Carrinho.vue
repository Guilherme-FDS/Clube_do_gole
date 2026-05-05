<template>
  <div class="carrinho">
    <section class="cart-container">
      <h2 class="titulo-lg">🛒 Meu Carrinho</h2>

      <!-- Alerta para usuários não logados -->
      <div v-if="!logado" class="guest-alert">
        <i class="fas fa-info-circle"></i>
        <div class="guest-message">
          <strong>Você não está logado</strong>
          <p>Adicione itens ao carrinho agora e faça login na hora de finalizar a compra. Seus itens serão mantidos!</p>
          <router-link to="/login?redirect=carrinho" class="btn-login-guest">
            <i class="fas fa-sign-in-alt"></i> Fazer Login
          </router-link>
        </div>
      </div>

      <!-- Mensagens de feedback -->
      <div class="flash-messages" v-if="mensagem">
        <div :class="['flash-' + mensagem.tipo]">{{ mensagem.texto }}</div>
      </div>

      <div v-if="itensCarrinho.length">
        <div class="tabela-wrapper">
          <table class="tabela-carrinho">
            <thead>
              <tr>
                <th>Produto</th>
                <th>Plano</th>
                <th>Quantidade</th>
                <th>Valor Unitário</th>
                <th>Total</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in itensCarrinho" :key="item.id_carrinho" class="cart-item">
                <td class="produto-info">
                  <div class="produto-detalhes">
                    <strong class="produto-nome">{{ item.nome_produto }}</strong>
                    <small v-if="item.descricao" class="produto-descricao">{{ item.descricao }}</small>
                  </div>
                </td>
                <td>
                  <span :class="['plano-badge', item.plano.toLowerCase()]">{{ item.plano }}</span>
                </td>
                <td class="quantidade-cell">
                  <div class="controle-quantidade">
                    <button type="button" @click="diminuirQuantidade(item.id_carrinho)" class="btn-quantidade btn-diminuir">
                      <i class="fas fa-minus"></i>
                    </button>
                    <input type="number" :id="`quantidade-${item.id_carrinho}`"
                      v-model.number="quantidades[item.id_carrinho]"
                      @change="atualizarQuantidadeManual(item.id_carrinho, quantidades[item.id_carrinho])"
                      min="1" class="quantidade-display quantidade-input" />
                    <button type="button" @click="aumentarQuantidade(item.id_carrinho)" class="btn-quantidade btn-aumentar">
                      <i class="fas fa-plus"></i>
                    </button>
                  </div>
                </td>
                <td class="valor-unitario">{{ formatarMoeda(item.valor_unitario) }}</td>
                <td class="item-total" :id="`total-${item.id_carrinho}`">{{ formatarMoeda(item.valor_total) }}</td>
                <td class="acoes-cell">
                  <div class="acoes-container">
                    <input type="checkbox" :value="item.id_carrinho" v-model="selecionados" class="checkbox-item" />
                    <button type="button" @click="excluirItem(item.id_carrinho)" class="btn-excluir-item" title="Excluir item">
                      <i class="fas fa-trash"></i>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="resumo-carrinho">
          <div class="total-carrinho">
            <span class="total-label">💰 Total do Carrinho:</span>
            <span class="total-valor">{{ formatarMoeda(totalGeral) }}</span>
          </div>

          <div class="acoes-carrinho">
            <router-link to="/#planos" class="btn-modern btn-continuar">
              <i class="fas fa-shopping-bag"></i> Continuar Comprando
            </router-link>
            <button type="button" @click="abrirCheckout" class="btn-modern btn-finalizar">
              <i class="fas fa-check-circle"></i> Finalizar Compra dos Selecionados
            </button>
          </div>
        </div>
      </div>

      <div v-else class="carrinho-vazio">
        <div class="carrinho-vazio-icon">
          <i class="fas fa-shopping-cart"></i>
        </div>
        <h3>Seu carrinho está vazio</h3>
        <p>Explore nossos produtos e adicione itens incríveis ao seu carrinho!</p>
        <router-link to="/#planos" class="btn-modern btn-continuar">
          <i class="fas fa-shopping-bag"></i> Continuar Comprando
        </router-link>
      </div>
    </section>
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

// Estado local
const selecionados = ref([])          // IDs dos itens selecionados para checkout
const quantidades = ref({})            // objeto para controle reativo das quantidades
const mensagem = ref(null)             // feedback (sucesso/erro)

// Computed
const logado = computed(() => authStore.logado)
const itensCarrinho = computed(() => carrinhoStore.itens)
const totalGeral = computed(() => carrinhoStore.total)

// Formatação de moeda
const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor || 0)
}

// Sincronizar quantidades reativas com os itens do carrinho
const sincronizarQuantidades = () => {
  const novoObj = {}
  itensCarrinho.value.forEach(item => {
    novoObj[item.id_carrinho] = item.quantidade
  })
  quantidades.value = novoObj
}

// Exibir mensagem temporária
const mostrarMensagem = (texto, tipo = 'success') => {
  mensagem.value = { texto, tipo }
  setTimeout(() => {
    mensagem.value = null
  }, 5000)
}

// Ações da API
const aumentarQuantidade = async (itemId) => {
  const novaQtd = quantidades.value[itemId] + 1
  await atualizarQuantidadeNoServidor(itemId, novaQtd)
}

const diminuirQuantidade = async (itemId) => {
  const novaQtd = quantidades.value[itemId] - 1
  if (novaQtd < 1) {
    mostrarMensagem('A quantidade deve ser pelo menos 1.', 'error')
    return
  }
  await atualizarQuantidadeNoServidor(itemId, novaQtd)
}

const atualizarQuantidadeManual = async (itemId, novaQtd) => {
  if (novaQtd < 1) {
    mostrarMensagem('A quantidade deve ser pelo menos 1.', 'error')
    // restaurar valor antigo
    const itemOriginal = itensCarrinho.value.find(i => i.id_carrinho == itemId)
    if (itemOriginal) quantidades.value[itemId] = itemOriginal.quantidade
    return
  }
  await atualizarQuantidadeNoServidor(itemId, novaQtd)
}

const atualizarQuantidadeNoServidor = async (itemId, novaQtd) => {
  try {
    await carrinhoStore.atualizarQuantidade(itemId, novaQtd)
    sincronizarQuantidades()          // atualiza o objeto local
    mostrarMensagem('Quantidade atualizada!', 'success')
  } catch (error) {
    console.error(error)
    mostrarMensagem('Erro ao atualizar quantidade.', 'error')
    // rollback visual
    const itemOriginal = itensCarrinho.value.find(i => i.id_carrinho == itemId)
    if (itemOriginal) quantidades.value[itemId] = itemOriginal.quantidade
  }
}

const excluirItem = async (itemId) => {
  if (!confirm('Tem certeza que deseja remover este item?')) return
  try {
    await carrinhoStore.remove(itemId)
    sincronizarQuantidades()
    mostrarMensagem('Item removido com sucesso!', 'success')
    // Se carrinho ficou vazio, recarregamos a lista (já está reativa)
  } catch (error) {
    console.error(error)
    mostrarMensagem('Erro ao remover item.', 'error')
  }
}

const abrirCheckout = async () => {
  if (selecionados.value.length === 0) {
    mostrarMensagem('Selecione pelo menos um item para finalizar a compra.', 'error')
    return
  }

  // Guarda os IDs selecionados no localStorage para uso na página de checkout
  localStorage.setItem('checkoutItems', JSON.stringify(selecionados.value))

  if (!logado.value) {
    mostrarMensagem('Faça login para finalizar a compra! Use o botão "Fazer Login" acima.', 'info')
    window.scrollTo({ top: 0, behavior: 'smooth' })
    return
  }

  // Usuário logado → redireciona para checkout
  router.push('/checkout')
}

// Carregar dados do carrinho ao montar
onMounted(async () => {
  await carrinhoStore.buscar()
  sincronizarQuantidades()
  // Se houver guest_id, não é necessário fazer nada extra, o store já gerencia
})
</script>

<style scoped>
/* ===== ESTILOS EXCLUSIVOS DO CARRINHO ===== */
/* (Os estilos globais já cobrem header, footer, botões principais, etc.) */

.guest-alert {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.guest-alert i {
  font-size: 24px;
  flex-shrink: 0;
}

.guest-message {
  flex: 1;
}

.guest-message strong {
  display: block;
  margin-bottom: 5px;
  font-size: 16px;
}

.guest-message p {
  margin: 0;
  opacity: 0.9;
  font-size: 14px;
}

.btn-login-guest {
  background: rgba(255,255,255,0.2);
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255,255,255,0.3);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-login-guest:hover {
  background: rgba(255,255,255,0.3);
  transform: translateY(-2px);
}

/* Tabela e itens */
.tabela-wrapper {
  overflow-x: auto;
  border-radius: var(--borda-radius-md);
  margin: var(--espacamento-md) 0;
}

.tabela-carrinho {
  width: 100%;
  border-collapse: collapse;
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-md);
  overflow: hidden;
  box-shadow: var(--sombra-suave);
}

.tabela-carrinho th {
  background: var(--gradiente-botao-dourado-claro-escuro);
  color: var(--cor-fundo);
  padding: var(--espacamento-sm);
  text-align: left;
  font-weight: 600;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tabela-carrinho td {
  padding: var(--espacamento-sm);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  color: var(--cor-texto);
  vertical-align: middle;
}

.produto-detalhes {
  flex: 1;
}

.produto-nome {
  color: var(--cor-texto);
  font-weight: 600;
  display: block;
  margin-bottom: var(--espacamento-xs);
}

.produto-descricao {
  color: var(--cor-texto-secundario);
  font-size: 0.875rem;
  line-height: 1.4;
}

.plano-badge {
  text-transform: capitalize;
  background: var(--gradiente-dourado);
  color: var(--cor-fundo);
  padding: 0.5rem 1rem;
  border-radius: var(--borda-radius-lg);
  font-size: 0.8rem;
  font-weight: 600;
  display: inline-block;
}

.plano-badge.mensal {
  background: var(--gradiente-dourado);
}

.plano-badge.semestral {
  background: linear-gradient(45deg, var(--cor-roxo-principal), var(--cor-roxo-claro));
}

.plano-badge.anual {
  background: linear-gradient(45deg, var(--cor-roxo-escuro), var(--cor-roxo-principal));
}

.quantidade-cell {
  text-align: center;
}

.controle-quantidade {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: rgba(255, 215, 0, 0.1);
  border-radius: var(--borda-radius-md);
  padding: 4px;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.btn-quantidade {
  background: var(--gradiente-botao-dourado-claro-escuro);
  color: var(--cor-fundo);
  border: none;
  border-radius: var(--borda-radius-sm);
  width: 32px;
  height: 32px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  font-weight: bold;
}

.btn-quantidade:hover {
  transform: scale(1.1);
  box-shadow: var(--sombra-suave);
}

.quantidade-display.quantidade-input {
  width: 60px;
  padding: 8px;
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: var(--borda-radius-sm);
  background: var(--cor-fundo-secundario);
  color: var(--cor-dourado);
  text-align: center;
  font-size: 1.1rem;
  font-weight: bold;
  -moz-appearance: textfield;
  appearance: textfield;
}

.quantidade-display.quantidade-input:focus {
  outline: none;
  border-color: var(--cor-dourado);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

.acoes-cell {
  text-align: center;
  width: 120px;
}

.acoes-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.btn-excluir-item {
  background: linear-gradient(45deg, #ff4444, #cc0000);
  color: white;
  border: none;
  border-radius: var(--borda-radius-sm);
  padding: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  flex-shrink: 0;
}

.btn-excluir-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 68, 68, 0.4);
}

.checkbox-item {
  transform: scale(1.3);
  cursor: pointer;
  accent-color: var(--cor-dourado);
}

.resumo-carrinho {
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  margin-top: var(--espacamento-lg);
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.total-carrinho {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: var(--espacamento-md);
  padding: var(--espacamento-sm);
  background: rgba(255, 215, 0, 0.1);
  border-radius: var(--borda-radius-md);
}

.total-label {
  color: var(--cor-texto);
}

.total-valor {
  color: var(--cor-dourado);
  font-size: 1.75rem;
}

.acoes-carrinho {
  display: flex;
  gap: var(--espacamento-sm);
  flex-wrap: wrap;
  justify-content: space-between;
}

.btn-continuar {
  order: 1;
  background: var(--gradiente-botao-dourado-claro-escuro);
}

.btn-finalizar {
  order: 2;
  background: linear-gradient(45deg, var(--cor-roxo-escuro), var(--cor-roxo-principal));
}

.carrinho-vazio {
  text-align: center;
  padding: var(--espacamento-xl);
  color: var(--cor-texto-secundario);
}

.carrinho-vazio-icon {
  font-size: 4rem;
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-md);
}

.flash-messages {
  margin: var(--espacamento-md) 0;
}

.flash-success {
  background: linear-gradient(135deg, #00ff88, #00cc66);
  color: var(--cor-fundo);
  padding: var(--espacamento-sm);
  border-radius: var(--borda-radius-md);
  text-align: center;
  font-weight: 500;
  margin-bottom: var(--espacamento-sm);
}

.flash-error {
  background: linear-gradient(135deg, #ff4444, #cc0000);
  color: white;
  padding: var(--espacamento-sm);
  border-radius: var(--borda-radius-md);
  text-align: center;
  font-weight: 500;
  margin-bottom: var(--espacamento-sm);
}

.flash-info {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: var(--espacamento-sm);
  border-radius: var(--borda-radius-md);
  text-align: center;
  font-weight: 500;
  margin-bottom: var(--espacamento-sm);
}

/* Responsividade */
@media (max-width: 768px) {
  .guest-alert {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  .acoes-container {
    flex-direction: column;
    gap: 8px;
  }
  .btn-continuar,
  .btn-finalizar {
    order: initial;
    width: 100%;
  }
  .total-carrinho {
    flex-direction: column;
    gap: var(--espacamento-xs);
    text-align: center;
  }
}

@media (max-width: 480px) {
  .quantidade-cell .controle-quantidade {
    flex-wrap: wrap;
  }
  .btn-quantidade {
    width: 28px;
    height: 28px;
  }
  .quantidade-display.quantidade-input {
    width: 50px;
    font-size: 0.9rem;
  }
  .acoes-cell {
    width: 80px;
  }
}
</style>