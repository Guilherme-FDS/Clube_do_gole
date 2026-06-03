<template>
  <div class="blog-page">
    <section class="blog-hero">
      <div class="container">
        <h1 class="titulo-xl">Blog</h1>
      </div>
    </section>

    <section class="blog-body">
      <div class="container">
        <div v-if="carregando" class="estado-vazio">
          <i class="fas fa-spinner fa-spin"></i>
        </div>

        <div v-else-if="posts.length" class="blog-grid">
          <router-link
            v-for="post in posts"
            :key="post.id"
            :to="`/blog/${post.slug}`"
            class="post-card"
          >
            <div class="post-card-body">
              <span class="post-data">{{ formatarData(post.publicado_em || post.createdAt) }}</span>
              <h2 class="post-titulo">{{ post.titulo }}</h2>
              <p v-if="post.resumo" class="post-resumo">{{ post.resumo }}</p>
              <span class="post-link">Ler mais <i class="fas fa-arrow-right"></i></span>
            </div>
          </router-link>
        </div>

        <div v-else class="estado-vazio">
          <i class="fas fa-newspaper"></i>
          <p>Nenhum post publicado ainda.</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPosts } from '@/services/strapi'

const posts = ref([])
const carregando = ref(true)

function formatarData(str) {
  if (!str) return ''
  return new Date(str).toLocaleDateString('pt-BR', { day: '2-digit', month: 'long', year: 'numeric' })
}

onMounted(async () => {
  try {
    const { data } = await getPosts()
    posts.value = (data?.data || []).map(p => ({ id: p.id, ...p }))
  } catch {
    posts.value = []
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
.blog-page { min-height: 100vh; background: var(--cor-secao-clara); color: var(--cor-texto-claro-bg); }

.blog-hero {
  padding: calc(64px + var(--espacamento-xl)) var(--espacamento-md) var(--espacamento-lg);
  background: var(--gradiente-hero);
  text-align: center;
}
.blog-hero .titulo-xl { color: #fff; }

.blog-body {
  padding: var(--espacamento-xl) var(--espacamento-md);
}

.blog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--espacamento-md);
  max-width: 1100px;
  margin: 0 auto;
}

.post-card {
  background: var(--cor-surface);
  border-radius: var(--borda-radius);
  padding: var(--espacamento-md);
  text-decoration: none;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(158,122,46,0.15);
  transition: transform 0.2s, box-shadow 0.2s;
}
.post-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.post-card-body { display: flex; flex-direction: column; gap: 0.625rem; }

.post-data { font-size: 0.8125rem; color: var(--cor-dourado); text-transform: uppercase; letter-spacing: 0.05em; }

.post-titulo {
  font-family: var(--fonte-principal);
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--cor-texto-claro-bg);
  line-height: 1.4;
}

.post-resumo {
  font-size: 0.9375rem;
  color: var(--cor-texto-secundario-claro-bg);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-link {
  font-size: 0.875rem;
  color: var(--cor-dourado);
  font-weight: 600;
  margin-top: auto;
  padding-top: 0.5rem;
}
.post-link i { font-size: 0.75rem; margin-left: 0.25rem; }

.estado-vazio {
  text-align: center; padding: var(--espacamento-xl);
  display: flex; flex-direction: column; align-items: center; gap: 1rem;
  margin-top: 60px;
}
.estado-vazio i { font-size: 2.5rem; color: var(--cor-dourado); opacity: 0.4; }
.estado-vazio p { color: var(--cor-texto-secundario-claro-bg); }
</style>
