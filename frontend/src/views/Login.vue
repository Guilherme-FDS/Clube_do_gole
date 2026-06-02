<template>
  <section class="login-page">
    <div class="card-login-borda">
      <div class="card-viewport">
        <Transition name="card-switch" mode="out-in">
          <article v-if="!modoCadastro" key="login" class="card-login">
            <header class="topo">
              <span class="chip">Clube do Gole</span>
              <h1>Entrar</h1>
              <p class="subtitulo">Digite seu email e senha para acessar sua conta.</p>
            </header>

            <div v-if="flashMensagem" :class="['flash-message', flashMensagem.tipo]">
              <i :class="flashIcon"></i>
              <p>{{ flashMensagem.texto }}</p>
            </div>

            <Transition name="fade-slide" mode="out-in">
              <div v-if="!modoEsqueceuSenha" key="login-form">
                <form class="form-login" @submit.prevent="handleLogin">
                  <div class="campo">
                    <label for="email-login">Email</label>
                    <input id="email-login" v-model="email" type="email" placeholder="seu@email.com" required />
                  </div>
                  <div class="campo">
                    <label for="senha-login">Senha</label>
                    <input id="senha-login" v-model="senha" type="password" placeholder="••••••••" required />
                  </div>
                  <div class="esqueceu-link">
                    <button type="button" class="link-alternar" @click="modoEsqueceuSenha = true">Esqueceu sua senha?</button>
                  </div>
                  <button type="submit" class="btn-submit" :class="{ loading: carregando }" :disabled="carregando">
                    <span class="btn-text">Entrar</span>
                    <div class="btn-loader"></div>
                  </button>
                </form>

                <div class="divisor-oauth"><span>ou continue com</span></div>

                <div class="oauth-botoes">
                  <button class="btn-oauth" @click="entrarGoogle" type="button">
                    <svg width="18" height="18" viewBox="0 0 48 48"><path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/><path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/><path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/><path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.18 1.48-4.97 2.31-8.16 2.31-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/></svg>
                    Google
                  </button>
                  <button class="btn-oauth btn-oauth--disabled" type="button" disabled title="Em breve">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="#aaa"><path d="M24 12.073C24 5.405 18.627 0 12 0S0 5.405 0 12.073C0 18.1 4.388 23.094 10.125 24v-8.437H7.078v-3.49h3.047V9.41c0-3.025 1.792-4.697 4.533-4.697 1.312 0 2.686.235 2.686.235v2.97h-1.513c-1.491 0-1.956.93-1.956 1.874v2.25h3.328l-.532 3.49h-2.796V24C19.612 23.094 24 18.1 24 12.073z"/></svg>
                    Facebook <span style="font-size:0.7rem;opacity:0.6">(em breve)</span>
                  </button>                  
                </div>

                <p class="rodape-card">
                  Ainda não tem conta?
                  <button type="button" class="link-alternar" @click="irParaCadastro">Criar cadastro</button>
                </p>
                <div class="back-link">
                  <router-link to="/">Voltar para o início</router-link>
                </div>
              </div>

              <div v-else key="esqueceu-form">
                <header class="topo" style="margin-bottom:1rem">
                  <h1 style="font-size:1.5rem">Recuperar senha</h1>
                  <p class="subtitulo">Informe seu email e enviaremos um link de recuperação.</p>
                </header>
                <form class="form-login" @submit.prevent="handleEsqueceuSenha">
                  <div class="campo">
                    <label>Email</label>
                    <input v-model="emailRecuperacao" type="email" placeholder="seu@email.com" required />
                  </div>
                  <button type="submit" class="btn-submit" :class="{ loading: carregando }" :disabled="carregando">
                    <span class="btn-text">Enviar link</span>
                    <div class="btn-loader"></div>
                  </button>
                </form>
                <p class="rodape-card" style="margin-top:1rem">
                  <button type="button" class="link-alternar" @click="modoEsqueceuSenha = false">← Voltar ao login</button>
                </p>
              </div>
            </Transition>
          </article>

          <article v-else key="cadastro" class="card-login">
            <header class="topo">
              <span class="chip">Clube do Gole</span>
              <h1>Criar conta</h1>
              <p class="subtitulo">Informe os dados para se cadastrar.</p>
            </header>

            <div v-if="flashMensagem" :class="['flash-message', flashMensagem.tipo]">
              <i :class="flashIcon"></i>
              <p>{{ flashMensagem.texto }}</p>
            </div>

            <form class="form-login" @submit.prevent="handleCadastro">
              <div class="campo">
                <label>Nome</label>
                <input v-model="nomeCadastro" type="text" placeholder="Seu nome" required />
              </div>
              <div class="campo">
                <label>Sobrenome</label>
                <input v-model="sobrenomeCadastro" type="text" placeholder="Seu sobrenome" required />
              </div>
              <div class="campo">
                <label>CPF</label>
                <input :value="cpfCadastro" @input="formatarCPF" type="text" placeholder="000.000.000-00" maxlength="14" required />
              </div>
              <div class="campo">
                <label>Email</label>
                <input v-model="emailCadastro" type="email" placeholder="seu@email.com" required />
              </div>
              <div class="campo">
                <label>Senha</label>
                <input v-model="senhaCadastro" type="password" placeholder="••••••••" required />
              </div>
              <div class="campo">
                <label>Telefone</label>
                <input v-model="telefoneCadastro" type="tel" placeholder="(00) 00000-0000" required />
              </div>
              <div class="campo">
                <label>Data de Nascimento</label>
                <input v-model="nascimentoCadastro" type="date" required />
              </div>
              <button type="submit" class="btn-submit" :class="{ loading: carregando }" :disabled="carregando">
                <span class="btn-text">Cadastrar</span>
                <div class="btn-loader"></div>
              </button>
            </form>

            <p class="rodape-card">
              Já tem conta?
              <button type="button" class="link-alternar" @click="irParaLogin">Voltar ao login</button>
            </p>
          </article>
        </Transition>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { cadastro as apiCadastro, esqueceuSenha, getGoogleAuthUrl, getFacebookAuthUrl } from '@/services/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const modoCadastro = ref(false)
const modoEsqueceuSenha = ref(false)
const email = ref('')
const senha = ref('')
const emailRecuperacao = ref('')
const nomeCadastro = ref('')
const sobrenomeCadastro = ref('')
const cpfCadastro = ref('')
const emailCadastro = ref('')
const senhaCadastro = ref('')
const telefoneCadastro = ref('')
const nascimentoCadastro = ref('')
const carregando = ref(false)
const flashMensagem = ref(null)

const flashIcon = computed(() => {
  if (!flashMensagem.value) return ''
  if (flashMensagem.value.tipo === 'error') return 'fas fa-exclamation-circle'
  if (flashMensagem.value.tipo === 'success') return 'fas fa-check-circle'
  return 'fas fa-info-circle'
})

function mostrarMensagem(texto, tipo = 'error') {
  flashMensagem.value = { texto, tipo }
}

function tratarErroLogin(e) {
  const status = e?.response?.status
  const detail = e?.response?.data?.detail
  const message = e?.message
  if (status === 401 || status === 400) return 'Email ou senha incorretos.'
  if (status === 422) return 'Verifique se o email e a senha foram preenchidos corretamente.'
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) return detail.map((d) => d.msg).join(' ')
  if (message === 'Network Error') return 'Não foi possível conectar ao servidor. Verifique se o backend está rodando.'
  return message || 'Não foi possível fazer login.'
}

function irParaCadastro() { flashMensagem.value = null; modoCadastro.value = true }
function irParaLogin() { flashMensagem.value = null; modoCadastro.value = false }

watch(modoCadastro, () => { flashMensagem.value = null })
watch(modoEsqueceuSenha, () => { flashMensagem.value = null })

function entrarGoogle() { window.location.href = getGoogleAuthUrl() }
function entrarFacebook() { window.location.href = getFacebookAuthUrl() }

async function handleLogin() {
  if (!email.value || !senha.value) return mostrarMensagem('Preencha email e senha.')
  carregando.value = true
  flashMensagem.value = null
  try {
    await authStore.entrar(email.value, senha.value)
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch (e) {
    mostrarMensagem(tratarErroLogin(e), 'error')
  } finally {
    carregando.value = false
  }
}

async function handleEsqueceuSenha() {
  if (!emailRecuperacao.value) return mostrarMensagem('Informe o email.')
  carregando.value = true
  flashMensagem.value = null
  try {
    await esqueceuSenha(emailRecuperacao.value)
    mostrarMensagem('Email de recuperação enviado!', 'success')
    emailRecuperacao.value = ''
  } catch (e) {
    mostrarMensagem(tratarErroLogin(e), 'error')
  } finally {
    carregando.value = false
  }
}

async function handleCadastro() {
  if (!nomeCadastro.value || !sobrenomeCadastro.value || !cpfCadastro.value ||
      !emailCadastro.value || !senhaCadastro.value || !telefoneCadastro.value || !nascimentoCadastro.value) {
    return mostrarMensagem('Preencha todos os campos.')
  }
  if (senhaCadastro.value.length < 6) return mostrarMensagem('A senha deve ter no mínimo 6 caracteres.')
  carregando.value = true
  flashMensagem.value = null
  try {
    await apiCadastro({
      nome: nomeCadastro.value,
      sobrenome: sobrenomeCadastro.value,
      cpf: cpfCadastro.value.replace(/\D/g, ''),
      email: emailCadastro.value,
      senha: senhaCadastro.value,
      telefone: telefoneCadastro.value.replace(/\D/g, ''),
      data_nascimento: nascimentoCadastro.value,
    })
    mostrarMensagem('Cadastro realizado! Faça login.', 'success')
    email.value = emailCadastro.value
    senha.value = ''
    modoCadastro.value = false
  } catch (e) {
    mostrarMensagem(tratarErroLogin(e), 'error')
  } finally {
    carregando.value = false
  }
}

function formatarCPF(e) {
  let v = e.target.value.replace(/\D/g, '').slice(0, 11)
  v = v.replace(/(\d{3})(\d)/, '$1.$2')
  v = v.replace(/(\d{3})(\d)/, '$1.$2')
  v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2')
  cpfCadastro.value = v
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

.esqueceu-link { text-align: right; margin-top: -0.4rem; }
.esqueceu-link .link-alternar { font-size: 0.82rem; font-weight: 600; }

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

.divisor-oauth {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin: 1.2rem 0 1rem;
  color: #aaa;
  font-size: 0.8rem;
}
.divisor-oauth::before,
.divisor-oauth::after { content: ''; flex: 1; height: 1px; background: #e2e2e2; }

.oauth-botoes { display: flex; gap: 0.75rem; margin-bottom: 1.2rem; }

.btn-oauth {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.72rem;
  border-radius: 11px;
  border: 1px solid #e2e2e2;
  background: #fafafa;
  color: #1b1a19;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.btn-oauth:hover { border-color: #C9A84C; box-shadow: 0 0 0 3px rgba(201,168,76,0.1); }

.btn-oauth--disabled { opacity: 0.45; cursor: not-allowed; }

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

.rodape-card, .back-link { text-align: center; font-size: 0.88rem; color: #666666; }

.link-alternar { background: none; border: none; color: #9E7A2E; font-weight: 700; cursor: pointer; }

.back-link a { color: #777777; text-decoration: none; font-size: 0.82rem; }

.fade-slide-enter-active, .fade-slide-leave-active { transition: opacity 0.2s, transform 0.2s; }
.fade-slide-enter-from { opacity: 0; transform: translateY(8px); }
.fade-slide-leave-to { opacity: 0; transform: translateY(-8px); }

@keyframes borda-dourada {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes spin { to { transform: translate(-50%, -50%) rotate(360deg); } }
</style>