<template>
  <DefaultLayout>
    <main class="admin-container">
      <div class="container">
        <div class="admin-header fade-in">
          <h1 class="titulo-lg"><i class="fas fa-edit"></i> Editar Produto</h1>
          <p class="texto-corrido">Altere os dados do produto e clique em salvar</p>
        </div>

        <div v-if="msg" :class="`flash-${msgTipo}`">{{ msg }}</div>

        <div class="form-wrapper fade-in" v-if="form.nome">
          <form class="admin-form" @submit.prevent="salvar">
            <div class="form-group"><label class="form-label">Nome do Produto:</label><input v-model="form.nome" type="text" class="form-input" required /></div>
            <div class="form-group">
              <label class="form-label">Tipo:</label>
              <select v-model="form.tipo" class="form-select" required>
                <option value="Gold">Gold</option>
                <option value="Premium">Premium</option>
              </select>
            </div>
            <div class="form-group"><label class="form-label">Descrição:</label><input v-model="form.descricao" type="text" class="form-input" required /></div>
            <div class="form-group"><label class="form-label">Preço:</label><input v-model="form.preco" type="number" step="0.01" min="0" class="form-input" required /></div>
            <div class="form-group"><label class="form-label">Estoque:</label><input v-model="form.estoque" type="number" min="0" class="form-input" required /></div>
            <div class="form-group">
              <label class="form-label">Imagem:</label>
              <input v-model="form.imagem" type="url" class="form-input" placeholder="https://..." style="margin-bottom:10px" />
              <input type="file" accept="image/*" class="form-input" @change="onImagem" />
              <img v-if="form.imagem" :src="form.imagem" class="image-preview" />
            </div>
            <div class="form-actions">
              <router-link to="/admin/produtos" class="btn-secondary">Cancelar</router-link>
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

const route  = useRoute()
const router = useRouter()
const loading = ref(false)
const msg     = ref(''); const msgTipo = ref('sucesso')
const form    = ref({})

function onImagem(e) {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = ev => form.value.imagem = ev.target.result
  reader.readAsDataURL(file)
}

async function salvar() {
  loading.value = true
  try {
    await api.put(`/admin/produtos/${route.params.id}`, form.value)
    msg.value = 'Produto atualizado!'; msgTipo.value = 'sucesso'
    setTimeout(() => router.push('/admin/produtos'), 1000)
  } catch {
    msg.value = 'Erro ao salvar'; msgTipo.value = 'erro'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  const { data } = await api.get(`/admin/produtos/${route.params.id}`)
  form.value = data
})
</script>