<template>
  <DefaultLayout>
    <div class="cadastro-page">
      <div class="cadastro-container">
        <h1>Cadastro de Usuário</h1>

        <div v-if="erro" class="flash-error"><p>{{ erro }}</p></div>
        <div v-if="sucesso" class="flash-success"><p>{{ sucesso }}</p></div>

        <form @submit.prevent="handleCadastro">
          <h2>Dados Pessoais</h2>
          <div class="form-grid">
            <input v-model="form.cpf"             type="text"     placeholder="CPF*"                maxlength="14" required />
            <input v-model="form.nome"            type="text"     placeholder="Nome*"               required />
            <input v-model="form.sobrenome"       type="text"     placeholder="Sobrenome*"          required />
            <input v-model="form.data_nascimento" type="date"     placeholder="Data de Nascimento*" required />
            <input v-model="form.email"           type="email"    placeholder="E-mail*"             required />
            <input v-model="form.senha"           type="password" placeholder="Senha*"              required />
            <input v-model="form.telefone"        type="tel"      placeholder="Telefone*"           required />
          </div>

          <button type="submit" class="btn-cadastrar" :disabled="loading">
            {{ loading ? 'Cadastrando...' : 'Cadastrar' }}
          </button>
        </form>

        <p class="login-link">
          Já tem uma conta? <router-link to="/login">Faça login</router-link>
        </p>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { cadastro } from '@/services/auth'
import DefaultLayout from '@/layouts/DefaultLayout.vue'

const router  = useRouter()
const loading = ref(false)
const erro    = ref('')
const sucesso = ref('')

const form = ref({
  cpf: '', nome: '', sobrenome: '',
  data_nascimento: '', email: '', senha: '', telefone: ''
})

async function handleCadastro() {
  erro.value = ''
  loading.value = true
  try {
    await cadastro(form.value)
    router.push('/login?cadastro=1')
  } catch (e) {
    erro.value = e.response?.data?.error || 'Erro ao cadastrar'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.cadastro-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--espacamento-sm);
  background: var(--gradiente-hero);
}

.cadastro-container {
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-lg);
  width: 100%;
  max-width: 900px;
  box-shadow: var(--sombra-destaque);
  border: 1px solid rgba(255, 215, 0, 0.2);
  position: relative;
  overflow: hidden;
  animation: fadeInUp 0.6s ease-out;
}

.cadastro-container::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--gradiente-botao);
}

.cadastro-container h1 {
  font-family: var(--fonte-secundaria);
  font-size: clamp(2rem, 4vw, 2.5rem);
  color: var(--cor-dourado);
  text-align: center;
  margin-bottom: var(--espacamento-md);
  font-weight: 600;
}

.cadastro-container h2 {
  font-family: var(--fonte-secundaria);
  font-size: 1.25rem;
  color: var(--cor-roxo-claro);
  margin: var(--espacamento-md) 0 var(--espacamento-sm) 0;
  padding-left: var(--espacamento-xs);
  border-left: 3px solid var(--cor-dourado);
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--espacamento-sm);
  margin-bottom: var(--espacamento-sm);
}

input {
  padding: 0.875rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--borda-radius-md);
  background: var(--cor-fundo);
  color: var(--cor-texto);
  font-family: var(--fonte-principal);
  font-size: 1rem;
  transition: all 0.3s ease;
  width: 100%;
}

input::placeholder { color: var(--cor-texto-secundario); opacity: 0.7; }

input:focus {
  outline: none;
  border-color: var(--cor-dourado);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

input:hover { border-color: rgba(255, 215, 0, 0.3); }

.btn-cadastrar {
  background: var(--gradiente-botao);
  color: var(--cor-fundo);
  border: none;
  padding: 1rem 2rem;
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  font-size: 1.1rem;
  display: block;
  margin: var(--espacamento-lg) auto var(--espacamento-sm);
  min-width: 200px;
}

.btn-cadastrar::before {
  content: '';
  position: absolute;
  top: 0; left: -100%;
  width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.btn-cadastrar:hover::before { left: 100%; }
.btn-cadastrar:hover { transform: translateY(-3px); box-shadow: var(--sombra-destaque); }
.btn-cadastrar:disabled { opacity: 0.7; cursor: not-allowed; transform: none; }

.flash-success {
  background: linear-gradient(135deg, #00ff88, #00cc66);
  color: var(--cor-fundo);
  padding: var(--espacamento-sm);
  border-radius: var(--borda-radius-md);
  margin-bottom: var(--espacamento-md);
  text-align: center;
  font-weight: 500;
}

.flash-error {
  background: linear-gradient(135deg, #ff4444, #cc0000);
  color: var(--cor-texto);
  padding: var(--espacamento-sm);
  border-radius: var(--borda-radius-md);
  margin-bottom: var(--espacamento-md);
  text-align: center;
  font-weight: 500;
}

.flash-success p, .flash-error p { margin: 0; }

.login-link {
  text-align: center;
  color: var(--cor-texto-secundario);
  margin-top: var(--espacamento-md);
}

.login-link a {
  color: var(--cor-dourado);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  position: relative;
}

.login-link a::after {
  content: '';
  position: absolute;
  bottom: -2px; left: 0;
  width: 0; height: 1px;
  background: var(--cor-dourado);
  transition: width 0.3s ease;
}

.login-link a:hover::after { width: 100%; }
.login-link a:hover { color: var(--cor-dourado-suave); }

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(30px); }
  to   { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .cadastro-container { padding: var(--espacamento-md); }
  .form-grid { grid-template-columns: 1fr; gap: var(--espacamento-xs); }
  .btn-cadastrar { width: 100%; }
}

@media (max-width: 480px) {
  .cadastro-container { padding: var(--espacamento-sm); border-radius: var(--borda-radius-md); }
  .cadastro-container h1 { font-size: 1.75rem; }
}
</style>