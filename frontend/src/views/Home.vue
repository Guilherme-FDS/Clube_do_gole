<template>
  <div class="home">

    <!-- HERO (escuro) -->
    <section class="hero" id="inicio">
      <div class="hero-content">
        <div class="hero-badge">Curadoria Exclusiva de Destilados</div>
        <h2 class="titulo-xl fade-in" :class="{ visible: fadeInVisible }">
          Descubra novos sabores<br><span>todos os meses</span>
        </h2>
        <p class="texto-corrido fade-in" :class="{ visible: fadeInVisible }">
          Assine o Clube do Gole e receba <strong>bebidas selecionadas</strong> de whisky,
          gin, vodka e licores diretamente na sua casa.
        </p>
        <div class="hero-botoes fade-in" :class="{ visible: fadeInVisible }">
          <button class="btn-modern" @click="scrollToSection('planos')">Conheça os Planos</button>
          <button class="btn-outline" @click="scrollToSection('como-funciona')">Como Funciona</button>
        </div>
        <div class="hero-stats fade-in" :class="{ visible: fadeInVisible }">
          <div class="stat-item">
            <span class="stat-numero">+500</span>
            <span class="stat-label">Rótulos Exclusivos</span>
          </div>
          <div class="stat-item">
            <span class="stat-numero">+3mil</span>
            <span class="stat-label">Membros Ativos</span>
          </div>
          <div class="stat-item">
            <span class="stat-numero">100%</span>
            <span class="stat-label">Premium Quality</span>
          </div>
        </div>
      </div>
    </section>

    <!-- CARROSSEL (sem seção alternada, neutro) -->
    <section class="carousel-modern">
      <button class="seta esquerda" @click="prevSlide">❮</button>
      <div class="carousel-container" ref="carouselContainer">
        <div class="carousel-slide" v-for="(slide, index) in slides" :key="index">
          <a v-if="slide.link" href="#" @click.prevent="scrollToSection('planos')"
            class="scroll-link carousel-clickable">
            <img :src="slide.image" :alt="slide.alt">
            <div class="slide-overlay"><span>{{ slide.overlayText }}</span></div>
          </a>
          <img v-else :src="slide.image" :alt="slide.alt">
        </div>
      </div>
      <button class="seta direita" @click="nextSlide">❯</button>
      <div class="indicadores">
        <div v-for="(slide, index) in slides" :key="index" class="indicador" :class="{ active: currentIndex === index }"
          @click="goToSlide(index)"></div>
      </div>
    </section>

    <!-- COMO FUNCIONA (claro) -->
    <section class="como-funciona" id="como-funciona">
      <div class="container" style="text-align:center;">
        <span class="section-badge">Processo Simples</span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
          Como <span class="dourado">Funciona</span>
        </h2>
        <p class="como-funciona-intro fade-in" :class="{ visible: fadeInVisible }">
          Em apenas 4 passos, você começa sua jornada de descobertas no mundo dos destilados premium
        </p>
        <div class="passos-container">
          <div v-for="(passo, index) in passos" :key="index" class="passo fade-in" :class="{ visible: fadeInVisible }"
            :style="{ transitionDelay: `${index * 100}ms` }">
            <i :class="passo.icone + ' icone-passo'"></i>
            <h3>{{ passo.titulo }}</h3>
            <p>{{ passo.descricao }}</p>
          </div>
        </div>
        <div class="como-funciona-cta fade-in" :class="{ visible: fadeInVisible }">
          <button class="btn-modern" style="background:var(--gradiente-botao);color:var(--cor-fundo);"
            @click="scrollToSection('planos')">
            Começar Agora
          </button>
        </div>
      </div>
    </section>

    <!-- NOSSOS PLANOS (escuro) -->
    <section id="planos" class="nossos-planos">
      <div class="container" style="text-align:center;">
        <span class="section-badge" style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">Nossas
          Assinaturas</span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
          Nossos <span class="dourado">Planos</span>
        </h2>

        <h3 class="categoria-titulo gold fade-in" :class="{ visible: fadeInVisible }">Box Gold</h3>
        <div v-if="produtosGold.length" class="produtos-container">
          <div v-for="produto in produtosGold" :key="produto.id" class="produto-card fade-in"
            :class="{ visible: fadeInVisible }">
            <div class="produto-imagem">
              <img :src="produto.imagem || '/img/sem_imagem.png'" :alt="produto.nome">
              <div class="badge-premium">GOLD</div>
            </div>
            <div class="produto-info">
              <h4 class="produto-titulo">{{ produto.nome }}</h4>
              <p class="produto-descricao">{{ produto.descricao }}</p>
              <p class="preco">{{ formatPrice(produto.preco) }}</p>
              <router-link :to="`/produto/${produto.id}`" class="btn-produto">Ver Produto</router-link>
            </div>
          </div>
        </div>
        <p v-else class="texto-centro fade-in" :class="{ visible: fadeInVisible }">Nenhum produto Gold cadastrado ainda.
        </p>

        <h3 class="categoria-titulo fade-in mt-5" :class="{ visible: fadeInVisible }">Box Premium</h3>
        <div v-if="produtosPremium.length" class="produtos-container">
          <div v-for="produto in produtosPremium" :key="produto.id" class="produto-card fade-in"
            :class="{ visible: fadeInVisible }">
            <div class="produto-imagem">
              <img :src="produto.imagem || '/img/sem_imagem.png'" :alt="produto.nome">
              <div class="badge-premium">PREMIUM</div>
            </div>
            <div class="produto-info">
              <h4 class="produto-titulo">{{ produto.nome }}</h4>
              <p class="produto-descricao">{{ produto.descricao }}</p>
              <p class="preco">{{ formatPrice(produto.preco) }}</p>
              <router-link :to="`/produto/${produto.id}`" class="btn-produto">Ver Produto</router-link>
            </div>
          </div>
        </div>
        <p v-else class="texto-centro fade-in" :class="{ visible: fadeInVisible }">Nenhum produto Premium cadastrado
          ainda.</p>
      </div>
    </section>

    <!-- SOBRE (claro) -->
    <section class="sobre" id="sobre">
      <div class="container" style="text-align:center;">
        <span class="section-badge">Sobre Nós</span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
          Clube do <span class="dourado" style="color:var(--cor-dourado-escuro);">Gole</span>
        </h2>
        <p class="sobre-intro fade-in" :class="{ visible: fadeInVisible }">
          Somos apaixonados por destilados e acreditamos que cada bebida tem uma história para
          contar. O Clube do Gole nasceu para democratizar o acesso a <strong>bebidas premium</strong> e criar
          uma comunidade de <strong>apreciadores</strong> que buscam qualidade e novas experiências.
        </p>
        <div class="sobre-blocos">
          <div v-for="(bloco, index) in sobreBlocos" :key="index" class="sobre-bloco fade-in"
            :class="{ visible: fadeInVisible }" :style="{ transitionDelay: `${index * 100}ms` }">
            <div class="sobre-bloco-icone">
              <i :class="bloco.icone"></i>
            </div>
            <h3>{{ bloco.titulo }}</h3>
            <p v-html="bloco.descricao"></p>
          </div>
        </div>
      </div>
    </section>

    <!-- CONTATO / CTA WHATSAPP (escuro) -->
<section id="contato" class="contato">
  <div class="container">
    <div class="contato-cta-box fade-in" :class="{ visible: fadeInVisible }">
      <span class="section-badge" style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">Fale Conosco</span>
      <h2>Entre em <span style="color:var(--cor-dourado);">Contato</span></h2>
      <p>Estamos aqui para ajudar. Entre em contato conosco através dos canais abaixo</p>
      <a href="https://api.whatsapp.com/send/?phone=5541999999999" target="_blank" class="btn-contato" style="display:inline-flex;margin:0 auto;">
        <i class="fa-brands fa-whatsapp"></i> Falar no WhatsApp
      </a>
    </div>

    <div class="contato-cards fade-in" :class="{ visible: fadeInVisible }">
      <div class="contato-card">
        <div class="contato-card-icone"><i class="fas fa-envelope"></i></div>
        <h4>E-mail</h4>
        <a href="mailto:contato@clubedogole.com.br">contato@clubedogole.com.br</a>
      </div>
      <div class="contato-card">
        <div class="contato-card-icone"><i class="fas fa-phone"></i></div>
        <h4>WhatsApp</h4>
        <span>(44) 99999-9999</span>
      </div>
      <div class="contato-card">
        <div class="contato-card-icone"><i class="fas fa-map-marker-alt"></i></div>
        <h4>Endereço</h4>
        <span>Maringá, Paraná - Brasil</span>
      </div>
    </div>
  </div>
</section>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useProdutosStore } from '@/stores/produtos'

// Store
const produtosStore = useProdutosStore()

// Estados locais
const fadeInVisible = ref(false)
const carouselContainer = ref(null)
const currentIndex = ref(0)
let carouselInterval = null
let isCarouselAnimating = false

// Dados do carrossel
const slides = ref([
  { image: '/img/carrossel1.png', alt: 'Imagem 1', link: null },
  { image: '/img/carrossel2.png', alt: 'Imagem 2', link: null },
  { image: '/img/carrossel3.png', alt: 'Imagem 3', link: '#planos', overlayText: 'Clique para ver nossos planos' },
  { image: '/img/carrossel4.png', alt: 'Imagem 4', link: '#planos', overlayText: 'Clique para ver nossos planos' }
])

// Dados estáticos
const passos = [
  { icone: 'fa-solid fa-wine-bottle', titulo: 'Escolha seu plano ideal', descricao: 'Selecione a assinatura que mais combina com você.' },
  { icone: 'fa-solid fa-calendar-days', titulo: 'Defina a frequência', descricao: 'Escolha mensal, trimestral ou semestral.' },
  { icone: 'fa-solid fa-box', titulo: 'Nós cuidamos da seleção', descricao: 'Selecionamos bebidas premium para você.' },
  { icone: 'fa-solid fa-glass-cheers', titulo: 'Receba e viva a experiência', descricao: 'Receba em casa e aproveite cada momento.' }
]

const sobreBlocos = [
  { icone: 'mdi mdi-medal-outline', titulo: 'Experiência Única', descricao: 'No <span>Clube do Gole</span>, transformamos a experiência de apreciar bebidas em momentos únicos.' },
  { icone: 'mdi mdi-magnify', titulo: 'Seleção Premium', descricao: 'Selecionamos cuidadosamente cada rótulo para que você receba em casa produtos de alta qualidade.' },
  { icone: 'mdi mdi-glass-cocktail', titulo: 'Descubra Novos Sabores', descricao: 'Explore novos sabores e viva experiências memoráveis a cada gole.' }
]

// Computed
const produtosGold = computed(() => produtosStore.produtosGold)
const produtosPremium = computed(() => produtosStore.produtosPremium)

// Métodos
const handleScroll = () => {
  const fadeElements = document.querySelectorAll('.fade-in')
  fadeElements.forEach(el => {
    const rect = el.getBoundingClientRect()
    if (rect.top <= window.innerHeight - 100) {
      el.classList.add('visible')
    }
  })
}

const scrollToSection = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    const headerHeight = document.querySelector('.main-header')?.offsetHeight || 80
    window.scrollTo({ top: element.offsetTop - headerHeight, behavior: 'smooth' })
  }
}

const updateCarousel = () => {
  if (isCarouselAnimating || !carouselContainer.value) return
  isCarouselAnimating = true
  carouselContainer.value.style.transform = `translateX(-${currentIndex.value * 100}%)`
  setTimeout(() => { isCarouselAnimating = false }, 500)
}

const nextSlide = () => {
  if (isCarouselAnimating) return
  currentIndex.value = (currentIndex.value + 1) % slides.value.length
  updateCarousel()
  resetCarouselInterval()
}

const prevSlide = () => {
  if (isCarouselAnimating) return
  currentIndex.value = (currentIndex.value - 1 + slides.value.length) % slides.value.length
  updateCarousel()
  resetCarouselInterval()
}

const goToSlide = (index) => {
  if (index !== currentIndex.value && !isCarouselAnimating) {
    currentIndex.value = index
    updateCarousel()
    resetCarouselInterval()
  }
}

const startCarouselAutoPlay = () => {
  carouselInterval = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % slides.value.length
    updateCarousel()
  }, 5000)
}

const stopCarouselAutoPlay = () => {
  if (carouselInterval) {
    clearInterval(carouselInterval)
    carouselInterval = null
  }
}

const resetCarouselInterval = () => {
  stopCarouselAutoPlay()
  startCarouselAutoPlay()
}

const formatPrice = (price) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(parseFloat(price))
}

// Lifecycle
onMounted(async () => {
  window.addEventListener('scroll', handleScroll)

  // Carregar produtos
  await produtosStore.fetchProdutos()

  setTimeout(() => {
    handleScroll()
    fadeInVisible.value = true
  }, 100)

  startCarouselAutoPlay()

  const carouselElement = carouselContainer.value
  if (carouselElement) {
    carouselElement.addEventListener('mouseenter', stopCarouselAutoPlay)
    carouselElement.addEventListener('mouseleave', startCarouselAutoPlay)
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  stopCarouselAutoPlay()

  const carouselElement = carouselContainer.value
  if (carouselElement) {
    carouselElement.removeEventListener('mouseenter', stopCarouselAutoPlay)
    carouselElement.removeEventListener('mouseleave', startCarouselAutoPlay)
  }
})
</script>