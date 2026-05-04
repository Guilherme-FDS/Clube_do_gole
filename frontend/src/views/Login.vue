<template>
  <DefaultLayout>
    <div class="login-page">
      <div class="login-container">
        <div class="login-box fade-in">
          <div class="login-header">
            <h2 class="titulo-lg">Bem-vindo de volta!</h2>
            <p class="texto-corrido">Faça login para continuar</p>
          </div>

          <div v-if="erro" class="flash-message error">
            <div class="flash-icon"><i class="fas fa-exclamation-circle"></i></div>
            <div class="flash-content"><p>{{ erro }}</p></div>
          </div>

          <div v-if="sucesso" class="flash-message success">
            <div class="flash-icon"><i class="fas fa-check-circle"></i></div>
            <div class="flash-content"><p>{{ sucesso }}</p></div>
          </div>

          <form class="login-form" @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="email" class="form-label">Email</label>
              <div class="input-container" :class="{ focused: focusEmail }">
                <i class="fas fa-envelope input-icon"></i>
                <input
                  v-model="form.email"
                  type="email" id="email"
                  placeholder="seu@email.com"
                  class="form-input"
                  required
                  @focus="focusEmail = true"
                  @blur="focusEmail = !!form.email"
                />
              </div>
            </div>

            <div class="form-group">
              <label for="senha" class="form-label">Senha</label>
              <div class="input-container" :class="{ focused: focusSenha }">
                <i class="fas fa-lock input-icon"></i>
                <input
                  v-model="form.senha"
                  :type="mostrarSenha ? 'text' : 'password'"
                  id="senha"
                  placeholder="••••••••"
                  class="form-input"
                  required
                  @focus="focusSenha = true"
                  @blur="focusSenha = !!form.senha"
                />
                <button type="button" class="password-toggle" @click="mostrarSenha = !mostrarSenha" aria-label="Mostrar senha">
                  <i :class="mostrarSenha ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
                </button>
              </div>
            </div>

            <button type="submit" class="btn-login" :class="{ loading }" :disabled="loading">
              <span class="btn-text" v-if="!loading">Entrar</span>
              <div class="btn-loader" v-else></div>
            </button>
          </form>

          <div class="divider"><span>Ou continue com</span></div>

          <div class="social-login">
            <button class="btn-social google" type="button" @click="socialInfo('Google')">
              <i class="fab fa-google"></i><span>Entrar com Google</span>
            </button>
            <button class="btn-social facebook" type="button" @click="socialInfo('Facebook')">
              <i class="fab fa-facebook-f"></i><span>Entrar com Facebook</span>
            </button>
          </div>

          <div class="login-links">
            <div class="signup-link">
              Não tem uma conta? <router-link to="/cadastro" class="link-accent">Cadastre-se</router-link>
            </div>
            <div class="back-link">
              <router-link to="/" class="link-secondary">
                <i class="fas fa-arrow-left"></i> Voltar para página inicial
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const auth   = useAuthStore()
const router = useRouter()
const route  = useRoute()

const form        = ref({ email: '', senha: '' })
const erro        = ref('')
const sucesso     = ref(route.query.cadastro ? 'Cadastro realizado! Faça login.' : '')
const loading     = ref(false)
const mostrarSenha = ref(false)
const focusEmail  = ref(false)
const focusSenha  = ref(false)

async function handleLogin() {
  erro.value = ''
  loading.value = true
  try {
    const data = await auth.entrar(form.value.email, form.value.senha)
    const redirect = route.query.redirect || (data.tipo === 'admin' ? '/admin' : '/')
    router.push(redirect)
  } catch (e) {
    erro.value = e.response?.data?.error || 'Erro ao fazer login'
  } finally {
    loading.value = false
  }
}

function socialInfo(rede) {
  erro.value = `Login com ${rede} em desenvolvimento.`
}

onMounted(() => {
  document.querySelectorAll('.fade-in').forEach((el, i) => {
    el.style.transitionDelay = `${i * 0.1}s`
    el.classList.add('visible')
  })
})
</script>

<style scoped>
:root {
  --cor-fundo: #000000;
  --cor-fundo-secundario: #0F0F0F;
  --cor-dourado: #FFD700;
  --cor-dourado-suave: #F4D03F;
  --cor-roxo-principal: #8A2BE2;
  --cor-roxo-escuro: #4B0082;
  --cor-texto: #FFFFFF;
  --cor-texto-secundario: #CCCCCC;
  --cor-erro: #ff4757;
  --cor-sucesso: #2ed573;
  --gradiente-hero: linear-gradient(135deg, var(--cor-roxo-escuro) 0%, var(--cor-fundo) 100%);
  --gradiente-botao: linear-gradient(45deg, var(--cor-roxo-principal), var(--cor-dourado));
  --sombra-destaque: 0 10px 25px rgba(139, 0, 255, 0.3);
  --sombra-input: 0 2px 10px rgba(139, 0, 255, 0.1);
  --borda-radius-md: 12px;
  --borda-radius-lg: 20px;
  --espacamento-xs: 0.5rem;
  --espacamento-sm: 1rem;
  --espacamento-md: 2rem;
  --espacamento-lg: 4rem;
  --espacamento-xl: 6rem;
  --transicao-rapida: 0.2s ease;
  --transicao-normal: 0.3s ease;
  --transicao-lenta: 0.5s ease;
  --fonte-principal: 'Inter', sans-serif;
  --fonte-secundaria: 'Playfair Display', serif;
}

.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 120px 20px 80px;
  background: var(--gradiente-hero);
  position: relative;
}
.login-page::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 20% 80%, rgba(120,0,255,0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255,215,0,0.1) 0%, transparent 50%);
  z-index: 1;
}
.login-container { width: 100%; max-width: 480px; position: relative; z-index: 2; }
.login-box {
  background: #0F0F0F;
  border: 1px solid rgba(255,215,0,0.2);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-xl);
  width: 100%;
  text-align: center;
  box-shadow: var(--sombra-destaque);
  backdrop-filter: blur(10px);
}
.login-header { margin-bottom: var(--espacamento-lg); }

.titulo-lg {
  font-family: var(--fonte-secundaria);
  font-size: clamp(1.5rem, 3vw, 2rem);
  font-weight: 600;
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-xs);
}
.texto-corrido { font-size: 1.125rem; line-height: 1.6; color: var(--cor-texto-secundario); }

/* Flash */
.flash-message {
  display: flex; align-items: center; gap: var(--espacamento-sm);
  padding: var(--espacamento-sm);
  border-radius: var(--borda-radius-md);
  margin-bottom: var(--espacamento-md);
  text-align: left;
  animation: slideIn 0.3s ease;
}
.flash-message.error  { background: rgba(255,71,87,0.1); border: 1px solid var(--cor-erro); color: var(--cor-erro); }
.flash-message.success{ background: rgba(46,213,115,0.1); border: 1px solid var(--cor-sucesso); color: var(--cor-sucesso); }
.flash-icon { font-size: 1.25rem; flex-shrink: 0; }
.flash-content p { margin: 0; font-size: 0.95rem; font-weight: 500; }

/* Form */
.login-form { margin-bottom: var(--espacamento-lg); }
.form-group { margin-bottom: var(--espacamento-md); text-align: left; }
.form-label { display: block; color: var(--cor-texto); margin-bottom: var(--espacamento-xs); font-weight: 500; font-size: 0.95rem; }
.input-container { position: relative; display: flex; align-items: center; transition: all var(--transicao-normal); }
.input-container.focused { transform: translateY(-1px); }
.input-container.focused .input-icon { color: var(--cor-dourado); }
.input-icon { position: absolute; left: 1rem; color: var(--cor-texto-secundario); font-size: 1rem; z-index: 2; transition: color var(--transicao-normal); }
.form-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  background: #000;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: var(--borda-radius-md);
  color: var(--cor-texto);
  font-size: 1rem;
  transition: all var(--transicao-normal);
  box-shadow: var(--sombra-input);
}
.form-input:focus { outline: none; border-color: var(--cor-dourado); box-shadow: 0 0 0 3px rgba(255,215,0,0.1); }
.form-input::placeholder { color: var(--cor-texto-secundario); }
.password-toggle {
  position: absolute; right: 1rem;
  background: none; border: none;
  color: var(--cor-texto-secundario);
  cursor: pointer; padding: 0.25rem;
  transition: all var(--transicao-rapida); z-index: 2;
}
.password-toggle:hover { color: var(--cor-dourado); transform: scale(1.1); }

/* Botão login */
.btn-login {
  width: 100%;
  background: var(--gradiente-botao);
  color: #000;
  border: none;
  padding: 1rem 2rem;
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transicao-normal);
  position: relative;
  overflow: hidden;
  font-size: 1.1rem;
  min-height: 54px;
}
.btn-login::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left var(--transicao-lenta);
}
.btn-login:hover:not(.loading)::before { left: 100%; }
.btn-login:hover:not(.loading) { transform: translateY(-2px); box-shadow: var(--sombra-destaque); }
.btn-login.loading { cursor: not-allowed; opacity: 0.8; }
.btn-loader {
  width: 20px; height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid #000;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

/* Divisor */
.divider { position: relative; margin: var(--espacamento-lg) 0; color: var(--cor-texto-secundario); font-size: 0.9rem; }
.divider::before { content: ''; position: absolute; top: 50%; left: 0; right: 0; height: 1px; background: rgba(255,255,255,0.1); }
.divider span { background: #0F0F0F; padding: 0 var(--espacamento-sm); position: relative; z-index: 1; }

/* Social */
.social-login { display: flex; flex-direction: column; gap: var(--espacamento-sm); margin-bottom: var(--espacamento-lg); }
.btn-social {
  display: flex; align-items: center; justify-content: center;
  gap: var(--espacamento-sm);
  padding: 1rem;
  border: 1px solid rgba(255,255,255,0.1);
  background: #000;
  color: var(--cor-texto);
  border-radius: var(--borda-radius-md);
  cursor: pointer;
  font-size: 1rem; font-weight: 500;
  transition: all var(--transicao-normal);
  position: relative; overflow: hidden;
}
.btn-social:hover { transform: translateY(-2px); border-color: var(--cor-dourado); }
.btn-social.google:hover  { background: #DB4437; color: #fff; }
.btn-social.facebook:hover{ background: #4267B2; color: #fff; }

/* Links */
.login-links { display: flex; flex-direction: column; gap: var(--espacamento-sm); }
.signup-link { color: var(--cor-texto-secundario); font-size: 0.95rem; }
.link-accent { color: var(--cor-dourado); text-decoration: none; font-weight: 600; transition: color var(--transicao-normal); }
.link-accent:hover { color: var(--cor-roxo-principal); }
.link-secondary {
  color: var(--cor-texto-secundario); text-decoration: none; font-size: 0.9rem;
  display: flex; align-items: center; justify-content: center;
  gap: 0.5rem; transition: color var(--transicao-normal);
}
.link-secondary:hover { color: var(--cor-dourado); }

/* Animações */
.fade-in { opacity: 0; transform: translateY(30px); transition: all var(--transicao-lenta); }
.fade-in.visible { opacity: 1; transform: translateY(0); }

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-10px); }
  to   { opacity: 1; transform: translateY(0); }
}
@keyframes spin {
  0%   { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Responsividade */
@media (max-width: 768px) {
  .login-box { padding: var(--espacamento-lg) var(--espacamento-md); }
  .login-page { padding: 100px var(--espacamento-sm) 60px; }
}
@media (max-width: 480px) {
  .login-box { padding: var(--espacamento-lg) var(--espacamento-sm); }
  .form-input { padding: 0.875rem 0.875rem 0.875rem 2.5rem; }
  .input-icon { left: 0.875rem; }
  .password-toggle { right: 0.875rem; }
}
</style>