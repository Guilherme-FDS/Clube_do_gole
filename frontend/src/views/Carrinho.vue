<template>
  <div class="carrinho-page">
    <div class="carrinho-container">

      <!-- HEADER -->
      <div class="carrinho-header">
        <div>
          <span class="section-badge section-badge-escuro">Sua Seleção</span>
          <h1 class="titulo-lg titulo-claro">Meu <span class="dourado-escuro">Carrinho</span></h1>
        </div>
        <router-link to="/produto/1" class="btn-continuar-link">
          ← Continuar explorando
        </router-link>
      </div>

      <!-- ALERTA NÃO LOGADO -->
      <div v-if="!logado" class="alerta-login">
        <i class="fas fa-lock"></i>
        <div>
          <strong>Faça login para finalizar sua compra</strong>
          <p>Seus itens serão mantidos após o login.</p>
        </div>
        <router-link to="/login?redirect=carrinho" class="btn-login-alerta">
          Fazer Login
        </router-link>
      </div>

      <!-- FLASH -->
      <transition name="fade">
        <div v-if="mensagem" :class="['flash', 'flash-' + mensagem.tipo]">
          <i :class="mensagem.tipo === 'success' ? 'fas fa-check-circle' : mensagem.tipo === 'error' ? 'fas fa-exclamation-circle' : 'fas fa-info-circle'"></i>
          {{ mensagem.texto }}
        </div>
      </transition>

      <!-- CONTEÚDO COM ITENS -->
      <div v-if="itensCarrinho.length" class="carrinho-layout">

        <!-- LISTA DE ITENS -->
        <div class="itens-lista">
          <div
            v-for="item in itensCarrinho"
            :key="item.id_carrinho"
            class="item-card"
            :class="{ selecionado: selecionados.includes(item.id_carrinho) }"
          >
            <!-- Checkbox de seleção -->
            <label class="item-select">
              <input type="checkbox" :value="item.id_carrinho" v-model="selecionados" />
              <span class="checkmark"></span>
            </label>

            <!-- Info do produto -->
            <div class="item-info">
              <div class="item-topo">
                <div>
                  <h3 class="item-nome">{{ item.nome_produto }}</h3>
                  <p v-if="item.descricao" class="item-descricao">{{ item.descricao }}</p>
                </div>
                <span :class="['plano-badge', item.plano]">{{ nomePlano(item.plano) }}</span>
              </div>

              <div class="item-rodape">
                <!-- Controle de quantidade -->
                <div class="controle-quantidade">
                  <button @click="diminuirQuantidade(item.id_carrinho)" class="btn-qtd">
                    <i class="fas fa-minus"></i>
                  </button>
                  <input
                    type="number"
                    v-model.number="quantidades[item.id_carrinho]"
                    @change="atualizarQuantidadeManual(item.id_carrinho, quantidades[item.id_carrinho])"
                    min="1"
                    class="qtd-input"
                  />
                  <button @click="aumentarQuantidade(item.id_carrinho)" class="btn-qtd">
                    <i class="fas fa-plus"></i>
                  </button>
                </div>

                <!-- Preço -->
                <div class="item-precos">
                  <span class="item-unitario">{{ formatarMoeda(item.valor_unitario) }}/un.</span>
                  <span class="item-total-valor">{{ formatarMoeda(item.valor_total) }}</span>
                </div>

                <!-- Remover -->
                <button @click="excluirItem(item.id_carrinho)" class="btn-remover" title="Remover item">
                  <i class="fas fa-trash-alt"></i>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- PAINEL DE RESUMO -->
        <aside class="resumo-painel">
          <h2 class="resumo-titulo">Resumo do Pedido</h2>

          <div class="resumo-linhas">
            <div class="resumo-linha" v-for="item in itensSelecionadosObj" :key="item.id_carrinho">
              <span class="resumo-item-nome">{{ item.nome_produto }} <em>({{ nomePlano(item.plano) }})</em></span>
              <span>{{ formatarMoeda(item.valor_total) }}</span>
            </div>
            <div v-if="itensSelecionadosObj.length === 0" class="resumo-vazio">
              Nenhum item selecionado
            </div>
          </div>

          <div class="resumo-divisor"></div>

          <div class="resumo-total">
            <span>Total</span>
            <span class="resumo-total-valor">{{ formatarMoeda(totalSelecionados) }}</span>
          </div>

          <button
            @click="abrirCheckout"
            class="btn-finalizar"
            :disabled="selecionados.length === 0"
          >
            Finalizar Compra
            <i class="fas fa-arrow-right"></i>
          </button>

          <p class="resumo-nota">
            <i class="fas fa-lock"></i> Pagamento seguro · Cancele quando quiser
          </p>
        </aside>
      </div>

      <!-- CARRINHO VAZIO -->
      <div v-else class="carrinho-vazio">
        <div class="vazio-icone">
          <i class="fas fa-shopping-bag"></i>
        </div>
        <h3 class="vazio-titulo">Seu carrinho está vazio</h3>
        <p class="vazio-sub">Explore nossos planos e escolha sua assinatura.</p>
        <router-link to="/produto/1" class="btn-explorar">
          Explorar Planos
        </router-link>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCarrinhoStore } from '@/stores/carrinho'

const router = useRouter()
const authStore = useAuthStore()
const carrinhoStore = useCarrinhoStore()

const selecionados = ref([])
const quantidades = ref({})
const mensagem = ref(null)

const logado = computed(() => authStore.logado)
const itensCarrinho = computed(() => carrinhoStore.itens)
const totalGeral = computed(() => carrinhoStore.total)

const itensSelecionadosObj = computed(() =>
  itensCarrinho.value.filter(i => selecionados.value.includes(i.id_carrinho))
)
const totalSelecionados = computed(() =>
  itensSelecionadosObj.value.reduce((s, i) => s + Number(i.valor_total), 0)
)

const nomePlano = (rec) => ({ mensal: 'Mensal', semestral: 'Semestral', anual: 'Anual' }[rec] || rec)

const formatarMoeda = (valor) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor || 0)

const sincronizarQuantidades = () => {
  const obj = {}
  itensCarrinho.value.forEach(i => { obj[i.id_carrinho] = i.quantidade })
  quantidades.value = obj
}

const mostrarMensagem = (texto, tipo = 'success') => {
  mensagem.value = { texto, tipo }
  setTimeout(() => { mensagem.value = null }, 4000)
}

const aumentarQuantidade = async (itemId) => {
  await atualizarQuantidadeNoServidor(itemId, quantidades.value[itemId] + 1)
}

const diminuirQuantidade = async (itemId) => {
  if (quantidades.value[itemId] <= 1) return
  await atualizarQuantidadeNoServidor(itemId, quantidades.value[itemId] - 1)
}

const atualizarQuantidadeManual = async (itemId, novaQtd) => {
  if (novaQtd < 1) {
    const original = itensCarrinho.value.find(i => i.id_carrinho == itemId)
    if (original) quantidades.value[itemId] = original.quantidade
    return
  }
  await atualizarQuantidadeNoServidor(itemId, novaQtd)
}

const atualizarQuantidadeNoServidor = async (itemId, novaQtd) => {
  try {
    await carrinhoStore.atualizarQuantidade(itemId, novaQtd)
    sincronizarQuantidades()
  } catch {
    mostrarMensagem('Erro ao atualizar quantidade.', 'error')
    const original = itensCarrinho.value.find(i => i.id_carrinho == itemId)
    if (original) quantidades.value[itemId] = original.quantidade
  }
}

const excluirItem = async (itemId) => {
  if (!confirm('Remover este item do carrinho?')) return
  try {
    await carrinhoStore.remove(itemId)
    selecionados.value = selecionados.value.filter(id => id !== itemId)
    sincronizarQuantidades()
    mostrarMensagem('Item removido.', 'success')
  } catch {
    mostrarMensagem('Erro ao remover item.', 'error')
  }
}

const abrirCheckout = () => {
  if (selecionados.value.length === 0) {
    mostrarMensagem('Selecione ao menos um item.', 'error')
    return
  }
  localStorage.setItem('checkoutItems', JSON.stringify(selecionados.value))
  if (!logado.value) {
    window.scrollTo({ top: 0, behavior: 'smooth' })
    mostrarMensagem('Faça login para finalizar a compra.', 'info')
    return
  }
  router.push('/checkout')
}

onMounted(async () => {
  document.body.classList.add('pagina-clara')
  await carrinhoStore.buscar()
  sincronizarQuantidades()
  // Pré-selecionar todos os itens
  selecionados.value = itensCarrinho.value.map(i => i.id_carrinho)
})

onUnmounted(() => {
  document.body.classList.remove('pagina-clara')
})
</script>

<style scoped>
/* ── PAGE ───────────────────────────────────────── */
.carrinho-page {
  min-height: 100vh;
  background: #fff;
}
.carrinho-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: calc(var(--espacamento-xl) + var(--espacamento-md)) var(--espacamento-md) var(--espacamento-xl);
}

/* ── HEADER ─────────────────────────────────────── */
.carrinho-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 2.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}
.titulo-claro { color: #1b1a19 !important; }
.dourado-escuro { color: var(--cor-dourado-escuro); }
.section-badge-escuro {
  border-color: var(--cor-dourado-escuro);
  color: var(--cor-dourado-escuro);
  background: rgba(158,122,46,0.06);
  margin-bottom: 0.75rem;
}
.btn-continuar-link {
  color: #888;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s;
}
.btn-continuar-link:hover { color: #1b1a19; }

/* ── ALERTA LOGIN ────────────────────────────────── */
.alerta-login {
  display: flex;
  align-items: center;
  gap: 1rem;
  background: #fafaf9;
  border: 1px solid #e8e4de;
  border-radius: 14px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}
.alerta-login i { color: var(--cor-dourado); font-size: 1.25rem; flex-shrink: 0; }
.alerta-login strong { display: block; color: #1b1a19; font-size: 0.95rem; }
.alerta-login p { color: #888; font-size: 0.85rem; margin: 0.15rem 0 0; }
.btn-login-alerta {
  margin-left: auto;
  background: #1b1a19;
  color: #fff;
  padding: 0.6rem 1.25rem;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 600;
  white-space: nowrap;
  transition: all 0.2s;
}
.btn-login-alerta:hover { background: #2d2b28; }

/* ── FLASH ──────────────────────────────────────── */
.flash {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.875rem 1.25rem;
  border-radius: 10px;
  font-size: 0.9rem;
  font-weight: 500;
  margin-bottom: 1.5rem;
}
.flash-success { background: #ecfdf5; color: #16a34a; border: 1px solid #bbf7d0; }
.flash-error   { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.flash-info    { background: #eff6ff; color: #2563eb; border: 1px solid #bfdbfe; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* ── LAYOUT ─────────────────────────────────────── */
.carrinho-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 2rem;
  align-items: start;
}

/* ── ITEM CARD ──────────────────────────────────── */
.itens-lista { display: flex; flex-direction: column; gap: 1rem; }

.item-card {
  display: flex;
  gap: 1.25rem;
  background: #fff;
  border: 1.5px solid #ede9e3;
  border-radius: 16px;
  padding: 1.5rem;
  transition: all 0.2s;
}
.item-card.selecionado {
  border-color: rgba(201,168,76,0.4);
  box-shadow: 0 4px 20px rgba(201,168,76,0.08);
}

/* Checkbox customizado */
.item-select { display: flex; align-items: flex-start; padding-top: 2px; flex-shrink: 0; }
.item-select input { display: none; }
.checkmark {
  width: 20px; height: 20px;
  border: 2px solid #d0cbc3;
  border-radius: 6px;
  display: flex; align-items: center; justify-content: center;
  cursor: pointer; transition: all 0.2s; flex-shrink: 0;
  background: #fff;
}
.item-select input:checked + .checkmark {
  background: var(--gradiente-dourado);
  border-color: transparent;
}
.item-select input:checked + .checkmark::after {
  content: '';
  width: 5px; height: 9px;
  border: 2px solid #1b1a19;
  border-top: none; border-left: none;
  transform: rotate(45deg) translateY(-1px);
  display: block;
}

/* Info */
.item-info { flex: 1; display: flex; flex-direction: column; gap: 1rem; }

.item-topo { display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; }

.item-nome {
  font-family: var(--fonte-principal);
  font-size: 1.2rem;
  color: #1b1a19;
  font-weight: 600;
  margin-bottom: 0.2rem;
}
.item-descricao { color: #888; font-size: 0.85rem; line-height: 1.5; }

/* Plano badges */
.plano-badge {
  display: inline-block;
  padding: 0.3rem 0.85rem;
  border-radius: 100px;
  font-size: 0.75rem;
  font-weight: 600;
  white-space: nowrap;
  flex-shrink: 0;
}
.plano-badge.mensal   { background: rgba(201,168,76,0.12); color: var(--cor-dourado-escuro); border: 1px solid rgba(201,168,76,0.3); }
.plano-badge.semestral { background: rgba(123,47,224,0.1); color: #6d28d9; border: 1px solid rgba(123,47,224,0.2); }
.plano-badge.anual    { background: rgba(27,26,25,0.06); color: #1b1a19; border: 1px solid rgba(27,26,25,0.15); }

/* Rodapé do item */
.item-rodape {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.75rem;
}

/* Controle de quantidade */
.controle-quantidade {
  display: flex;
  align-items: center;
  gap: 0;
  border: 1.5px solid #e8e4de;
  border-radius: 10px;
  overflow: hidden;
}
.btn-qtd {
  background: #f8f7f5;
  border: none;
  width: 36px; height: 36px;
  cursor: pointer;
  color: #555;
  display: flex; align-items: center; justify-content: center;
  font-size: 0.75rem;
  transition: background 0.15s;
}
.btn-qtd:hover { background: #ede9e3; }
.qtd-input {
  width: 48px;
  border: none;
  border-left: 1.5px solid #e8e4de;
  border-right: 1.5px solid #e8e4de;
  background: #fff;
  text-align: center;
  font-size: 0.95rem;
  font-weight: 600;
  color: #1b1a19;
  height: 36px;
  -moz-appearance: textfield;
  appearance: textfield;
  outline: none;
}
.qtd-input::-webkit-inner-spin-button,
.qtd-input::-webkit-outer-spin-button { -webkit-appearance: none; }

/* Preços */
.item-precos { display: flex; flex-direction: column; align-items: flex-end; }
.item-unitario { font-size: 0.78rem; color: #aaa; }
.item-total-valor {
  font-family: var(--fonte-principal);
  font-size: 1.3rem;
  font-weight: 700;
  color: #1b1a19;
}

/* Remover */
.btn-remover {
  background: none;
  border: none;
  color: #ccc;
  cursor: pointer;
  font-size: 0.95rem;
  padding: 0.4rem;
  border-radius: 8px;
  transition: all 0.2s;
  flex-shrink: 0;
}
.btn-remover:hover { color: #dc2626; background: #fef2f2; }

/* ── PAINEL RESUMO ──────────────────────────────── */
.resumo-painel {
  background: #fafaf9;
  border: 1.5px solid #ede9e3;
  border-radius: 20px;
  padding: 2rem;
  position: sticky;
  top: 6rem;
}
.resumo-titulo {
  font-family: var(--fonte-principal);
  font-size: 1.4rem;
  color: #1b1a19;
  margin-bottom: 1.5rem;
}
.resumo-linhas { display: flex; flex-direction: column; gap: 0.75rem; margin-bottom: 1rem; }
.resumo-linha {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: #555;
}
.resumo-item-nome { flex: 1; }
.resumo-item-nome em { color: #aaa; font-style: normal; }
.resumo-vazio { color: #bbb; font-size: 0.875rem; text-align: center; padding: 0.5rem 0; }
.resumo-divisor { height: 1px; background: #e8e4de; margin: 1rem 0; }
.resumo-total {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  margin-bottom: 1.5rem;
  font-weight: 600;
  color: #1b1a19;
}
.resumo-total-valor {
  font-family: var(--fonte-principal);
  font-size: 1.75rem;
  color: #1b1a19;
}

.btn-finalizar {
  width: 100%;
  background: #1b1a19;
  color: #fff;
  border: none;
  padding: 1rem;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.6rem;
  transition: all 0.2s;
  margin-bottom: 1rem;
}
.btn-finalizar:hover:not(:disabled) {
  background: #2d2b28;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}
.btn-finalizar:disabled { opacity: 0.4; cursor: not-allowed; }

.resumo-nota {
  text-align: center;
  color: #bbb;
  font-size: 0.78rem;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
}
.resumo-nota i { color: var(--cor-dourado-escuro); }

/* ── CARRINHO VAZIO ─────────────────────────────── */
.carrinho-vazio {
  text-align: center;
  padding: 5rem 2rem;
}
.vazio-icone {
  width: 72px; height: 72px;
  background: rgba(201,168,76,0.08);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1.5rem;
  font-size: 1.75rem;
  color: var(--cor-dourado);
}
.vazio-titulo {
  font-family: var(--fonte-principal);
  font-size: 1.75rem;
  color: #1b1a19;
  margin-bottom: 0.5rem;
}
.vazio-sub { color: #888; margin-bottom: 2rem; }
.btn-explorar {
  display: inline-block;
  background: #1b1a19;
  color: #fff;
  padding: 0.875rem 2rem;
  border-radius: 10px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s;
}
.btn-explorar:hover { background: #2d2b28; transform: translateY(-2px); }

/* ── RESPONSIVO ─────────────────────────────────── */
@media (max-width: 900px) {
  .carrinho-layout { grid-template-columns: 1fr; }
  .resumo-painel { position: static; }
}
@media (max-width: 600px) {
  .carrinho-header { flex-direction: column; align-items: flex-start; }
  .item-topo { flex-direction: column; }
  .item-rodape { flex-direction: column; align-items: flex-start; }
  .item-precos { align-items: flex-start; }
}
</style>
