<template>
  <section class="faq-page">
    <div class="container">
      <div class="faq-header">
        <span class="section-badge">Dúvidas Frequentes</span>
        <h1>Perguntas <span class="dourado">Frequentes</span></h1>
        <p class="faq-subtitulo">Encontre respostas para as principais dúvidas sobre o Clube do Gole.</p>
      </div>

      <div v-if="carregando" class="faq-loading">
        <div class="loader-ring"></div>
      </div>

      <div v-else-if="faqs.length" class="faq-lista">
        <div v-for="(faq, index) in faqs" :key="faq.id" class="faq-item"
          :class="{ aberto: aberto === index }" @click="toggle(index)">
          <div class="faq-pergunta">
            <span>{{ faq.pergunta }}</span>
            <i :class="aberto === index ? 'fas fa-chevron-up' : 'fas fa-chevron-down'"></i>
          </div>
          <div class="faq-resposta" v-show="aberto === index">
            <p>{{ faq.resposta }}</p>
          </div>
        </div>
      </div>

      <p v-else class="faq-vazio">Nenhuma pergunta cadastrada ainda.</p>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getFaqs } from '@/services/strapi'

const faqs = ref([])
const carregando = ref(true)
const aberto = ref(null)

const toggle = (index) => {
  aberto.value = aberto.value === index ? null : index
}

onMounted(async () => {
  try {
    const { data } = await getFaqs()
    faqs.value = (data?.data || []).map(f => ({
      id: f.id,
      pergunta: f.pergunta,
      resposta: f.resposta
    }))
  } catch {
    faqs.value = []
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
.faq-page {
  min-height: 100vh;
  padding: 120px 1.25rem 80px;
  background: linear-gradient(135deg, #f8f8f6 0%, #ffffff 100%);
}

.container { max-width: 780px; margin: 0 auto; }

.faq-header { text-align: center; margin-bottom: 3rem; }

.section-badge {
  display: inline-flex;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #9E7A2E;
  background: rgba(201,168,76,0.08);
  border: 1px solid rgba(201,168,76,0.25);
  border-radius: 999px;
  padding: 0.25rem 0.75rem;
  margin-bottom: 0.9rem;
}

.faq-header h1 { font-size: 2.2rem; color: #1b1a19; margin: 0.5rem 0; }
.dourado { color: #C9A84C; }
.faq-subtitulo { color: #666; font-size: 0.95rem; }

.faq-loading {
  display: flex;
  justify-content: center;
  padding: 3rem;
}

.loader-ring {
  width: 48px; height: 48px;
  border: 3px solid rgba(201,168,76,0.2);
  border-top-color: #C9A84C;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}

.faq-lista { display: flex; flex-direction: column; gap: 1rem; }

.faq-item {
  background: #fff;
  border: 1px solid #e2e2e2;
  border-radius: 14px;
  overflow: hidden;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.faq-item:hover,
.faq-item.aberto {
  border-color: #C9A84C;
  box-shadow: 0 0 0 3px rgba(201,168,76,0.1);
}

.faq-pergunta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.2rem 1.4rem;
  font-weight: 600;
  color: #1b1a19;
  font-size: 0.95rem;
  gap: 1rem;
}

.faq-pergunta i { color: #C9A84C; flex-shrink: 0; }

.faq-resposta {
  padding: 0 1.4rem 1.2rem;
  color: #555;
  font-size: 0.9rem;
  line-height: 1.7;
}

.faq-vazio { text-align: center; color: #999; padding: 3rem; }

@keyframes spin { to { transform: rotate(360deg); } }
</style>