<template>
  <div class="estoque-container">
    <div class="estoque-header">
      <h1 class="titulo-lg"><i class="fas fa-edit"></i> Editar Produto</h1>
      <p class="texto-corrido">Altere as informações do produto</p>
    </div>

    <div class="form-container">
      <form @submit.prevent="atualizarProduto">
        <div class="form-group">
          <label for="nomeProduto">Nome do Produto:</label>
          <input type="text" id="nomeProduto" v-model="form.nome" required>
        </div>

        <div class="form-group">
          <label for="tipoProduto">Tipo:</label>
          <select id="tipoProduto" v-model="form.tipo" required>
            <option value="Gold">Gold</option>
            <option value="Premium">Premium</option>
          </select>
        </div>

        <div class="form-group">
          <label for="descricaoProduto">Descrição:</label>
          <input type="text" id="descricaoProduto" v-model="form.descricao" required>
        </div>

        <div class="form-group">
          <label for="precoProduto">Preço:</label>
          <input type="number" id="precoProduto" v-model="form.preco" step="0.01" min="0" required>
        </div>

        <div class="form-group">
          <label for="estoqueProduto">Estoque:</label>
          <input type="number" id="estoqueProduto" v-model="form.estoque" min="0" required>
        </div>

        <div class="modal-buttons">
          <router-link to="/admin/produtos" class="btn-modal btn-modal-cancelar">Cancelar</router-link>
          <button type="submit" class="btn-modal btn-modal-salvar" :disabled="salvando">
            {{ salvando ? 'Salvando...' : 'Salvar Alterações' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProdutosAdminStore } from '@/stores/admin/produtos'

const route = useRoute()
const router = useRouter()
const produtosStore = useProdutosAdminStore()

const form = ref({
  nome: '',
  tipo: 'Gold',
  descricao: '',
  preco: '',
  estoque: ''
})
const salvando = ref(false)

const carregarProduto = async () => {
  const id = route.params.id
  try {
    const produtos = await produtosStore.fetchProdutos()
    const produto = produtos.find(p => p.id == id)
    if (produto) {
      form.value = {
        nome: produto.nome,
        tipo: produto.tipo,
        descricao: produto.descricao,
        preco: produto.preco,
        estoque: produto.estoque
      }
    }
  } catch (error) {
    console.error('Erro ao carregar produto:', error)
  }
}

const atualizarProduto = async () => {
  salvando.value = true
  try {
    await produtosStore.atualizarProduto(route.params.id, form.value)
    router.push('/admin/produtos')
  } catch (error) {
    console.error('Erro ao atualizar produto:', error)
  } finally {
    salvando.value = false
  }
}

onMounted(() => {
  carregarProduto()
})
</script>

<style scoped>
.form-container {
  max-width: 600px;
  margin: 0 auto;
  background: var(--cor-fundo-secundario);
  padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-lg);
  border: 2px solid var(--cor-dourado);
}

.modal-buttons {
  display: flex;
  gap: var(--espacamento-sm);
  justify-content: flex-end;
  margin-top: var(--espacamento-lg);
}

.btn-modal {
  padding: var(--espacamento-sm) var(--espacamento-md);
  border: none;
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}
</style>