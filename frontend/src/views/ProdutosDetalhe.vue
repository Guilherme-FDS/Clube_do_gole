<template>
  <div class="produto-container">

    <!-- HERO -->
    <div class="produto-hero">
      <div class="produto-imagem">
        <img :src="strapiImagem || '/img/sem_imagem.png'" :alt="produto.nome" class="imagem-principal">
        <span class="badge-surpresa">✦ Seleção Surpresa</span>
      </div>

      <div class="produto-info">
        <span class="section-badge">Assinatura Premium</span>
        <h1 class="titulo-produto">{{ produto.nome }}</h1>
        <p class="descricao-produto">{{ produto.descricao }}</p>

        <div class="pills-row">
          <span class="pill"><span class="pill-dot"></span>Curadoria especializada</span>
          <span class="pill"><span class="pill-dot"></span>2 rótulos por mês</span>
          <span class="pill"><span class="pill-dot"></span>Cancele quando quiser</span>
        </div>

        <div class="preco-bloco" v-if="planoMensal">
          <span class="preco-valor">{{ formatarMoeda(planoMensal.preco_base) }}</span>
          <span class="preco-per">/mês · 2 rótulos premium</span>
        </div>

        <button class="btn-modern" @click="scrollToPlanos">Escolher Plano ↓</button>
      </div>
    </div>

    <!-- PLANOS -->
    <section class="planos-section" id="planos">
      <div class="planos-header">
        <span class="section-badge section-badge-escuro">Nossas Assinaturas</span>
        <h2 class="titulo-lg titulo-claro">Escolha seu <span class="dourado-escuro">Plano</span></h2>
        <p class="planos-sub">Você sabe o nível. A surpresa é nossa.</p>
      </div>

      <div class="planos-grid" v-if="planos.length">
        <div
          v-for="plano in planos"
          :key="plano.id"
          class="plano-card"
          :class="{ selecionado: planoSelecionado === plano.id, 'plano-destaque': plano.recorrencia === 'semestral' }"
          @click="planoSelecionado = plano.id"
        >
          <div class="plano-badge-popular" v-if="plano.recorrencia === 'semestral'">Mais Popular</div>

          <div class="plano-header-row">
            <h3 class="plano-nome">{{ nomePlano(plano.recorrencia) }}</h3>
            <span class="economia-tag" v-if="plano.desconto_pct > 0">-{{ plano.desconto_pct }}%</span>
          </div>

          <div class="plano-preco">
            <span class="valor">{{ formatarMoeda(plano.preco_total) }}</span>
            <span class="periodo">/{{ periodoLabel(plano.recorrencia) }}</span>
          </div>

          <div class="economia-info" v-if="plano.economia > 0">
            Economize {{ formatarMoeda(plano.economia) }}
          </div>

          <p class="plano-copy">{{ copyPlano(plano.recorrencia) }}</p>

          <ul class="plano-lista">
            <li v-for="item in listaPlano(plano)" :key="item">{{ item }}</li>
          </ul>

          <div class="plano-acoes">
            <button class="btn-carrinho" @click.stop="irParaCarrinho(plano)">
              <i class="fas fa-shopping-cart"></i> Carrinho
            </button>
            <button class="btn-assinar" @click.stop="irParaCheckout(plano)">Assinar</button>
          </div>
        </div>
      </div>

      <div v-else class="planos-loading">
        <p>Carregando planos...</p>
      </div>

      <p class="planos-nota">
        <i class="fas fa-lock"></i> Pagamento seguro · Cancele quando quiser · Sem taxas ocultas
      </p>
    </section>

    <!-- ENTREGAS ANTERIORES -->
    <EntregasAnteriores :entregas="entregasAnteriores" titulo="O que já entregamos" />

    <!-- BENEFÍCIOS -->
    <section class="beneficios-section">
      <div class="container">
        <div class="beneficios-grid">
          <div class="beneficio-card">
            <div class="beneficio-icone"><i class="fas fa-shipping-fast"></i></div>
            <h3>Entrega Rápida</h3>
            <p>Em todo o Brasil, com agilidade e segurança</p>
          </div>
          <div class="beneficio-card">
            <div class="beneficio-icone"><i class="fas fa-lock"></i></div>
            <h3>Compra Segura</h3>
            <p>Dados protegidos com criptografia de última geração</p>
          </div>
          <div class="beneficio-card">
            <div class="beneficio-icone"><i class="fas fa-headset"></i></div>
            <h3>Suporte Premium</h3>
            <p>Atendimento especializado para nossos membros</p>
          </div>
          <div class="beneficio-card">
            <div class="beneficio-icone"><i class="fas fa-undo"></i></div>
            <h3>Garantia Total</h3>
            <p>Satisfação garantida ou seu dinheiro de volta em 7 dias</p>
          </div>
        </div>
      </div>
    </section>

    <div id="toast-container"></div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCarrinhoStore } from '@/stores/carrinho'
import { useAuthStore } from '@/stores/auth'
import { getEntregasAnteriores } from '@/services/strapi'
import EntregasAnteriores from '@/components/EntregasAnteriores.vue'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()
const carrinhoStore = useCarrinhoStore()
const authStore = useAuthStore()

const produto = reactive({ id: null, nome: '', descricao: '', ativo: true })
const planos = ref([])
const strapiImagem = ref('')
const planoSelecionado = ref(null)
const entregasAnteriores = ref([])
const carregando = ref(false)

const planoMensal = computed(() => planos.value.find(p => p.recorrencia === 'mensal'))

const formatarMoeda = (valor) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(valor || 0)

const nomePlano = (rec) => ({ mensal: 'Mensal', semestral: 'Semestral', anual: 'Anual' }[rec] || rec)
const periodoLabel = (rec) => ({ mensal: 'mês', semestral: 'semestre', anual: 'ano' }[rec] || rec)

const copyPlano = (rec) => ({
  mensal: 'Flexibilidade total. Sua entrada para um mundo de rótulos que você não encontra em nenhuma prateleira.',
  semestral: 'Rótulos selecionados de qualidade elevada. Experiência completa, entregue todo mês.',
  anual: 'Para quem entende que algumas garrafas não têm preço. Têm acesso.',
}[rec] || '')

const listaPlano = (plano) => ({
  mensal:    ['Renovação mensal', 'Sem compromisso', 'Cancele quando quiser'],
  semestral: ['5% de desconto', '6 meses de acesso', 'Melhor custo-benefício'],
  anual:     ['10% de desconto', '12 meses de acesso', 'Maior economia'],
}[plano.recorrencia] || [])

const carregarProduto = async () => {
  const id = route.params.id
  if (!id) { router.push('/'); return }
  carregando.value = true
  try {
    const { data } = await api.get(`/produtos/${id}`)
    Object.assign(produto, data)
    planos.value = data.planos || []
    const semestral = planos.value.find(p => p.recorrencia === 'semestral')
    planoSelecionado.value = semestral?.id ?? planos.value[0]?.id ?? null
  } catch {
    mostrarToast('Produto não encontrado', 'error')
    router.push('/')
  } finally {
    carregando.value = false
  }
}

const carregarEntregas = async () => {
  try {
    const { data } = await getEntregasAnteriores()
    entregasAnteriores.value = data.data || []
  } catch { /* silencioso */ }
}

const scrollToPlanos = () => {
  document.getElementById('planos')?.scrollIntoView({ behavior: 'smooth' })
}

const irParaCarrinho = async (plano) => {
  if (!authStore.logado) {
    router.push('/login?redirect=/carrinho')
    return
  }
  try {
    await carrinhoStore.add(produto.id, plano.id, 1)
    mostrarToast('Adicionado ao carrinho!', 'success')
    router.push('/carrinho')
  } catch {
    mostrarToast('Erro ao adicionar ao carrinho', 'error')
  }
}

const irParaCheckout = async (plano) => {
  if (!authStore.logado) {
    const dest = `/produto/${produto.id}`
    router.push(`/login?redirect=${encodeURIComponent(dest)}`)
    return
  }
  try {
    await carrinhoStore.add(produto.id, plano.id, 1)
    const item = carrinhoStore.itens.find(
      i => i.id_plano === plano.id || (i.id_produto === produto.id && i.plano === plano.recorrencia)
    )
    if (!item) throw new Error('Item não encontrado no carrinho')
    localStorage.setItem('checkoutItems', JSON.stringify([item.id_carrinho]))
    router.push('/checkout')
  } catch {
    mostrarToast('Erro ao iniciar checkout', 'error')
  }
}

const mostrarToast = (mensagem, tipo = 'success') => {
  const container = document.getElementById('toast-container')
  if (!container) return
  const toast = document.createElement('div')
  toast.className = `toast-message toast-${tipo}`
  toast.innerHTML = `<div class="toast-content">
    <i class="fas ${tipo === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
    <span>${mensagem}</span>
    <button class="toast-close" onclick="this.parentElement.parentElement.remove()"><i class="fas fa-times"></i></button>
  </div>`
  container.appendChild(toast)
  setTimeout(() => toast.classList.add('show'), 10)
  setTimeout(() => { toast.classList.remove('show'); setTimeout(() => toast.remove(), 300) }, 5000)
}

onMounted(() => {
  document.body.classList.add('pagina-clara')
  carregarProduto()
  carregarEntregas()
})

onUnmounted(() => {
  document.body.classList.remove('pagina-clara')
})
</script>

<style scoped>
/* ── CONTAINER ─────────────────────────────────── */
.produto-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: calc(var(--espacamento-xl) + var(--espacamento-md)) var(--espacamento-md) var(--espacamento-xl);
}

/* ── HERO ───────────────────────────────────────── */
.produto-hero {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;
  margin-bottom: 5rem;
}

.produto-imagem {
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  background: #f5f4f2;
  box-shadow: 0 20px 60px rgba(0,0,0,0.08);
}
.imagem-principal {
  width: 100%; display: block; object-fit: cover;
  transition: transform 0.4s ease;
  min-height: 400px;
}
.produto-imagem:hover .imagem-principal { transform: scale(1.03); }

.badge-surpresa {
  position: absolute; top: 1.25rem; left: 1.25rem;
  background: var(--gradiente-dourado);
  color: #fff; font-weight: 700; font-size: 0.72rem;
  text-transform: uppercase; letter-spacing: 1.5px;
  padding: 0.4rem 1rem; border-radius: 100px;
}

/* Info */
.section-badge {
  display: inline-flex; align-items: center; gap: 0.4rem;
  border: 1px solid var(--cor-dourado);
  color: var(--cor-dourado-escuro);
  font-size: 0.75rem; font-weight: 600; letter-spacing: 1px;
  text-transform: uppercase;
  padding: 0.35rem 0.9rem; border-radius: 100px;
  margin-bottom: 1.25rem;
  background: rgba(201,168,76,0.06);
}

.titulo-produto {
  font-family: var(--fonte-principal);
  font-size: clamp(2.2rem, 4vw, 3.2rem);
  color: #1b1a19;
  line-height: 1.15;
  margin-bottom: 1rem;
  font-weight: 600;
}

.descricao-produto {
  font-size: 1.05rem;
  color: #555;
  margin-bottom: 2rem;
  line-height: 1.75;
}

.pills-row {
  display: flex; flex-wrap: wrap; gap: 0.5rem;
  margin-bottom: 2rem;
}
.pill {
  display: flex; align-items: center; gap: 0.4rem;
  background: #f8f7f5;
  border: 1px solid #e8e4de;
  border-radius: 100px;
  padding: 0.45rem 1rem;
  font-size: 0.82rem; color: #555;
}
.pill-dot { width: 6px; height: 6px; background: var(--cor-dourado); border-radius: 50%; flex-shrink: 0; }

.preco-bloco {
  display: flex; align-items: baseline; gap: 0.6rem;
  border: 1.5px solid #ede9e2;
  border-radius: 16px;
  padding: 1.5rem 1.75rem;
  margin-bottom: 2rem;
  background: #fdfcfa;
}
.preco-valor {
  font-family: var(--fonte-principal);
  font-size: 2.5rem; color: #1b1a19; font-weight: 700;
}
.preco-per { color: #888; font-size: 0.9rem; }

.btn-modern {
  width: 100%;
  background: #1b1a19;
  color: #fff;
  border: none;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-size: 1rem; font-weight: 600; cursor: pointer;
  transition: all 0.25s;
  letter-spacing: 0.3px;
}
.btn-modern:hover {
  background: #2d2b28;
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

/* ── DIVISOR SECTION ────────────────────────────── */
.section-divider {
  height: 1px;
  background: linear-gradient(90deg, transparent, #e8e4de, transparent);
  margin: 0 calc(-1 * var(--espacamento-md));
}

/* ── PLANOS ─────────────────────────────────────── */
.planos-section {
  background: #f8f7f5;
  margin: 0 calc(-1 * var(--espacamento-md));
  padding: 5rem var(--espacamento-md);
}

.planos-header { text-align: center; margin-bottom: 3.5rem; }

.section-badge-escuro {
  border-color: #9E7A2E;
  color: #9E7A2E;
  background: rgba(158,122,46,0.06);
}

.titulo-claro {
  color: #1b1a19 !important;
  font-size: clamp(2rem, 4vw, 2.8rem);
}
.dourado-escuro { color: var(--cor-dourado-escuro); }

.planos-sub {
  color: #777;
  font-size: 1rem;
  font-style: italic;
}

.planos-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  max-width: 1000px;
  margin: 0 auto;
  align-items: start;
}
.planos-loading { text-align: center; color: #888; padding: 3rem; }

.plano-card {
  background: #fff;
  border: 1.5px solid #e8e4de;
  border-radius: 20px;
  padding: 2rem;
  position: relative; cursor: pointer;
  transition: all 0.25s ease;
}
.plano-card:hover, .plano-card.selecionado {
  transform: translateY(-4px);
  box-shadow: 0 16px 40px rgba(0,0,0,0.08);
  border-color: rgba(201,168,76,0.4);
}

/* Card destaque — único que é escuro, para contraste premium */
.plano-destaque {
  background: #1b1a19;
  border-color: rgba(201,168,76,0.3);
  transform: translateY(-10px);
  box-shadow: 0 24px 60px rgba(0,0,0,0.18);
}
.plano-destaque:hover { transform: translateY(-14px); }

.plano-badge-popular {
  position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
  background: var(--gradiente-dourado); color: #fff;
  font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px;
  padding: 0.3rem 1.1rem; border-radius: 100px; white-space: nowrap;
}

.plano-header-row {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 0.75rem;
}
.plano-nome {
  font-family: var(--fonte-principal); font-size: 1.375rem; font-weight: 600;
  color: #1b1a19;
}
.plano-destaque .plano-nome { color: #fff; }

.economia-tag {
  background: #ecfdf5; color: #16a34a;
  font-size: 0.73rem; font-weight: 700;
  padding: 0.2rem 0.65rem; border-radius: 100px;
}
.plano-destaque .economia-tag { background: rgba(74,222,128,0.12); color: #4ade80; }

.plano-preco { margin-bottom: 0.3rem; }
.plano-preco .valor {
  font-family: var(--fonte-principal); font-size: 2rem;
  color: var(--cor-dourado); font-weight: 700;
}
.plano-preco .periodo { color: #999; font-size: 0.85rem; margin-left: 0.2rem; }
.plano-destaque .plano-preco .periodo { color: #aaa; }

.economia-info { color: #16a34a; font-size: 0.8rem; margin-bottom: 1rem; font-weight: 500; }
.plano-destaque .economia-info { color: #4ade80; }

.plano-copy {
  color: #666; font-size: 0.875rem;
  font-style: italic; line-height: 1.65;
  margin-bottom: 1.25rem;
  border-top: 1px solid #f0ece6; padding-top: 1rem;
}
.plano-destaque .plano-copy { color: #aaa; border-color: rgba(255,255,255,0.08); }

.plano-lista {
  list-style: none; margin-bottom: 1.5rem;
  display: flex; flex-direction: column; gap: 0.55rem;
}
.plano-lista li {
  color: #555; font-size: 0.85rem;
  display: flex; align-items: center; gap: 0.5rem;
}
.plano-destaque .plano-lista li { color: #ccc; }
.plano-lista li::before {
  content: ''; width: 5px; height: 5px;
  background: var(--cor-dourado); border-radius: 50%; flex-shrink: 0;
}

.plano-acoes { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem; }
.btn-carrinho {
  background: transparent;
  border: 1.5px solid #e0dbd2;
  color: #555;
  padding: 0.75rem 0.5rem; border-radius: 10px;
  font-size: 0.82rem; font-weight: 600; cursor: pointer;
  display: flex; align-items: center; justify-content: center; gap: 0.4rem;
  transition: all 0.2s; white-space: nowrap;
}
.btn-carrinho:hover { background: #f5f4f2; border-color: #ccc; }
.plano-destaque .btn-carrinho { border-color: rgba(255,255,255,0.15); color: #ccc; }
.plano-destaque .btn-carrinho:hover { background: rgba(255,255,255,0.06); }

.btn-assinar {
  background: var(--gradiente-botao); color: #1b1a19;
  border: none; padding: 0.75rem 0.5rem; border-radius: 10px;
  font-size: 0.82rem; font-weight: 700; cursor: pointer;
  transition: all 0.2s; white-space: nowrap;
}
.btn-assinar:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(201,168,76,0.35); }

.planos-nota {
  text-align: center; margin-top: 2.5rem;
  color: #888; font-size: 0.82rem;
  display: flex; align-items: center; justify-content: center; gap: 0.5rem;
}
.planos-nota i { color: var(--cor-dourado-escuro); }

/* ── BENEFÍCIOS ─────────────────────────────────── */
.beneficios-section {
  padding: 5rem 0;
  background: #fff;
}
.beneficios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px,1fr));
  gap: 1.5rem;
}
.beneficio-card {
  background: #fafaf9;
  border: 1px solid #ede9e3;
  padding: 2rem 1.5rem;
  border-radius: 16px; text-align: center;
  transition: all 0.25s;
}
.beneficio-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.06);
  border-color: rgba(201,168,76,0.25);
}
.beneficio-icone {
  width: 52px; height: 52px;
  background: rgba(201,168,76,0.1);
  border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1rem; font-size: 1.2rem; color: var(--cor-dourado);
}
.beneficio-card h3 { font-size: 1rem; font-weight: 600; margin-bottom: 0.4rem; color: #1b1a19; }
.beneficio-card p { color: #777; font-size: 0.85rem; line-height: 1.55; }

/* ── TOAST ──────────────────────────────────────── */
#toast-container {
  position: fixed; top: 100px; right: 1.5rem;
  z-index: 10000; display: flex; flex-direction: column; gap: 0.5rem;
}
.toast-message {
  opacity: 0; transform: translateX(110%); padding: 0.75rem 1rem;
  border-radius: 12px; font-weight: 600;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
  transition: all 0.3s; min-width: 280px;
}
.toast-message.show { opacity: 1; transform: translateX(0); }
.toast-success { background: #ecfdf5; color: #16a34a; border: 1px solid #bbf7d0; }
.toast-error   { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.toast-content { display: flex; align-items: center; gap: 0.75rem; }
.toast-content span { flex: 1; }
.toast-close { background: none; border: none; color: inherit; cursor: pointer; opacity: 0.6; }

/* ── RESPONSIVO ─────────────────────────────────── */
@media (max-width: 1024px) {
  .produto-hero { grid-template-columns: 1fr; gap: 2.5rem; }
  .imagem-principal { min-height: 300px; }
}
@media (max-width: 768px) {
  .planos-grid { grid-template-columns: 1fr; }
  .plano-destaque { transform: none; }
  .beneficios-grid { grid-template-columns: 1fr 1fr; }
}
@media (max-width: 480px) { .beneficios-grid { grid-template-columns: 1fr; } }
</style>