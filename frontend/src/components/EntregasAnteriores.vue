<template>
  <section class="entregas-anteriores" id="entregas-anteriores">
    <div class="container">
      <div class="entregas-header">
        <span class="section-badge">Entregas Exclusivas</span>
        <h2 class="titulo-lg">
          {{ titulo || 'O que já entregamos' }}
        </h2>
      </div>

      <div class="entregas-grid">
        <!-- CARROSSEL -->
        <div class="entregas-carrossel" v-if="entregas.length">
          <div class="carrossel-wrapper">
            <button class="carrossel-seta esq" @click="prev" aria-label="Anterior">&#10094;</button>
            <div class="carrossel-viewport">
              <div class="carrossel-track" :style="{ transform: `translateX(-${atual * 100}%)` }">
                <div class="carrossel-item" v-for="(entrega, i) in entregas" :key="i">
                  <div class="carrossel-img-wrap">
                    <img :src="getImagem(entrega)" :alt="getTitulo(entrega)" class="carrossel-img" />
                    <div class="carrossel-overlay">
                      <span class="carrossel-mes">{{ getMes(entrega) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <button class="carrossel-seta dir" @click="next" aria-label="Próximo">&#10095;</button>
          </div>
          <div class="carrossel-dots">
            <button
              v-for="(_, i) in entregas" :key="i"
              class="carrossel-dot" :class="{ ativo: atual === i }"
              @click="atual = i"
            ></button>
          </div>
        </div>

        <!-- TEXTO DIREITO -->
        <div class="entregas-texto">
          <div class="entregas-badge-wrap">
            <span class="entregas-badge-label">Curadoria Exclusiva</span>
          </div>
          <div v-if="textoMarkdown" class="entregas-descricao" v-html="textoHtml"></div>
          <div v-else class="entregas-descricao">
            <p>Cada mês, nossa equipe de especialistas percorre o mundo em busca de rótulos que a maioria nunca terá acesso.</p>
            <p>Destilados raros, premiados e com história — selecionados por quem entende, entregues para quem aprecia.</p>
            <p>Você não escolhe o que vai receber. E é exatamente isso que torna cada entrega uma <strong>experiência única.</strong></p>
          </div>
          <ul class="entregas-features">
            <li><i class="fas fa-check-circle"></i> Rótulos não disponíveis em prateleiras comuns</li>
            <li><i class="fas fa-check-circle"></i> Cartão de degustação incluso em cada entrega</li>
            <li><i class="fas fa-check-circle"></i> Embalagem colecionável exclusiva</li>
            <li><i class="fas fa-check-circle"></i> Curadoria por especialistas globais</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  entregas: { type: Array, default: () => [] },
  titulo: { type: String, default: '' },
  textoMarkdown: { type: String, default: '' }
})

const strapiUrl = import.meta.env.VITE_STRAPI_URL || 'http://localhost:1337'
const atual = ref(0)
let autoplay = null

const getImagem = (entrega) => {
  const attr = entrega.attributes || entrega
  const img = attr?.imagem?.data?.attributes || attr?.imagem?.data || attr?.imagem
  if (img?.url) return img.url.startsWith('http') ? img.url : `${strapiUrl}${img.url}`
  if (img?.formats?.medium?.url) { const u = img.formats.medium.url; return u.startsWith('http') ? u : `${strapiUrl}${u}` }
  return '/img/logo.webp'
}

const getTitulo = (entrega) => (entrega.attributes || entrega)?.titulo || ''
const getMes = (entrega) => (entrega.attributes || entrega)?.mes_referencia || ''

const textoHtml = computed(() => {
  if (!props.textoMarkdown) return ''
  return props.textoMarkdown
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\n\n/g, '</p><p>')
    .replace(/^/, '<p>').replace(/$/, '</p>')
})

const prev = () => { atual.value = atual.value === 0 ? props.entregas.length - 1 : atual.value - 1; resetAutoplay() }
const next = () => { atual.value = (atual.value + 1) % props.entregas.length; resetAutoplay() }
const resetAutoplay = () => { clearInterval(autoplay); autoplay = setInterval(() => { atual.value = (atual.value + 1) % props.entregas.length }, 4000) }

onMounted(() => { if (props.entregas.length > 1) autoplay = setInterval(() => { atual.value = (atual.value + 1) % props.entregas.length }, 4000) })
onUnmounted(() => clearInterval(autoplay))
</script>

<style scoped>
.entregas-anteriores {
  padding: var(--espacamento-xl) 0;
  background: var(--cor-secao-escura);
  color: var(--cor-texto);
}

.entregas-header {
  text-align: center;
  margin-bottom: var(--espacamento-lg);
}

.entregas-header .section-badge {
  border-color: var(--cor-dourado);
  color: var(--cor-dourado);
}

.entregas-header .titulo-lg {
  color: var(--cor-texto);
}

.entregas-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
  max-width: 900px;
  margin: 0 auto;
}

/* CARROSSEL */
.entregas-carrossel {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.carrossel-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.carrossel-viewport {
  flex: 1;
  overflow: hidden;
  border-radius: 10px;
  aspect-ratio: 1/1;
  max-width: 380px;
}

.carrossel-track {
  display: flex;
  transition: transform 0.45s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
}

.carrossel-item {
  min-width: 100%;
  height: 100%;
}

.carrossel-img-wrap {
  position: relative;
  width: 100%;
  height: 100%;
}

.carrossel-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.carrossel-overlay {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  background: linear-gradient(transparent, rgba(0,0,0,0.65));
  padding: 1rem;
}

.carrossel-mes {
  color: #C9A84C;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.carrossel-seta {
  background: rgba(201,168,76,0.15);
  border: 1px solid rgba(201,168,76,0.3);
  color: var(--cor-dourado);
  width: 34px; height: 34px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.8rem;
  display: flex; align-items: center; justify-content: center;
  transition: all 0.2s;
  flex-shrink: 0;
}
.carrossel-seta:hover {
  background: rgba(201,168,76,0.25);
  border-color: var(--cor-dourado);
}

.carrossel-dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.carrossel-dot {
  width: 8px; height: 8px;
  border-radius: 50%;
  background: rgba(255,255,255,0.2);
  border: none; cursor: pointer;
  transition: all 0.2s; padding: 0;
}
.carrossel-dot.ativo {
  background: #C9A84C;
  width: 24px; border-radius: 4px;
}

/* TEXTO */
.entregas-texto {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.entregas-badge-wrap {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.entregas-badge-label {
  color: var(--cor-dourado);
  font-size: 0.875rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}

.entregas-descricao {
  color: var(--cor-texto-secundario);
  line-height: 1.8;
  font-size: 1rem;
}
.entregas-descricao p { margin-bottom: 0.75rem; }
.entregas-descricao strong { color: var(--cor-dourado); }

.entregas-features {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-direction: column; gap: 0.625rem;
}
.entregas-features li {
  display: flex; align-items: center; gap: 0.625rem;
  font-size: 0.9rem; color: rgba(255,255,255,0.8);
}
.entregas-features li i {
  color: var(--cor-dourado);
  font-size: 0.875rem; flex-shrink: 0;
}

@media (max-width: 900px) {
  .entregas-grid { grid-template-columns: 1fr; gap: 2rem; }
  .carrossel-viewport { max-width: 100%; aspect-ratio: 4/3; }
}
</style>