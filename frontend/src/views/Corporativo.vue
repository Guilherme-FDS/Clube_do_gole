<template>
  <div class="corporativo-page">
    <section class="corp-hero">
      <div class="container corp-hero-content">
        <span class="section-badge" style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">
          Soluções B2B
        </span>
        <h1 class="titulo-xl">
          Presentes que <span style="color:var(--cor-dourado);">impressionam</span>
        </h1>
        <p class="texto-corrido" style="color:rgba(255,255,255,0.75);max-width:560px;margin:0 auto 2rem;">
          Surpreenda clientes, parceiros e equipe com experiências de degustação curadas — entregues com sofisticação.
        </p>
        <div style="display:flex;gap:1rem;justify-content:center;flex-wrap:wrap;">
          <a href="https://api.whatsapp.com/send/?phone=5544999999999" target="_blank" class="btn-modern">
            <i class="fa-brands fa-whatsapp"></i> Falar no WhatsApp
          </a>
          <router-link to="/contato" class="btn-outline">Enviar uma mensagem</router-link>
        </div>
      </div>
    </section>

    <section class="corp-incluso">
      <div class="container" style="text-align:center;">
        <span class="section-badge">O que está incluso</span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
          Uma experiência <span class="dourado">completa</span>
        </h2>
        <div class="corp-grid">
          <div v-for="(item, i) in itens" :key="i" class="corp-card fade-in" :class="{ visible: fadeInVisible }"
            :style="{ transitionDelay: `${i * 100}ms` }">
            <div class="corp-card-icone"><i :class="item.icone"></i></div>
            <h3>{{ item.titulo }}</h3>
            <p>{{ item.descricao }}</p>
          </div>
        </div>
      </div>
    </section>

    <section class="corp-cta">
      <div class="container" style="text-align:center;">
        <h2 class="titulo-lg" style="color:var(--cor-texto);">
          Pronto para surpreender?
        </h2>
        <p style="color:var(--cor-texto-secundario);max-width:480px;margin:0 auto 2rem;">
          Entre em contato e montamos uma proposta personalizada para o seu volume.
        </p>
        <a href="https://api.whatsapp.com/send/?phone=5544999999999" target="_blank" class="btn-modern">
          <i class="fa-brands fa-whatsapp"></i> Falar no WhatsApp
        </a>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const fadeInVisible = ref(false)

const itens = [
  { icone: 'fas fa-wine-bottle', titulo: '2 Rótulos Curados', descricao: 'Seleção exclusiva de destilados premium escolhidos pela nossa equipe especializada.' },
  { icone: 'fas fa-box-open', titulo: 'Caixa Premium', descricao: 'Embalagem sofisticada com acabamento de alto padrão, digna de qualquer ocasião.' },
  { icone: 'fas fa-scroll', titulo: 'Cartão de Degustação', descricao: 'Guia personalizado com notas de degustação e história de cada rótulo.' },
  { icone: 'fas fa-truck', titulo: 'Entrega Nacional', descricao: 'Enviamos para todo o Brasil com segurança e rastreamento completo.' },
]

onMounted(() => {
  const handleScroll = () => {
    document.querySelectorAll('.fade-in').forEach(el => {
      if (el.getBoundingClientRect().top <= window.innerHeight - 100) el.classList.add('visible')
    })
  }
  window.addEventListener('scroll', handleScroll)
  setTimeout(() => { fadeInVisible.value = true; handleScroll() }, 100)
})
</script>

<style scoped>
.corporativo-page { min-height: 100vh; }

.corp-hero {
  padding: calc(64px + var(--espacamento-xl)) var(--espacamento-md) var(--espacamento-xl);
  background: var(--gradiente-hero); text-align: center;
  position: relative; overflow: hidden;
}
.corp-hero::before {
  content: '';
  position: absolute; inset: 0;
  background: radial-gradient(ellipse at 80% 20%, rgba(201,168,76,0.08) 0%, transparent 55%);
}
.corp-hero-content { position: relative; z-index: 1; }
.corp-hero .titulo-xl { color: #fff; margin-bottom: 1.25rem; }

.corp-incluso {
  padding: var(--espacamento-xl) var(--espacamento-md);
  background: var(--cor-secao-clara);
  color: var(--cor-texto-claro-bg);
}
.corp-incluso .titulo-lg { color: var(--cor-texto-claro-bg); }
.corp-incluso .section-badge { border-color: var(--cor-dourado-escuro); color: var(--cor-dourado-escuro); }

.corp-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--espacamento-md);
  margin-top: var(--espacamento-md);
}
.corp-card {
  background: #f9f8f7;
  border: 1px solid rgba(27,26,25,0.07);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  text-align: center;
  transition: all 0.25s ease;
}
.corp-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(27,26,25,0.1);
  border-color: rgba(201,168,76,0.25);
}
.corp-card-icone {
  width: 56px; height: 56px;
  background: rgba(201,168,76,0.12); border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  margin: 0 auto 1rem;
}
.corp-card-icone i { font-size: 1.4rem; color: var(--cor-dourado-escuro); }
.corp-card h3 { color: var(--cor-texto-claro-bg); font-size: 1rem; font-weight: 600; margin-bottom: 0.5rem; }
.corp-card p  { color: var(--cor-texto-secundario-claro-bg); font-size: 0.9rem; line-height: 1.6; }

.corp-cta {
  padding: var(--espacamento-xl) var(--espacamento-md);
  background: var(--cor-secao-escura);
}

.fade-in { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }
</style>