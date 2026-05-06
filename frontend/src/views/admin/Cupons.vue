<template>
  <main class="cupons-container">
    <div class="container">
      <div class="cupons-header">
        <h1 class="titulo-lg">Gerenciar Cupons de Desconto</h1>
        <p class="texto-corrido texto-centro">Controle os cupons de desconto do Clube do Gole</p>
        <button class="btn-adicionar" @click="abrirModal">
          <i class="fas fa-plus"></i> Adicionar Novo Cupom
        </button>
      </div>

      <div class="tabela-wrapper">
        <table id="tabelaCupons">
          <thead>
            <tr>
              <th>Código</th>
              <th>Desconto</th>
              <th>Usos Máximos</th>
              <th>Usos Restantes</th>
              <th>Status</th>
              <th>Ações</th>
            </tr>
          </thead>
          <tbody id="tbodyCupons">
            <tr v-if="carregando">
              <td colspan="6" class="texto-centro">
                <i class="fas fa-spinner fa-spin"></i> Carregando...
              </td>
            </tr>
            <tr v-else-if="cupons.length === 0">
              <td colspan="6" class="empty-state">
                <i class="fas fa-tags"></i>
                <p>Nenhum cupom cadastrado.</p>
              </td>
            </tr>
            <tr v-else v-for="cupom in cupons" :key="cupom.id" class="fade-in">
              <td><strong>{{ cupom.codigo }}</strong></td>
              <td>{{ cupom.desconto_percentual }}%</td>
              <td>{{ cupom.usos_maximos }}</td>
              <td>
                <span :class="['uso-indicator', cupom.usos_restantes > 0 ? 'uso-disponivel' : 'uso-esgotado']">
                  {{ cupom.usos_restantes }}
                </span>
              </td>
              <td>
                <span :class="['status-badge', `status-${cupom.status}`]">{{ cupom.status | capitalize }}</span>
              </td>
              <td class="acoes">
                <!-- Botão Ativar/Inativar -->
                <button v-if="cupom.status === 'ativo'" @click="alterarStatus(cupom.id, 'inativo')" class="btn-acao btn-inativar">
                  <i class="fas fa-pause"></i> Inativar
                </button>
                <button v-else @click="alterarStatus(cupom.id, 'ativo')" class="btn-acao btn-ativar">
                  <i class="fas fa-play"></i> Ativar
                </button>

                <!-- Botão Editar -->
                <router-link :to="`/admin/cupons/editar/${cupom.id}`" class="btn-acao btn-editar">
                  <i class="fas fa-edit"></i> Editar
                </router-link>

                <!-- Botão Excluir -->
                <button @click="excluirCupom(cupom.id)" class="btn-acao btn-excluir">
                  <i class="fas fa-trash"></i> Excluir
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- MODAL DE ADIÇÃO -->
    <div v-if="modalAberto" class="modal" @click.self="fecharModal">
      <div class="modal-content">
        <h2 class="titulo-md"><i class="fas fa-tag"></i> Adicionar Novo Cupom</h2>
        <form @submit.prevent="salvarCupom" id="formCupom">
          <div class="form-group">
            <label for="codigoCupom">Código do Cupom:</label>
            <input type="text" id="codigoCupom" v-model="form.codigo" placeholder="Ex: CLUBE10" 
                   required maxlength="20" @input="form.codigo = form.codigo.toUpperCase().replace(/[^A-Z0-9]/g, '')"
                   class="input-cupom">
          </div>

          <div class="form-group">
            <label for="descontoCupom">Desconto (%):</label>
            <input type="number" id="descontoCupom" v-model.number="form.desconto_percentual" 
                   placeholder="Ex: 10 para 10% de desconto" min="1" max="100" required
                   class="input-cupom">
          </div>

          <div class="form-group">
            <label for="usosCupom">Usos Máximos:</label>
            <input type="number" id="usosCupom" v-model.number="form.usos_maximos" 
                   placeholder="Ex: 100" min="1" required
                   class="input-cupom">
          </div>

          <div class="form-group">
            <label for="statusCupom">Status Inicial:</label>
            <select id="statusCupom" v-model="form.status" required class="input-cupom">
              <option value="ativo">Ativo</option>
              <option value="inativo">Inativo</option>
            </select>
          </div>

          <div v-if="erros.length" class="erros-container">
            <div v-for="erro in erros" :key="erro" class="erro-mensagem">
              <i class="fas fa-exclamation-circle"></i> {{ erro }}
            </div>
          </div>

          <div class="modal-buttons">
            <button type="button" class="btn-modal btn-modal-cancelar" @click="fecharModal">Cancelar</button>
            <button type="submit" class="btn-modal btn-modal-salvar" :disabled="salvando">
              {{ salvando ? 'Salvando...' : 'Salvar Cupom' }}
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
import { useCuponsAdminStore } from '@/stores/admin/cupons'

const router = useRouter()
const cuponsStore = useCuponsAdminStore()

// Estados
const cupons = ref([])
const carregando = ref(false)
const modalAberto = ref(false)
const salvando = ref(false)
const erros = ref([])

// Formulário
const form = ref({
  codigo: '',
  desconto_percentual: '',
  usos_maximos: '',
  status: 'ativo'
})

// Funções
const carregarCupons = async () => {
  carregando.value = true
  try {
    cupons.value = await cuponsStore.fetchCupons()
  } catch (error) {
    console.error('Erro ao carregar cupons:', error)
    mostrarNotificacao('Erro ao carregar cupons', 'error')
  } finally {
    carregando.value = false
  }
}

const abrirModal = () => {
  modalAberto.value = true
  document.body.style.overflow = 'hidden'
  resetForm()
  erros.value = []
}

const fecharModal = () => {
  modalAberto.value = false
  document.body.style.overflow = ''
  resetForm()
  erros.value = []
}

const resetForm = () => {
  form.value = {
    codigo: '',
    desconto_percentual: '',
    usos_maximos: '',
    status: 'ativo'
  }
}

const validarFormulario = () => {
  erros.value = []
  
  if (!form.value.codigo || form.value.codigo.length < 3) {
    erros.value.push('Código deve ter pelo menos 3 caracteres')
  }
  if (!form.value.codigo.match(/^[A-Z0-9]{3,20}$/)) {
    erros.value.push('Código deve conter apenas letras maiúsculas e números')
  }
  if (!form.value.desconto_percentual || form.value.desconto_percentual < 1 || form.value.desconto_percentual > 100) {
    erros.value.push('Desconto deve ser entre 1% e 100%')
  }
  if (!form.value.usos_maximos || form.value.usos_maximos < 1) {
    erros.value.push('Usos máximos deve ser pelo menos 1')
  }
  
  return erros.value.length === 0
}

const salvarCupom = async () => {
  if (!validarFormulario()) return
  
  salvando.value = true
  try {
    const dados = {
      codigo: form.value.codigo,
      desconto_percentual: form.value.desconto_percentual,
      usos_maximos: form.value.usos_maximos,
      status: form.value.status
    }
    
    await cuponsStore.adicionarCupom(dados)
    mostrarNotificacao('Cupom adicionado com sucesso!', 'success')
    fecharModal()
    await carregarCupons()
  } catch (error) {
    console.error('Erro ao salvar cupom:', error)
    mostrarNotificacao(error.message || 'Erro ao salvar cupom', 'error')
  } finally {
    salvando.value = false
  }
}

const alterarStatus = async (id, novoStatus) => {
  const acao = novoStatus === 'ativo' ? 'ativar' : 'inativar'
  if (!confirm(`Tem certeza que deseja ${acao} este cupom?`)) return
  
  try {
    await cuponsStore.alterarStatus(id, novoStatus)
    mostrarNotificacao(`Cupom ${acao}do com sucesso!`, 'success')
    await carregarCupons()
  } catch (error) {
    console.error('Erro ao alterar status:', error)
    mostrarNotificacao('Erro ao alterar status', 'error')
  }
}

const excluirCupom = async (id) => {
  if (!confirm('Tem certeza que deseja excluir este cupom?')) return
  
  try {
    await cuponsStore.excluirCupom(id)
    mostrarNotificacao('Cupom excluído com sucesso!', 'success')
    await carregarCupons()
  } catch (error) {
    console.error('Erro ao excluir cupom:', error)
    mostrarNotificacao('Erro ao excluir cupom', 'error')
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
  carregarCupons()
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = ''
})
</script>

<style scoped>
/* ===== ESTILOS EXCLUSIVOS DO ADMIN CUPONS ===== */
.cupons-container {
  padding: 140px 0 var(--espacamento-xl);
  background: var(--gradiente-hero);
  min-height: 100vh;
}

.cupons-header {
  text-align: center;
  margin-bottom: var(--espacamento-lg);
}

.cupons-header .titulo-lg {
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-sm);
  position: relative;
}

.cupons-header .titulo-lg::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background: var(--gradiente-botao);
  border-radius: var(--borda-radius-sm);
}

.btn-adicionar {
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
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: var(--espacamento-sm);
}

.btn-adicionar::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.btn-adicionar:hover::before {
  left: 100%;
}

.btn-adicionar:hover {
  transform: translateY(-3px);
  box-shadow: var(--sombra-destaque);
}

/* Tabela */
.tabela-wrapper {
  overflow-x: auto;
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-md);
  border: 1px solid rgba(255, 215, 0, 0.2);
  box-shadow: var(--sombra-card);
  position: relative;
}

.tabela-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradiente-botao);
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: var(--cor-roxo-principal);
}

th {
  padding: 1rem;
  text-align: left;
  color: var(--cor-texto);
  font-weight: 600;
  border-bottom: 2px solid var(--cor-dourado);
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

td {
  padding: 1rem;
  color: var(--cor-texto);
  vertical-align: middle;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.95rem;
}

tbody tr {
  transition: all 0.3s ease;
}

tbody tr:hover {
  background: rgba(255, 215, 0, 0.05);
  transform: translateX(5px);
}

/* Indicadores */
.uso-indicator {
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: var(--borda-radius-sm);
  font-size: 0.85rem;
}

.uso-disponivel {
  background: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.uso-esgotado {
  background: rgba(244, 67, 54, 0.2);
  color: #f44336;
  border: 1px solid rgba(244, 67, 54, 0.3);
}

.status-badge {
  font-weight: 600;
  padding: 0.25rem 0.75rem;
  border-radius: var(--borda-radius-sm);
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-ativo {
  background: rgba(76, 175, 80, 0.2);
  color: #4CAF50;
  border: 1px solid rgba(76, 175, 80, 0.3);
}

.status-inativo {
  background: rgba(255, 152, 0, 0.2);
  color: #ff9800;
  border: 1px solid rgba(255, 152, 0, 0.3);
}

/* Botões de ação */
.acoes {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-acao {
  padding: 0.5rem 0.75rem;
  border-radius: var(--borda-radius-sm);
  text-decoration: none;
  font-size: 0.8rem;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  white-space: nowrap;
  border: 1px solid transparent;
  cursor: pointer;
  background: none;
}

.btn-ativar {
  background: rgba(76, 175, 80, 0.1);
  color: #4CAF50;
  border-color: rgba(76, 175, 80, 0.3);
}

.btn-ativar:hover {
  background: #4CAF50;
  color: white;
  transform: translateY(-2px);
}

.btn-inativar {
  background: rgba(255, 152, 0, 0.1);
  color: #ff9800;
  border-color: rgba(255, 152, 0, 0.3);
}

.btn-inativar:hover {
  background: #ff9800;
  color: white;
  transform: translateY(-2px);
}

.btn-editar {
  background: rgba(33, 150, 243, 0.1);
  color: #2196F3;
  border-color: rgba(33, 150, 243, 0.3);
}

.btn-editar:hover {
  background: #2196F3;
  color: white;
  transform: translateY(-2px);
}

.btn-excluir {
  background: rgba(244, 67, 54, 0.1);
  color: #f44336;
  border-color: rgba(244, 67, 54, 0.3);
}

.btn-excluir:hover {
  background: #f44336;
  color: white;
  transform: translateY(-2px);
}

/* Estado vazio */
.empty-state {
  text-align: center;
  color: var(--cor-texto-secundario);
  padding: var(--espacamento-lg) !important;
}

.empty-state i {
  font-size: 3rem;
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-sm);
  display: block;
  opacity: 0.7;
}

.texto-centro {
  text-align: center;
}

/* Modal */
.modal {
  position: fixed;
  z-index: 10000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(5px);
  animation: fadeIn 0.3s ease-out;
}

.modal-content {
  background: var(--cor-fundo-secundario);
  padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-lg);
  border: 1px solid rgba(255, 215, 0, 0.2);
  max-width: 500px;
  width: 90%;
  animation: slideDown 0.3s ease-out;
  position: relative;
  box-shadow: var(--sombra-destaque);
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradiente-botao);
}

.modal-content .titulo-md {
  color: var(--cor-dourado);
  margin-bottom: var(--espacamento-md);
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

/* Formulário */
.form-group {
  margin-bottom: var(--espacamento-md);
}

.form-group label {
  display: block;
  margin-bottom: var(--espacamento-xs);
  color: var(--cor-dourado);
  font-weight: 500;
  font-size: 0.9rem;
}

.input-cupom {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--borda-radius-md);
  background: var(--cor-fundo);
  color: var(--cor-texto);
  font-size: 1rem;
  transition: all 0.3s ease;
}

.input-cupom:focus {
  outline: none;
  border-color: var(--cor-dourado);
  box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.1);
}

.erros-container {
  background: rgba(244, 67, 54, 0.1);
  border: 1px solid #f44336;
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-sm);
  margin-bottom: var(--espacamento-md);
}

.erro-mensagem {
  color: #f44336;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.erro-mensagem:last-child {
  margin-bottom: 0;
}

.modal-buttons {
  display: flex;
  gap: var(--espacamento-sm);
  justify-content: flex-end;
  margin-top: var(--espacamento-lg);
}

.btn-modal {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: var(--borda-radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-modal-salvar {
  background: var(--gradiente-botao);
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
  background: rgba(255, 255, 255, 0.1);
  color: var(--cor-texto);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.btn-modal-cancelar:hover {
  background: rgba(255, 255, 255, 0.2);
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
  z-index: 10001;
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

/* Animações */
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
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

/* Responsividade */
@media (max-width: 1024px) {
  .cupons-container {
    padding: 120px 0 var(--espacamento-lg);
  }
  .tabela-wrapper {
    padding: var(--espacamento-sm);
  }
}

@media (max-width: 768px) {
  .cupons-container {
    padding: 100px 0 var(--espacamento-md);
  }
  .acoes {
    flex-direction: column;
    gap: 0.25rem;
  }
  .btn-acao {
    justify-content: center;
    font-size: 0.75rem;
  }
  table {
    font-size: 0.85rem;
  }
  th, td {
    padding: 0.75rem 0.5rem;
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
  .cupons-header .titulo-lg {
    font-size: 2rem;
  }
  table {
    font-size: 0.75rem;
  }
  .uso-indicator,
  .status-badge {
    font-size: 0.7rem;
    padding: 0.2rem 0.5rem;
  }
  .modal-content {
    padding: var(--espacamento-sm);
  }
}
</style>