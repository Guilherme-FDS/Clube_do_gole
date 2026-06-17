<template>
  <div class="container meus-pedidos">
    <h1 class="titulo-lg">Meus Pedidos</h1>

    <div v-if="bannerPagamento" :class="['banner-pagamento', bannerPagamento.tipo]">
      <i :class="bannerPagamento.icone"></i>
      {{ bannerPagamento.msg }}
    </div>

    <div v-if="carregando" class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i> Carregando pedidos...
    </div>

    <div v-else-if="pedidos.length" class="pedidos-lista">
      <div v-for="pedido in pedidos" :key="pedido.id" class="pedido-card fade-in"
        :class="{ visible: fadeInVisible }">

        <div class="pedido-header" @click="toggleDetalhes(pedido.id)">
          <div class="pedido-header-info">
            <span class="pedido-id">#{{ pedido.id }}</span>
            <span class="badge-status" :class="pedido.status">{{ pedido.status }}</span>
          </div>
          <div class="pedido-header-valores">
            <span class="pedido-data">{{ formatarData(pedido.data) }}</span>
            <span class="pedido-total">{{ formatarMoeda(pedido.valor_total) }}</span>
            <i class="fas" :class="aberto === pedido.id ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
          </div>
        </div>

        <div v-show="aberto === pedido.id" class="pedido-detalhes">
          <div v-if="pedido.cupom_aplicado" class="cupom-info">
            <i class="fas fa-tag"></i>
            Cupom <strong>{{ pedido.cupom_aplicado }}</strong> —
            economia de {{ formatarMoeda(pedido.economia) }}
          </div>

          <div class="itens-lista">
            <div v-for="item in pedido.itens" :key="item.id_produto" class="item-pedido">
              <img :src="item.imagem || '/img/sem_imagem.png'" :alt="item.nome_produto" class="item-img">
              <div class="item-info">
                <strong class="item-nome">{{ item.nome_produto }}</strong>
                <span class="item-plano">Plano {{ item.plano }}</span>
                <span class="item-qtd">{{ item.quantidade }}x {{ formatarMoeda(item.valor_unitario) }}</span>
              </div>
              <span class="item-total">{{ formatarMoeda(item.valor_total) }}</span>
              <router-link v-if="item.id_produto" :to="`/produto/${item.id_produto}`"
                class="btn-recomprar" title="Comprar novamente">
                <i class="fas fa-redo"></i>
              </router-link>
            </div>
          </div>

          <div class="pedido-resumo">
            <div v-if="pedido.desconto_aplicado > 0" class="resumo-linha desconto">
              <span>Desconto</span>
              <span>- {{ formatarMoeda(pedido.desconto_aplicado) }}</span>
            </div>
            <div class="resumo-linha total">
              <span>Total pago</span>
              <span>{{ formatarMoeda(pedido.valor_total) }}</span>
            </div>
          </div>
        </div>

      </div>
    </div>

    <div v-else class="pedidos-vazio texto-centro">
      <i class="fas fa-shopping-bag"></i>
      <p class="texto-corrido">Você ainda não fez nenhum pedido.</p>
      <router-link to="/#planos" class="btn-modern">Conhecer Planos</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const router = useRouter()
const route  = useRoute()
const authStore = useAuthStore()

const pedidos = ref([])

const bannerPagamento = computed(() => {
  const s = route.query.pagamento
  if (!s) return null
  if (s === 'sucesso') return { tipo: 'sucesso', icone: 'fas fa-check-circle', msg: 'Pagamento aprovado! Seu pedido está confirmado.' }
  if (s === 'pendente') return { tipo: 'pendente', icone: 'fas fa-clock', msg: 'Pagamento em análise. Você será notificado quando aprovado.' }
  return { tipo: 'falha', icone: 'fas fa-times-circle', msg: 'Pagamento não aprovado. Tente novamente.' }
})
const carregando = ref(false)
const fadeInVisible = ref(false)
const aberto = ref(null)

const formatarMoeda = (valor) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor || 0)

const formatarData = (dataStr) => {
  if (!dataStr) return ''
  return new Date(dataStr).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
}

function toggleDetalhes(id) {
  aberto.value = aberto.value === id ? null : id
}

async function carregarPedidos() {
  carregando.value = true
  try {
    const { data } = await api.get('/configuracoes/perfil')
    pedidos.value = data.pedidos || []
  } catch {
    console.error('Erro ao carregar pedidos.')
  } finally {
    carregando.value = false
    setTimeout(() => { fadeInVisible.value = true }, 100)
  }
}

onMounted(async () => {
  if (!authStore.logado) {
    router.push('/login?redirect=/meus-pedidos')
    return
  }
  await carregarPedidos()
})
</script>

<style scoped>
.meus-pedidos {
  margin-top: 120px;
  min-height: 60vh;
  padding-bottom: var(--espacamento-xl);
}
.meus-pedidos .titulo-lg { text-align: center; margin-bottom: var(--espacamento-lg); }

.banner-pagamento {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 14px 20px;
  border-radius: 10px;
  font-weight: 600;
  font-size: 15px;
  margin-bottom: 24px;
}
.banner-pagamento.sucesso  { background: #EBF8F0; color: #2E8B57; border: 1px solid #2E8B57; }
.banner-pagamento.pendente { background: #FEF8E7; color: #B7791F; border: 1px solid #B7791F; }
.banner-pagamento.falha    { background: #FEF2F2; color: #DC2626; border: 1px solid #DC2626; }

.pedidos-lista {
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-md);
  max-width: 860px;
  margin: 0 auto;
}

.pedido-card {
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-lg);
  border: 1px solid rgba(201,168,76,0.2);
  overflow: hidden;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.pedido-card:hover { border-color: rgba(201,168,76,0.4); box-shadow: var(--sombra-destaque); }

.pedido-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem var(--espacamento-md);
  cursor: pointer;
  gap: 1rem;
  flex-wrap: wrap;
}
.pedido-header:hover { background: rgba(201,168,76,0.04); }

.pedido-header-info { display: flex; align-items: center; gap: 0.75rem; }
.pedido-id { font-family: monospace; font-weight: 700; color: var(--cor-dourado); font-size: 1rem; }

.badge-status {
  padding: 0.25rem 0.75rem;
  border-radius: var(--borda-radius-lg);
  font-size: 0.75rem; font-weight: 700; text-transform: uppercase; border: 1px solid;
}
.badge-status.pago      { background: rgba(76,175,80,.2);  color: #4CAF50; border-color: #4CAF50; }
.badge-status.pendente  { background: rgba(255,193,7,.2);  color: #FFC107; border-color: #FFC107; }
.badge-status.cancelado { background: rgba(244,67,54,.2);  color: #f44336; border-color: #f44336; }
.badge-status.estornado { background: rgba(33,150,243,.2); color: #2196F3; border-color: #2196F3; }

.pedido-header-valores { display: flex; align-items: center; gap: 1.25rem; }
.pedido-data  { color: var(--cor-texto-secundario); font-size: 0.875rem; }
.pedido-total { font-weight: 700; color: var(--cor-dourado); font-size: 1.1rem; }
.pedido-header-valores .fas { color: var(--cor-texto-secundario); font-size: 0.875rem; }

.pedido-detalhes {
  border-top: 1px solid rgba(201,168,76,0.15);
  padding: var(--espacamento-md);
}

.cupom-info {
  display: flex; align-items: center; gap: 0.5rem;
  background: rgba(201,168,76,0.08);
  border: 1px solid rgba(201,168,76,0.2);
  border-radius: var(--borda-radius-sm);
  padding: 0.5rem 1rem;
  font-size: 0.875rem;
  color: var(--cor-texto-secundario);
  margin-bottom: var(--espacamento-md);
}
.cupom-info .fas { color: var(--cor-dourado); }
.cupom-info strong { color: var(--cor-dourado); }

.itens-lista { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: var(--espacamento-md); }
.item-pedido {
  display: flex; align-items: center; gap: 1rem;
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-sm);
  padding: 0.75rem 1rem;
  border: 1px solid rgba(255,255,255,0.05);
}
.item-img {
  width: 56px; height: 56px;
  object-fit: cover; border-radius: var(--borda-radius-sm);
  flex-shrink: 0;
}
.item-info { flex: 1; display: flex; flex-direction: column; gap: 0.2rem; }
.item-nome { color: var(--cor-texto); font-size: 0.9375rem; font-weight: 600; }
.item-plano { color: var(--cor-dourado); font-size: 0.8rem; text-transform: capitalize; }
.item-qtd  { color: var(--cor-texto-secundario); font-size: 0.8125rem; }
.item-total { font-weight: 700; color: var(--cor-dourado); white-space: nowrap; }
.btn-recomprar {
  width: 32px; height: 32px; border-radius: 50%;
  background: rgba(201,168,76,0.12);
  border: 1px solid rgba(201,168,76,0.3);
  color: var(--cor-dourado);
  display: flex; align-items: center; justify-content: center;
  text-decoration: none; font-size: 0.8rem;
  transition: all 0.2s ease; flex-shrink: 0;
}
.btn-recomprar:hover { background: rgba(201,168,76,0.25); transform: scale(1.1); }

.pedido-resumo {
  border-top: 1px solid rgba(255,255,255,0.06);
  padding-top: 0.75rem;
  display: flex; flex-direction: column; gap: 0.4rem;
  align-items: flex-end;
}
.resumo-linha { display: flex; gap: 2rem; font-size: 0.9rem; }
.resumo-linha.desconto { color: #4CAF50; }
.resumo-linha.total { font-weight: 700; font-size: 1rem; color: var(--cor-dourado); }

.pedidos-vazio {
  margin-top: var(--espacamento-xl);
  display: flex; flex-direction: column; align-items: center; gap: var(--espacamento-md);
}
.pedidos-vazio .fas { font-size: 4rem; color: var(--cor-dourado); opacity: 0.4; }
.pedidos-vazio .texto-corrido { color: var(--cor-texto-secundario); }

.loading-spinner {
  text-align: center; padding: var(--espacamento-xl);
  font-size: 1.2rem; color: var(--cor-dourado);
}

.fade-in { opacity: 0; transform: translateY(20px); transition: opacity 0.5s ease, transform 0.5s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }

@media (max-width: 768px) {
  .pedido-header { flex-direction: column; align-items: flex-start; }
  .pedido-header-valores { width: 100%; justify-content: space-between; }
  .item-pedido { flex-wrap: wrap; }
}
</style>