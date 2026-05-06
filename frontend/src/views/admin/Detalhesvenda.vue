<template>
  <div class="detalhes-container">
    <h1 class="detalhes-titulo"><i class="fas fa-receipt"></i> Detalhes da Venda</h1>

    <div v-if="carregando" class="loading-spinner">
      <i class="fas fa-spinner fa-spin"></i> Carregando detalhes...
    </div>

    <div v-else-if="venda" class="detalhes-grid">
      <!-- INFORMAÇÕES DA VENDA -->
      <div class="detalhes-card fade-in" :class="{ visible: fadeInVisible }">
        <h3><i class="fas fa-info-circle"></i> Informações da Venda</h3>
        <div class="info-list">
          <div class="info-item">
            <strong>ID da Venda:</strong>
            <span>{{ venda.id_compra }}</span>
          </div>
          <div class="info-item">
            <strong>Data e Hora:</strong>
            <span>{{ formatarDataHora(venda.data) }}</span>
          </div>
          <div class="info-item">
            <strong>Produto:</strong>
            <span>{{ venda.nome_produto }}</span>
          </div>
          <div class="info-item">
            <strong>Tipo:</strong>
            <span :class="['badge-tipo', venda.tipo_produto.toLowerCase()]">{{ venda.tipo_produto }}</span>
          </div>
          <div class="info-item">
            <strong>Quantidade:</strong>
            <span>{{ venda.quantidade }} unidades</span>
          </div>
          <div class="info-item">
            <strong>Preço Unitário:</strong>
            <span>{{ formatarMoeda(venda.preco_unitario) }}</span>
          </div>
          <div class="info-item" v-if="venda.valor_sem_desconto">
            <strong>Valor Original:</strong>
            <span class="valor-original">{{ formatarMoeda(venda.valor_sem_desconto) }}</span>
          </div>
          <div class="info-item" v-if="venda.desconto_aplicado && venda.desconto_aplicado > 0">
            <strong>Desconto:</strong>
            <span class="valor-desconto">{{ venda.desconto_aplicado }}%</span>
          </div>
          <div class="info-item total">
            <strong>Valor Total:</strong>
            <span class="valor-total">{{ formatarMoeda(venda.valor_total) }}</span>
          </div>
          <div class="info-item" v-if="venda.cupom_aplicado">
            <strong>Cupom Utilizado:</strong>
            <span class="cupom-info">{{ venda.cupom_aplicado }}</span>
          </div>
        </div>
      </div>

      <!-- INFORMAÇÕES DO CLIENTE -->
      <div class="detalhes-card fade-in" :class="{ visible: fadeInVisible }">
        <h3><i class="fas fa-user"></i> Informações do Cliente</h3>
        <div class="info-list">
          <div class="info-item">
            <strong>Nome:</strong>
            <span>{{ venda.nome_usuario || venda.cliente_nome || 'Cliente não identificado' }}</span>
          </div>
          <div class="info-item">
            <strong>Email:</strong>
            <span>{{ venda.email_usuario || venda.cliente_email || '---' }}</span>
          </div>
          <div class="info-item">
            <strong>ID do Cliente:</strong>
            <span>{{ venda.id_usuario || venda.cliente_id || '---' }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Detalhes do Endereço de Entrega (se disponível) -->
    <div v-if="venda && venda.endereco" class="detalhes-card full-width fade-in" :class="{ visible: fadeInVisible }">
      <h3><i class="fas fa-map-marker-alt"></i> Endereço de Entrega</h3>
      <div class="info-list endereco-list">
        <div class="info-item">
          <strong>Endereço:</strong>
          <span>{{ venda.endereco }}, {{ venda.numero }}</span>
        </div>
        <div class="info-item" v-if="venda.complemento">
          <strong>Complemento:</strong>
          <span>{{ venda.complemento }}</span>
        </div>
        <div class="info-item">
          <strong>Bairro:</strong>
          <span>{{ venda.bairro }}</span>
        </div>
        <div class="info-item">
          <strong>Cidade/UF:</strong>
          <span>{{ venda.cidade }}/{{ venda.estado }}</span>
        </div>
        <div class="info-item">
          <strong>CEP:</strong>
          <span>{{ venda.cep }}</span>
        </div>
      </div>
    </div>

    <!-- AÇÕES -->
    <div class="acoes-detalhes fade-in" :class="{ visible: fadeInVisible }">
      <router-link to="/admin" class="btn-voltar">
        <i class="fas fa-arrow-left"></i> Voltar ao Dashboard
      </router-link>
      <button @click="imprimirRecibo" class="btn-imprimir">
        <i class="fas fa-print"></i> Imprimir Recibo
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// Estados
const venda = ref(null)
const carregando = ref(false)
const fadeInVisible = ref(false)

// Formatação
const formatarMoeda = (valor) => {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(valor || 0)
}

const formatarDataHora = (dataStr) => {
  if (!dataStr) return '---'
  const data = new Date(dataStr)
  return data.toLocaleDateString('pt-BR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Carregar detalhes da venda
const carregarDetalhesVenda = async () => {
  const vendaId = route.params.id
  if (!vendaId) {
    mostrarNotificacao('ID da venda não informado', 'error')
    router.push('/admin')
    return
  }

  carregando.value = true
  try {
    const response = await fetch(`/api/admin/vendas/${vendaId}`, {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`,
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Venda não encontrada')
      }
      if (response.status === 403) {
        throw new Error('Acesso não autorizado')
      }
      throw new Error('Erro ao carregar detalhes da venda')
    }

    const data = await response.json()
    venda.value = data.venda || data
    mostrarNotificacao('Detalhes carregados com sucesso!', 'success')
  } catch (error) {
    console.error('Erro:', error)
    mostrarNotificacao(error.message, 'error')
    setTimeout(() => {
      router.push('/admin')
    }, 2000)
  } finally {
    carregando.value = false
    setTimeout(() => {
      fadeInVisible.value = true
    }, 100)
  }
}

// Imprimir recibo
const imprimirRecibo = () => {
  window.print()
}

// Mostrar notificação
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

// Verificar autenticação e permissão
onMounted(async () => {
  if (!authStore.logado || authStore.tipo !== 'admin') {
    router.push('/login?redirect=' + route.fullPath)
    return
  }
  await carregarDetalhesVenda()
})
</script>

<style scoped>
/* ===== ESTILOS EXCLUSIVOS PARA DETALHES DE VENDA ===== */
.detalhes-container {
  max-width: 1000px;
  margin: 120px auto 2rem;
  padding: 0 20px;
}

.detalhes-titulo {
  color: var(--cor-dourado);
  text-align: center;
  margin-bottom: 2rem;
  font-size: 2.2rem;
}

.detalhes-titulo i {
  margin-right: 10px;
}

.detalhes-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
  margin-bottom: 2rem;
}

.detalhes-card {
  background: var(--cor-fundo-secundario);
  border: 1px solid rgba(255, 215, 0, 0.2);
  border-radius: var(--borda-radius-lg);
  padding: 1.5rem;
  transition: all 0.3s ease;
}

.detalhes-card.full-width {
  grid-column: 1 / -1;
}

.detalhes-card:hover {
  transform: translateY(-5px);
  box-shadow: var(--sombra-destaque);
  border-color: var(--cor-dourado);
}

.detalhes-card h3 {
  color: var(--cor-dourado);
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  padding-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.detalhes-card h3 i {
  font-size: 1.2rem;
}

.info-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem 1rem;
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-md);
  transition: all 0.3s ease;
}

.info-item:hover {
  background: rgba(255, 215, 0, 0.05);
  transform: translateX(5px);
}

.info-item.total {
  background: rgba(255, 215, 0, 0.1);
  border: 1px solid var(--cor-dourado);
}

.info-item strong {
  color: var(--cor-texto);
  font-weight: 600;
}

.info-item span {
  color: var(--cor-texto-secundario);
}

.valor-total {
  color: var(--cor-dourado) !important;
  font-weight: bold;
  font-size: 1.2rem;
}

.valor-original {
  text-decoration: line-through;
  color: #888 !important;
}

.valor-desconto {
  color: #4CAF50 !important;
  font-weight: bold;
}

.cupom-info {
  color: #2196F3 !important;
  font-weight: bold;
}

/* Badges */
.badge-tipo {
  padding: 0.3rem 0.8rem;
  border-radius: var(--borda-radius-xl);
  font-size: 0.8rem;
  font-weight: bold;
  display: inline-block;
}

.badge-tipo.gold {
  background: rgba(255, 215, 0, 0.2);
  color: var(--cor-dourado);
  border: 1px solid rgba(255, 215, 0, 0.3);
}

.badge-tipo.premium {
  background: rgba(138, 43, 226, 0.2);
  color: var(--cor-roxo-principal);
  border: 1px solid rgba(138, 43, 226, 0.3);
}

/* Botões */
.acoes-detalhes {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.btn-voltar {
  background: var(--gradiente-botao);
  color: var(--cor-fundo);
  padding: 0.8rem 1.8rem;
  border-radius: var(--borda-radius-lg);
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
}

.btn-voltar:hover {
  transform: translateY(-3px);
  box-shadow: var(--sombra-destaque);
}

.btn-imprimir {
  background: linear-gradient(135deg, #4CAF50, #45a049);
  color: white;
  padding: 0.8rem 1.8rem;
  border: none;
  border-radius: var(--borda-radius-lg);
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
}

.btn-imprimir:hover {
  transform: translateY(-3px);
  box-shadow: var(--sombra-destaque);
}

/* Loading spinner */
.loading-spinner {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: var(--cor-dourado);
}

.loading-spinner i {
  margin-right: 0.5rem;
}

/* Animações */
.fade-in {
  opacity: 0;
  transform: translateY(20px);
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
  padding: 1rem 1.5rem;
  border-radius: var(--borda-radius-md);
  box-shadow: var(--sombra-destaque);
  z-index: 10000;
  display: flex;
  align-items: center;
  gap: 0.8rem;
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

/* Estilos para impressão */
@media print {
  .header, .footer, .acoes-detalhes, .admin-notification, .btn-imprimir, .btn-voltar {
    display: none !important;
  }
  
  .detalhes-container {
    margin: 0;
    padding: 0;
  }
  
  .detalhes-card {
    break-inside: avoid;
    page-break-inside: avoid;
  }
  
  .detalhes-card h3 {
    color: black;
  }
  
  .info-item {
    background: white;
    border: 1px solid #ddd;
  }
  
  .badge-tipo.gold {
    background: #FFD700;
    color: black;
  }
  
  .badge-tipo.premium {
    background: #8A2BE2;
    color: white;
  }
}

/* Responsividade */
@media (max-width: 768px) {
  .detalhes-container {
    margin-top: 100px;
  }

  .detalhes-grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .detalhes-card {
    padding: 1rem;
  }

  .info-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }

  .acoes-detalhes {
    flex-direction: column;
    align-items: center;
  }

  .btn-voltar, .btn-imprimir {
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .detalhes-container {
    padding: 0 15px;
  }

  .detalhes-titulo {
    font-size: 1.6rem;
  }

  .detalhes-card h3 {
    font-size: 1.1rem;
  }

  .info-item {
    padding: 0.6rem 0.8rem;
  }

  .btn-voltar, .btn-imprimir {
    padding: 0.6rem 1.2rem;
  }
}
</style>