<template>
  <DefaultLayout>
    <main class="carrinho">
      <section class="cart-container">
        <h2 class="titulo-lg">🛒 Meu Carrinho</h2>

        <div v-if="isGuest" class="guest-alert">
          <i class="fas fa-info-circle"></i>
          <div class="guest-message">
            <strong>Você não está logado</strong>
            <p>Adicione itens ao carrinho agora e faça login na hora de finalizar a compra.</p>
            <router-link to="/login" class="btn-login-guest">
              <i class="fas fa-sign-in-alt"></i> Fazer Login
            </router-link>
          </div>
        </div>

        <div v-if="flash" :class="`flash-${flash.tipo}`">{{ flash.msg }}</div>

        <template v-if="itens.length">
          <div class="tabela-wrapper">
            <table class="tabela-carrinho">
              <thead>
                <tr>
                  <th>Produto</th><th>Plano</th><th>Quantidade</th>
                  <th>Valor Unitário</th><th>Total</th><th>Ações</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in itens" :key="item.id_carrinho" class="cart-item">
                  <td class="produto-info">
                    <div class="produto-detalhes">
                      <strong class="produto-nome">{{ item.nome_produto }}</strong>
                      <small v-if="item.descricao" class="produto-descricao">{{ item.descricao }}</small>
                    </div>
                  </td>
                  <td><span :class="`plano-badge ${item.plano}`">{{ item.plano }}</span></td>
                  <td class="quantidade-cell">
                    <div class="controle-quantidade">
                      <button type="button" class="btn-quantidade" @click="alterarQtd(item, -1)">
                        <i class="fas fa-minus"></i>
                      </button>
                      <input type="number" min="1" :value="item.quantidade"
                        class="quantidade-display quantidade-input"
                        @change="e => setQtd(item, e.target.value)" />
                      <button type="button" class="btn-quantidade" @click="alterarQtd(item, 1)">
                        <i class="fas fa-plus"></i>
                      </button>
                    </div>
                  </td>
                  <td class="valor-unitario">R$ {{ fmt(item.valor_unitario) }}</td>
                  <td class="item-total">R$ {{ fmt(item.valor_total) }}</td>
                  <td class="acoes-cell">
                    <div class="acoes-container">
                      <input type="checkbox" v-model="selecionados" :value="item.id_carrinho" class="checkbox-item" />
                      <button type="button" class="btn-excluir-item" @click="excluir(item.id_carrinho)">
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
              <span class="total-valor">R$ {{ fmt(total) }}</span>
            </div>
            <div class="acoes-carrinho">
              <a href="/#planos" class="btn-modern btn-continuar">
                <i class="fas fa-shopping-bag"></i> Continuar Comprando
              </a>
              <button class="btn-modern btn-finalizar" @click="irCheckout">
                <i class="fas fa-check-circle"></i> Finalizar Compra dos Selecionados
              </button>
            </div>
          </div>
        </template>

        <div v-else class="carrinho-vazio">
          <div class="carrinho-vazio-icon"><i class="fas fa-shopping-cart"></i></div>
          <h3>Seu carrinho está vazio</h3>
          <p>Explore nossos produtos e adicione itens incríveis!</p>
          <a href="/#planos" class="btn-modern btn-continuar">
            <i class="fas fa-shopping-bag"></i> Continuar Comprando
          </a>
        </div>
      </section>
    </main>
  </DefaultLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCarrinhoStore } from '@/stores/carrinho'
import { useAuthStore } from '@/stores/auth'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const carrinho    = useCarrinhoStore()
const auth        = useAuthStore()
const router      = useRouter()
const itens       = computed(() => carrinho.itens)
const total       = computed(() => carrinho.total)
const isGuest     = computed(() => !auth.logado)
const selecionados = ref([])
const flash        = ref(null)

function fmt(v) { return parseFloat(v || 0).toFixed(2).replace('.', ',') }

function mostrarFlash(msg, tipo = 'sucesso') {
  flash.value = { msg, tipo }
  setTimeout(() => flash.value = null, 3000)
}

async function alterarQtd(item, delta) {
  await carrinho.atualizarQuantidade(item.id_carrinho, Math.max(1, item.quantidade + delta))
}

async function setQtd(item, valor) {
  await carrinho.atualizarQuantidade(item.id_carrinho, Math.max(1, parseInt(valor) || 1))
}

async function excluir(id) {
  await carrinho.remove([id])
  selecionados.value = selecionados.value.filter(s => s !== id)
  mostrarFlash('Item removido!')
}

function irCheckout() {
  if (!auth.logado) { router.push('/login?redirect=/checkout'); return }
  if (!selecionados.value.length) { mostrarFlash('Selecione ao menos um item.', 'erro'); return }
  sessionStorage.setItem('checkout_ids', JSON.stringify(selecionados.value))
  router.push('/checkout')
}

onMounted(async () => {
  await carrinho.buscar()
  selecionados.value = itens.value.map(i => i.id_carrinho)
})
</script>

<style scoped>
.carrinho {
  padding: calc(var(--espacamento-xl) + var(--espacamento-md)) var(--espacamento-md) var(--espacamento-xl);
  max-width: 1200px;
  margin: 0 auto;
  min-height: 100vh;
}

.cart-container {
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-lg);
  box-shadow: var(--sombra-destaque);
  border: 1px solid rgba(255, 215, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.cart-container::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--gradiente-botao-dourado-claro-escuro, linear-gradient(45deg, #F4D03F, #b58500));
}

.titulo-lg {
  font-family: var(--fonte-secundaria);
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 600;
  margin-bottom: var(--espacamento-md);
  text-align: center;
  color: var(--cor-dourado);
}

/* Guest */
.guest-alert {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 15px 20px;
  border-radius: 10px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.guest-alert i { font-size: 24px; flex-shrink: 0; }
.guest-message strong { display: block; margin-bottom: 5px; }
.guest-message p { margin: 0 0 8px; opacity: 0.9; font-size: 14px; }

.btn-login-guest {
  background: rgba(255,255,255,0.2);
  color: white;
  padding: 8px 16px;
  border-radius: 6px;
  text-decoration: none;
  font-size: 14px;
  transition: all 0.3s;
  border: 1px solid rgba(255,255,255,0.3);
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}
.btn-login-guest:hover { background: rgba(255,255,255,0.3); }

/* Flash */
.flash-sucesso {
  background: linear-gradient(135deg, #00ff88, #00cc66);
  color: #000; padding: var(--espacamento-sm);
  border-radius: var(--borda-radius-md); text-align: center;
  font-weight: 500; margin-bottom: var(--espacamento-sm);
}
.flash-erro {
  background: linear-gradient(135deg, #ff4444, #cc0000);
  color: #fff; padding: var(--espacamento-sm);
  border-radius: var(--borda-radius-md); text-align: center;
  font-weight: 500; margin-bottom: var(--espacamento-sm);
}

/* Tabela */
.tabela-wrapper { overflow-x: auto; border-radius: var(--borda-radius-md); margin: var(--espacamento-md) 0; }

.tabela-carrinho {
  width: 100%; border-collapse: collapse;
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-md); overflow: hidden;
}

.tabela-carrinho th {
  background: linear-gradient(45deg, #F4D03F, #b58500);
  color: var(--cor-fundo);
  padding: var(--espacamento-sm);
  text-align: left; font-weight: 600; font-size: 0.9rem;
  text-transform: uppercase; letter-spacing: 0.5px;
}

.tabela-carrinho td {
  padding: var(--espacamento-sm);
  border-bottom: 1px solid rgba(255,255,255,0.1);
  color: var(--cor-texto); vertical-align: middle;
}

.tabela-carrinho tr:last-child td { border-bottom: none; }
.tabela-carrinho tr:hover { background: rgba(255, 215, 0, 0.05); }

.produto-nome { color: var(--cor-texto); font-weight: 600; display: block; margin-bottom: var(--espacamento-xs); }
.produto-descricao { color: var(--cor-texto-secundario); font-size: 0.875rem; }

.plano-badge {
  text-transform: capitalize;
  background: linear-gradient(45deg, var(--cor-dourado), var(--cor-dourado-suave));
  color: var(--cor-fundo);
  padding: 0.5rem 1rem; border-radius: var(--borda-radius-lg);
  font-size: 0.8rem; font-weight: 600; display: inline-block;
}
.plano-badge.semestral { background: linear-gradient(45deg, var(--cor-roxo-principal), #9370DB); }
.plano-badge.anual     { background: linear-gradient(45deg, var(--cor-roxo-escuro), var(--cor-roxo-principal)); }

.valor-unitario { color: var(--cor-texto-secundario); font-weight: 500; }
.item-total { font-weight: bold; color: var(--cor-dourado); font-size: 1.1rem; }

/* Quantidade */
.quantidade-cell { text-align: center; }
.controle-quantidade {
  display: flex; align-items: center; justify-content: center;
  gap: 8px; background: rgba(255, 215, 0, 0.1);
  border-radius: var(--borda-radius-md); padding: 4px;
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.btn-quantidade {
  background: linear-gradient(45deg, #F4D03F, #b58500);
  color: var(--cor-fundo); border: none;
  border-radius: var(--borda-radius-sm);
  width: 32px; height: 32px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.3s; font-weight: bold;
}
.btn-quantidade:hover { transform: scale(1.1); }

.quantidade-display.quantidade-input {
  width: 60px; padding: 8px;
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: var(--borda-radius-sm);
  background: var(--cor-fundo-secundario); color: var(--cor-dourado);
  text-align: center; font-size: 1.1rem; font-weight: bold;
  -moz-appearance: textfield; appearance: textfield;
}
.quantidade-display.quantidade-input::-webkit-outer-spin-button,
.quantidade-display.quantidade-input::-webkit-inner-spin-button { -webkit-appearance: none; }
.quantidade-display.quantidade-input:focus {
  outline: none; border-color: var(--cor-dourado);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

/* Ações */
.acoes-cell { text-align: center; width: 120px; }
.acoes-container { display: flex; align-items: center; justify-content: center; gap: 12px; }

.btn-excluir-item {
  background: linear-gradient(45deg, #ff4444, #cc0000);
  color: white; border: none; border-radius: var(--borda-radius-sm);
  padding: 8px; cursor: pointer; transition: all 0.3s;
  display: flex; align-items: center; justify-content: center;
  width: 36px; height: 36px;
}
.btn-excluir-item:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(255,68,68,0.4); }

.checkbox-item { transform: scale(1.3); cursor: pointer; accent-color: var(--cor-dourado); }

/* Resumo */
.resumo-carrinho {
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  margin-top: var(--espacamento-lg);
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.total-carrinho {
  display: flex; justify-content: space-between; align-items: center;
  font-size: 1.5rem; font-weight: bold;
  margin-bottom: var(--espacamento-md); padding: var(--espacamento-sm);
  background: rgba(255, 215, 0, 0.1); border-radius: var(--borda-radius-md);
}
.total-label { color: var(--cor-texto); }
.total-valor { color: var(--cor-dourado); font-size: 1.75rem; }

.acoes-carrinho { display: flex; gap: var(--espacamento-sm); flex-wrap: wrap; justify-content: space-between; }

.btn-modern {
  background: linear-gradient(45deg, #F4D03F, #b58500);
  color: var(--cor-fundo); border: none;
  padding: 1rem 2rem; border-radius: var(--borda-radius-lg);
  font-weight: 600; cursor: pointer; transition: all 0.3s;
  position: relative; overflow: hidden; font-size: 1.1rem;
  text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem;
}
.btn-modern::before {
  content: ''; position: absolute; top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}
.btn-modern:hover::before { left: 100%; }
.btn-modern:hover { transform: translateY(-3px); box-shadow: var(--sombra-destaque); }

.btn-finalizar { background: linear-gradient(45deg, var(--cor-roxo-escuro), var(--cor-roxo-principal)); }

/* Vazio */
.carrinho-vazio { text-align: center; padding: var(--espacamento-xl); color: var(--cor-texto-secundario); }
.carrinho-vazio-icon { font-size: 4rem; color: var(--cor-dourado); margin-bottom: var(--espacamento-md); }
.carrinho-vazio h3 { font-family: var(--fonte-secundaria); color: var(--cor-dourado); font-size: 1.5rem; margin-bottom: var(--espacamento-sm); }
.carrinho-vazio p  { font-size: 1.1rem; margin-bottom: var(--espacamento-lg); }

/* Responsivo */
@media (max-width: 768px) {
  .tabela-carrinho th, .tabela-carrinho td { padding: 0.75rem 0.5rem; }
  .acoes-carrinho { flex-direction: column; }
  .btn-modern { width: 100%; justify-content: center; }
  .total-carrinho { flex-direction: column; gap: var(--espacamento-xs); text-align: center; }
  .guest-alert { flex-direction: column; text-align: center; }
}

@media (max-width: 480px) {
  .carrinho { padding: calc(var(--espacamento-xl) + var(--espacamento-xs)) var(--espacamento-xs) var(--espacamento-lg); }
  .cart-container { padding: var(--espacamento-sm); border-radius: var(--borda-radius-md); }
  .tabela-carrinho { font-size: 0.8rem; }
}
</style>