<template>
  <div class="home">

    <!-- HERO -->
    <section class="hero" id="inicio">
      <div class="hero-content">
        <div class="hero-badge">Curadoria Exclusiva de Destilados</div>
        <h2 class="titulo-xl fade-in" :class="{ visible: fadeInVisible }" v-html="heroTitulo"></h2>
        <p class="texto-corrido fade-in" :class="{ visible: fadeInVisible }" v-html="heroSubtitulo"></p>
        <div class="hero-botoes fade-in" :class="{ visible: fadeInVisible }">
          <button class="btn-modern" @click="scrollToSection('planos')">{{ heroCta }}</button>
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

    <!-- CARROSSEL -->
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
        <div v-for="(slide, index) in slides" :key="index" class="indicador"
          :class="{ active: currentIndex === index }" @click="goToSlide(index)"></div>
      </div>
    </section>

    <!-- COMO FUNCIONA -->
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
          <div v-for="(passo, index) in passos" :key="index" class="passo fade-in"
            :class="{ visible: fadeInVisible }" :style="{ transitionDelay: `${index * 100}ms` }">
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

    <!-- NOSSOS PLANOS -->
    <section id="planos" class="nossos-planos">
      <div class="container" style="text-align:center;">
        <span class="section-badge"
          style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">Nossas Assinaturas</span>
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
        <p v-else class="texto-centro fade-in" :class="{ visible: fadeInVisible }">Nenhum produto Gold cadastrado ainda.</p>

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
        <p v-else class="texto-centro fade-in" :class="{ visible: fadeInVisible }">Nenhum produto Premium cadastrado ainda.</p>
      </div>
    </section>

    <!-- SOBRE -->
    <section class="sobre" id="sobre">
      <div class="container" style="text-align:center;">
        <span class="section-badge">Sobre Nós</span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
          {{ sobreTitulo }}
        </h2>
        <p class="sobre-intro fade-in" :class="{ visible: fadeInVisible }" v-html="sobreTexto"></p>
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

    <!-- DEPOIMENTOS -->
    <section class="depoimentos" id="depoimentos" v-if="depoimentos.length">
      <div class="container" style="text-align:center;">
        <span class="section-badge"
          style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">O que dizem nossos membros</span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
          Depoimentos
        </h2>
        <div class="depoimentos-container">
          <div v-for="dep in depoimentos" :key="dep.id" class="depoimento-card fade-in"
            :class="{ visible: fadeInVisible }">
            <div class="depoimento-estrelas">
              <i v-for="n in 5" :key="n" class="fas fa-star"
                :style="{ color: n <= dep.avaliacao ? 'var(--cor-dourado)' : '#444' }"></i>
            </div>
            <p class="depoimento-texto">"{{ dep.texto }}"</p>
            <div class="depoimento-autor">
              <img v-if="dep.foto?.url"
                :src="`${strapiUrl}${dep.foto.url}`"
                :alt="dep.nome" class="depoimento-foto">
              <div v-else class="depoimento-foto-placeholder">
                <i class="fas fa-user"></i>
              </div>
              <span class="depoimento-nome">{{ dep.nome }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ -->
    <section class="faq" id="faq" v-if="faqs.length">
      <div class="container" style="text-align:center;">
        <span class="section-badge">Dúvidas Frequentes</span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
          Perguntas <span class="dourado">Frequentes</span>
        </h2>
        <div class="faq-lista">
          <div v-for="(item, index) in faqs" :key="item.id" class="faq-item fade-in"
            :class="{ visible: fadeInVisible, aberto: faqAberto === index }">
            <button class="faq-pergunta" @click="faqAberto = faqAberto === index ? null : index">
              <span>{{ item.pergunta }}</span>
              <i class="fas" :class="faqAberto === index ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
            </button>
            <div class="faq-resposta" v-show="faqAberto === index">
              <p v-if="typeof item.resposta === 'string'">{{ item.resposta }}</p>
              <template v-else-if="Array.isArray(item.resposta)">
                <p v-for="(block, i) in item.resposta" :key="i">
                  {{ block.children?.map(c => c.text).join('') }}
                </p>
              </template>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CONTATO -->
    <section id="contato" class="contato">
      <div class="container">
        <div class="contato-cta-box fade-in" :class="{ visible: fadeInVisible }">
          <span class="section-badge"
            style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">Fale Conosco</span>
          <h2>Entre em <span style="color:var(--cor-dourado);">Contato</span></h2>
          <p>Estamos aqui para ajudar. Entre em contato conosco através dos canais abaixo</p>
          <a href="https://api.whatsapp.com/send/?phone=5541999999999" target="_blank" class="btn-contato"
            style="display:inline-flex;margin:0 auto;">
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
import { getBanners, getHome, getDepoimentos, getFaqs } from '@/services/strapi'

const produtosStore = useProdutosStore()
const strapiUrl = import.meta.env.VITE_STRAPI_URL || 'http://localhost:1337'

const fadeInVisible = ref(false)
const carouselContainer = ref(null)
const currentIndex = ref(0)
let carouselInterval = null
let isCarouselAnimating = false

// Strapi data
const heroTitulo = ref('Descubra novos sabores<br><span>todos os meses</span>')
const heroSubtitulo = ref('Assine o Clube do Gole e receba <strong>bebidas selecionadas</strong> de whisky, gin, vodka e licores diretamente na sua casa.')
const heroCta = ref('Conheça os Planos')
const sobreTitulo = ref('Clube do Gole')
const sobreTexto = ref('Somos apaixonados por destilados e acreditamos que cada bebida tem uma história para contar. O Clube do Gole nasceu para democratizar o acesso a <strong>bebidas premium</strong> e criar uma comunidade de <strong>apreciadores</strong> que buscam qualidade e novas experiências.')
const depoimentos = ref([])
const faqs = ref([])
const faqAberto = ref(null)

const slidesLocal = [
  { image: '/img/carrossel1.png', alt: 'Imagem 1', link: null },
  { image: '/img/carrossel2.png', alt: 'Imagem 2', link: null },
  { image: '/img/carrossel3.png', alt: 'Imagem 3', link: '#planos', overlayText: 'Clique para ver nossos planos' },
  { image: '/img/carrossel4.png', alt: 'Imagem 4', link: '#planos', overlayText: 'Clique para ver nossos planos' }
]

const slides = ref([])

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

const produtosGold = computed(() => produtosStore.produtosGold)
const produtosPremium = computed(() => produtosStore.produtosPremium)

const handleScroll = () => {
  document.querySelectorAll('.fade-in').forEach(el => {
    if (el.getBoundingClientRect().top <= window.innerHeight - 100)
      el.classList.add('visible')
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
  updateCarousel(); resetCarouselInterval()
}

const prevSlide = () => {
  if (isCarouselAnimating) return
  currentIndex.value = (currentIndex.value - 1 + slides.value.length) % slides.value.length
  updateCarousel(); resetCarouselInterval()
}

const goToSlide = (index) => {
  if (index !== currentIndex.value && !isCarouselAnimating) {
    currentIndex.value = index
    updateCarousel(); resetCarouselInterval()
  }
}

const startCarouselAutoPlay = () => {
  carouselInterval = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % slides.value.length
    updateCarousel()
  }, 5000)
}

const stopCarouselAutoPlay = () => {
  if (carouselInterval) { clearInterval(carouselInterval); carouselInterval = null }
}

const resetCarouselInterval = () => { stopCarouselAutoPlay(); startCarouselAutoPlay() }

const formatPrice = (price) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(parseFloat(price))

onMounted(async () => {
  window.addEventListener('scroll', handleScroll)

  await produtosStore.fetchProdutos()

  // Home SingleType
  try {
    const { data } = await getHome()
    const h = data?.data
    if (h) {
      if (h.hero_titulo) heroTitulo.value = h.hero_titulo
      if (h.hero_subtitulo) heroSubtitulo.value = h.hero_subtitulo
      if (h.hero_cta_texto) heroCta.value = h.hero_cta_texto
      if (h.sobre_titulo) sobreTitulo.value = h.sobre_titulo
      if (h.sobre_texto) sobreTexto.value = h.sobre_texto
    }
  } catch {}

  // Depoimentos
  try {
    const { data } = await getDepoimentos()
    depoimentos.value = data?.data || []
  } catch {}

  // FAQs
  try {
    const { data } = await getFaqs()
    faqs.value = data?.data || []
  } catch {}

  // Banners
  try {
    const { data } = await getBanners()
    const banners = data?.data || []
    slides.value = banners.length
      ? banners.map(b => ({
          image: b.imagem?.url ? `${strapiUrl}${b.imagem.url}` : '/img/sem_imagem.png',
          alt: b.titulo || '',
          link: b.link || null,
          overlayText: b.titulo || ''
        }))
      : slidesLocal
  } catch {
    slides.value = slidesLocal
  }

  setTimeout(() => { handleScroll(); fadeInVisible.value = true }, 100)

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

<style scoped>
/* DEPOIMENTOS */
.depoimentos {
  padding: var(--espacamento-xl) 0;
  background: var(--cor-secao-escura);
}
.depoimentos .titulo-lg { color: var(--cor-texto); }
.depoimentos-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--espacamento-md);
  margin-top: var(--espacamento-md);
}
.depoimento-card {
  background: var(--cor-fundo-card);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: var(--borda-radius-md);
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.25s ease;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.depoimento-card:hover {
  transform: translateY(-4px);
  border-color: rgba(201,168,76,0.2);
  box-shadow: var(--sombra-destaque);
}
.depoimento-estrelas { display: flex; justify-content: center; gap: 0.25rem; font-size: 0.9rem; }
.depoimento-texto {
  color: var(--cor-texto-secundario);
  font-size: 0.9375rem;
  line-height: 1.65;
  font-style: italic;
  flex: 1;
}
.depoimento-autor {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
}
.depoimento-foto {
  width: 44px; height: 44px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid rgba(201,168,76,0.3);
}
.depoimento-foto-placeholder {
  width: 44px; height: 44px;
  border-radius: 50%;
  background: rgba(201,168,76,0.12);
  border: 2px solid rgba(201,168,76,0.3);
  display: flex; align-items: center; justify-content: center;
  color: var(--cor-dourado);
  font-size: 1rem;
}
.depoimento-nome {
  font-family: var(--fonte-ui);
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--cor-texto);
}

/* FAQ */
.faq {
  padding: var(--espacamento-xl) 0;
  background: var(--cor-secao-clara);
  color: var(--cor-texto-claro-bg);
}
.faq .titulo-lg { color: var(--cor-texto-claro-bg); }
.faq .section-badge {
  border-color: var(--cor-dourado-escuro);
  color: var(--cor-dourado-escuro);
}
.faq-lista {
  max-width: 760px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  text-align: left;
}
.faq-item {
  border: 1px solid rgba(27,26,25,0.1);
  border-radius: var(--borda-radius-md);
  overflow: hidden;
  background: #f9f8f7;
  transition: border-color 0.2s ease;
}
.faq-item.aberto { border-color: rgba(201,168,76,0.35); }
.faq-pergunta {
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 1.125rem 1.25rem;
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  font-family: var(--fonte-ui);
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--cor-texto-claro-bg);
  transition: color 0.2s ease;
}
.faq-item.aberto .faq-pergunta { color: var(--cor-dourado-escuro); }
.faq-pergunta i { flex-shrink: 0; font-size: 0.8125rem; color: var(--cor-dourado-escuro); }
.faq-resposta {
  padding: 0 1.25rem 1.125rem;
  color: var(--cor-texto-secundario-claro-bg);
  font-size: 0.9rem;
  line-height: 1.65;
}
.faq-resposta p + p { margin-top: 0.5rem; }
</style>