<template>
  <div class="container meus-pedidos">
    <h1 class="titulo-lg">Meus Pedidos</h1>

    <div v-if="carregando" class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i> Carregando pedidos...
    </div>

    <div v-else-if="pedidos.length" class="pedidos-lista">
      <div v-for="pedido in pedidos" :key="pedido.id_compra" class="pedido-card fade-in" :class="{ visible: fadeInVisible }">
        <div class="pedido-info">
          <h3 class="produto-nome">{{ pedido.nome_produto }}</h3>
          <p><span class="label">Quantidade:</span> {{ pedido.quantidade }}</p>
          <p><span class="label">Total:</span> {{ formatarMoeda(pedido.valor_total) }}</p>
          <p><span class="label">Data:</span> {{ formatarData(pedido.data) }}</p>
          <p v-if="pedido.plano" class="plano-destaque">
            <span class="label">Plano:</span> {{ pedido.plano | capitalize }}
          </p>
          <!-- Se houver cupom aplicado -->
          <p v-if="pedido.cupom_aplicado"><span class="label">Cupom:</span> {{ pedido.cupom_aplicado }}</p>
        </div>
        <div class="pedido-actions">
          <router-link :to="`/produto/${pedido.id_produto}`" class="btn-secondary">
            <i class="fas fa-redo"></i> Comprar novamente
          </router-link>
          <button class="btn-primary" @click="verDetalhes(pedido.id_compra)" v-if="pedido.id_compra">
            <i class="fas fa-eye"></i> Ver detalhes
          </button>
        </div>
      </div>
    </div>

    <div v-else class="pedidos-vazio texto-centro">
      <i class="fas fa-shopping-bag"></i>
      <p class="texto-corrido">Você ainda não fez nenhum pedido.</p>
      <div class="texto-centro">
        <router-link to="/#planos" class="btn-modern">Conhecer Planos</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// Estado
const pedidos = ref([])
const carregando = ref(false)
const fadeInVisible = ref(false)

// Formatação
const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor || 0)
}

const formatarData = (dataStr) => {
  if (!dataStr) return ''
  const data = new Date(dataStr)
  return data.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

// Carregar pedidos da API
async function carregarPedidos() {
  carregando.value = true
  try {
    const response = await fetch('/api/meus-pedidos', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      }
    })
    if (!response.ok) throw new Error('Erro ao buscar pedidos')
    const data = await response.json()
    pedidos.value = data.pedidos || data.vendas || [] // adapta conforme retorno da API
  } catch (error) {
    console.error('Erro ao carregar pedidos:', error)
    // Exibir notificação de erro (opcional)
  } finally {
    carregando.value = false
    // Animar cards após carregar
    setTimeout(() => { fadeInVisible.value = true }, 100)
  }
}

// Navegar para detalhes do pedido (se disponível)
function verDetalhes(idCompra) {
  router.push(`/pedido/${idCompra}`)
}

// Verificar autenticação ao montar
onMounted(async () => {
  if (!authStore.logado) {
    router.push('/login?redirect=meus-pedidos')
    return
  }
  await carregarPedidos()
})
</script>

<style scoped>
/* ===== ESTILOS EXCLUSIVOS PARA MEUS PEDIDOS ===== */
.meus-pedidos {
  margin-top: 120px;
  min-height: 60vh;
  padding: 0 var(--espacamento-sm);
}

.pedidos-lista {
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-md);
  margin-top: var(--espacamento-lg);
}

.pedido-card {
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-md);
  border: 1px solid rgba(255, 215, 0, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--espacamento-sm);
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
}

.pedido-card.fade-in {
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.pedido-card.visible {
  opacity: 1;
  transform: translateY(0);
}

.pedido-card:hover {
  border-color: var(--cor-dourado);
  transform: translateY(-4px);
  box-shadow: var(--sombra-destaque);
}

.pedido-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.pedido-info h3 {
  font-size: 1.3rem;
  color: var(--cor-dourado);
  margin-bottom: 0.25rem;
}

.pedido-info p {
  margin: 0;
  color: var(--cor-texto-secundario);
  font-size: 0.95rem;
}

.pedido-info .label {
  font-weight: 600;
  color: var(--cor-texto);
}

.plano-destaque {
  background: rgba(255, 215, 0, 0.1);
  padding: 0.25rem 0.5rem;
  border-radius: var(--borda-radius-sm);
  display: inline-block;
  width: fit-content;
}

.pedido-actions {
  display: flex;
  gap: var(--espacamento-sm);
  align-items: center;
  flex-wrap: wrap;
}

.btn-secondary {
  background: var(--cor-fundo);
  border: 1px solid var(--cor-dourado);
  color: var(--cor-texto);
  padding: 0.6rem 1.2rem;
  border-radius: var(--borda-radius-md);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
.btn-secondary:hover {
  background: var(--cor-dourado);
  color: var(--cor-fundo);
  transform: translateY(-2px);
}

.btn-primary {
  background: var(--gradiente-botao-dourado-claro-escuro);
  color: var(--cor-fundo);
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: var(--borda-radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: var(--sombra-destaque);
}

.pedidos-vazio {
  margin-top: var(--espacamento-xl);
}
.pedidos-vazio i {
  font-size: 4rem;
  color: var(--cor-dourado);
  opacity: 0.5;
  margin-bottom: var(--espacamento-sm);
  display: inline-block;
}

.loading-spinner {
  text-align: center;
  padding: var(--espacamento-xl);
  font-size: 1.2rem;
  color: var(--cor-dourado);
}

.texto-centro {
  text-align: center;
}

/* Responsividade */
@media (max-width: 768px) {
  .pedido-card {
    flex-direction: column;
    align-items: stretch;
  }
  .pedido-actions {
    justify-content: center;
  }
  .pedido-info {
    text-align: center;
  }
  .plano-destaque {
    margin: 0 auto;
  }
}
</style>