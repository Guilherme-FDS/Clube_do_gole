<template>
  <div class="pagina-institucional">
    <section class="inst-hero">
      <div class="container">
        <span class="section-badge">Informações</span>
        <h1 class="titulo-xl">Política de <span style="color:var(--cor-dourado);">Reembolso</span></h1>
      </div>
    </section>
    <section class="inst-body">
      <div class="container inst-prose">
        <template v-if="conteudoCms.length">
          <template v-for="(block, i) in conteudoCms" :key="i">
            <p v-if="block.type === 'paragraph'">{{ extrairTexto(block.children) }}</p>
            <h2 v-else-if="block.type === 'heading' && block.level === 2">{{ extrairTexto(block.children) }}</h2>
            <h3 v-else-if="block.type === 'heading' && block.level === 3">{{ extrairTexto(block.children) }}</h3>
            <blockquote v-else-if="block.type === 'quote'">{{ extrairTexto(block.children) }}</blockquote>
            <ul v-else-if="block.type === 'list' && block.format === 'unordered'">
              <li v-for="(item, j) in block.children" :key="j">{{ extrairTexto(item.children) }}</li>
            </ul>
          </template>
        </template>
        <template v-else>
          <p>Nossa política de reembolso está sendo atualizada.</p>
          <p>Para solicitações ou dúvidas, entre em contato pelo e-mail <a href="mailto:contato@clubedogole.com.br">contato@clubedogole.com.br</a>.</p>
          <router-link to="/contato" class="btn-modern" style="display:inline-flex;margin-top:1.5rem;">Falar Conosco</router-link>
        </template>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPagina } from '@/services/strapi'
const conteudoCms = ref([])
function extrairTexto(children = []) { return children.map(c => c.text || '').join('') }
onMounted(async () => {
  try {
    const { data } = await getPagina('politica-reembolso')
    conteudoCms.value = data?.data?.[0]?.conteudo || []
  } catch {}
})
</script>

<style scoped>
.pagina-institucional { min-height: 100vh; }
.inst-hero {
  padding: calc(64px + var(--espacamento-xl)) var(--espacamento-md) var(--espacamento-lg);
  background: var(--gradiente-hero); text-align: center;
}
.inst-hero .titulo-xl { color: #fff; }
.inst-body { padding: var(--espacamento-xl) var(--espacamento-md); background: var(--cor-secao-clara); }
.inst-prose {
  max-width: 760px; display: flex; flex-direction: column; gap: 1.25rem;
  color: var(--cor-texto-claro-bg);
}
.inst-prose p { font-size: 1.0625rem; line-height: 1.8; color: var(--cor-texto-secundario-claro-bg); }
.inst-prose a { color: var(--cor-dourado-escuro); }
.inst-prose h2 { font-family: var(--fonte-principal); font-size: 1.75rem; color: var(--cor-dourado-escuro); margin-top: 1rem; }
.inst-prose h3 { font-family: var(--fonte-principal); font-size: 1.375rem; color: var(--cor-dourado-escuro); }
.inst-prose blockquote { border-left: 3px solid var(--cor-dourado-escuro); padding: 0.875rem 1.25rem; background: rgba(158,122,46,0.07); font-style: italic; color: var(--cor-texto-secundario-claro-bg); }
.inst-prose ul { padding-left: 1.5rem; display: flex; flex-direction: column; gap: 0.5rem; }
.inst-prose li { color: var(--cor-texto-secundario-claro-bg); line-height: 1.7; }
.inst-prose ul li::marker { color: var(--cor-dourado-escuro); }
</style>