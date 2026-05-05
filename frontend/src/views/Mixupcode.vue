<template>
  <div class="mixupcode-page">
    <!-- HERO -->
    <section id="inicio" class="hero">
      <div class="hero-content">
        <img src="/img/logo_mix_up.png" alt="Logo MixupCode" class="hero-logo" />
        <h1>Bem-vindo à <span>MixupCode</span></h1>
        <p><strong>Soluções criativas e tecnológicas para o seu negócio.</strong></p>
        <a href="#portfolio" class="btn" @click.prevent="scrollTo('portfolio')">Ver portfólio</a>
      </div>
    </section>

    <!-- SOBRE -->
    <section id="sobre" class="sobre">
      <h2>Sobre nós</h2>
      <p>
        Na MixupCode, desenvolvemos soluções digitais modernas, eficientes e totalmente alinhadas às necessidades atuais
        do mercado. Cada projeto que criamos transforma ideias em experiências inovadoras, unindo design inteligente,
        alta performance e tecnologia de ponta para gerar resultados reais.
        <br /><br />
        Inspirados em recomendações de organizações globais como a OMS (Organização Mundial da Saúde), adotamos práticas
        que priorizam a gestão digital de informações, garantindo mais segurança, precisão e agilidade. Ao substituir
        processos baseados em inúmeros arquivos físicos por sistemas digitais integrados, ajudamos empresas a reduzir
        custos, minimizar erros e fortalecer a organização de dados.
        <br /><br />
        Além da eficiência, acreditamos na responsabilidade ambiental: a digitalização contribui diretamente para
        reduzir o desperdício de papel e combater o desmatamento, tornando cada solução tecnológica também um passo em
        direção à sustentabilidade.
        <br /><br />
        Da criação de sites institucionais a plataformas completas de gestão, desenvolvemos sistemas projetados para
        impulsionar negócios e conectar pessoas, dados e resultados.
        <br /><br />
        MixupCode — conectando tecnologia e resultados.
      </p>
    </section>

    <!-- NOSSA EQUIPE (Carrossel) -->
    <section id="nossa-equipe" class="nossa-equipe">
      <h2>Nossa Equipe</h2>
      <div class="carousel-container" ref="carouselContainer">
        <button type="button" class="prev" @click="prevSlide">&#10094;</button>
        <div class="carousel-wrapper">
          <div class="carousel" ref="carousel" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
            <div v-for="(membro, idx) in equipe" :key="idx" class="carousel-item">
              <img :src="membro.imagem" :alt="membro.nome" />
              <div class="info">
                <h3>{{ membro.nome }}</h3>
                <p>{{ membro.cargo }}</p>
              </div>
            </div>
          </div>
        </div>
        <button type="button" class="next" @click="nextSlide">&#10095;</button>
      </div>
    </section>

    <!-- PORTFÓLIO -->
    <section id="portfolio" class="portfolio">
      <h2>Portfólio</h2>
      <div class="portfolio-single">
        <div class="portfolio-card">
          <h3>Clube do Gole</h3>
          <p><strong>Website institucional moderno e responsivo.</strong></p>
          <router-link to="/" class="portfolio-button">
            <img src="/img/clubedogole.png" alt="Clube do Gole" class="portfolio-image" />
          </router-link>
          <p class="portfolio-description">
            Desenvolvimento completo de website institucional com design moderno,
            responsivo e funcionalidades avançadas de e-commerce.
          </p>
        </div>
      </div>
    </section>

    <!-- CONTATO -->
    <section id="contato" class="contato">
      <h2>Entre em contato</h2>
      <br />
      <p><strong>Tem um projeto em mente? Vamos conversar!</strong></p>
      <br /><br />
      <div class="contact-buttons">
        <a href="https://www.instagram.com/mixupcode?igsh=MWpldngydW4xd3h3dA==" class="contact-button instagram" target="_blank" rel="noopener">
          <span class="material-symbols-outlined icon">camera_alt</span> Instagram
        </a>
        <a href="https://www.linkedin.com/in/mixup-code-86492638a" class="contact-button linkedin" target="_blank" rel="noopener">
          <span class="material-symbols-outlined icon">business</span> LinkedIn
        </a>
        <a href="mailto:mixupcode1@gmail.com?subject=Contato&body=Olá,%20gostaria%20de%20contratar%20seus%20serviços" class="contact-button email">
          <span class="material-symbols-outlined icon">email</span> E-mail
        </a>
      </div>
    </section>

    <!-- RODAPÉ -->
    <footer class="footer">
      <p>© 2025 MixupCode — Todos os direitos reservados.</p>
    </footer>

    <!-- Ícone flutuante WhatsApp -->
    <a href="https://wa.me/5544984385699?text=Ol%C3%A1%20Mixup,%20gostaria%20de%20solicitar%20um%20projeto.%20Podemos%20conversar%3F"
       class="whatsapp-float" target="_blank" rel="noopener" title="Converse com a Mixup no WhatsApp">
      <img src="/img/whats.png" alt="WhatsApp" />
    </a>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Dados da equipe
const equipe = ref([
  { nome: 'Vinicius Rafael Petrim', cargo: 'Frontend', imagem: '/img/vinicius.jpg' },
  { nome: 'Jackson', cargo: 'Backend', imagem: '/img/jackson.jpeg' },
  { nome: 'Guilherme Faustino', cargo: 'Frontend', imagem: '/img/guilherme.jpg' },
  { nome: 'Esdras Filipe', cargo: 'Comunicação', imagem: '/img/esdras.jpg' },
  { nome: 'Lucas Felipe', cargo: 'Comunicação', imagem: '/img/lucas-felipe.jpeg' },
  { nome: 'Alessandro', cargo: 'Comunicação', imagem: '/img/image.png' }
])

// Estado do carrossel
const currentIndex = ref(0)
let autoPlayInterval = null
const carouselContainer = ref(null)

// Funções do carrossel
const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % equipe.value.length
  resetAutoPlay()
}

const prevSlide = () => {
  currentIndex.value = (currentIndex.value - 1 + equipe.value.length) % equipe.value.length
  resetAutoPlay()
}

const startAutoPlay = () => {
  autoPlayInterval = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % equipe.value.length
  }, 4000)
}

const stopAutoPlay = () => {
  if (autoPlayInterval) {
    clearInterval(autoPlayInterval)
    autoPlayInterval = null
  }
}

const resetAutoPlay = () => {
  stopAutoPlay()
  startAutoPlay()
}

// Scroll suave para seções
const scrollTo = (sectionId) => {
  const element = document.getElementById(sectionId)
  if (element) {
    const offset = 80 // altura do header fixo
    const top = element.offsetTop - offset
    window.scrollTo({ top, behavior: 'smooth' })
  }
}

// Pausar autoplay ao passar mouse sobre o carrossel
const handleMouseEnter = () => stopAutoPlay()
const handleMouseLeave = () => startAutoPlay()

// Lifecycle
onMounted(() => {
  startAutoPlay()
  if (carouselContainer.value) {
    carouselContainer.value.addEventListener('mouseenter', handleMouseEnter)
    carouselContainer.value.addEventListener('mouseleave', handleMouseLeave)
  }
})

onUnmounted(() => {
  stopAutoPlay()
  if (carouselContainer.value) {
    carouselContainer.value.removeEventListener('mouseenter', handleMouseEnter)
    carouselContainer.value.removeEventListener('mouseleave', handleMouseLeave)
  }
})
</script>

<style scoped>
/* ===== VARIÁVEIS LOCAIS (já existem no global, mas mantemos para consistência) ===== */
.mixupcode-page {
  --gold: #c8a850;
  --black: #1a1a1a;
  --gray-light: #f4f4f4;
  --gray: #dcdcdc;
  --white: #ffffff;
  --instagram: #c13584;
  --linkedin: #0077b5;
  --email: #c85050;
  --whatsapp: #25d366;
  --spacing-xs: 0.5rem;
  --spacing-sm: 1rem;
  --spacing-md: 1.5rem;
  --spacing-lg: 2rem;
  --spacing-xl: 3rem;
  --spacing-xxl: 5rem;
  --border-radius-sm: 8px;
  --border-radius-md: 12px;
  --border-radius-lg: 16px;
  --border-radius-circle: 50%;
  --shadow-light: 0 2px 6px rgba(0, 0, 0, 0.1);
  --shadow-medium: 0 3px 12px rgba(0, 0, 0, 0.1);
  --shadow-heavy: 0 4px 10px rgba(0, 0, 0, 0.3);
  --transition-fast: 0.2s ease;
  --transition-normal: 0.3s ease;
  --transition-slow: 0.6s ease-in-out;
}

/* Reset específico para a página (evita conflitos com global) */
.mixupcode-page {
  background: var(--gray-light);
  color: var(--black);
  font-family: 'Poppins', sans-serif;
  line-height: 1.6;
}

/* Seções */
.mixupcode-page section {
  scroll-margin-top: 80px;
  padding: var(--spacing-xxl) 10%;
  text-align: center;
  position: relative;
}

.mixupcode-page section::before {
  content: "";
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: var(--gold);
}

.mixupcode-page h2 {
  margin-bottom: var(--spacing-lg);
  font-size: 2.5rem;
  color: var(--gold);
  text-transform: uppercase;
  letter-spacing: 2px;
}

/* Hero */
.hero {
  background: var(--gray-light);
  padding: var(--spacing-xxl) var(--spacing-lg);
}
.hero-logo {
  width: 200px;
  margin-bottom: var(--spacing-lg);
}
.hero h1 {
  font-size: 3rem;
}
.hero span {
  color: var(--gold);
}
.hero p {
  margin: var(--spacing-sm) 0 var(--spacing-lg);
  color: #444;
}
.btn {
  background: var(--gold);
  color: var(--white);
  padding: 0.75rem 1.5rem;
  border-radius: var(--border-radius-sm);
  text-decoration: none;
  transition: var(--transition-normal);
  font-weight: 500;
  display: inline-block;
}
.btn:hover {
  background: #b89642;
  transform: translateY(-2px);
}

/* Sobre */
.sobre {
  background: var(--white);
}
.sobre p {
  max-width: 900px;
  margin: 0 auto;
  line-height: 1.8;
  color: #555;
  font-size: 1.1rem;
  text-align: justify;
  padding: 0 var(--spacing-sm);
}

/* Carrossel da equipe */
.nossa-equipe {
  background: var(--gray-light);
}
.carousel-container {
  position: relative;
  max-width: 1000px;
  margin: 0 auto;
  overflow: hidden;
  padding: 0 60px;
}
.carousel-wrapper {
  width: 100%;
  overflow: hidden;
  border-radius: var(--border-radius-lg);
}
.carousel {
  display: flex;
  transition: transform 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  width: 100%;
}
.carousel-item {
  flex: 0 0 100%;
  min-width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
  background: var(--white);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-medium);
}
.carousel-item img {
  width: 250px;
  height: 250px;
  border-radius: var(--border-radius-circle);
  object-fit: cover;
  margin-bottom: var(--spacing-md);
  border: 6px solid var(--gold);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
}
.carousel-item:hover img {
  transform: scale(1.05);
}
.info h3 {
  color: var(--gold);
  font-size: 1.5rem;
  margin-bottom: var(--spacing-xs);
}
.info p {
  color: #555;
  font-size: 1.1rem;
  font-weight: 500;
}
.prev, .next {
  background: var(--gold);
  color: var(--white);
  border: none;
  font-size: 1.5rem;
  padding: 0.8rem 1rem;
  cursor: pointer;
  border-radius: var(--border-radius-circle);
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  transition: var(--transition-normal);
  z-index: 5;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.prev:hover, .next:hover {
  background: #b89642;
  transform: translateY(-50%) scale(1.1);
}
.prev { left: 10px; }
.next { right: 10px; }

/* Portfólio */
.portfolio {
  background: var(--white);
}
.portfolio-single {
  display: flex;
  justify-content: center;
  align-items: center;
  max-width: 600px;
  margin: 0 auto;
}
.portfolio-card {
  background: var(--gray-light);
  border: 1px solid var(--gray);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-medium);
  text-align: center;
  transition: var(--transition-normal);
  width: 100%;
}
.portfolio-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}
.portfolio-card h3 {
  color: var(--gold);
  font-size: 1.8rem;
  margin-bottom: var(--spacing-sm);
}
.portfolio-card p {
  color: #555;
  margin-bottom: var(--spacing-md);
  font-size: 1.1rem;
}
.portfolio-button {
  display: block;
  text-decoration: none;
  margin-bottom: var(--spacing-md);
}
.portfolio-image {
  width: 100%;
  height: auto;
  border-radius: var(--border-radius-md);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: var(--transition-normal);
}
.portfolio-button:hover .portfolio-image {
  transform: scale(1.02);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}
.portfolio-description {
  color: #666;
  font-size: 1rem;
  line-height: 1.6;
  text-align: center;
  margin-top: var(--spacing-md);
  padding: 0 var(--spacing-sm);
}

/* Contato */
.contato {
  background: var(--gray-light);
}
.contact-buttons {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}
.contact-button {
  text-decoration: none;
  color: var(--white);
  padding: 12px 20px;
  border-radius: var(--border-radius-sm);
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  transition: var(--transition-normal);
  font-weight: 500;
}
.instagram { background: var(--instagram); }
.linkedin { background: var(--linkedin); }
.email { background: var(--email); }
.contact-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

/* Footer */
.footer {
  background: var(--black);
  color: var(--white);
  text-align: center;
  padding: var(--spacing-md) 0;
  font-size: 0.9rem;
  margin-top: var(--spacing-lg);
}

/* WhatsApp flutuante */
.whatsapp-float {
  position: fixed;
  bottom: 20px;
  right: 20px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius-circle);
  background-color: var(--whatsapp);
  box-shadow: var(--shadow-heavy);
  z-index: 999;
  transition: var(--transition-normal);
}
.whatsapp-float img {
  width: 35px;
  height: 35px;
}
.whatsapp-float:hover {
  transform: scale(1.1);
}

/* Responsividade */
@media (max-width: 768px) {
  .mixupcode-page section {
    padding: var(--spacing-xl) 5%;
  }
  .hero h1 {
    font-size: 2rem;
  }
  .hero-logo {
    width: 150px;
  }
  .carousel-container {
    padding: 0 40px;
  }
  .carousel-item img {
    width: 200px;
    height: 200px;
  }
  .sobre p {
    font-size: 1rem;
    text-align: left;
  }
  .portfolio-single {
    max-width: 90%;
  }
  .portfolio-card {
    padding: var(--spacing-lg);
  }
  .contact-buttons {
    flex-direction: column;
    align-items: center;
  }
  .contact-button {
    width: 200px;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .carousel-item img {
    width: 150px;
    height: 150px;
  }
  .prev, .next {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
    padding: 0.5rem;
  }
  .carousel-container {
    padding: 0 30px;
  }
  .portfolio-card {
    padding: var(--spacing-md);
  }
  .portfolio-card h3 {
    font-size: 1.5rem;
  }
}
</style>