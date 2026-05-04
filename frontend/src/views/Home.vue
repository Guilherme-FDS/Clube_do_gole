<template>
  <DefaultLayout>
    <!-- HERO -->
    <section class="hero" id="inicio">
      <div class="hero-content">
        <h2 class="titulo-xl fade-in">Descubra novos sabores todos os meses</h2>
        <p class="texto-corrido fade-in">Assine o Clube do Gole e receba bebidas selecionadas diretamente na sua casa.</p>
        <button class="btn-modern fade-in" @click="irParaPlanos">Conheça os Planos</button>
      </div>
    </section>

    <!-- CARROSSEL -->
    <section class="carousel-modern" @mouseenter="pausar" @mouseleave="retomar">
      <button class="seta esquerda" @click="prevSlide">❮</button>
      <div class="carousel-container">
        <div class="carousel-slide" v-for="(slide, i) in slides" :key="i" v-show="slideAtual === i">
          <a v-if="slide.link" href="#planos" @click.prevent="irParaPlanos" class="carousel-clickable">
            <img :src="slide.img" :alt="slide.alt" />
            <div class="slide-overlay"><span>Clique para ver nossos planos</span></div>
          </a>
          <img v-else :src="slide.img" :alt="slide.alt" />
        </div>
      </div>
      <button class="seta direita" @click="nextSlide">❯</button>
      <div class="indicadores">
        <span
          v-for="(_, i) in slides" :key="i"
          class="indicador"
          :class="{ active: slideAtual === i }"
          @click="slideAtual = i"
        ></span>
      </div>
    </section>

    <!-- COMO FUNCIONA -->
    <section class="como-funciona" id="comofunciona">
      <div class="container">
        <h2 class="titulo-lg fade-in">Como Funciona</h2>
        <div class="passos-container">
          <div class="passo fade-in">
            <i class="fa-solid fa-wine-bottle icone-passo"></i>
            <h3>Escolha seu plano ideal</h3>
            <p>Selecione a assinatura que mais combina com você.</p>
          </div>
          <div class="passo fade-in">
            <i class="fa-solid fa-calendar-days icone-passo"></i>
            <h3>Defina a frequência</h3>
            <p>Escolha mensal, trimestral ou semestral.</p>
          </div>
          <div class="passo fade-in">
            <i class="fa-solid fa-box icone-passo"></i>
            <h3>Nós cuidamos da seleção</h3>
            <p>Selecionamos bebidas premium para você.</p>
          </div>
          <div class="passo fade-in">
            <i class="fa-solid fa-glass-cheers icone-passo"></i>
            <h3>Receba e viva a experiência</h3>
            <p>Receba em casa e aproveite cada momento.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- NOSSOS PLANOS -->
    <section id="planos" class="nossos-planos">
      <div class="container">
        <h2 class="titulo-lg fade-in">Nossos Planos</h2>

        <h3 class="categoria-titulo fade-in">Box Gold</h3>
        <div v-if="produtosGold.length" class="produtos-container">
          <div class="produto-card fade-in" v-for="p in produtosGold" :key="p.id">
            <div class="produto-imagem">
              <img :src="p.imagem || '/img/sem_imagem.png'" :alt="p.nome" />
              <div class="badge-premium">GOLD</div>
            </div>
            <div class="produto-info">
              <h4 class="produto-titulo">{{ p.nome }}</h4>
              <p class="produto-descricao">{{ p.descricao }}</p>
              <p class="produto-preco">R$ {{ formatarPreco(p.preco) }}</p>
              <router-link :to="`/produto/${p.id}`" class="btn-produto">Ver Produto</router-link>
            </div>
          </div>
        </div>
        <p v-else class="texto-centro fade-in">Nenhum produto Gold cadastrado ainda.</p>

        <h3 class="categoria-titulo fade-in mt-5">Box Premium</h3>
        <div v-if="produtosPremium.length" class="produtos-container">
          <div class="produto-card fade-in" v-for="p in produtosPremium" :key="p.id">
            <div class="produto-imagem">
              <img :src="p.imagem || '/img/sem_imagem.png'" :alt="p.nome" />
              <div class="badge-premium">PREMIUM</div>
            </div>
            <div class="produto-info">
              <h4 class="produto-titulo">{{ p.nome }}</h4>
              <p class="produto-descricao">{{ p.descricao }}</p>
              <p class="produto-preco">R$ {{ formatarPreco(p.preco) }}</p>
              <router-link :to="`/produto/${p.id}`" class="btn-produto">Ver Produto</router-link>
            </div>
          </div>
        </div>
        <p v-else class="texto-centro fade-in">Nenhum produto Premium cadastrado ainda.</p>
      </div>
    </section>

    <!-- SOBRE -->
    <section id="sobre" class="sobre">
      <div class="container">
        <h2 class="titulo-lg fade-in">Sobre o Clube do Gole</h2>
        <div class="sobre-blocos">
          <div class="sobre-bloco fade-in">
            <h3>Experiência Única</h3>
            <p>No <span>Clube do Gole</span>, transformamos a experiência de apreciar bebidas em momentos únicos.</p>
          </div>
          <div class="sobre-bloco fade-in">
            <h3>Seleção Premium</h3>
            <p>Selecionamos cuidadosamente cada rótulo para que você receba em casa produtos de alta qualidade.</p>
          </div>
          <div class="sobre-bloco fade-in">
            <h3>Descubra Novos Sabores</h3>
            <p>Explore novos sabores e viva experiências memoráveis a cada gole.</p>
          </div>
        </div>
        <p class="sobre-cta fade-in">🍻 Junte-se ao clube e descubra um mundo de sabores!</p>
      </div>
    </section>

    <!-- CONTATO -->
    <section id="contato" class="contato">
      <div class="container">
        <h2 class="titulo-lg fade-in">Fale Conosco</h2>
        <p class="texto-corrido fade-in">Queremos ouvir você! Entre em contato pelo e-mail ou pelas nossas redes sociais...</p>
        <div class="contato-info fade-in">
          <div class="contato-item-email">
            <i class="fas fa-envelope"></i>
            <div><strong>Email:</strong> <a href="mailto:contato@clubedogole.com.br">contato@clubedogole.com.br</a></div>
          </div>
          <div class="contato-item">
            <i class="fas fa-phone"></i>
            <div><strong>WhatsApp:</strong> <span>(41) 99999-9999</span></div>
          </div>
          <div class="contato-item">
            <i class="fas fa-map-marker-alt"></i>
            <div><strong>Endereço:</strong> <span>Maringá, Paraná - Brasil</span></div>
          </div>
          <div class="contato-item-horario">
            <i class="fas fa-clock"></i>
            <div>
              <strong>Horário:</strong><br />
              <span>Seg a Sex: 9h às 18h</span><br />
              <span>Sáb: 9h às 13h</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import { gold, premium } from '@/services/produtos'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const produtosGold    = ref([])
const produtosPremium = ref([])
const slideAtual      = ref(0)
let intervalo = null

const slides = [
  { img: '/img/carrossel1.png', alt: 'Imagem 1', link: false },
  { img: '/img/carrossel2.png', alt: 'Imagem 2', link: false },
  { img: '/img/carrossel3.png', alt: 'Imagem 3', link: true  },
  { img: '/img/carrossel4.png', alt: 'Imagem 4', link: true  },
]

function nextSlide() { slideAtual.value = (slideAtual.value + 1) % slides.length }
function prevSlide() { slideAtual.value = (slideAtual.value - 1 + slides.length) % slides.length }
function pausar()   { clearInterval(intervalo) }
function retomar()  { intervalo = setInterval(nextSlide, 5000) }
function irParaPlanos() { document.getElementById('planos')?.scrollIntoView({ behavior: 'smooth' }) }
function formatarPreco(v) { return parseFloat(v).toFixed(2).replace('.', ',') }

function initFadeIn() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible') })
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' })
  document.querySelectorAll('.fade-in').forEach(el => observer.observe(el))
}

onMounted(async () => {
  try {
    const [g, p] = await Promise.all([gold(), premium()])
    produtosGold.value    = g.data
    produtosPremium.value = p.data
  } catch (e) {
    console.error('Erro ao carregar produtos:', e)
  }
  intervalo = setInterval(nextSlide, 5000)
  await nextTick()
  initFadeIn()
})

onUnmounted(() => clearInterval(intervalo))
</script>

<style scoped>
/* ===== VARIÁVEIS ===== */
:root {
  --cor-fundo: #000000;
  --cor-fundo-secundario: #0F0F0F;
  --cor-dourado: #FFD700;
  --cor-dourado-suave: #F4D03F;
  --cor-dourado-escuro: #b58500;
  --cor-roxo-principal: #8A2BE2;
  --cor-roxo-escuro: #4B0082;
  --cor-roxo-bem-claro: #f6bffc;
  --cor-texto: #FFFFFF;
  --cor-texto-secundario: #CCCCCC;
  --cor-branco: #ffffff;
  --gradiente-hero: linear-gradient(135deg, #000000 0%, #2D004D 100%);
  --gradiente-botao: linear-gradient(45deg, var(--cor-roxo-principal), var(--cor-dourado));
  --gradiente-botao-dourado-claro-escuro: linear-gradient(45deg, var(--cor-dourado-suave), var(--cor-dourado-escuro));
  --sombra-suave: 0 4px 6px rgba(0,0,0,0.1);
  --sombra-destaque: 0 10px 25px rgba(139,0,255,0.3);
  --sombra-card: 0 8px 30px rgba(0,0,0,0.5);
  --espacamento-xs: 0.5rem;
  --espacamento-sm: 1rem;
  --espacamento-md: 2rem;
  --espacamento-lg: 4rem;
  --espacamento-xl: 6rem;
  --borda-radius-sm: 8px;
  --borda-radius-md: 12px;
  --borda-radius-lg: 20px;
  --fonte-principal: 'Inter', sans-serif;
  --fonte-secundaria: 'Playfair Display', serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--espacamento-sm);
}

/* ===== TIPOGRAFIA ===== */
.titulo-xl {
  font-family: var(--fonte-secundaria);
  font-size: clamp(2.5rem, 5vw, 4rem);
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: var(--espacamento-sm);
}
.titulo-lg {
  font-family: var(--fonte-secundaria);
  font-size: clamp(2rem, 4vw, 3rem);
  font-weight: 600;
  line-height: 1.2;
  margin-bottom: var(--espacamento-md);
  text-align: center;
  color: var(--cor-dourado);
}
.texto-corrido {
  font-size: 1.125rem;
  line-height: 1.6;
  color: var(--cor-texto-secundario);
}
.texto-centro { text-align: center; color: var(--cor-texto-secundario); }
.mt-5 { margin-top: var(--espacamento-xl); }

/* ===== BOTÕES ===== */
.btn-modern {
  background: var(--gradiente-botao-dourado-claro-escuro);
  color: #000;
  border: none;
  padding: 1rem 2rem;
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  font-size: 1.1rem;
}
.btn-modern::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}
.btn-modern:hover::before { left: 100%; }
.btn-modern:hover { transform: translateY(-3px); box-shadow: var(--sombra-destaque); }

/* ===== HERO ===== */
.hero {
  position: relative;
  min-height: 80vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: var(--espacamento-xl) var(--espacamento-md);
  background: var(--gradiente-hero);
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 80%, rgba(120,0,255,0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255,215,0,0.1) 0%, transparent 50%);
  z-index: 1;
}
.hero-content { position: relative; z-index: 2; max-width: 800px; }

/* ===== CARROSSEL ===== */
.carousel-modern {
  position: relative;
  border-radius: var(--borda-radius-lg);
  overflow: hidden;
  box-shadow: var(--sombra-destaque);
  margin: var(--espacamento-lg) auto;
  max-width: 1200px;
}
.carousel-container { display: flex; transition: transform 0.5s ease-in-out; }
.carousel-slide {
  position: relative;
  min-width: 100%;
  height: 0;
  padding-bottom: 55.81%;
}
.carousel-slide::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 50%;
  background: linear-gradient(transparent, rgba(0,0,0,0.7));
  z-index: 2;
}
.carousel-slide img {
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 100%;
  object-fit: cover;
}
.carousel-clickable { display: block; width: 100%; height: 100%; position: absolute; inset: 0; z-index: 3; }
.slide-overlay {
  position: absolute;
  bottom: 2rem; left: 50%;
  transform: translateX(-50%);
  background: rgba(0,0,0,0.7);
  color: var(--cor-dourado);
  padding: 0.5rem 1.5rem;
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  z-index: 4;
}
.seta {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0,0,0,0.7);
  color: var(--cor-dourado);
  border: none;
  font-size: 2rem;
  cursor: pointer;
  padding: 1rem;
  z-index: 10;
  transition: all 0.3s ease;
  border-radius: var(--borda-radius-sm);
}
.seta:hover { background: rgba(0,0,0,0.9); transform: translateY(-50%) scale(1.1); }
.seta.esquerda { left: 1rem; }
.seta.direita  { right: 1rem; }
.indicadores {
  position: absolute;
  bottom: 1rem; left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;
  z-index: 10;
}
.indicador {
  width: 12px; height: 12px;
  border-radius: 50%;
  background: rgba(255,255,255,0.5);
  cursor: pointer;
  transition: all 0.3s ease;
}
.indicador.active { background: var(--cor-dourado); transform: scale(1.2); }

/* ===== COMO FUNCIONA ===== */
.como-funciona { padding: var(--espacamento-xl) 0; background: #0F0F0F; }
.passos-container {
  display: flex;
  flex-wrap: wrap;
  gap: var(--espacamento-lg);
  counter-reset: step-counter;
  justify-content: center;
}
.passo {
  text-align: center;
  position: relative;
  padding: var(--espacamento-md);
  background: #000;
  border-radius: var(--borda-radius-md);
  transition: all 0.3s ease;
  width: 260px;
}
.passo::before {
  counter-increment: step-counter;
  content: counter(step-counter);
  position: absolute;
  top: -1rem; left: 50%;
  transform: translateX(-50%);
  width: 3rem; height: 3rem;
  background: var(--gradiente-botao);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #000;
  font-size: 1.25rem;
  z-index: 2;
}
.passo:hover { transform: translateY(-5px); box-shadow: var(--sombra-destaque); }
.icone-passo { font-size: 3rem; color: var(--cor-dourado); margin-bottom: var(--espacamento-sm); display: block; }
.passo h3 { color: #fff; margin-bottom: var(--espacamento-sm); font-size: 1.25rem; }
.passo p  { color: var(--cor-texto-secundario); }

/* ===== PLANOS / PRODUTOS ===== */
.nossos-planos { padding: var(--espacamento-xl) 0; background: #000; }
.categoria-titulo {
  font-family: var(--fonte-secundaria);
  font-size: 2rem;
  color: var(--cor-roxo-principal);
  margin: var(--espacamento-lg) 0 var(--espacamento-md);
  text-align: center;
}
.produtos-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--espacamento-md);
  margin: var(--espacamento-md) 0;
}
.produto-card {
  background: #0F0F0F;
  border-radius: var(--borda-radius-md);
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid rgba(255,215,0,0.1);
  position: relative;
}
.produto-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--gradiente-botao);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}
.produto-card:hover::before { transform: scaleX(1); }
.produto-card:hover { transform: translateY(-8px); box-shadow: var(--sombra-destaque); border-color: var(--cor-dourado); }
.produto-imagem { position: relative; overflow: hidden; height: 250px; }
.produto-imagem img { width: 100%; height: 100%; object-fit: cover; transition: transform 0.5s ease; }
.produto-card:hover .produto-imagem img { transform: scale(1.05); }
.badge-premium {
  position: absolute;
  top: 1rem; right: 1rem;
  background: var(--gradiente-botao);
  color: #000;
  padding: 0.25rem 0.75rem;
  border-radius: var(--borda-radius-lg);
  font-size: 0.75rem;
  font-weight: 600;
  z-index: 2;
}
.produto-info { padding: var(--espacamento-md); text-align: center; }
.produto-titulo { color: var(--cor-dourado); font-size: 1.25rem; margin-bottom: var(--espacamento-xs); font-weight: 600; }
.produto-descricao { color: var(--cor-texto-secundario); margin-bottom: var(--espacamento-sm); line-height: 1.5; }
.produto-preco { color: var(--cor-dourado); font-size: 1.5rem; font-weight: bold; margin-bottom: var(--espacamento-sm); }
.btn-produto {
  background: var(--cor-dourado-suave);
  color: #000;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-block;
}
.btn-produto:hover { transform: translateY(-2px); box-shadow: var(--sombra-destaque); }

/* ===== SOBRE ===== */
.sobre { padding: var(--espacamento-xl) 0; background: #0F0F0F; }
.sobre-blocos {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: var(--espacamento-md);
  margin-bottom: var(--espacamento-lg);
}
.sobre-bloco {
  background: #000;
  padding: var(--espacamento-md);
  border-radius: var(--borda-radius-md);
  text-align: center;
  transition: all 0.3s ease;
  border: 1px solid rgba(255,215,0,0.2);
}
.sobre-bloco:hover { transform: translateY(-5px); box-shadow: var(--sombra-destaque); border-color: var(--cor-dourado); }
.sobre-bloco h3 { color: var(--cor-roxo-principal); margin-bottom: var(--espacamento-sm); font-size: 1.25rem; }
.sobre-bloco p  { color: var(--cor-texto-secundario); line-height: 1.6; }
.sobre-bloco p span { color: var(--cor-dourado); font-weight: 600; }
.sobre-cta { text-align: center; font-style: italic; color: var(--cor-dourado); font-size: 1.25rem; margin-top: var(--espacamento-lg); }

/* ===== CONTATO ===== */
.contato { padding: var(--espacamento-xl) 0; background: #000; }
.contato-info { display: flex; flex-wrap: wrap; gap: var(--espacamento-md); margin: var(--espacamento-lg) 0; }
.contato-item {
  display: flex; align-items: center; gap: var(--espacamento-sm);
  padding: var(--espacamento-md);
  background: #0F0F0F;
  border-radius: var(--borda-radius-md);
  width: 350px;
  color: var(--cor-texto-secundario);
}
.contato-item-email {
  display: flex; align-items: center; gap: var(--espacamento-sm);
  padding: var(--espacamento-md);
  background: #0F0F0F;
  border-radius: var(--borda-radius-md);
  width: 500px;
  color: #fff;
}
.contato-item-horario {
  display: flex; align-items: center; gap: var(--espacamento-sm);
  padding: var(--espacamento-md);
  background: #0F0F0F;
  border-radius: var(--borda-radius-md);
  width: 370px;
  color: var(--cor-texto-secundario);
}
.contato-item i,
.contato-item-email i,
.contato-item-horario i { color: var(--cor-dourado); font-size: 1rem; }
.contato-item strong,
.contato-item-email strong,
.contato-item-horario strong { color: #fff; display: block; margin-bottom: 0.25rem; }
.contato-item-email a { text-decoration: none; color: var(--cor-texto-secundario); }
.contato-item a, .contato-item span { color: var(--cor-texto-secundario); text-decoration: none; }

/* ===== ANIMAÇÕES FADE-IN ===== */
.fade-in { opacity: 0; transform: translateY(30px); transition: all 0.6s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }

/* ===== RESPONSIVIDADE ===== */
@media (max-width: 768px) {
  .hero { padding: var(--espacamento-lg) var(--espacamento-sm); min-height: 80vh; }
  .passos-container { flex-direction: column; align-items: center; }
  .sobre-blocos { grid-template-columns: 1fr; }
  .contato-info { flex-direction: column; }
  .contato-item, .contato-item-email, .contato-item-horario { width: 100%; }
}
@media (max-width: 480px) {
  .produtos-container { grid-template-columns: 1fr; }
  .carousel-modern { margin: var(--espacamento-md) auto; }
  .seta { padding: 0.5rem; font-size: 1.5rem; }
}
</style>