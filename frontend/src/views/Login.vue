<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-box fade-in" :class="{ visible: fadeInVisible }">
        <div class="login-header">
          <h2 class="titulo-lg">Bem-vindo de volta!</h2>
          <p class="texto-corrido">Faça login para continuar</p>
        </div>

        <!-- Mensagens flash (erro / sucesso) -->
        <div v-if="flashMensagem" :class="['flash-message', flashMensagem.tipo]">
          <div class="flash-icon">
            <i :class="flashIcon"></i>
          </div>
          <div class="flash-content">
            <p>{{ flashMensagem.texto }}</p>
          </div>
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <div class="input-container" :class="{ focused: emailFocused || email }">
              <i class="fas fa-envelope input-icon"></i>
              <input type="email" id="email" v-model="email" placeholder="seu@email.com"
                     class="form-input" required @focus="emailFocused = true" @blur="emailFocused = false">
            </div>
          </div>

          <div class="form-group">
            <label for="senha" class="form-label">Senha</label>
            <div class="input-container" :class="{ focused: senhaFocused || senha }">
              <i class="fas fa-lock input-icon"></i>
              <input :type="senhaVisivel ? 'text' : 'password'" id="senha" v-model="senha"
                     placeholder="••••••••" class="form-input" required
                     @focus="senhaFocused = true" @blur="senhaFocused = false">
              <button type="button" class="password-toggle" @click="toggleSenhaVisivel"
                      :aria-label="senhaVisivel ? 'Ocultar senha' : 'Mostrar senha'">
                <i :class="senhaVisivel ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
              </button>
            </div>
          </div>

          <button type="submit" class="btn-login" :class="{ loading: carregando }" :disabled="carregando">
            <span class="btn-text">Entrar</span>
            <div class="btn-loader"></div>
          </button>
        </form>

        <div class="divider">
          <span>Ou continue com</span>
        </div>

        <div class="social-login">
          <button type="button" class="btn-social google" @click="socialLogin('google')" :disabled="carregandoSocial">
            <i class="fab fa-google"></i>
            <span>Entrar com Google</span>
          </button>
          <button type="button" class="btn-social facebook" @click="socialLogin('facebook')" :disabled="carregandoSocial">
            <i class="fab fa-facebook-f"></i>
            <span>Entrar com Facebook</span>
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
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// Dados do formulário
const email = ref('')
const senha = ref('')
const senhaVisivel = ref(false)
const carregando = ref(false)
const carregandoSocial = ref(false)
const flashMensagem = ref(null)

// Estados de foco para animação
const emailFocused = ref(false)
const senhaFocused = ref(false)
const fadeInVisible = ref(false)

// Ícone da mensagem flash
const flashIcon = computed(() => {
  if (!flashMensagem.value) return ''
  const tipo = flashMensagem.value.tipo
  if (tipo === 'error') return 'fas fa-exclamation-circle'
  if (tipo === 'success') return 'fas fa-check-circle'
  return 'fas fa-info-circle'
})

// Mostrar mensagem temporária
function mostrarMensagem(texto, tipo = 'error') {
  flashMensagem.value = { texto, tipo }
  // Auto-remover após 5 segundos
  setTimeout(() => {
    flashMensagem.value = null
  }, 5000)
}

// Alternar visibilidade da senha
function toggleSenhaVisivel() {
  senhaVisivel.value = !senhaVisivel.value
}

// Login normal
async function handleLogin() {
  // Validação visual básica
  if (!email.value || !senha.value) {
    mostrarMensagem('Preencha todos os campos.', 'error')
    return
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    mostrarMensagem('Por favor, insira um email válido.', 'error')
    return
  }

  carregando.value = true
  try {
    await authStore.entrar(email.value, senha.value)
    // Login bem-sucedido: redireciona conforme parâmetro 'redirect' ou para página inicial
    const redirectTo = route.query.redirect || '/'
    router.push(redirectTo)
  } catch (error) {
    console.error('Erro no login:', error)
    mostrarMensagem(error.message || 'Email ou senha inválidos.', 'error')
  } finally {
    carregando.value = false
  }
}

// Login social (apenas simulação para as telas, conforme código original)
async function socialLogin(provedor) {
  carregandoSocial.value = true
  setTimeout(() => {
    mostrarMensagem(`Login com ${provedor} em desenvolvimento.`, 'info')
    carregandoSocial.value = false
  }, 1500)
}

// Animação de entrada
onMounted(() => {
  setTimeout(() => {
    fadeInVisible.value = true
  }, 100)

  // Se houver parâmetro de erro na URL (ex: ?error=...), exibe mensagem
  if (route.query.error) {
    mostrarMensagem(decodeURIComponent(route.query.error), 'error')
  }
  if (route.query.success) {
    mostrarMensagem(decodeURIComponent(route.query.success), 'success')
  }
})
</script>

<style scoped>
/* ===== ESTILOS EXCLUSIVOS DA PÁGINA DE LOGIN ===== */
/* (Os estilos globais já fornecem variáveis, reset, tipografia, etc. 
   Apenas o necessário para este layout) */

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
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 80%, rgba(120, 0, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 215, 0, 0.1) 0%, transparent 50%);
  z-index: 1;
}

.login-container {
  width: 100%;
  max-width: 480px;
  position: relative;
  z-index: 2;
}

.login-box {
  background: var(--cor-fundo-secundario);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-xl);
  width: 100%;
  text-align: center;
  box-shadow: var(--sombra-destaque);
  backdrop-filter: blur(10px);
}

.login-header {
  margin-bottom: var(--espacamento-lg);
}

/* Mensagens flash */
.flash-message {
  display: flex;
  align-items: center;
  gap: var(--espacamento-sm);
  padding: var(--espacamento-sm);
  border-radius: var(--borda-radius-md);
  margin-bottom: var(--espacamento-md);
  text-align: left;
  animation: slideIn 0.3s ease;
}

.flash-message.error {
  background: rgba(255, 71, 87, 0.1);
  border: 1px solid var(--cor-erro);
  color: var(--cor-erro);
}

.flash-message.success {
  background: rgba(46, 213, 115, 0.1);
  border: 1px solid var(--cor-sucesso);
  color: var(--cor-sucesso);
}

.flash-message.info {
  background: rgba(55, 66, 250, 0.1);
  border: 1px solid var(--cor-info);
  color: var(--cor-info);
}

.flash-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.flash-content {
  flex: 1;
}

.flash-content p {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 500;
}

/* Formulário */
.login-form {
  margin-bottom: var(--espacamento-lg);
}

.form-group {
  margin-bottom: var(--espacamento-md);
  text-align: left;
}

.form-label {
  display: block;
  color: var(--cor-texto);
  margin-bottom: var(--espacamento-xs);
  font-weight: 500;
  font-size: 0.95rem;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
  transition: all var(--transicao-normal);
}

.input-container.focused {
  transform: translateY(-1px);
}

.input-container.focused .input-icon {
  color: var(--cor-dourado);
}

.input-icon {
  position: absolute;
  left: 1rem;
  color: var(--cor-texto-secundario);
  font-size: 1rem;
  z-index: 2;
  transition: color var(--transicao-normal);
}

.form-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  background: var(--cor-fundo);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--borda-radius-md);
  color: var(--cor-texto);
  font-size: 1rem;
  transition: all var(--transicao-normal);
  box-shadow: var(--sombra-input);
}

.form-input:focus {
  outline: none;
  border-color: var(--cor-dourado);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

.password-toggle {
  position: absolute;
  right: 1rem;
  background: none;
  border: none;
  color: var(--cor-texto-secundario);
  cursor: pointer;
  padding: 0.25rem;
  transition: all var(--transicao-rapida);
  z-index: 2;
}

.password-toggle:hover {
  color: var(--cor-dourado);
  transform: scale(1.1);
}

/* Botão de login */
.btn-login {
  width: 100%;
  background: var(--gradiente-botao);
  color: var(--cor-fundo);
  border: none;
  padding: 1rem 2rem;
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transicao-normal);
  position: relative;
  overflow: hidden;
  font-size: 1.1rem;
}

.btn-login::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left var(--transicao-lenta);
}

.btn-login:hover:not(:disabled)::before {
  left: 100%;
}

.btn-login:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--sombra-destaque);
}

.btn-login.loading {
  cursor: not-allowed;
  opacity: 0.8;
}

.btn-login.loading .btn-text {
  opacity: 0;
}

.btn-loader {
  display: none;
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid var(--cor-fundo);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.btn-login.loading .btn-loader {
  display: block;
}

/* Divisor */
.divider {
  position: relative;
  margin: var(--espacamento-lg) 0;
  color: var(--cor-texto-secundario);
  font-size: 0.9rem;
}

.divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background: rgba(255, 255, 255, 0.1);
}

.divider span {
  background: var(--cor-fundo-secundario);
  padding: 0 var(--espacamento-sm);
  position: relative;
  z-index: 1;
}

/* Login social */
.social-login {
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-sm);
  margin-bottom: var(--espacamento-lg);
}

.btn-social {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--espacamento-sm);
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  background: var(--cor-fundo);
  color: var(--cor-texto);
  border-radius: var(--borda-radius-md);
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all var(--transicao-normal);
  position: relative;
  overflow: hidden;
}

.btn-social::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  transition: left var(--transicao-lenta);
}

.btn-social:hover:not(:disabled)::before {
  left: 100%;
}

.btn-social:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--sombra-suave);
  border-color: var(--cor-dourado);
}

.btn-social.google {
  color: #DB4437;
}
.btn-social.google:hover:not(:disabled) {
  background: #DB4437;
  color: var(--cor-texto);
}
.btn-social.facebook {
  color: #4267B2;
}
.btn-social.facebook:hover:not(:disabled) {
  background: #4267B2;
  color: var(--cor-texto);
}

/* Links */
.login-links {
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-sm);
}
.signup-link {
  color: var(--cor-texto-secundario);
  font-size: 0.95rem;
}
.link-accent {
  color: var(--cor-dourado);
  text-decoration: none;
  font-weight: 600;
  transition: color var(--transicao-normal);
}
.link-accent:hover {
  color: var(--cor-roxo-principal);
}
.link-secondary {
  color: var(--cor-texto-secundario);
  text-decoration: none;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  transition: color var(--transicao-normal);
}
.link-secondary:hover {
  color: var(--cor-dourado);
}

/* Animações */
.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: all var(--transicao-lenta);
}
.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}
@keyframes spin {
  0% { transform: translate(-50%, -50%) rotate(0deg); }
  100% { transform: translate(-50%, -50%) rotate(360deg); }
}

/* Responsividade */
@media (max-width: 768px) {
  .login-box {
    padding: var(--espacamento-lg) var(--espacamento-md);
    margin: 0 var(--espacamento-sm);
  }
  .login-page {
    padding: 100px var(--espacamento-sm) 60px;
  }
  .btn-social {
    padding: 0.875rem;
    font-size: 0.95rem;
  }
}

@media (max-width: 480px) {
  .login-box {
    padding: var(--espacamento-lg) var(--espacamento-sm);
  }
  .form-input {
    padding: 0.875rem 0.875rem 0.875rem 2.5rem;
  }
  .input-icon {
    left: 0.875rem;
  }
  .password-toggle {
    right: 0.875rem;
  }
}
</style>