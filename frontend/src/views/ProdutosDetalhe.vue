<template>
  <DefaultLayout>
    <main class="carrinho">
      <section class="cart-container">
        <h2 class="titulo-lg">🛒 Meu Carrinho</h2>

        <!-- Guest alert -->
        <div v-if="isGuest" class="guest-alert">
          <i class="fas fa-info-circle"></i>
          <div class="guest-message">
            <strong>Você não está logado</strong>
            <p>Adicione itens ao carrinho agora e faça login na hora de finalizar a compra. Seus itens serão mantidos!</p>
            <router-link to="/login" class="btn-login-guest">
              <i class="fas fa-sign-in-alt"></i> Fazer Login
            </router-link>
          </div>
        </div>

        <div v-if="flash" :class="`flash-${flash.tipo}`">{{ flash.msg }}</div>

        <!-- Com itens -->
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
                      <button type="button" class="btn-quantidade btn-diminuir" @click="alterarQtd(item, -1)">
                        <i class="fas fa-minus"></i>
                      </button>
                      <input type="number" min="1" :value="item.quantidade"
                        class="quantidade-display quantidade-input"
                        @change="e => setQtd(item, e.target.value)" />
                      <button type="button" class="btn-quantidade btn-aumentar" @click="alterarQtd(item, 1)">
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

        <!-- Vazio -->
        <div v-else class="carrinho-vazio">
          <div class="carrinho-vazio-icon"><i class="fas fa-shopping-cart"></i></div>
          <h3>Seu carrinho está vazio</h3>
          <p>Explore nossos produtos e adicione itens incríveis ao seu carrinho!</p>
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

const carrinho = useCarrinhoStore()
const auth     = useAuthStore()
const router   = useRouter()

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
  const nova = Math.max(1, item.quantidade + delta)
  await carrinho.atualizarQuantidade(item.id_carrinho, nova)
}

async function setQtd(item, valor) {
  const nova = Math.max(1, parseInt(valor) || 1)
  await carrinho.atualizarQuantidade(item.id_carrinho, nova)
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