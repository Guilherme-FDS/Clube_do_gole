<template>
  <div class="pagina-page">
    <div v-if="carregando" class="estado-vazio">
      <i class="fas fa-spinner fa-spin"></i>
    </div>

    <div v-else-if="pagina" class="pagina-wrapper">
      <section class="pagina-hero">
        <div class="container">
          <h1 class="titulo-xl">{{ pagina.titulo }}</h1>
        </div>
      </section>

      <section class="pagina-body">
        <div class="container pagina-prose">
          <template v-for="(block, i) in pagina.conteudo" :key="i">
            <p v-if="block.type === 'paragraph'">
              {{ extrairTexto(block.children) }}
            </p>
            <h2 v-else-if="block.type === 'heading' && block.level === 2">
              {{ extrairTexto(block.children) }}
            </h2>
            <h3 v-else-if="block.type === 'heading' && block.level === 3">
              {{ extrairTexto(block.children) }}
            </h3>
            <blockquote v-else-if="block.type === 'quote'">
              {{ extrairTexto(block.children) }}
            </blockquote>
            <ul v-else-if="block.type === 'list' && block.format === 'unordered'">
              <li v-for="(item, j) in block.children" :key="j">
                {{ extrairTexto(item.children) }}
              </li>
            </ul>
            <ol v-else-if="block.type === 'list' && block.format === 'ordered'">
              <li v-for="(item, j) in block.children" :key="j">
                {{ extrairTexto(item.children) }}
              </li>
            </ol>
          </template>
        </div>
      </section>
    </div>

    <div v-else class="estado-vazio">
      <i class="fas fa-search"></i>
      <p>Página não encontrada.</p>
      <router-link to="/" class="btn-modern">Voltar ao início</router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { getPagina } from '@/services/strapi'

const route = useRoute()
const pagina = ref(null)
const carregando = ref(true)

function extrairTexto(children = []) {
  return children.map(c => c.text || '').join('')
}

async function carregar(slug) {
  carregando.value = true
  pagina.value = null
  try {
    const { data } = await getPagina(slug)
    const items = data?.data || []
    pagina.value = items.length ? items[0] : null
  } catch {
    pagina.value = null
  } finally {
    carregando.value = false
  }
}

onMounted(() => carregar(route.params.slug))
watch(() => route.params.slug, (slug) => { if (slug) carregar(slug) })
</script>

<style scoped>
.pagina-page { min-height: 100vh; background: var(--cor-secao-clara); color: var(--cor-texto-claro-bg); }

.pagina-hero {
  padding: calc(64px + var(--espacamento-xl)) var(--espacamento-md) var(--espacamento-lg);
  background: var(--gradiente-hero);
  text-align: center;
}
.pagina-hero .titulo-xl { color: #fff; }

.pagina-body {
  padding: var(--espacamento-xl) var(--espacamento-md);
  background: var(--cor-secao-clara);
}
.pagina-prose {
  max-width: 760px;
  display: flex; flex-direction: column; gap: 1.25rem;
}
.pagina-prose p {
  color: var(--cor-texto-secundario-claro-bg);
  font-size: 1.0625rem; line-height: 1.8;
}
.pagina-prose h2 {
  font-family: var(--fonte-principal);
  font-size: 1.75rem; font-weight: 600;
  color: var(--cor-dourado-escuro); margin-top: 1rem;
}
.pagina-prose h3 {
  font-family: var(--fonte-principal);
  font-size: 1.375rem; font-weight: 600;
  color: var(--cor-dourado-escuro);
}
.pagina-prose blockquote {
  border-left: 3px solid var(--cor-dourado-escuro);
  padding: 0.875rem 1.25rem;
  background: rgba(158,122,46,0.07);
  border-radius: 0 var(--borda-radius-sm) var(--borda-radius-sm) 0;
  color: var(--cor-texto-secundario-claro-bg);
  font-style: italic;
}
.pagina-prose ul, .pagina-prose ol {
  padding-left: 1.5rem;
  display: flex; flex-direction: column; gap: 0.5rem;
}
.pagina-prose li { color: var(--cor-texto-secundario-claro-bg); line-height: 1.7; }
.pagina-prose ul li::marker { color: var(--cor-dourado-escuro); }
.pagina-prose ol li::marker { color: var(--cor-dourado-escuro); font-weight: 700; }

.estado-vazio {
  text-align: center; padding: var(--espacamento-xl);
  display: flex; flex-direction: column; align-items: center; gap: 1rem;
  margin-top: 100px;
}
.estado-vazio i { font-size: 2.5rem; color: var(--cor-dourado); opacity: 0.4; }
</style>