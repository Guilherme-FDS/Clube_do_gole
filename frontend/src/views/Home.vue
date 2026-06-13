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
            <span class="stat-numero">2</span>
            <span class="stat-label">Rótulos por Mês</span>
          </div>
          <div class="stat-item">
            <span class="stat-numero">100%</span>
            <span class="stat-label">Curadoria Especializada</span>
          </div>
          <div class="stat-item">
            <span class="stat-numero">Surpresa</span>
            <span class="stat-label">Seleção Exclusiva</span>
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
      <div class="container">
        <div class="como-funciona-header">
          <span class="section-badge">Processo Simples</span>
          <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
            Como <span class="dourado" style="color:var(--cor-dourado-escuro);">Funciona</span>
          </h2>
        </div>
        <div class="passos-container">
          <div v-for="(passo, index) in passos" :key="index"
            class="passo fade-in" :class="{ visible: fadeInVisible }"
            :style="{ transitionDelay: `${index * 120}ms` }">
            <span class="passo-numero">{{ String(index + 1).padStart(2, '0') }}</span>
            <div class="passo-icone-wrap">
              <i :class="passo.icone"></i>
            </div>
            <h3 class="passo-titulo">{{ passo.titulo }}</h3>
            <p class="passo-descricao">{{ passo.descricao }}</p>
          </div>
        </div>
        <div class="como-funciona-cta fade-in" :class="{ visible: fadeInVisible }">
          <button class="btn-modern" @click="scrollToSection('planos')">Começar Agora</button>
        </div>
      </div>
    </section>

    <!-- ENTREGAS ANTERIORES -->
    <EntregasAnteriores
      :entregas="entregasAnteriores"
      :titulo="entregasTitulo"
      :textoMarkdown="entregasTexto"
    />

    <!-- PLANOS -->
    <section id="planos" class="nossos-planos">
      <div class="container" style="text-align:center;">
        <span class="section-badge" style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">
          Nossas Assinaturas
        </span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
          Escolha seu <span class="dourado">Plano</span>
        </h2>
        <p class="planos-subtitulo fade-in" :class="{ visible: fadeInVisible }">
          Dois rótulos premium curados por especialistas. Entregues na sua porta todo mês.
        </p>

        <div class="planos-grid">
          <!-- MENSAL -->
          <div class="plano-card fade-in" :class="{ visible: fadeInVisible }">
            <div class="plano-topo">
              <span class="plano-nome">Mensal</span>
            </div>
            <div class="plano-preco-bloco">
              <span class="plano-valor">R$ 649</span>
              <span class="plano-periodo">/mês</span>
            </div>
            <ul class="plano-lista">
              <li><i class="fas fa-check"></i> 2 rótulos curados por mês</li>
              <li><i class="fas fa-check"></i> Caixa com identidade premium</li>
              <li><i class="fas fa-check"></i> Cartão de degustação incluso</li>
              <li><i class="fas fa-check"></i> Frete incluso</li>
              <li><i class="fas fa-check"></i> Flexibilidade total</li>
            </ul>
            <button class="plano-cta" @click="irParaPlano">Começar Agora</button>
          </div>

          <!-- SEMESTRAL -->
          <div class="plano-card plano-destaque fade-in" :class="{ visible: fadeInVisible }">
            <div class="plano-badge-popular">Mais Popular</div>
            <div class="plano-topo">
              <span class="plano-nome">Semestral</span>
            </div>
            <div class="plano-preco-bloco">
              <span class="plano-valor">R$ 616</span>
              <span class="plano-periodo">/mês</span>
            </div>
            <div class="plano-economia">Economize 5% — R$ 194,70 no semestre</div>
            <ul class="plano-lista">
              <li><i class="fas fa-check"></i> 2 rótulos curados por mês</li>
              <li><i class="fas fa-check"></i> Caixa com identidade premium</li>
              <li><i class="fas fa-check"></i> Cartão de degustação incluso</li>
              <li><i class="fas fa-check"></i> Frete incluso</li>
              <li><i class="fas fa-check"></i> 5% de desconto</li>
            </ul>
            <button class="plano-cta plano-cta-destaque" @click="irParaPlano">Começar Agora</button>
          </div>

          <!-- ANUAL -->
          <div class="plano-card fade-in" :class="{ visible: fadeInVisible }">
            <div class="plano-topo">
              <span class="plano-nome">Anual</span>
              <span class="plano-badge-economia">Melhor Oferta</span>
            </div>
            <div class="plano-preco-bloco">
              <span class="plano-valor">R$ 584</span>
              <span class="plano-periodo">/mês</span>
            </div>
            <div class="plano-economia">Economize 10% — R$ 778,80 no ano</div>
            <ul class="plano-lista">
              <li><i class="fas fa-check"></i> 2 rótulos curados por mês</li>
              <li><i class="fas fa-check"></i> Caixa com identidade premium</li>
              <li><i class="fas fa-check"></i> Cartão de degustação incluso</li>
              <li><i class="fas fa-check"></i> Frete incluso</li>
              <li><i class="fas fa-check"></i> 10% de desconto</li>
            </ul>
            <button class="plano-cta" @click="irParaPlano">Começar Agora</button>
          </div>
        </div>

        <p class="planos-nota fade-in" :class="{ visible: fadeInVisible }">
          <i class="fas fa-lock"></i> Pagamento seguro · Cancele quando quiser · Sem taxas ocultas
        </p>
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
        <span class="section-badge" style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">
          O que dizem nossos membros
        </span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">Depoimentos</h2>
        <div class="depoimentos-container">
          <div v-for="dep in depoimentos" :key="dep.id" class="depoimento-card fade-in"
            :class="{ visible: fadeInVisible }">
            <div class="depoimento-estrelas">
              <i v-for="n in 5" :key="n" class="fas fa-star"
                :style="{ color: n <= dep.avaliacao ? 'var(--cor-dourado)' : '#444' }"></i>
            </div>
            <p class="depoimento-texto">"{{ dep.texto }}"</p>
            <div class="depoimento-autor">
              <img v-if="dep.foto?.url" :src="mediaUrl(dep.foto.url)"
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

    <!-- BLOG PREVIEW -->
    <section class="blog-preview" id="blog" v-if="postDestaque.length">
      <div class="container" style="text-align:center;">
        <span class="section-badge" style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">
          Do nosso blog
        </span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
          O que está por <span class="dourado">trás do copo</span>
        </h2>
        <div class="blog-preview-grid">
          <article v-for="post in postDestaque" :key="post.id"
            class="blog-preview-card fade-in" :class="{ visible: fadeInVisible }"
            @click="$router.push(`/blog/${post.slug}`)">
            <div class="blog-preview-capa">
              <img v-if="post.capa?.url" :src="mediaUrl(post.capa.url)" :alt="post.titulo">
              <div v-else class="blog-preview-placeholder">
                <i class="fas fa-wine-bottle"></i>
              </div>
            </div>
            <div class="blog-preview-info">
              <span class="blog-preview-data">{{ formatarDataPost(post.publicado_em) }}</span>
              <h3 class="blog-preview-titulo">{{ post.titulo }}</h3>
              <p class="blog-preview-resumo">{{ post.resumo }}</p>
              <span class="blog-preview-link">
                Ler artigo <i class="fas fa-arrow-right"></i>
              </span>
            </div>
          </article>
        </div>
        <div style="margin-top:var(--espacamento-md);">
          <router-link to="/blog" class="btn-outline">Ver todos os artigos</router-link>
        </div>
      </div>
    </section>

    <!-- CONTATO -->
    <section id="contato" class="contato">
      <div class="container">
        <div class="contato-cta-box fade-in" :class="{ visible: fadeInVisible }">
          <span class="section-badge" style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">
            Atendimento
          </span>
          <h2>Central de <span style="color:var(--cor-dourado);">Relacionamento</span></h2>
          <p>Nossa equipe está pronta para atender você. Envie sua mensagem e retornaremos em até 24 horas.</p>

          <form class="contato-form" @submit.prevent="enviarContato">
            <div class="contato-form-row">
              <div class="contato-form-grupo">
                <label>Nome</label>
                <input v-model="contatoForm.nome" type="text" placeholder="Seu nome completo" required />
              </div>
              <div class="contato-form-grupo">
                <label>E-mail</label>
                <input v-model="contatoForm.email" type="email" placeholder="seu@email.com" required />
              </div>
            </div>
            <div class="contato-form-grupo">
              <label>Assunto</label>
              <select v-model="contatoForm.assunto" required>
                <option value="">Selecione um assunto</option>
                <option value="assinatura">Dúvidas sobre assinatura</option>
                <option value="entrega">Entrega e rastreamento</option>
                <option value="cancelamento">Cancelamento</option>
                <option value="parceria">Parceria comercial</option>
                <option value="outro">Outro</option>
              </select>
            </div>
            <div class="contato-form-grupo">
              <label>Mensagem</label>
              <textarea v-model="contatoForm.mensagem" rows="4"
                placeholder="Descreva sua dúvida ou solicitação..." required></textarea>
            </div>
            <button type="submit" class="btn-contato-enviar" :disabled="contatoEnviando">
              <span v-if="!contatoEnviando"><i class="fas fa-paper-plane"></i> Enviar Mensagem</span>
              <span v-else><i class="fas fa-spinner fa-spin"></i> Enviando...</span>
            </button>
            <p v-if="contatoSucesso" class="contato-sucesso">
              <i class="fas fa-check-circle"></i> Mensagem enviada! Retornaremos em até 24 horas.
            </p>
          </form>
        </div>

        <div class="contato-cards fade-in" :class="{ visible: fadeInVisible }">
          <div class="contato-card">
            <div class="contato-card-icone"><i class="fas fa-envelope"></i></div>
            <h4>E-mail</h4>
            <a href="mailto:contato@clubedogole.com.br">contato@clubedogole.com.br</a>
          </div>
          <div class="contato-card">
            <div class="contato-card-icone"><i class="fas fa-clock"></i></div>
            <h4>Horário de Atendimento</h4>
            <span>Seg–Sex, das 9h às 18h</span>
          </div>
          <div class="contato-card">
            <div class="contato-card-icone"><i class="fas fa-headset"></i></div>
            <h4>Tempo de Resposta</h4>
            <span>Até 24 horas úteis</span>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { getBanners, getHome, getDepoimentos, getFaqs, getPosts, getEntregasAnteriores } from '@/services/strapi'
import EntregasAnteriores from '@/components/EntregasAnteriores.vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const router = useRouter()
const authStore = useAuthStore()

const irParaPlano = () => {
  if (authStore.logado) {
    router.push('/produto/1')
  } else {
    router.push('/login?redirect=/produto/1')
  }
}

const strapiUrl = import.meta.env.VITE_STRAPI_URL || 'http://localhost:1337'
const mediaUrl = (url) => {
  if (!url) return '/img/sem_imagem.png'
  if (url.startsWith('http')) return url
  return strapiUrl + url
}

const fadeInVisible = ref(false)
const carouselContainer = ref(null)
const currentIndex = ref(0)
let carouselInterval = null
let isCarouselAnimating = false

const heroTitulo = ref('Pertencer a um clube que poucos conhecem.')
const heroSubtitulo = ref('Curadoria global de destilados raros e cachaças premium entregues na sua porta todo mês. Você escolhe o nível de acesso. A surpresa é nossa.')
const heroCta = ref('Conheça o Clube')
const sobreTitulo = ref('Não é uma caixa de bebidas. É acesso a um mundo que a maioria não consegue entrar.')
const sobreTexto = ref('O Clube do Gole reúne destilados raros do mundo inteiro e cachaças premium brasileiras selecionadas por especialistas globais. Cada garrafa tem origem, história e raridade — você recebe o que não encontraria sozinho.')
const depoimentos = ref([])
const faqs = ref([])
const faqAberto = ref(null)
const postDestaque = ref([])
const entregasAnteriores = ref([])
const entregasTitulo = ref('')
const entregasTexto = ref('')
const contatoForm = ref({ nome: '', email: '', assunto: '', mensagem: '' })
const contatoEnviando = ref(false)
const contatoSucesso = ref(false)

const slidesLocal = [
  { image: '/img/carrossel1.webp', alt: 'Imagem 1', link: null },
  { image: '/img/carrossel2.webp', alt: 'Imagem 2', link: null },
  { image: '/img/carrossel3.webp', alt: 'Imagem 3', link: '#planos', overlayText: 'Conheça nossos planos' },
  { image: '/img/carrossel4.webp', alt: 'Imagem 4', link: '#planos', overlayText: 'Conheça nossos planos' }
]
const slides = ref([])

const passos = [
  { icone: 'fa-solid fa-wine-bottle', titulo: 'Escolha seu plano', descricao: 'Selecione a frequência que mais combina com você.' },
  { icone: 'fa-solid fa-calendar-days', titulo: 'Confirme sua assinatura', descricao: 'Pagamento seguro e recorrente, sem surpresas.' },
  { icone: 'fa-solid fa-box', titulo: 'Nós cuidamos da curadoria', descricao: 'Especialistas selecionam rótulos raros para você.' },
  { icone: 'fa-solid fa-glass-cheers', titulo: 'Receba e viva a experiência', descricao: 'Abra sua caixa e descubra o extraordinário.' }
]

const sobreBlocos = [
  { icone: 'fas fa-medal', titulo: 'Rótulos Exclusivos', descricao: 'Destilados de distribuição limitada que você não encontra nas prateleiras locais.' },
  { icone: 'fas fa-search', titulo: 'Curadoria Especializada', descricao: 'Cada garrafa é selecionada por especialistas com critérios rígidos de qualidade e raridade.' },
  { icone: 'fas fa-cocktail', titulo: 'Experiência Completa', descricao: 'Caixa premium, cartão de degustação e a história de cada rótulo entregue junto.' }
]

const formatarDataPost = (d) => {
  if (!d) return ''
  return new Date(d).toLocaleDateString('pt-BR', { day: '2-digit', month: 'short', year: 'numeric' })
}

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

const enviarContato = async () => {
  contatoEnviando.value = true
  await new Promise(r => setTimeout(r, 1200))
  contatoSucesso.value = true
  contatoEnviando.value = false
  contatoForm.value = { nome: '', email: '', assunto: '', mensagem: '' }
  setTimeout(() => { contatoSucesso.value = false }, 5000)
}

onMounted(async () => {
  window.addEventListener('scroll', handleScroll)

  try {
    const { data } = await getHome()
    const h = data?.data
    if (h) {
      if (h.hero_titulo) heroTitulo.value = h.hero_titulo
      if (h.hero_subtitulo) heroSubtitulo.value = h.hero_subtitulo
      if (h.hero_cta_texto) heroCta.value = h.hero_cta_texto
      if (h.sobre_titulo) sobreTitulo.value = h.sobre_titulo
      if (h.sobre_texto) sobreTexto.value = h.sobre_texto
      if (h.entregas_titulo) entregasTitulo.value = h.entregas_titulo
      if (h.entregas_texto) entregasTexto.value = h.entregas_texto
    }
  } catch {}

  try {
    const { data } = await getDepoimentos()
    depoimentos.value = data?.data || []
  } catch {}

  try {
    const { data } = await getFaqs()
    faqs.value = data?.data || []
  } catch {}

  try {
    const { data } = await getPosts({ 'pagination[limit]': 3 })
    postDestaque.value = data?.data || []
  } catch {}

  try {
    const { data } = await getEntregasAnteriores()
    entregasAnteriores.value = data?.data || []
  } catch {}
  
  try {
    const { data } = await getBanners()
    const banners = data?.data || []
    slides.value = banners.length
      ? banners.map(b => ({
          image: mediaUrl(b.imagem?.url),
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
/* COMO FUNCIONA — scoped override */
.como-funciona-header { text-align: center; margin-bottom: var(--espacamento-lg); }
.como-funciona-header .section-badge { border-color: var(--cor-dourado-escuro); color: var(--cor-dourado-escuro); }
.como-funciona-header .titulo-lg { color: var(--cor-texto-claro-bg); margin-bottom: 0; }

.passos-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  position: relative;
}
.passos-container::before {
  content: '';
  position: absolute;
  top: 2.5rem; left: 12%; right: 12%; height: 1px;
  background: linear-gradient(90deg, transparent, rgba(158,122,46,0.3), rgba(158,122,46,0.3), transparent);
  z-index: 0;
}
.passo {
  position: relative; z-index: 1; text-align: center; padding: 0 0.5rem;
  background: transparent; border: none; border-radius: 0;
  counter-increment: none;
}
.passo::before { display: none; }
.passo-numero {
  font-family: var(--fonte-principal); font-size: 4rem; font-weight: 700;
  color: var(--cor-dourado-escuro); opacity: 0.25; line-height: 1;
  display: block; margin-bottom: 0.5rem; letter-spacing: -2px; transition: opacity 0.3s ease;
}
.passo:hover .passo-numero { opacity: 0.55; }
.passo-icone-wrap {
  width: 52px; height: 52px;
  background: rgba(201,168,76,0.1); border: 1px solid rgba(201,168,76,0.2);
  border-radius: 50%; display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1rem; transition: all 0.3s ease;
}
.passo:hover .passo-icone-wrap {
  background: rgba(201,168,76,0.18); border-color: rgba(201,168,76,0.4); transform: scale(1.08);
}
.passo-icone-wrap i { font-size: 1.25rem; color: var(--cor-dourado-escuro); }
.passo-titulo {
  font-family: var(--fonte-principal); font-size: 1.125rem; font-weight: 600;
  color: var(--cor-texto-claro-bg); margin-bottom: 0.5rem;
}
.passo-descricao { font-size: 0.875rem; color: var(--cor-texto-secundario-claro-bg); line-height: 1.55; }
.como-funciona-cta { text-align: center; margin-top: 3rem; }

/* PLANOS — claro */
.nossos-planos .section-badge { border-color: var(--cor-dourado-escuro); color: var(--cor-dourado-escuro); }
.planos-subtitulo { color: var(--cor-texto-secundario-claro-bg); font-size: 1rem; max-width: 520px; margin: -1rem auto 3rem; }
.planos-grid {
  display: grid; grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem; max-width: 1000px; margin: 0 auto; align-items: start;
}
.plano-card {
  background: #f9f8f7; border: 1px solid rgba(27,26,25,0.1);
  border-radius: var(--borda-radius-lg); padding: 2rem 1.75rem;
  position: relative; transition: all 0.25s ease; text-align: left;
}
.plano-card:hover { border-color: rgba(201,168,76,0.3); transform: translateY(-4px); box-shadow: 0 12px 30px rgba(27,26,25,0.1); }
.plano-destaque {
  border-color: rgba(201,168,76,0.45);
  background: linear-gradient(160deg, #2a2520 0%, #1f1c17 100%);
  transform: translateY(-8px); box-shadow: 0 20px 50px rgba(201,168,76,0.15);
}
.plano-destaque:hover { transform: translateY(-12px); }
.plano-badge-popular {
  position: absolute; top: -14px; left: 50%; transform: translateX(-50%);
  background: var(--gradiente-dourado); color: var(--cor-fundo);
  font-size: 0.7rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
  padding: 0.3rem 1rem; border-radius: var(--borda-radius-xl); white-space: nowrap;
}
.plano-topo { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.25rem; }
.plano-nome { font-family: var(--fonte-principal); font-size: 1.375rem; font-weight: 600; color: var(--cor-texto-claro-bg); }
.plano-destaque .plano-nome { color: var(--cor-texto); }
.plano-badge-economia {
  font-size: 0.7rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase;
  color: var(--cor-dourado); border: 1px solid rgba(201,168,76,0.4);
  padding: 0.2rem 0.6rem; border-radius: var(--borda-radius-xl);
}
.plano-preco-bloco { display: flex; align-items: baseline; gap: 0.25rem; margin-bottom: 0.5rem; }
.plano-valor { font-family: var(--fonte-principal); font-size: 2.5rem; font-weight: 700; color: var(--cor-dourado); line-height: 1; }
.plano-periodo { font-size: 0.9rem; color: var(--cor-texto-secundario-claro-bg); }
.plano-destaque .plano-periodo { color: var(--cor-texto-secundario); }
.plano-economia { font-size: 0.8rem; color: #16a34a; margin-bottom: 1.5rem; font-weight: 500; }
.plano-destaque .plano-economia { color: #4ade80; }
.plano-lista { list-style: none; display: flex; flex-direction: column; gap: 0.65rem; margin-bottom: 2rem; }
.plano-lista li { display: flex; align-items: center; gap: 0.6rem; font-size: 0.875rem; color: var(--cor-texto-secundario-claro-bg); }
.plano-destaque .plano-lista li { color: var(--cor-texto-secundario); }
.plano-lista i { color: var(--cor-dourado); font-size: 0.75rem; flex-shrink: 0; }
.plano-cta {
  display: block; width: 100%; text-align: center;
  background: transparent; color: var(--cor-dourado);
  border: 1px solid rgba(201,168,76,0.5); padding: 0.85rem;
  border-radius: var(--borda-radius-sm); font-weight: 600; font-size: 0.9rem;
  text-decoration: none; transition: all 0.2s ease; font-family: var(--fonte-ui); cursor: pointer;
}
.plano-cta:hover { background: rgba(201,168,76,0.1); border-color: var(--cor-dourado); }
.plano-cta-destaque { background: var(--gradiente-dourado); color: var(--cor-fundo); border-color: transparent; }
.plano-cta-destaque:hover { background: var(--gradiente-botao); transform: translateY(-1px); box-shadow: 0 6px 20px rgba(201,168,76,0.3); }
.planos-nota {
  margin-top: 2rem; color: var(--cor-texto-secundario-claro-bg);
  font-size: 0.82rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;
}
.planos-nota i { color: var(--cor-dourado-escuro); }

/* SOBRE — seção escura, badge e ícones sobrescritos via global */
.sobre .section-badge { border-color: var(--cor-dourado) !important; color: var(--cor-dourado) !important; }

/* DEPOIMENTOS — claro */
.depoimentos .section-badge { border-color: var(--cor-dourado-escuro); color: var(--cor-dourado-escuro); }

/* FAQ — seção escura */
.faq .section-badge { border-color: var(--cor-dourado); color: var(--cor-dourado); }
.faq .dourado { color: var(--cor-dourado); }

/* BLOG — claro */
.blog-preview .section-badge { border-color: var(--cor-dourado-escuro); color: var(--cor-dourado-escuro); }
.blog-preview .dourado { color: var(--cor-dourado-escuro); }

/* CONTATO */
.contato-form {
  margin-top: 2rem; display: flex; flex-direction: column; gap: 1rem;
  max-width: 600px; margin-left: auto; margin-right: auto; text-align: left;
}
.contato-form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.contato-form-grupo { display: flex; flex-direction: column; gap: 0.4rem; }
.contato-form-grupo label { font-size: 0.82rem; font-weight: 600; color: rgba(255,255,255,0.6); }
.contato-form-grupo input,
.contato-form-grupo select,
.contato-form-grupo textarea {
  background: rgba(255,255,255,0.05); border: 1px solid rgba(201,168,76,0.2);
  border-radius: var(--borda-radius-sm); color: var(--cor-texto);
  font-size: 0.9rem; padding: 0.75rem 1rem; font-family: var(--fonte-ui);
  transition: border-color 0.2s; resize: none;
}
.contato-form-grupo input:focus,
.contato-form-grupo select:focus,
.contato-form-grupo textarea:focus {
  outline: none; border-color: var(--cor-dourado); background: rgba(255,255,255,0.07);
}
.contato-form-grupo select option { background: var(--cor-fundo-card); }
.btn-contato-enviar {
  background: var(--gradiente-botao); color: var(--cor-fundo); border: none;
  padding: 0.875rem 2rem; border-radius: var(--borda-radius-sm);
  font-weight: 600; font-size: 0.9375rem; cursor: pointer;
  transition: all 0.25s ease; display: inline-flex; align-items: center;
  justify-content: center; gap: 0.5rem; font-family: var(--fonte-ui); align-self: flex-start;
}
.btn-contato-enviar:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(201,168,76,0.35); }
.btn-contato-enviar:disabled { opacity: 0.7; cursor: not-allowed; }
.contato-sucesso { color: #4ade80; font-size: 0.875rem; display: flex; align-items: center; gap: 0.5rem; }

@media (max-width: 1024px) {
  .passos-container { grid-template-columns: repeat(2, 1fr); }
  .passos-container::before { display: none; }
}
@media (max-width: 768px) {
  .planos-grid { grid-template-columns: 1fr; }
  .plano-destaque { transform: none; }
  .passos-container { grid-template-columns: 1fr 1fr; }
  .contato-form-row { grid-template-columns: 1fr; }
}
@media (max-width: 480px) {
  .passos-container { grid-template-columns: 1fr; }
  .passo-numero { font-size: 3rem; }
}
</style>