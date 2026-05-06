<template>
  <main class="estoque-container">
    <div class="estoque-header">
      <h1 class="titulo-lg"><i class="fas fa-boxes"></i> Gerenciar Produtos</h1>
      <p class="texto-corrido">Controle os produtos do catálogo do Clube do Gole</p>
      <button class="btn-modern" @click="abrirModal">
        <i class="fas fa-plus"></i> Adicionar Novo Produto
      </button>
    </div>

    <div class="tabela-wrapper">
      <table id="tabelaProdutos">
        <thead>
          <tr>
            <th>Produto</th>
            <th>Tipo</th>
            <th>Descrição</th>
            <th>Preço</th>
            <th>Estoque</th>
            <th>Imagem</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody id="tbodyProdutos">
          <tr v-if="carregando">
            <td colspan="7" class="texto-centro">
              <i class="fas fa-spinner fa-spin"></i> Carregando...
            </td>
          </tr>
          <tr v-else-if="produtos.length === 0">
            <td colspan="7" class="sem-produtos">Nenhum produto cadastrado.</td>
          </tr>
          <tr v-else v-for="produto in produtos" :key="produto.id">
            <td>{{ produto.nome }}</td>
            <td>
              <span :class="['badge-tipo', produto.tipo.toLowerCase()]">{{ produto.tipo }}</span>
            </td>
            <td>{{ produto.descricao }}</td>
            <td>{{ formatarPreco(produto.preco) }}</td>
            <td>
              <span :class="['estoque-badge', getEstoqueClass(produto.estoque)]">
                {{ produto.estoque }}
              </span>
            </td>
            <td>
              <img v-if="produto.imagem" :src="produto.imagem" :alt="produto.nome" class="produto-thumb">
              <span v-else class="sem-imagem">—</span>
            </td>
            <td class="acoes">
              <router-link :to="`/admin/produtos/editar/${produto.id}`" class="btn-editar" title="Editar">
                <i class="fas fa-edit"></i> Editar
              </router-link>
              <button @click="excluirProduto(produto.id)" class="btn-excluir" title="Excluir">
                <i class="fas fa-trash"></i> Excluir
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- MODAL DE ADIÇÃO -->
    <div v-if="modalAberto" class="modal" @click.self="fecharModal">
      <div class="modal-content">
        <h2 class="titulo-md"><i class="fas fa-box"></i> Adicionar Novo Produto</h2>
        <form @submit.prevent="salvarProduto">
          <div class="form-group">
            <label for="nomeProduto">Nome do Produto:</label>
            <input type="text" id="nomeProduto" v-model="form.nome" placeholder="Ex: Box 6" required>
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
            <input type="text" id="descricaoProduto" v-model="form.descricao" placeholder="Descrição do produto" required>
          </div>

          <div class="form-group">
            <label for="precoProduto">Preço:</label>
            <input type="number" id="precoProduto" v-model="form.preco" placeholder="Ex: 49.90" step="0.01" min="0" required>
          </div>

          <div class="form-group">
            <label for="estoqueProduto">Estoque:</label>
            <input type="number" id="estoqueProduto" v-model="form.estoque" placeholder="Ex: 10" min="0" required>
          </div>

          <div class="form-group">
            <label for="imagemProduto">Imagem:</label>
            <input type="url" id="imagemProdutoUrl" v-model="form.imagem_url" placeholder="https://..." style="margin-bottom: 10px;">
            <input type="file" id="imagemProdutoFile" @change="processarImagem" accept="image/*" style="margin-bottom: 10px;">
            <img v-if="form.imagem_preview" :src="form.imagem_preview" alt="Preview" class="preview-imagem">
          </div>

          <div class="modal-buttons">
            <button type="button" class="btn-modal btn-modal-cancelar" @click="fecharModal">Cancelar</button>
            <button type="submit" class="btn-modal btn-modal-salvar" :disabled="salvando">
              {{ salvando ? 'Salvando...' : 'Salvar' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useProdutosAdminStore } from '@/stores/admin/produtos'

const router = useRouter()
const produtosStore = useProdutosAdminStore()

// Estados
const produtos = ref([])
const carregando = ref(false)
const modalAberto = ref(false)
const salvando = ref(false)

// Formulário
const form = ref({
  nome: '',
  tipo: 'Gold',
  descricao: '',
  preco: '',
  estoque: '',
  imagem_url: '',
  imagem_base64: '',
  imagem_preview: ''
})

// Funções
const carregarProdutos = async () => {
  carregando.value = true
  try {
    produtos.value = await produtosStore.fetchProdutos()
  } catch (error) {
    console.error('Erro ao carregar produtos:', error)
    mostrarNotificacao('Erro ao carregar produtos', 'error')
  } finally {
    carregando.value = false
  }
}

const getEstoqueClass = (estoque) => {
  if (estoque > 20) return 'estoque-alto'
  if (estoque > 5) return 'estoque-medio'
  return 'estoque-baixo'
}

const formatarPreco = (preco) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(preco || 0)
}

const abrirModal = () => {
  modalAberto.value = true
  document.body.style.overflow = 'hidden'
  resetForm()
}

const fecharModal = () => {
  modalAberto.value = false
  document.body.style.overflow = ''
  resetForm()
}

const resetForm = () => {
  form.value = {
    nome: '',
    tipo: 'Gold',
    descricao: '',
    preco: '',
    estoque: '',
    imagem_url: '',
    imagem_base64: '',
    imagem_preview: ''
  }
}

// Compressão de imagem
const compressImage = (file, maxWidth = 800, maxHeight = 600, quality = 0.7) => {
  return new Promise((resolve, reject) => {
    const canvas = document.createElement('canvas')
    const ctx = canvas.getContext('2d')
    const img = new Image()
    
    img.onload = () => {
      let width = img.width
      let height = img.height
      
      if (width > maxWidth || height > maxHeight) {
        const ratio = Math.min(maxWidth / width, maxHeight / height)
        width = Math.round(width * ratio)
        height = Math.round(height * ratio)
      }
      
      canvas.width = width
      canvas.height = height
      ctx.drawImage(img, 0, 0, width, height)
      
      const base64 = canvas.toDataURL('image/jpeg', quality)
      
      resolve({
        base64,
        compressionRatio: Math.round((1 - (base64.length * 3) / (4 * file.size)) * 100)
      })
    }
    
    img.onerror = () => reject(new Error('Erro ao carregar imagem'))
    img.src = URL.createObjectURL(file)
  })
}

const processarImagem = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  if (!file.type.startsWith('image/')) {
    mostrarNotificacao('Por favor, selecione apenas imagens!', 'error')
    event.target.value = ''
    return
  }

  try {
    // Preview
    form.value.imagem_preview = URL.createObjectURL(file)
    
    // Comprimir imagem
    const result = await compressImage(file)
    form.value.imagem_base64 = result.base64
    form.value.imagem_url = ''
    
    mostrarNotificacao(`Imagem comprimida com sucesso! (${result.compressionRatio}% menor)`, 'success')
  } catch (error) {
    console.error('Erro ao processar imagem:', error)
    mostrarNotificacao('Erro ao processar a imagem', 'error')
  }
}

const salvarProduto = async () => {
  // Validações
  if (!form.value.nome) {
    mostrarNotificacao('Nome do produto é obrigatório', 'error')
    return
  }
  if (!form.value.descricao) {
    mostrarNotificacao('Descrição é obrigatória', 'error')
    return
  }
  if (!form.value.preco || form.value.preco <= 0) {
    mostrarNotificacao('Preço deve ser um valor positivo', 'error')
    return
  }
  if (form.value.estoque === '' || form.value.estoque < 0) {
    mostrarNotificacao('Estoque deve ser um número não negativo', 'error')
    return
  }

  salvando.value = true
  try {
    const dados = {
      nome: form.value.nome,
      tipo: form.value.tipo,
      descricao: form.value.descricao,
      preco: parseFloat(form.value.preco),
      estoque: parseInt(form.value.estoque),
      imagem: form.value.imagem_base64 || form.value.imagem_url
    }
    
    await produtosStore.adicionarProduto(dados)
    mostrarNotificacao('Produto adicionado com sucesso!', 'success')
    fecharModal()
    await carregarProdutos()
  } catch (error) {
    console.error('Erro ao salvar produto:', error)
    mostrarNotificacao('Erro ao salvar produto', 'error')
  } finally {
    salvando.value = false
  }
}

const excluirProduto = async (id) => {
  if (!confirm('Tem certeza que deseja excluir este produto?')) return
  
  try {
    await produtosStore.excluirProduto(id)
    mostrarNotificacao('Produto excluído com sucesso!', 'success')
    await carregarProdutos()
  } catch (error) {
    console.error('Erro ao excluir produto:', error)
    mostrarNotificacao('Erro ao excluir produto', 'error')
  }
}

const mostrarNotificacao = (message, type = 'success') => {
  const existing = document.querySelector('.admin-notification')
  if (existing) existing.remove()
  
  const notification = document.createElement('div')
  notification.className = `admin-notification admin-notification-${type}`
  
  const icons = { success: 'check', error: 'exclamation', info: 'info', warning: 'exclamation-triangle' }
  
  notification.innerHTML = `<i class="fas fa-${icons[type]}"></i><span>${message}</span>`
  
  document.body.appendChild(notification)
  
  setTimeout(() => notification.style.opacity = '1', 10)
  setTimeout(() => {
    notification.style.opacity = '0'
    setTimeout(() => notification.remove(), 300)
  }, 5000)
}

// Tecla ESC fecha modal
const handleKeydown = (event) => {
  if (event.key === 'Escape' && modalAberto.value) {
    fecharModal()
  }
}

// Lifecycle
onMounted(() => {
  carregarProdutos()
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* ===== ESTILOS EXCLUSIVOS DO ADMIN PRODUTOS ===== */
.estoque-container {
  flex: 1;
  padding: var(--espacamento-xl) var(--espacamento-md);
  max-width: 1400px;
  margin: 0 auto;
  width: 100%;
  margin-top: 80px;
}

.estoque-header {
  text-align: center;
  margin-bottom: var(--espacamento-lg);
}

.estoque-header h1 {
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.estoque-header p {
  color: var(--cor-texto-secundario);
  margin-bottom: var(--espacamento-md);
}

/* Tabela */
.tabela-wrapper {
  overflow-x: auto;
  background-color: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  border: 2px solid var(--cor-dourado);
  box-shadow: var(--sombra-destaque);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--gradiente-botao);
}

th {
  padding: var(--espacamento-sm);
  text-align: left;
  color: var(--cor-fundo);
  font-weight: 600;
  border-bottom: 2px solid var(--cor-dourado);
}

td {
  padding: var(--espacamento-sm);
  color: var(--cor-texto);
  vertical-align: middle;
  text-align: left;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
}

tbody tr {
  transition: all 0.3s ease;
}

tbody tr:hover {
  background-color: rgba(255, 215, 0, 0.1);
  transform: translateY(-2px);
}

/* Badges */
.badge-tipo {
  padding: 0.25rem 0.75rem;
  border-radius: var(--borda-radius-lg);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.badge-tipo.gold {
  background: var(--gradiente-dourado);
  color: var(--cor-fundo);
}

.badge-tipo.premium {
  background: var(--gradiente-botao);
  color: var(--cor-fundo);
}

.estoque-badge {
  padding: 0.25rem 0.75rem;
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  font-size: 0.875rem;
}

.estoque-alto {
  background: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
  border: 1px solid #4CAF50;
}

.estoque-medio {
  background: rgba(255, 152, 0, 0.2);
  color: #FF9800;
  border: 1px solid #FF9800;
}

.estoque-baixo {
  background: rgba(244, 67, 54, 0.2);
  color: #F44336;
  border: 1px solid #F44336;
}

.produto-thumb {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: var(--borda-radius-sm);
  border: 2px solid var(--cor-dourado);
  box-shadow: var(--sombra-suave);
}

.preview-imagem {
  max-width: 200px;
  margin-top: 10px;
  border-radius: var(--borda-radius-sm);
  border: 2px solid var(--cor-dourado);
}

.sem-imagem {
  color: var(--cor-texto-secundario);
  font-style: italic;
}

.sem-produtos {
  text-align: center;
  color: var(--cor-texto-secundario);
  padding: var(--espacamento-lg);
}

/* Botões de ação */
.acoes {
  display: flex;
  gap: var(--espacamento-xs);
  flex-wrap: wrap;
}

.btn-editar, .btn-excluir {
  padding: 0.5rem 1rem;
  border-radius: var(--borda-radius-sm);
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  border: none;
  cursor: pointer;
}

.btn-editar {
  background: var(--gradiente-dourado);
  color: var(--cor-fundo);
}

.btn-editar:hover {
  transform: translateY(-2px);
  box-shadow: var(--sombra-destaque);
}

.btn-excluir {
  background: rgba(244, 67, 54, 0.2);
  color: #F44336;
  border: 1px solid #F44336;
}

.btn-excluir:hover {
  background: #F44336;
  color: var(--cor-texto);
  transform: translateY(-2px);
}

/* Modal */
.modal {
  position: fixed;
  z-index: 2000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(5px);
}

.modal-content {
  background-color: var(--cor-fundo-secundario);
  padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-lg);
  border: 2px solid var(--cor-dourado);
  max-width: 550px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideDown 0.3s ease-out;
  box-shadow: var(--sombra-destaque);
}

@keyframes slideDown {
  from {
    transform: translateY(-50px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.modal-content h2 {
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-md);
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

/* Formulário */
.form-group {
  margin-bottom: var(--espacamento-md);
}

.form-group label {
  display: block;
  margin-bottom: var(--espacamento-xs);
  color: var(--cor-dourado);
  font-weight: 600;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: var(--espacamento-sm);
  background-color: var(--cor-fundo);
  border: 1px solid var(--cor-dourado);
  color: var(--cor-texto);
  border-radius: var(--borda-radius-sm);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--cor-roxo-principal);
  box-shadow: 0 0 0 2px rgba(138, 43, 226, 0.2);
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
  font-size: 1rem;
}

.btn-modal-salvar {
  background: var(--gradiente-botao-dourado-claro-escuro);
  color: var(--cor-fundo);
}

.btn-modal-salvar:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--sombra-destaque);
}

.btn-modal-salvar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-modal-cancelar {
  background: var(--cor-fundo);
  color: var(--cor-texto);
  border: 1px solid var(--cor-dourado);
}

.btn-modal-cancelar:hover {
  background: var(--cor-dourado);
  color: var(--cor-fundo);
  transform: translateY(-2px);
}

/* Notificações */
.admin-notification {
  position: fixed;
  bottom: 20px;
  right: 20px;
  background: linear-gradient(135deg, #00ff88, #00cc66);
  color: var(--cor-fundo);
  padding: 1rem 1.5rem;
  border-radius: var(--borda-radius-md);
  font-weight: 600;
  z-index: 10000;
  display: flex;
  align-items: center;
  gap: 10px;
  opacity: 0;
  transform: translateX(100%);
  transition: all 0.3s ease;
  box-shadow: var(--sombra-destaque);
}

.admin-notification-error {
  background: linear-gradient(135deg, #ff4444, #cc0000);
  color: var(--cor-texto);
}

.admin-notification-info {
  background: linear-gradient(135deg, #2196F3, #1976D2);
  color: var(--cor-texto);
}

.texto-centro {
  text-align: center;
}

/* Responsividade */
@media (max-width: 768px) {
  .estoque-container {
    padding: var(--espacamento-lg) var(--espacamento-sm);
    margin-top: 120px;
  }

  .estoque-header h1 {
    font-size: 1.75rem;
    flex-direction: column;
  }

  .tabela-wrapper {
    padding: var(--espacamento-sm);
  }

  table {
    font-size: 0.85rem;
  }

  th, td {
    padding: var(--espacamento-xs);
  }

  .acoes {
    flex-direction: column;
  }

  .btn-editar, .btn-excluir {
    font-size: 0.75rem;
    padding: 0.4rem 0.8rem;
  }

  .modal-content {
    padding: var(--espacamento-md);
    max-width: 95%;
  }

  .modal-buttons {
    flex-direction: column;
  }

  .btn-modal {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .estoque-header h1 {
    font-size: 1.5rem;
  }

  table {
    font-size: 0.75rem;
  }

  .produto-thumb {
    width: 40px;
    height: 40px;
  }

  .badge-tipo, .estoque-badge {
    font-size: 0.7rem;
    padding: 0.2rem 0.5rem;
  }

  .preview-imagem {
    max-width: 150px;
  }
}
</style>