<template>
  <main class="admin-container">
    <div class="container">
      <div class="admin-header fade-in" :class="{ visible: fadeInVisible }">
        <h1 class="titulo-lg"><i class="fas fa-edit"></i> Editar Produto</h1>
        <p class="texto-corrido">Altere os dados do produto e clique em salvar</p>
      </div>

      <div class="form-wrapper fade-in" :class="{ visible: fadeInVisible }">
        <form @submit.prevent="salvarProduto" class="admin-form" enctype="multipart/form-data">
          <div class="form-group">
            <label for="nomeProduto" class="form-label">Nome do Produto:</label>
            <input type="text" id="nomeProduto" v-model="form.nome" class="form-input" required>
          </div>

          <div class="form-group">
            <label for="tipoProduto" class="form-label">Tipo:</label>
            <select id="tipoProduto" v-model="form.tipo" class="form-select" required>
              <option value="Gold">Gold</option>
              <option value="Premium">Premium</option>
            </select>
          </div>

          <div class="form-group">
            <label for="descricaoProduto" class="form-label">Descrição:</label>
            <input type="text" id="descricaoProduto" v-model="form.descricao" class="form-input" required>
          </div>

          <div class="form-group">
            <label for="precoProduto" class="form-label">Preço:</label>
            <input type="number" id="precoProduto" v-model.number="form.preco" step="0.01" min="0" class="form-input" required>
          </div>

          <div class="form-group">
            <label for="estoqueProduto" class="form-label">Estoque:</label>
            <input type="number" id="estoqueProduto" v-model.number="form.estoque" min="0" class="form-input" required>
          </div>

          <div class="form-group">
            <label for="imagemProduto" class="form-label">Imagem:</label>
            
            <!-- Campo URL (mantido para compatibilidade) -->
            <input type="url" id="imagemProdutoUrl" v-model="form.imagem_url" 
                   class="form-input" placeholder="https://..." style="margin-bottom: 10px;">
            
            <!-- Campo para upload de arquivo -->
            <input type="file" id="imagemProdutoFile" @change="processarImagem" accept="image/*" class="form-input" style="margin-bottom: 10px;">
            
            <!-- Preview da imagem -->
            <img v-if="form.imagem_preview" :src="form.imagem_preview" alt="Preview da imagem" class="image-preview">
            
            <small class="form-help">Use o campo URL para links ou faça upload de uma imagem do seu computador</small>
          </div>

          <div class="form-buttons">
            <router-link to="/admin/produtos" class="btn-admin btn-cancelar">Cancelar</router-link>
            <button type="submit" class="btn-admin btn-salvar" :disabled="salvando">
              {{ salvando ? 'Salvando...' : 'Salvar Alterações' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProdutosAdminStore } from '@/stores/admin/produtos'

const route = useRoute()
const router = useRouter()
const produtosStore = useProdutosAdminStore()

// Estados
const carregando = ref(false)
const salvando = ref(false)
const fadeInVisible = ref(false)
const produtoId = ref(null)

// Formulário
const form = reactive({
  nome: '',
  tipo: 'Gold',
  descricao: '',
  preco: '',
  estoque: '',
  imagem_url: '',
  imagem_base64: '',
  imagem_preview: ''
})

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

const getOptimalCompressionSettings = (file) => {
  const settings = { maxWidth: 800, maxHeight: 600, quality: 0.7 }
  
  if (file.type === 'image/png') {
    settings.quality = 0.8
  } else if (file.type === 'image/jpeg') {
    settings.quality = 0.7
  }
  
  if (file.size > 2 * 1024 * 1024) {
    settings.quality = 0.6
    settings.maxWidth = 600
    settings.maxHeight = 400
  } else if (file.size > 1 * 1024 * 1024) {
    settings.quality = 0.7
  }
  
  return settings
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
    form.imagem_preview = URL.createObjectURL(file)
    
    // Comprimir imagem
    const settings = getOptimalCompressionSettings(file)
    const result = await compressImage(file, settings.maxWidth, settings.maxHeight, settings.quality)
    
    form.imagem_base64 = result.base64
    form.imagem_url = ''
    
    console.log(`Imagem comprimida: ${result.compressionRatio}% redução`)
    mostrarNotificacao(`Imagem comprimida com sucesso! (${result.compressionRatio}% menor)`, 'success')
  } catch (error) {
    console.error('Erro ao processar imagem:', error)
    mostrarNotificacao('Erro ao processar a imagem', 'error')
  }
}

// Carregar produto da API
const carregarProduto = async () => {
  produtoId.value = route.params.id
  if (!produtoId.value) {
    router.push('/admin/produtos')
    return
  }
  
  carregando.value = true
  try {
    const produtos = await produtosStore.fetchProdutos()
    const produto = produtos.find(p => p.id == produtoId.value)
    
    if (produto) {
      form.nome = produto.nome
      form.tipo = produto.tipo
      form.descricao = produto.descricao
      form.preco = produto.preco
      form.estoque = produto.estoque
      
      // Configurar imagem
      if (produto.imagem) {
        if (produto.imagem.startsWith('data:image')) {
          form.imagem_base64 = produto.imagem
          form.imagem_url = ''
        } else {
          form.imagem_url = produto.imagem
        }
        form.imagem_preview = produto.imagem
      }
    } else {
      mostrarNotificacao('Produto não encontrado', 'error')
      router.push('/admin/produtos')
    }
  } catch (error) {
    console.error('Erro ao carregar produto:', error)
    mostrarNotificacao('Erro ao carregar produto', 'error')
  } finally {
    carregando.value = false
    setTimeout(() => { fadeInVisible.value = true }, 100)
  }
}

// Salvar produto
const salvarProduto = async () => {
  // Validações
  if (!form.nome) {
    mostrarNotificacao('Nome do produto é obrigatório', 'error')
    return
  }
  if (!form.descricao) {
    mostrarNotificacao('Descrição é obrigatória', 'error')
    return
  }
  if (!form.preco || form.preco <= 0) {
    mostrarNotificacao('Preço deve ser um valor positivo', 'error')
    return
  }
  if (form.estoque === '' || form.estoque < 0) {
    mostrarNotificacao('Estoque deve ser um número não negativo', 'error')
    return
  }

  salvando.value = true
  try {
    const dados = {
      nome: form.nome,
      tipo: form.tipo,
      descricao: form.descricao,
      preco: parseFloat(form.preco),
      estoque: parseInt(form.estoque),
      imagem: form.imagem_base64 || form.imagem_url
    }
    
    await produtosStore.atualizarProduto(produtoId.value, dados)
    mostrarNotificacao('Produto atualizado com sucesso!', 'success')
    router.push('/admin/produtos')
  } catch (error) {
    console.error('Erro ao salvar produto:', error)
    mostrarNotificacao('Erro ao salvar produto', 'error')
  } finally {
    salvando.value = false
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

// Lifecycle
onMounted(() => {
  carregarProduto()
})
</script>

<style scoped>
/* ===== ESTILOS EXCLUSIVOS PARA EDIÇÃO DE PRODUTOS ===== */
.admin-container {
  min-height: 100vh;
  background: var(--gradiente-hero);
  padding: var(--espacamento-xl) 0;
  margin-top: 80px;
}

.admin-header {
  text-align: center;
  margin-bottom: var(--espacamento-lg);
  padding: var(--espacamento-md);
}

.admin-header h1 {
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--espacamento-sm);
}

.admin-header p {
  color: var(--cor-texto-secundario);
  margin-bottom: var(--espacamento-md);
  font-size: 1.1rem;
}

.form-wrapper {
  max-width: 600px;
  margin: 0 auto;
  background: var(--cor-fundo-secundario);
  padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-lg);
  border: 1px solid rgba(255, 215, 0, 0.2);
  box-shadow: var(--sombra-card);
}

.admin-form {
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-md);
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-xs);
}

.form-label {
  color: var(--cor-dourado);
  font-weight: 600;
  font-size: 1rem;
}

.form-input,
.form-select {
  padding: 0.75rem 1rem;
  background: var(--cor-fundo);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: var(--borda-radius-md);
  color: var(--cor-texto);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-input:focus,
.form-select:focus {
  outline: none;
  border-color: var(--cor-dourado);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

.form-input::placeholder {
  color: var(--cor-texto-secundario);
}

.form-help {
  color: var(--cor-texto-secundario);
  font-size: 0.75rem;
  margin-top: 0.25rem;
}

.form-buttons {
  display: flex;
  gap: var(--espacamento-sm);
  margin-top: var(--espacamento-md);
  flex-wrap: wrap;
}

.btn-admin {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--borda-radius-lg);
  font-weight: 600;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--espacamento-xs);
  flex: 1;
  min-width: 140px;
}

.btn-salvar {
  background: var(--gradiente-botao-dourado-claro-escuro);
  color: var(--cor-fundo);
}

.btn-salvar:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: var(--sombra-destaque);
}

.btn-salvar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-cancelar {
  background: var(--cor-fundo);
  color: var(--cor-texto);
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.btn-cancelar:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: var(--cor-dourado);
  transform: translateY(-2px);
}

/* Preview da imagem */
.image-preview {
  max-width: 200px;
  max-height: 200px;
  border: 2px solid var(--cor-dourado);
  border-radius: var(--borda-radius-md);
  margin-top: 10px;
  object-fit: cover;
}

/* Animações */
.fade-in {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.6s ease;
}

.fade-in.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Notificações */
.admin-notification {
  position: fixed;
  top: 100px;
  right: 20px;
  padding: var(--espacamento-sm) var(--espacamento-md);
  border-radius: var(--borda-radius-md);
  box-shadow: var(--sombra-destaque);
  z-index: 10000;
  display: flex;
  align-items: center;
  gap: var(--espacamento-sm);
  font-weight: 600;
  max-width: 400px;
  opacity: 0;
  transform: translateX(100%);
  transition: all 0.3s ease;
}

.admin-notification-success {
  background: linear-gradient(135deg, #00ff88, #00cc66);
  color: var(--cor-fundo);
}

.admin-notification-error {
  background: linear-gradient(135deg, #ff4444, #cc0000);
  color: var(--cor-texto);
}

.admin-notification-info {
  background: linear-gradient(135deg, #2196F3, #1976D2);
  color: var(--cor-texto);
}

/* Responsividade */
@media (max-width: 768px) {
  .admin-container {
    margin-top: 120px;
    padding: var(--espacamento-md) 0;
  }
  
  .form-wrapper {
    margin: 0 var(--espacamento-sm);
    padding: var(--espacamento-md);
  }
  
  .form-buttons {
    flex-direction: column;
  }
  
  .btn-admin {
    flex: none;
    width: 100%;
  }
  
  .admin-header h1 {
    font-size: 1.75rem;
    flex-direction: column;
    gap: var(--espacamento-xs);
  }
}

@media (max-width: 480px) {
  .form-wrapper {
    padding: var(--espacamento-sm);
  }
  
  .admin-header {
    padding: var(--espacamento-sm);
  }
  
  .image-preview {
    max-width: 150px;
    max-height: 150px;
  }
}
</style>