<template>
  <section class="login-page">
    <div class="card-login-borda">
      <div class="card-viewport">
        <article class="card-login">
          <header class="topo">
            <span class="chip">Clube do Gole</span>
            <h1>Redefinir senha</h1>
            <p class="subtitulo">Crie uma nova senha para acessar sua conta.</p>
          </header>

          <div v-if="flashMensagem" :class="['flash-message', flashMensagem.tipo]">
            <i :class="flashIcon"></i>
            <p>{{ flashMensagem.texto }}</p>
          </div>

          <!-- Sucesso: contagem regressiva e volta ao login -->
          <div v-if="sucesso" class="sucesso-box">
            <p class="redirecionando">
              Redirecionando para o login em <strong>{{ segundos }}s</strong>…
            </p>
            <router-link to="/login" class="link-alternar">Entrar agora</router-link>
          </div>

          <!-- Formulário -->
          <form v-else-if="tokenValido" class="form-login" @submit.prevent="submeter">
            <div class="campo">
              <label for="nova-senha">Nova senha</label>
              <input
                id="nova-senha"
                v-model="novaSenha"
                type="password"
                placeholder="••••••••"
                minlength="6"
                required
              />
            </div>
            <div class="campo">
              <label for="confirmar-senha">Confirmar senha</label>
              <input
                id="confirmar-senha"
                v-model="confirmar"
                type="password"
                placeholder="••••••••"
                required
              />
            </div>
            <button type="submit" class="btn-submit" :class="{ loading: carregando }" :disabled="carregando">
              <span class="btn-text">Redefinir senha</span>
              <div class="btn-loader"></div>
            </button>
          </form>

          <div v-if="!sucesso" class="back-link">
            <router-link to="/login">← Voltar ao login</router-link>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

const novaSenha = ref('')
const confirmar = ref('')
const carregando = ref(false)
const sucesso = ref(false)
const tokenValido = ref(true)
const token = ref('')
const flashMensagem = ref(null)
const segundos = ref(5)
let intervaloRedirect = null

const flashIcon = computed(() => {
  if (!flashMensagem.value) return ''
  if (flashMensagem.value.tipo === 'error') return 'fas fa-exclamation-circle'
  if (flashMensagem.value.tipo === 'success') return 'fas fa-check-circle'
  return 'fas fa-info-circle'
})

function mostrarMensagem(texto, tipo = 'error') {
  flashMensagem.value = { texto, tipo }
}

onMounted(() => {
  token.value = route.query.token
  if (!token.value) {
    tokenValido.value = false
    mostrarMensagem('Token inválido ou expirado. Solicite um novo link.', 'error')
  }
})

onBeforeUnmount(() => {
  if (intervaloRedirect) clearInterval(intervaloRedirect)
})

function iniciarContagemRegressiva() {
  segundos.value = 5
  intervaloRedirect = setInterval(() => {
    segundos.value -= 1
    if (segundos.value <= 0) {
      clearInterval(intervaloRedirect)
      router.push('/login')
    }
  }, 1000)
}

async function submeter() {
  flashMensagem.value = null
  if (novaSenha.value.length < 6) {
    return mostrarMensagem('A senha deve ter no mínimo 6 caracteres.')
  }
  if (novaSenha.value !== confirmar.value) {
    return mostrarMensagem('As senhas não coincidem.')
  }
  carregando.value = true
  try {
    await api.post('/auth/redefinir-senha', {
      token: token.value,
      nova_senha: novaSenha.value,
    })
    sucesso.value = true
    mostrarMensagem('Senha redefinida com sucesso!', 'success')
    iniciarContagemRegressiva()
  } catch (e) {
    mostrarMensagem(e?.response?.data?.detail || 'Erro ao redefinir senha.', 'error')
  } finally {
    carregando.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 120px 1.25rem 80px;
  background:
    radial-gradient(circle at top, rgba(201,168,76,0.08), transparent 25%),
    linear-gradient(135deg, #f8f8f6 0%, #ffffff 100%);
}

.card-login-borda {
  width: 100%;
  max-width: 430px;
  padding: 2px;
  border-radius: 18px;
  background: linear-gradient(135deg, #9E7A2E, #E2C06A, #C9A84C, #9E7A2E);
  background-size: 300% 300%;
  animation: borda-dourada 5s ease infinite;
  box-shadow: 0 18px 50px rgba(0,0,0,0.08), 0 0 25px rgba(201,168,76,0.10);
}

.card-viewport { border-radius: 16px; overflow: hidden; }

.card-login { background: #ffffff; border-radius: 16px; padding: 2.2rem 1.8rem; }

.topo { margin-bottom: 1.4rem; }

.chip {
  display: inline-flex;
  gap: 5px;
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

.chip::before { content: '●'; font-size: 6px; }

.topo h1 { margin: 0; font-size: 2rem; color: #1b1a19; }
.subtitulo { margin-top: 0.55rem; font-size: 0.92rem; color: #666666; }

.form-login { display: flex; flex-direction: column; gap: 1rem; margin-bottom: 1.3rem; }

.campo { display: grid; gap: 0.42rem; }
.campo label { color: #2b2b2b; font-size: 0.86rem; font-weight: 600; }
.campo input {
  width: 100%;
  border: 1px solid #e2e2e2;
  border-radius: 11px;
  background: #fafafa;
  color: #1b1a19;
  font-size: 0.93rem;
  padding: 0.78rem 0.9rem;
}
.campo input:focus {
  outline: none;
  border-color: #C9A84C;
  background: #ffffff;
  box-shadow: 0 0 0 4px rgba(201,168,76,0.12);
}

.btn-submit {
  width: 100%;
  background: linear-gradient(45deg, #9E7A2E, #E2C06A);
  color: #1b1a19;
  border: none;
  border-radius: 11px;
  font-weight: 700;
  padding: 0.82rem;
  cursor: pointer;
  position: relative;
}
.btn-submit:disabled { opacity: 0.7; cursor: not-allowed; }
.btn-submit.loading .btn-text { opacity: 0; }
.btn-loader {
  display: none;
  width: 18px;
  height: 18px;
  border: 2px solid transparent;
  border-top-color: #1b1a19;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  position: absolute;
  top: 50%;
  left: 50%;
}
.btn-submit.loading .btn-loader { display: block; }

.flash-message {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  padding: 0.8rem 1rem;
  border-radius: 10px;
  margin-bottom: 1rem;
  font-size: 0.85rem;
}
.flash-message.error { background: rgba(255,71,87,0.08); border: 1px solid rgba(255,71,87,0.2); color: #d62839; }
.flash-message.success { background: rgba(46,213,115,0.08); border: 1px solid rgba(46,213,115,0.2); color: #1b8f52; }

.sucesso-box { text-align: center; margin-bottom: 1.3rem; }
.redirecionando { font-size: 0.92rem; color: #666666; margin-bottom: 0.6rem; }

.back-link { text-align: center; font-size: 0.88rem; color: #666666; }
.back-link a { color: #777777; text-decoration: none; font-size: 0.82rem; }

.link-alternar { background: none; border: none; color: #9E7A2E; font-weight: 700; cursor: pointer; text-decoration: none; }

@keyframes borda-dourada {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes spin { to { transform: translate(-50%, -50%) rotate(360deg); } }
</style>
