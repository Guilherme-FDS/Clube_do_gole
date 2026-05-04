<template>
  <DefaultLayout>
    <main class="estoque-container">
      <div class="estoque-header">
        <h1 class="titulo-lg"><i class="fas fa-boxes"></i> Gerenciar Produtos</h1>
        <p class="texto-corrido">Controle os produtos do catálogo do Clube do Gole</p>
        <button class="btn-modern" @click="abrirModal()"><i class="fas fa-plus"></i> Adicionar Novo Produto</button>
      </div>

      <div v-if="msg" :class="`flash-${msgTipo}`">{{ msg }}</div>

      <div class="tabela-wrapper">
        <table id="tabelaProdutos">
          <thead>
            <tr><th>Produto</th><th>Tipo</th><th>Descrição</th><th>Preço</th><th>Estoque</th><th>Imagem</th><th>Ações</th></tr>
          </thead>
          <tbody>
            <tr v-if="!produtos.length"><td colspan="7" class="sem-produtos">Nenhum produto cadastrado.</td></tr>
            <tr v-for="p in produtos" :key="p.id">
              <td>{{ p.nome }}</td>
              <td><span :class="`badge-tipo ${p.tipo?.toLowerCase()}`">{{ p.tipo }}</span></td>
              <td>{{ p.descricao }}</td>
              <td>R$ {{ fmt(p.preco) }}</td>
              <td>
                <span :class="`estoque-badge ${p.estoque > 20 ? 'estoque-alto' : p.estoque > 5 ? 'estoque-medio' : 'estoque-baixo'}`">
                  {{ p.estoque }}
                </span>
              </td>
              <td>
                <img v-if="p.imagem" :src="p.imagem" :alt="p.nome" class="produto-thumb" />
                <span v-else class="sem-imagem">—</span>
              </td>
              <td class="acoes">
                <router-link :to="`/admin/produtos/${p.id}`" class="btn-editar"><i class="fas fa-edit"></i> Editar</router-link>
                <button class="btn-excluir" @click="excluir(p.id)"><i class="fas fa-trash"></i> Excluir</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </main>

    <!-- Modal Adicionar -->
    <div v-if="modalAberto" class="modal">
      <div class="modal-content">
        <h2 class="titulo-md"><i class="fas fa-box"></i> Adicionar Novo Produto</h2>
        <form @submit.prevent="salvar">
          <div class="form-group"><label>Nome do Produto:</label><input v-model="form.nome" type="text" required /></div>
          <div class="form-group">
            <label>Tipo:</label>
            <select v-model="form.tipo" required>
              <option value="Gold">Gold</option>
              <option value="Premium">Premium</option>
            </select>
          </div>
          <div class="form-group"><label>Descrição:</label><input v-model="form.descricao" type="text" required /></div>
          <div class="form-group"><label>Preço:</label><input v-model="form.preco" type="number" step="0.01" min="0" required /></div>
          <div class="form-group"><label>Estoque:</label><input v-model="form.estoque" type="number" min="0" required /></div>
          <div class="form-group">
            <label>Imagem (URL ou Base64):</label>
            <input v-model="form.imagem" type="url" placeholder="https://..." />
            <input type="file" accept="image/*" @change="onImagem" />
            <img v-if="form.imagem" :src="form.imagem" class="image-preview" />
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="modalAberto = false">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="loading">
              <i class="fas fa-save"></i> {{ loading ? 'Salvando...' : 'Salvar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import api from '@/services/api'

const produtos    = ref([])
const modalAberto = ref(false)
const loading     = ref(false)
const msg         = ref(''); const msgTipo = ref('sucesso')
const form        = ref(formVazio())

function formVazio() {
  return { nome: '', tipo: 'Gold', descricao: '', preco: '', estoque: 0, imagem: '' }
}
const fmt = v => parseFloat(v || 0).toFixed(2).replace('.', ',')

function abrirModal() { form.value = formVazio(); modalAberto.value = true }

function onImagem(e) {
  const file = e.target.files[0]
  if (!file) return
  const reader = new FileReader()
  reader.onload = ev => form.value.imagem = ev.target.result
  reader.readAsDataURL(file)
}

async function salvar() {
  loading.value = true
  await api.post('/admin/produtos', form.value)
  await carregar()
  modalAberto.value = false
  loading.value = false
  msg.value = 'Produto adicionado!'; msgTipo.value = 'sucesso'
}

async function excluir(id) {
  if (!confirm('Excluir este produto?')) return
  await api.delete(`/admin/produtos/${id}`)
  await carregar()
  msg.value = 'Produto removido!'; msgTipo.value = 'sucesso'
}

async function carregar() {
  const { data } = await api.get('/admin/produtos')
  produtos.value = data
}

onMounted(carregar)
</script>