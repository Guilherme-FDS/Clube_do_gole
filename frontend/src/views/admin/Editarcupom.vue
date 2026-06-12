<template>
  <main class="editar-cupom-container">
    <div class="container">

      <div class="page-header fade-in">
        <span class="section-badge"><i class="fas fa-tags"></i> Administração</span>
        <h1 class="titulo-lg dourado">Editar Cupom</h1>
        <p class="texto-corrido texto-centro">Modifique as informações do cupom de desconto</p>
        <router-link to="/admin/cupons" class="btn-outline" style="margin-top:1rem; display:inline-flex">
          <i class="fas fa-arrow-left"></i> Voltar para Cupons
        </router-link>
      </div>

      <div v-if="msg" :class="['flash-msg', `flash-${msgTipo}`]">
        <i :class="msgTipo === 'sucesso' ? 'fas fa-check-circle' : 'fas fa-exclamation-circle'"></i>
        {{ msg }}
      </div>

      <div class="form-card fade-in" v-if="form.id">
        <form @submit.prevent="salvar">
          <div class="form-group">
            <label>Código do Cupom</label>
            <input v-model="form.codigo" type="text" required class="form-input" />
          </div>
          <div class="form-group">
            <label>Desconto (%)</label>
            <input v-model="form.desconto_percentual" type="number" min="1" max="100" required class="form-input" />
          </div>
          <div class="form-group">
            <label>Usos Máximos</label>
            <input v-model="form.usos_maximos" type="number" min="1" required class="form-input" />
            <small class="form-hint">Usos restantes atuais: {{ form.usos_restantes }}</small>
          </div>
          <div class="form-group">
            <label>Status</label>
            <select v-model="form.status" required class="form-input">
              <option value="ativo">Ativo</option>
              <option value="inativo">Inativo</option>
            </select>
          </div>
          <div class="form-actions">
            <router-link to="/admin/cupons" class="btn-outline">Cancelar</router-link>
            <button type="submit" class="btn-modern" :disabled="loading">
              <i class="fas fa-save"></i> {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
            </button>
          </div>
        </form>
      </div>

      <div v-else-if="!msg" class="texto-centro" style="padding: 4rem 0; color: var(--cor-texto-secundario)">
        <i class="fas fa-spinner fa-spin" style="font-size:2rem"></i>
      </div>

    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route   = useRoute()
const router  = useRouter()
const loading = ref(false)
const msg     = ref('')
const msgTipo = ref('sucesso')
const form    = ref({})

async function salvar() {
  loading.value = true
  try {
    await api.put(`/admin/cupons/${route.params.id}`, form.value)
    msg.value = 'Cupom atualizado com sucesso!'
    msgTipo.value = 'sucesso'
    setTimeout(() => router.push('/admin/cupons'), 1200)
  } catch {
    msg.value = 'Erro ao salvar alterações.'
    msgTipo.value = 'erro'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  try {
    const { data } = await api.get(`/admin/cupons/${route.params.id}`)
    form.value = data
    setTimeout(() => {
      document.querySelectorAll('.fade-in').forEach(el => el.classList.add('visible'))
    }, 50)
  } catch {
    msg.value = 'Erro ao carregar cupom.'
    msgTipo.value = 'erro'
  }
})
</script>

<style scoped>
.editar-cupom-container {
  min-height: 100vh;
  padding: 120px 0 var(--espacamento-xl);
  background: var(--gradiente-hero);
}

.page-header {
  text-align: center;
  margin-bottom: var(--espacamento-lg);
}

.form-card {
  max-width: 560px;
  margin: 0 auto;
  background: var(--cor-fundo-secundario);
  border: 1px solid rgba(201,168,76,0.2);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-md);
  box-shadow: var(--sombra-card);
  position: relative;
}

.form-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 3px;
  background: var(--gradiente-botao);
  border-radius: var(--borda-radius-lg) var(--borda-radius-lg) 0 0;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  margin-bottom: 1.25rem;
}

.form-group label {
  color: var(--cor-dourado);
  font-size: 0.875rem;
  font-weight: 600;
}

.form-input {
  background: var(--cor-fundo);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: var(--borda-radius-sm);
  color: var(--cor-texto);
  padding: 0.75rem 1rem;
  font-size: 0.95rem;
  transition: border-color 0.2s ease;
  width: 100%;
}

.form-input:focus {
  outline: none;
  border-color: var(--cor-dourado);
  box-shadow: 0 0 0 3px rgba(201,168,76,0.1);
}

.form-hint {
  color: var(--cor-texto-secundario);
  font-size: 0.8rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: var(--espacamento-md);
}

.flash-msg {
  max-width: 560px;
  margin: 0 auto var(--espacamento-sm);
  padding: 0.875rem 1rem;
  border-radius: var(--borda-radius-sm);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
}

.flash-sucesso {
  background: rgba(76,175,80,0.1);
  border: 1px solid rgba(76,175,80,0.3);
  color: #4CAF50;
}

.flash-erro {
  background: rgba(244,67,54,0.1);
  border: 1px solid rgba(244,67,54,0.3);
  color: #f44336;
}

/* ===== ERP LIGHT THEME (sobrescreve o tema escuro acima) ===== */
.editar-cupom-container {
  background: #F4F5F7;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
}
.page-header { text-align: left; max-width: 560px; margin: 0 auto var(--espacamento-lg); }
.page-header :deep(.titulo-lg),
.page-header h1 {
  font-family: 'DM Sans', 'Segoe UI', sans-serif !important;
  font-size: 22px !important;
  font-weight: 700;
  color: #1B1A19 !important;
  text-align: left;
}
.page-header :deep(p) { color: #6B7280 !important; font-size: 13px; text-align: left; }
.form-card {
  background: #FFFFFF;
  border: 1px solid #E3E5E8;
  border-radius: 12px;
  box-shadow: none;
}
.form-card::before { display: none; }
.form-group label { color: #4B5563; font-size: 12px; }
.form-input {
  background: #FFFFFF;
  border: 1px solid #D6D9DE;
  color: #1B1A19;
  font-family: inherit;
}
.form-input:focus { border-color: #C9A84C; box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.15); }
.form-hint { color: #9CA3AF; }
.flash-sucesso { background: #EBF8F0; border-color: #2E8B57; color: #2E8B57; }
.flash-erro { background: #FEF2F2; border-color: #DC2626; color: #DC2626; }
</style>