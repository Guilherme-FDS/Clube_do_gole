<template>
  <DefaultLayout>
    <main class="cupons-container">
      <div class="container">
        <div class="cupons-header fade-in">
          <h1><i class="fas fa-edit"></i> Editar Cupom</h1>
          <p>Modifique as informações do cupom de desconto</p>
          <router-link to="/admin/cupons" class="btn-voltar"><i class="fas fa-arrow-left"></i> Voltar para Cupons</router-link>
        </div>

        <div v-if="msg" :class="`flash-${msgTipo}`">{{ msg }}</div>

        <div class="form-container fade-in" v-if="form.codigo">
          <form @submit.prevent="salvar">
            <div class="form-group"><label>Código do Cupom:</label><input v-model="form.codigo" type="text" required class="form-input" /></div>
            <div class="form-group"><label>Desconto (%):</label><input v-model="form.desconto_percentual" type="number" min="1" max="100" required class="form-input" /></div>
            <div class="form-group">
              <label>Usos Máximos:</label>
              <input v-model="form.usos_maximos" type="number" min="1" required class="form-input" />
              <small>Usos restantes atuais: {{ form.usos_restantes }}</small>
            </div>
            <div class="form-group">
              <label>Status:</label>
              <select v-model="form.status" required class="form-select">
                <option value="ativo">Ativo</option>
                <option value="inativo">Inativo</option>
              </select>
            </div>
            <div class="form-actions">
              <router-link to="/admin/cupons" class="btn-secondary">Cancelar</router-link>
              <button type="submit" class="btn-primary" :disabled="loading">
                <i class="fas fa-save"></i> {{ loading ? 'Salvando...' : 'Salvar Alterações' }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </main>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

const route   = useRoute()
const router  = useRouter()
const loading = ref(false)
const msg     = ref(''); const msgTipo = ref('sucesso')
const form    = ref({})

async function salvar() {
  loading.value = true
  try {
    await api.put(`/admin/cupons/${route.params.id}`, form.value)
    msg.value = 'Cupom atualizado!'; msgTipo.value = 'sucesso'
    setTimeout(() => router.push('/admin/cupons'), 1000)
  } catch {
    msg.value = 'Erro ao salvar'; msgTipo.value = 'erro'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const { data } = await api.get(`/admin/cupons/${route.params.id}`)
  form.value = data
})
</script>