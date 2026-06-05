<template>
  <div class="contato-page">
    <section class="contato-hero">
      <div class="container" style="text-align:center;">
        <span class="section-badge" style="border-color:rgba(201,168,76,0.4);color:var(--cor-dourado);">
          Fale Conosco
        </span>
        <h1 class="titulo-xl" style="color:#fff;">
          Entre em <span style="color:var(--cor-dourado);">Contato</span>
        </h1>
        <p class="texto-corrido" style="color:rgba(255,255,255,0.7);max-width:500px;margin:0 auto;">
          {{ introTexto }}
        </p>
      </div>
    </section>

    <section class="contato-body">
      <div class="container contato-grid">
        <!-- CANAIS -->
        <div class="canais">
          <h2 class="titulo-md" style="margin-bottom:var(--espacamento-md);">Canais de Atendimento</h2>

          <div class="canal-card">
            <div class="canal-icone"><i class="fa-brands fa-whatsapp"></i></div>
            <div class="canal-info">
              <h4>WhatsApp</h4>
              <p>Atendimento rápido e direto</p>
              <a href="https://api.whatsapp.com/send/?phone=5544999999999" target="_blank" class="canal-link">
                Iniciar conversa <i class="fas fa-arrow-right"></i>
              </a>
            </div>
          </div>

          <div class="canal-card">
            <div class="canal-icone"><i class="fas fa-envelope"></i></div>
            <div class="canal-info">
              <h4>E-mail</h4>
              <p>Resposta em até 24h úteis</p>
              <a href="mailto:contato@clubedogole.com.br" class="canal-link">
                contato@clubedogole.com.br <i class="fas fa-arrow-right"></i>
              </a>
            </div>
          </div>

          <div class="canal-card">
            <div class="canal-icone"><i class="fas fa-poll"></i></div>
            <div class="canal-info">
              <h4>Pesquisa de Mercado</h4>
              <p>Ajude a moldar o clube</p>
              <a href="https://tally.so/r/gDvqpD" target="_blank" rel="noopener noreferrer" class="canal-link">
                Responder pesquisa <i class="fas fa-arrow-right"></i>
              </a>
            </div>
          </div>
        </div>

        <!-- FORMULÁRIO -->
        <div class="form-contato-wrapper">
          <h2 class="titulo-md" style="margin-bottom:var(--espacamento-md);">Envie uma mensagem</h2>
          <form class="form-contato" @submit.prevent="enviar">
            <div class="form-group">
              <label>Nome *</label>
              <input type="text" v-model="form.nome" required placeholder="Seu nome completo">
            </div>
            <div class="form-group">
              <label>E-mail *</label>
              <input type="email" v-model="form.email" required placeholder="seu@email.com">
            </div>
            <div class="form-group">
              <label>Assunto *</label>
              <select v-model="form.assunto" required>
                <option value="">Selecione...</option>
                <option>Dúvida sobre assinatura</option>
                <option>Problema com pedido</option>
                <option>Parceria corporativa</option>
                <option>Imprensa</option>
                <option>Outro</option>
              </select>
            </div>
            <div class="form-group">
              <label>Mensagem *</label>
              <textarea v-model="form.mensagem" required rows="5" placeholder="Descreva sua dúvida ou mensagem..."></textarea>
            </div>
            <p v-if="msg" class="form-msg" :class="msgTipo">{{ msg }}</p>
            <button type="submit" class="btn-modern" style="width:100%;" :disabled="enviando">
              <i class="fas fa-paper-plane"></i>
              {{ enviando ? 'Enviando...' : 'Enviar Mensagem' }}
            </button>
          </form>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPagina } from '@/services/strapi'

const introTexto = ref('Estamos aqui para ajudar. Escolha o canal mais conveniente ou envie uma mensagem diretamente.')
const form = ref({ nome: '', email: '', assunto: '', mensagem: '' })
const enviando = ref(false)
const msg = ref('')
const msgTipo = ref('success')

function enviar() {
  enviando.value = true
  const { nome, email, assunto, mensagem } = form.value
  const subject = encodeURIComponent(`[Clube do Gole] ${assunto}`)
  const body = encodeURIComponent(`Nome: ${nome}\nEmail: ${email}\nAssunto: ${assunto}\n\n${mensagem}`)
  window.location.href = `mailto:contato@clubedogole.com.br?subject=${subject}&body=${body}`
  msg.value = 'Seu cliente de e-mail foi aberto. Obrigado pelo contato!'
  msgTipo.value = 'msg-success'
  enviando.value = false
  form.value = { nome: '', email: '', assunto: '', mensagem: '' }
}

onMounted(async () => {
  try {
    const { data } = await getPagina('contato')
    const pagina = data?.data?.[0]
    if (pagina?.conteudo?.[0]) {
      const texto = pagina.conteudo[0].children?.map(c => c.text || '').join('')
      if (texto) introTexto.value = texto
    }
  } catch {}
})
</script>

<style scoped>
.contato-page { min-height: 100vh; }

.contato-hero {
  padding: calc(64px + var(--espacamento-xl)) var(--espacamento-md) var(--espacamento-xl);
  background: var(--gradiente-hero);
}
.contato-hero .titulo-xl { margin-bottom: 1rem; }

.contato-body {
  padding: var(--espacamento-xl) var(--espacamento-md);
  background: var(--cor-secao-escura);
}
.contato-grid {
  display: grid; grid-template-columns: 1fr 1.4fr;
  gap: var(--espacamento-lg); align-items: start;
}
.canais .titulo-md { color: var(--cor-dourado); font-family: var(--fonte-principal); }

.canal-card {
  display: flex; align-items: flex-start; gap: 1rem;
  background: var(--cor-fundo-card); border: 1px solid rgba(255,255,255,0.06);
  border-radius: var(--borda-radius-md); padding: 1.25rem;
  margin-bottom: 1rem; transition: border-color 0.2s ease;
}
.canal-card:hover { border-color: rgba(201,168,76,0.2); }
.canal-icone {
  width: 48px; height: 48px; border-radius: 50%;
  background: rgba(201,168,76,0.12); flex-shrink: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 1.25rem; color: var(--cor-dourado);
}
.canal-info h4 { color: var(--cor-texto); font-weight: 600; margin-bottom: 0.25rem; }
.canal-info p  { color: var(--cor-texto-secundario); font-size: 0.875rem; margin-bottom: 0.5rem; }
.canal-link {
  color: var(--cor-dourado); font-size: 0.875rem; font-weight: 600;
  text-decoration: none; display: inline-flex; align-items: center; gap: 0.4rem;
  transition: gap 0.2s ease;
}
.canal-link:hover { gap: 0.7rem; }

.form-contato-wrapper .titulo-md { color: var(--cor-dourado); font-family: var(--fonte-principal); }
.form-contato { display: flex; flex-direction: column; gap: var(--espacamento-sm); }
.form-group { display: flex; flex-direction: column; gap: 0.4rem; }
.form-group label { font-size: 0.875rem; font-weight: 500; color: var(--cor-texto-secundario); }
.form-group input, .form-group select, .form-group textarea {
  padding: 0.625rem 0.875rem;
  background: var(--cor-fundo); border: 1px solid rgba(201,168,76,0.2);
  border-radius: var(--borda-radius-sm); color: var(--cor-texto);
  font-size: 0.9rem; outline: none; transition: border-color 0.2s; font-family: var(--fonte-ui);
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus { border-color: var(--cor-dourado); }
.form-group textarea { resize: vertical; min-height: 120px; }
.form-group select option { background: var(--cor-fundo); }

.form-msg { font-size: 0.875rem; padding: 0.5rem 0.75rem; border-radius: var(--borda-radius-sm); }
.msg-success { background: rgba(76,175,80,.15); color: #4CAF50; border: 1px solid #4CAF50; }
.msg-error   { background: rgba(244,67,54,.15); color: #f44336; border: 1px solid #f44336; }

@media (max-width: 768px) {
  .contato-grid { grid-template-columns: 1fr; }
}
</style>