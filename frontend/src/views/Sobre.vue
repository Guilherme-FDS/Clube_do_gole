<template>
  <div class="sobre-page">
    <!-- HERO -->
    <section class="sobre-hero">
      <div class="container sobre-hero-content">
        <span class="section-badge" style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">
          Nossa História
        </span>
        <h1 class="titulo-xl">
          Nascemos da <span style="color:var(--cor-dourado);">frustração</span><br>de quem realmente entende
        </h1>
        <p class="texto-corrido" style="color:rgba(255,255,255,0.75);max-width:580px;margin:0 auto;">
          Um clube criado por quem viveu a falta de acesso a destilados de qualidade fora dos grandes centros.
        </p>
      </div>
    </section>

    <!-- HISTÓRIA -->
    <section class="sobre-historia" id="historia">
      <div class="container">
        <div class="historia-grid">
          <div class="historia-texto fade-in" :class="{ visible: fadeInVisible }">
            <span class="section-badge">A origem</span>
            <h2 class="titulo-lg" style="text-align:left;">
              De Maringá para <span class="dourado">o mundo</span>
            </h2>
            <template v-if="sobreTexto">
              <p v-for="(p, i) in sobreTexto" :key="i">{{ p }}</p>
            </template>
            <template v-else>
              <p>O Clube do Gole nasceu em Maringá, Paraná — uma cidade vibrante, mas que historicamente enfrenta limitações no acesso a destilados premium vindos do mundo todo.</p>
              <p>Guilherme, fundador do clube, transitou por áreas distintas antes de chegar até aqui: sete anos no mercado financeiro, formação em Análise e Desenvolvimento de Sistemas, e uma paixão genuína pela gastronomia e cultura de bebidas.</p>
              <p>A frustração era simples: por que era tão difícil ter acesso a um bom whisky japonês, a um gin artesanal escocês, a uma cachaça de alambique envelhecida — sem precisar pagar o triplo ou depender de importadores incertos?</p>
              <p>A resposta foi o Clube do Gole.</p>
            </template>
          </div>
          <div class="historia-visual fade-in" :class="{ visible: fadeInVisible }" style="transition-delay:200ms;">
            <div class="historia-card">
              <div class="historia-stat"><span class="stat-n">7+</span><span class="stat-l">Anos de experiência no mercado financeiro</span></div>
              <div class="historia-stat"><span class="stat-n">ADS</span><span class="stat-l">Formação em tecnologia</span></div>
              <div class="historia-stat"><span class="stat-n">🇧🇷</span><span class="stat-l">Nascido em Maringá, pensado para o Brasil</span></div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- MISSÃO E VALORES -->
    <section class="sobre-missao" id="missao">
      <div class="container" style="text-align:center;">
        <span class="section-badge">Propósito</span>
        <h2 class="titulo-lg fade-in" :class="{ visible: fadeInVisible }">
          Missão e <span class="dourado" style="color:var(--cor-dourado-escuro);">Valores</span>
        </h2>

        <div class="mv-grid">
          <div class="mv-card fade-in" :class="{ visible: fadeInVisible }">
            <div class="mv-icone"><i class="fas fa-bullseye"></i></div>
            <h3>Missão</h3>
            <p>Levar a cultura das bebidas do mundo para qualquer lugar do planeta, com curadoria especializada, surpresa garantida e experiência mensal de descoberta.</p>
          </div>
          <div class="mv-card fade-in" :class="{ visible: fadeInVisible }" style="transition-delay:100ms;">
            <div class="mv-icone"><i class="fas fa-eye"></i></div>
            <h3>Visão</h3>
            <p>Ser o maior clube de assinatura de destilados do mundo — referência global em curadoria e experiência de unboxing.</p>
          </div>
        </div>

        <h3 class="valores-titulo fade-in" :class="{ visible: fadeInVisible }">Nossos Valores</h3>
        <div class="valores-grid">
          <div v-for="(v, i) in valores" :key="i" class="valor-item fade-in"
            :class="{ visible: fadeInVisible }" :style="{ transitionDelay: `${i * 80}ms` }">
            <i :class="v.icone"></i>
            <span>{{ v.label }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="sobre-cta">
      <div class="container" style="text-align:center;">
        <h2 class="titulo-lg" style="color:var(--cor-texto);">Faça parte do clube</h2>
        <p style="color:var(--cor-texto-secundario);max-width:480px;margin:0 auto 2rem;">
          Uma seleção nova todo mês. Entregue na sua porta.
        </p>
        <router-link to="/#planos" class="btn-modern">Ver Planos</router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPagina } from '@/services/strapi'

const fadeInVisible = ref(false)
const sobreTexto = ref(null)

const valores = [
  { icone: 'fas fa-unlock-alt', label: 'Acesso' },
  { icone: 'fas fa-gem', label: 'Exclusividade' },
  { icone: 'fas fa-crown', label: 'Sofisticação' },
  { icone: 'fas fa-users', label: 'Pertencimento' },
  { icone: 'fas fa-search', label: 'Curadoria' },
  { icone: 'fas fa-compass', label: 'Espírito de Descoberta' },
]

function extrairTexto(children = []) { return children.map(c => c.text || '').join('') }

onMounted(async () => {
  try {
    const { data } = await getPagina('sobre')
    const blocks = data?.data?.[0]?.conteudo || []
    if (blocks.length) {
      sobreTexto.value = blocks
        .filter(b => b.type === 'paragraph')
        .map(b => extrairTexto(b.children))
    }
  } catch {}

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
.sobre-page { min-height: 100vh; }

.sobre-hero {
  padding: calc(64px + var(--espacamento-xl)) var(--espacamento-md) var(--espacamento-xl);
  background: var(--gradiente-hero); text-align: center; position: relative; overflow: hidden;
}
.sobre-hero::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse at 20% 80%, rgba(123,47,224,0.1) 0%, transparent 55%),
              radial-gradient(ellipse at 80% 20%, rgba(201,168,76,0.07) 0%, transparent 55%);
}
.sobre-hero-content { position: relative; z-index: 1; }
.sobre-hero .titulo-xl { color: #fff; margin-bottom: 1.25rem; }

.sobre-historia {
  padding: var(--espacamento-xl) var(--espacamento-md);
  background: var(--cor-secao-escura);
}
.historia-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: var(--espacamento-lg); align-items: center;
}
.historia-texto .titulo-lg { color: var(--cor-texto); margin-bottom: var(--espacamento-md); }
.historia-texto .section-badge { border-color: rgba(201,168,76,0.4); color: var(--cor-dourado); }
.historia-texto p { color: var(--cor-texto-secundario); line-height: 1.75; margin-bottom: 1rem; font-size: 1rem; }

.historia-card {
  background: var(--cor-fundo-card);
  border: 1px solid rgba(201,168,76,0.15);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-lg);
  display: flex; flex-direction: column; gap: var(--espacamento-md);
}
.historia-stat { display: flex; flex-direction: column; gap: 0.3rem; }
.stat-n { font-family: var(--fonte-principal); font-size: 2rem; font-weight: 700; color: var(--cor-dourado); }
.stat-l { color: var(--cor-texto-secundario); font-size: 0.875rem; line-height: 1.4; }

.sobre-missao {
  padding: var(--espacamento-xl) var(--espacamento-md);
  background: var(--cor-secao-clara); color: var(--cor-texto-claro-bg);
}
.sobre-missao .titulo-lg { color: var(--cor-texto-claro-bg); }
.sobre-missao .section-badge { border-color: var(--cor-dourado-escuro); color: var(--cor-dourado-escuro); }

.mv-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: var(--espacamento-md); margin: var(--espacamento-md) 0;
}
.mv-card {
  background: #f9f8f7; border: 1px solid rgba(27,26,25,0.07);
  border-radius: var(--borda-radius-md); padding: var(--espacamento-lg);
  text-align: center; transition: all 0.25s ease;
}
.mv-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(27,26,25,0.1); }
.mv-icone {
  width: 56px; height: 56px; background: rgba(201,168,76,0.12); border-radius: 50%;
  display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem;
}
.mv-icone i { font-size: 1.4rem; color: var(--cor-dourado-escuro); }
.mv-card h3 { color: var(--cor-texto-claro-bg); font-weight: 600; margin-bottom: 0.75rem; }
.mv-card p  { color: var(--cor-texto-secundario-claro-bg); line-height: 1.65; font-size: 0.9375rem; }

.valores-titulo {
  font-family: var(--fonte-principal); font-size: 1.5rem; font-weight: 600;
  color: var(--cor-texto-claro-bg); margin: var(--espacamento-lg) 0 var(--espacamento-md);
}
.valores-grid {
  display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem;
}
.valor-item {
  display: flex; align-items: center; gap: 0.5rem;
  background: #f9f8f7; border: 1px solid rgba(27,26,25,0.08);
  border-radius: var(--borda-radius-xl);
  padding: 0.625rem 1.25rem;
  font-size: 0.9rem; font-weight: 500; color: var(--cor-texto-claro-bg);
  transition: all 0.2s ease;
}
.valor-item:hover { border-color: rgba(201,168,76,0.3); background: rgba(201,168,76,0.06); }
.valor-item i { color: var(--cor-dourado-escuro); font-size: 0.875rem; }

.sobre-cta { padding: var(--espacamento-xl) var(--espacamento-md); background: var(--cor-secao-escura); }

.fade-in { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
.fade-in.visible { opacity: 1; transform: translateY(0); }

@media (max-width: 768px) {
  .historia-grid { grid-template-columns: 1fr; }
  .mv-grid { grid-template-columns: 1fr; }
}
</style>