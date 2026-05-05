<template>
  <DefaultLayout>
    <main class="cupons-container">
      <div class="container">
        <div class="cupons-header">
          <h1 class="titulo-lg">Gerenciar Cupons de Desconto</h1>
          <p class="texto-corrido texto-centro">Controle os cupons de desconto do Clube do Gole</p>
          <button class="btn-adicionar" @click="modalAberto = true"><i class="fas fa-plus"></i> Adicionar Novo Cupom</button>
        </div>

        <div v-if="msg" :class="`flash-${msgTipo}`">{{ msg }}</div>

        <div class="tabela-wrapper">
          <table id="tabelaCupons">
            <thead>
              <tr><th>Código</th><th>Desconto</th><th>Usos Máximos</th><th>Usos Restantes</th><th>Status</th><th>Ações</th></tr>
            </thead>
            <tbody>
              <tr v-if="!cupons.length"><td colspan="6" class="sem-dados">Nenhum cupom cadastrado.</td></tr>
              <tr v-for="c in cupons" :key="c.id" class="fade-in">
                <td><strong>{{ c.codigo }}</strong></td>
                <td>{{ c.desconto_percentual }}%</td>
                <td>{{ c.usos_maximos }}</td>
                <td>
                  <span :class="`uso-indicator ${parseInt(c.usos_restantes) > 0 ? 'uso-disponivel' : 'uso-esgotado'}`">
                    {{ c.usos_restantes }}
                  </span>
                </td>
                <td><span :class="`status-badge status-${c.status}`">{{ c.status }}</span></td>
                <td class="acoes">
                  <button v-if="c.status === 'ativo'" class="btn-acao btn-inativar" @click="alterarStatus(c.id, 'inativo')">
                    <i class="fas fa-pause"></i> Inativar
                  </button>
                  <button v-else class="btn-acao btn-ativar" @click="alterarStatus(c.id, 'ativo')">
                    <i class="fas fa-play"></i> Ativar
                  </button>
                  <router-link :to="`/admin/cupons/${c.id}`" class="btn-acao btn-editar">
                    <i class="fas fa-edit"></i> Editar
                  </router-link>
                  <button class="btn-acao btn-excluir" @click="excluir(c.id)">
                    <i class="fas fa-trash"></i> Excluir
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>

    <!-- Modal Adicionar -->
    <div v-if="modalAberto" class="modal">
      <div class="modal-content">
        <h2>Adicionar Novo Cupom</h2>
        <form @submit.prevent="salvar">
          <div class="form-group"><label>Código:</label><input v-model="form.codigo" type="text" required /></div>
          <div class="form-group"><label>Desconto (%):</label><input v-model="form.desconto_percentual" type="number" min="1" max="100" required /></div>
          <div class="form-group"><label>Usos Máximos:</label><input v-model="form.usos_maximos" type="number" min="1" required /></div>
          <div class="form-group">
            <label>Status:</label>
            <select v-model="form.status">
              <option value="ativo">Ativo</option>
              <option value="inativo">Inativo</option>
            </select>
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

const cupons      = ref([])
const modalAberto = ref(false)
const loading     = ref(false)
const msg         = ref(''); const msgTipo = ref('sucesso')
const form        = ref({ codigo: '', desconto_percentual: '', usos_maximos: 1, status: 'ativo' })

async function carregar() {
  const { data } = await api.get('/admin/cupons')
  cupons.value = data
}

async function salvar() {
  loading.value = true
  await api.post('/admin/cupons', form.value)
  await carregar()
  modalAberto.value = false
  loading.value = false
  msg.value = 'Cupom adicionado!'; msgTipo.value = 'sucesso'
}

async function excluir(id) {
  if (!confirm('Excluir este cupom?')) return
  await api.delete(`/admin/cupons/${id}`)
  await carregar()
  msg.value = 'Cupom removido!'; msgTipo.value = 'sucesso'
}

async function alterarStatus(id, status) {
  await api.patch(`/admin/cupons/${id}/status`, { status })
  await carregar()
}

onMounted(carregar)
</script>