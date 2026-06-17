<template>
  <main class="cupons-container">
    <div class="container">
      <BotaoVoltarAdmin />
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
              <th>Validade</th>
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
            <template v-else>
              <tr v-if="cupons.length === 0">
                <td colspan="6" class="empty-state">
                  <i class="fas fa-tags"></i>
                  <p>Nenhum cupom cadastrado.</p>
                </td>
              </tr>
              <tr v-for="cupom in cupons" :key="cupom.id">
                <td><strong>{{ cupom.codigo }}</strong></td>
                <td>
                  <span v-if="cupom.tipo_desconto === 'fixo'">R$ {{ Number(cupom.desconto_fixo).toFixed(2) }}</span>
                  <span v-else>{{ cupom.desconto_percentual }}%</span>
                </td>
                <td>
                  <span v-if="cupom.valido_ate" :class="['uso-indicator', estaExpirado(cupom.valido_ate) ? 'uso-esgotado' : 'uso-disponivel']">
                    {{ formatarData(cupom.valido_ate) }}
                  </span>
                  <span v-else class="uso-indicator uso-disponivel">Sem prazo</span>
                </td>
                <td>
                  <span v-if="cupom.usos_restantes === null" class="uso-indicator uso-disponivel">Ilimitado</span>
                  <span v-else :class="['uso-indicator', cupom.usos_restantes > 0 ? 'uso-disponivel' : 'uso-esgotado']">
                    {{ cupom.usos_restantes }} / {{ cupom.usos_maximos }}
                  </span>
                </td>
                <td>
                  <span :class="['status-badge', `status-${cupom.status}`]">{{ cupom.status }}</span>
                </td>
                <td class="acoes">
                  <button v-if="cupom.status === 'ativo'" @click="alterarStatus(cupom.id, 'inativo')" class="btn-acao btn-inativar">
                    <i class="fas fa-pause"></i> Inativar
                  </button>
                  <button v-else @click="alterarStatus(cupom.id, 'ativo')" class="btn-acao btn-ativar">
                    <i class="fas fa-play"></i> Ativar
                  </button>
                  <router-link :to="`/admin/cupons/editar/${cupom.id}`" class="btn-acao btn-editar">
                    <i class="fas fa-edit"></i> Editar
                  </router-link>
                  <button @click="excluirCupom(cupom.id)" class="btn-acao btn-excluir">
                    <i class="fas fa-trash"></i> Excluir
                  </button>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
      </div>
    </div>

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
            <label>Tipo de Desconto:</label>
            <div style="display:flex;gap:12px;margin-top:4px">
              <label style="display:flex;align-items:center;gap:6px;cursor:pointer;color:#4B5563;font-size:13px;font-weight:400">
                <input type="radio" v-model="form.tipo_desconto" value="percentual"> Percentual (%)
              </label>
              <label style="display:flex;align-items:center;gap:6px;cursor:pointer;color:#4B5563;font-size:13px;font-weight:400">
                <input type="radio" v-model="form.tipo_desconto" value="fixo"> Valor fixo (R$)
              </label>
            </div>
          </div>

          <div v-if="form.tipo_desconto === 'percentual'" class="form-group">
            <label for="descontoPct">Desconto (%):</label>
            <input type="number" id="descontoPct" v-model.number="form.desconto_percentual"
                   placeholder="Ex: 10 para 10% de desconto" min="1" max="100" :required="form.tipo_desconto === 'percentual'"
                   class="input-cupom">
          </div>
          <div v-else class="form-group">
            <label for="descontoFixo">Valor do Desconto (R$):</label>
            <input type="number" id="descontoFixo" v-model.number="form.desconto_fixo"
                   placeholder="Ex: 50.00" min="0.01" step="0.01" :required="form.tipo_desconto === 'fixo'"
                   class="input-cupom">
          </div>

          <div class="form-group">
            <label>Limite de Usos:</label>
            <div style="display:flex;gap:12px;margin-top:4px;margin-bottom:8px">
              <label style="display:flex;align-items:center;gap:6px;cursor:pointer;color:#4B5563;font-size:13px;font-weight:400">
                <input type="radio" v-model="form.limite_tipo" value="ilimitado"> Ilimitado
              </label>
              <label style="display:flex;align-items:center;gap:6px;cursor:pointer;color:#4B5563;font-size:13px;font-weight:400">
                <input type="radio" v-model="form.limite_tipo" value="quantidade"> Por quantidade
              </label>
              <label style="display:flex;align-items:center;gap:6px;cursor:pointer;color:#4B5563;font-size:13px;font-weight:400">
                <input type="radio" v-model="form.limite_tipo" value="data"> Por data
              </label>
              <label style="display:flex;align-items:center;gap:6px;cursor:pointer;color:#4B5563;font-size:13px;font-weight:400">
                <input type="radio" v-model="form.limite_tipo" value="ambos"> Ambos
              </label>
            </div>
            <input v-if="form.limite_tipo === 'quantidade' || form.limite_tipo === 'ambos'"
                   type="number" v-model.number="form.usos_maximos"
                   placeholder="Usos máximos (ex: 100)" min="1"
                   class="input-cupom" style="margin-bottom:8px">
            <input v-if="form.limite_tipo === 'data' || form.limite_tipo === 'ambos'"
                   type="date" v-model="form.valido_ate"
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
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCuponsAdminStore } from '@/stores/admin/cupons'
import BotaoVoltarAdmin from '@/components/BotaoVoltarAdmin.vue'

const router = useRouter()
const cuponsStore = useCuponsAdminStore()

const cupons = computed(() => cuponsStore.cupons)
const carregando = ref(false)
const modalAberto = ref(false)
const salvando = ref(false)
const erros = ref([])

const form = ref({
  codigo: '',
  tipo_desconto: 'percentual',
  desconto_percentual: '',
  desconto_fixo: '',
  limite_tipo: 'ilimitado',
  usos_maximos: '',
  valido_ate: '',
  status: 'ativo'
})

const carregarCupons = async () => {
  carregando.value = true
  try {
    await cuponsStore.fetchCupons()
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
    tipo_desconto: 'percentual',
    desconto_percentual: '',
    desconto_fixo: '',
    limite_tipo: 'ilimitado',
    usos_maximos: '',
    valido_ate: '',
    status: 'ativo'
  }
}

const validarFormulario = () => {
  erros.value = []
  if (!form.value.codigo || !form.value.codigo.match(/^[A-Z0-9]{3,20}$/)) {
    erros.value.push('Código deve ter 3-20 caracteres (letras maiúsculas e números)')
  }
  if (form.value.tipo_desconto === 'percentual') {
    if (!form.value.desconto_percentual || form.value.desconto_percentual < 1 || form.value.desconto_percentual > 100) {
      erros.value.push('Desconto percentual deve ser entre 1% e 100%')
    }
  } else {
    if (!form.value.desconto_fixo || form.value.desconto_fixo <= 0) {
      erros.value.push('Informe um valor de desconto maior que R$ 0')
    }
  }
  if ((form.value.limite_tipo === 'quantidade' || form.value.limite_tipo === 'ambos') && (!form.value.usos_maximos || form.value.usos_maximos < 1)) {
    erros.value.push('Informe a quantidade máxima de usos')
  }
  if ((form.value.limite_tipo === 'data' || form.value.limite_tipo === 'ambos') && !form.value.valido_ate) {
    erros.value.push('Informe a data de validade')
  }
  return erros.value.length === 0
}

const salvarCupom = async () => {
  if (!validarFormulario()) return
  salvando.value = true
  try {
    const temQtd = form.value.limite_tipo === 'quantidade' || form.value.limite_tipo === 'ambos'
    const temData = form.value.limite_tipo === 'data' || form.value.limite_tipo === 'ambos'
    const dados = {
      codigo: form.value.codigo,
      tipo_desconto: form.value.tipo_desconto,
      desconto_percentual: form.value.tipo_desconto === 'percentual' ? Number(form.value.desconto_percentual) : 0,
      desconto_fixo: form.value.tipo_desconto === 'fixo' ? Number(form.value.desconto_fixo) : null,
      usos_maximos: temQtd ? Number(form.value.usos_maximos) : null,
      valido_ate: temData ? form.value.valido_ate : null,
      status: form.value.status
    }
    await cuponsStore.adicionarCupom(dados)
    mostrarNotificacao('Cupom adicionado com sucesso!', 'success')
    fecharModal()
    await carregarCupons()
  } catch (error) {
    console.error('Erro ao salvar cupom:', error)
    const detail = error?.response?.data?.detail
    const msg = Array.isArray(detail)
      ? detail.map(e => e.msg).join('. ')
      : (typeof detail === 'string' ? detail : error.message || 'Erro ao salvar cupom')
    erros.value.push(msg)
    mostrarNotificacao(msg, 'error')
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
  setTimeout(() => {
    notification.style.opacity = '1'
    notification.style.transform = 'translateX(0)'
  }, 10)
  setTimeout(() => {
    notification.style.opacity = '0'
    setTimeout(() => notification.remove(), 300)
  }, 5000)
}

const formatarData = (data) => {
  if (!data) return ''
  const [ano, mes, dia] = data.split('-')
  return `${dia}/${mes}/${ano}`
}

const estaExpirado = (data) => {
  if (!data) return false
  return new Date(data + 'T23:59:59') < new Date()
}

const handleKeydown = (event) => {
  if (event.key === 'Escape' && modalAberto.value) {
    fecharModal()
  }
}

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

/* ===== ERP LIGHT THEME (sobrescreve o tema escuro acima) ===== */
.cupons-container {
  background: #F4F5F7;
  min-height: 100vh;
  padding: 110px 0 60px;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
}
.cupons-header { text-align: left; }
.cupons-header .titulo-lg {
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
  font-size: 22px;
  font-weight: 700;
  color: #1B1A19;
  text-align: left;
}
.cupons-header .titulo-lg::after { display: none; }
.cupons-header p { color: #6B7280; font-size: 13px; text-align: left; }
.btn-adicionar {
  background: linear-gradient(135deg, #9E7A2E, #E2C06A);
  color: #1B1A19;
  font-family: inherit;
  font-size: 13px;
  font-weight: 600;
  border-radius: 8px;
  box-shadow: none;
}
.btn-adicionar::before { display: none; }
.btn-adicionar:hover { transform: none; opacity: 0.88; box-shadow: none; }
.tabela-wrapper {
  background: #FFFFFF;
  border: 1px solid #E3E5E8;
  border-radius: 10px;
  box-shadow: none;
  padding: 0;
}
.tabela-wrapper::before { display: none; }
thead { background: #F9FAFB; }
th { color: #6B7280; font-size: 11px; letter-spacing: 0.06em; border-bottom: 1px solid #E3E5E8; }
td { color: #1B1A19; border-bottom: 1px solid #F0F1F3; font-size: 13px; }
tbody tr:hover { background: #FAFAF8; transform: none; }
.uso-disponivel { background: #EBF8F0; color: #2E8B57; border-color: #2E8B57; }
.uso-esgotado { background: #FEF2F2; color: #DC2626; border-color: #DC2626; }
.status-ativo { background: #EBF8F0; color: #2E8B57; border-color: #2E8B57; }
.status-inativo { background: #F0F1F3; color: #6B7280; border-color: #9CA3AF; }
.btn-ativar { background: #EBF8F0; color: #2E8B57; border-color: #2E8B57; }
.btn-inativar { background: #FFF8E5; color: #B8860B; border-color: #B8860B; }
.btn-editar { background: #FDF6E5; color: #8A6520; border-color: #C9A84C; }
.btn-excluir { background: #FEF2F2; color: #DC2626; border-color: #DC2626; }
.empty-state { color: #9CA3AF; }
.empty-state i { color: #C9A84C; }
.modal-content {
  background: #FFFFFF;
  border: 1px solid #E3E5E8;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(27, 26, 25, 0.2);
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
}
.modal-content::before { display: none; }
.modal-content .titulo-md { color: #1B1A19; font-family: inherit; font-size: 17px; font-weight: 700; }
.form-group label { color: #4B5563; font-size: 12px; font-weight: 600; }
.input-cupom {
  background: #FFFFFF;
  border: 1px solid #D6D9DE;
  color: #1B1A19;
  font-family: inherit;
}
.input-cupom:focus { border-color: #C9A84C; box-shadow: 0 0 0 3px rgba(201, 168, 76, 0.15); }
.btn-modal-salvar { background: linear-gradient(135deg, #9E7A2E, #E2C06A); color: #1B1A19; }
.btn-modal-cancelar { background: #F0F1F3; color: #4B5563; border: 1px solid #E3E5E8; }
.btn-modal-cancelar:hover { background: #E3E5E8; color: #1B1A19; }
</style>