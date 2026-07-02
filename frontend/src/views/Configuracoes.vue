<template>
  <div class="configuracoes-page">
    <div class="container">
      <nav class="breadcrumb-nav">
        <router-link to="/">Início</router-link>
        <span>/</span>
        <span>Configurações</span>
      </nav>

      <div v-if="carregando" class="loading-spinner">
        <i class="fas fa-spinner fa-spin"></i> Carregando...
      </div>

      <div v-else class="configuracoes-layout">
        <!-- SIDEBAR -->
        <aside class="configuracoes-sidebar">
          <div class="user-profile-summary">
            <div class="user-avatar"><i class="fas fa-user-circle"></i></div>
            <div class="user-info">
              <h3 :title="`${usuario.nome} ${usuario.sobrenome}`">{{ usuario.nome }} {{ usuario.sobrenome }}</h3>
              <p :title="usuario.email">{{ usuario.email }}</p>
            </div>
          </div>
          <nav class="configuracoes-menu">
            <a href="#" class="menu-item" :class="{ active: aba === 'perfil' }" @click.prevent="aba = 'perfil'">
              <i class="fas fa-user"></i> Perfil
            </a>
            <a href="#" class="menu-item" :class="{ active: aba === 'enderecos' }" @click.prevent="aba = 'enderecos'">
              <i class="fas fa-map-marker-alt"></i> Endereços
            </a>
            <a href="#" class="menu-item" :class="{ active: aba === 'seguranca' }" @click.prevent="aba = 'seguranca'">
              <i class="fas fa-shield-alt"></i> Segurança
            </a>
            <a href="#" class="menu-item" :class="{ active: aba === 'pedidos' }" @click.prevent="aba = 'pedidos'">
              <i class="fas fa-shopping-bag"></i> Meus Pedidos
            </a>
          </nav>
        </aside>

        <!-- CONTEÚDO -->
        <div class="configuracoes-content">

          <!-- ABA PERFIL -->
          <div v-show="aba === 'perfil'" class="tab-content">
            <div class="tab-header">
              <h2>Meu Perfil</h2>
              <p>Gerencie suas informações pessoais</p>
            </div>
            <form @submit.prevent="salvarPerfil">
              <div class="form-grid">
                <div class="form-group">
                  <label>Nome *</label>
                  <input type="text" v-model="usuario.nome" required>
                </div>
                <div class="form-group">
                  <label>Sobrenome *</label>
                  <input type="text" v-model="usuario.sobrenome" required>
                </div>
              </div>
              <div class="form-grid">
                <div class="form-group">
                  <label>Email *</label>
                  <input type="email" v-model="usuario.email" required>
                </div>
                <div class="form-group">
                  <label>Telefone *</label>
                  <input type="tel" v-model="usuario.telefone" required>
                </div>
              </div>
              <div class="form-grid">
                <div class="form-group">
                  <label>CPF</label>
                  <input type="text" v-model="usuario.cpf" :readonly="!!cpfOriginal" :class="{ readonly: !!cpfOriginal }" placeholder="000.000.000-00" maxlength="14" @input="formatarCPF">
                  <small v-if="cpfOriginal" class="dica-cpf">Para alterar o CPF já cadastrado, contate o suporte.</small>
                </div>
                <div class="form-group">
                  <label>Data de Nascimento</label>
                  <input type="date" v-model="usuario.data_nascimento">
                </div>
              </div>
              <p v-if="msgPerfil" class="msg" :class="msgPerfilTipo">{{ msgPerfil }}</p>
              <div class="form-actions">
                <button type="button" class="btn-secondary" @click="carregarDados">Cancelar</button>
                <button type="submit" class="btn-primary" :disabled="salvandoPerfil">
                  <i class="fas fa-save"></i> {{ salvandoPerfil ? 'Salvando...' : 'Salvar Alterações' }}
                </button>
              </div>
            </form>
          </div>

          <!-- ABA ENDEREÇOS -->
          <div v-show="aba === 'enderecos'" class="tab-content">
            <div class="tab-header">
              <h2>Meus Endereços</h2>
              <p>Gerencie seus endereços de entrega</p>
            </div>
            <div class="enderecos-container">
              <div v-for="end in enderecos" :key="end.id" class="endereco-card"
                :class="{ principal: end.principal }">
                <div class="endereco-header">
                  <h3>{{ end.tipo || 'Endereço' }}</h3>
                  <span v-if="end.principal" class="badge-principal">Principal</span>
                </div>
                <div class="endereco-info">
                  <p>{{ end.endereco }}, {{ end.numero }}
                    <span v-if="end.complemento"> — {{ end.complemento }}</span>
                  </p>
                  <p>{{ end.bairro }} — {{ end.cidade }}/{{ end.estado }}</p>
                  <p>CEP: {{ end.cep }}</p>
                </div>
                <div class="endereco-actions">
                  <button class="btn-edit" @click="abrirModal(end)"><i class="fas fa-edit"></i> Editar</button>
                  <button v-if="!end.principal" class="btn-set-primary" @click="setPrincipal(end.id)">
                    <i class="fas fa-star"></i> Tornar Principal
                  </button>
                  <button class="btn-delete" @click="removerEndereco(end.id)"><i class="fas fa-trash"></i></button>
                </div>
              </div>

              <div class="add-endereco-card" @click="abrirModal()">
                <div class="add-endereco-content">
                  <i class="fas fa-plus-circle"></i>
                  <h3>Adicionar Novo Endereço</h3>
                </div>
              </div>
            </div>
          </div>

          <!-- ABA SEGURANÇA -->
          <div v-show="aba === 'seguranca'" class="tab-content">
            <div class="tab-header">
              <h2>Segurança</h2>
              <p>Gerencie a segurança da sua conta</p>
            </div>
            <div class="seguranca-card">
              <h3>Alterar Senha</h3>
              <form @submit.prevent="alterarSenha">
                <div class="form-group">
                  <label>Senha Atual</label>
                  <input type="password" v-model="senhaForm.senha_atual" required>
                </div>
                <div class="form-group">
                  <label>Nova Senha</label>
                  <input type="password" v-model="senhaForm.nova_senha" required>
                  <small v-if="senhaForm.nova_senha && erroNovaSenha" class="erro-senha">{{ erroNovaSenha }}</small>
                </div>
                <div class="form-group">
                  <label>Confirmar Nova Senha</label>
                  <input type="password" v-model="senhaForm.confirmar_senha" required>
                </div>
                <p v-if="msgSenha" class="msg" :class="msgSenhaTipo">{{ msgSenha }}</p>
                <button type="submit" class="btn-primary" :disabled="salvandoSenha">
                  <i class="fas fa-key"></i> {{ salvandoSenha ? 'Salvando...' : 'Alterar Senha' }}
                </button>
              </form>
            </div>
          </div>

          <!-- ABA PEDIDOS -->
          <div v-show="aba === 'pedidos'" class="tab-content">
            <div class="tab-header">
              <h2>Meus Pedidos</h2>
              <p>Histórico de compras</p>
            </div>
            <div v-if="pedidos.length" class="pedidos-lista">
              <div v-for="pedido in pedidos" :key="pedido.id" class="pedido-card">
                <div class="pedido-header" @click="togglePedido(pedido.id)">
                  <div class="pedido-header-info">
                    <span class="pedido-id">#{{ pedido.id }}</span>
                    <span class="badge-status" :class="pedido.status">{{ pedido.status }}</span>
                  </div>
                  <div class="pedido-header-right">
                    <span class="pedido-data">{{ formatarData(pedido.data) }}</span>
                    <span class="pedido-total">{{ formatarMoeda(pedido.valor_total) }}</span>
                    <i class="fas" :class="pedidoAberto === pedido.id ? 'fa-chevron-up' : 'fa-chevron-down'"></i>
                  </div>
                </div>

                <div v-show="pedidoAberto === pedido.id" class="pedido-detalhes">
                  <div v-if="pedido.cupom_aplicado" class="cupom-info">
                    <i class="fas fa-tag"></i>
                    Cupom <strong>{{ pedido.cupom_aplicado }}</strong> —
                    economia de {{ formatarMoeda(pedido.economia) }}
                  </div>
                  <div class="itens-lista">
                    <div v-for="item in pedido.itens" :key="item.id_produto" class="item-pedido">
                      <img :src="item.imagem || '/img/sem_imagem.png'" :alt="item.nome_produto" class="item-img">
                      <div class="item-info">
                        <strong>{{ item.nome_produto }}</strong>
                        <span class="item-plano">Plano {{ item.plano }}</span>
                        <span class="item-qtd">{{ item.quantidade }}x {{ formatarMoeda(item.valor_unitario) }}</span>
                      </div>
                      <span class="item-total">{{ formatarMoeda(item.valor_total) }}</span>
                      <router-link v-if="item.id_produto" :to="`/produto/${item.id_produto}`"
                        class="btn-recomprar" title="Comprar novamente">
                        <i class="fas fa-redo"></i>
                      </router-link>
                    </div>
                  </div>
                  <div class="pedido-resumo">
                    <div v-if="pedido.desconto_aplicado > 0" class="resumo-linha desconto">
                      <span>Desconto</span>
                      <span>- {{ formatarMoeda(pedido.desconto_aplicado) }}</span>
                    </div>
                    <div class="resumo-linha total">
                      <span>Total pago</span>
                      <span>{{ formatarMoeda(pedido.valor_total) }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="pedidos-vazio">
              <i class="fas fa-shopping-bag"></i>
              <p>Você ainda não fez nenhum pedido.</p>
              <router-link to="/#planos" class="btn-modern">Conhecer Planos</router-link>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- MODAL ENDEREÇO -->
    <div v-if="modalAberto" class="modal" @click.self="fecharModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editandoId ? 'Editar Endereço' : 'Novo Endereço' }}</h3>
          <button class="modal-close" @click="fecharModal"><i class="fas fa-times"></i></button>
        </div>
        <form class="endereco-form" @submit.prevent="salvarEndereco">
          <div class="form-group">
            <label>CEP *</label>
            <input type="text" v-model="endForm.cep" @blur="buscarCep" required maxlength="9">
          </div>
          <div class="form-grid">
            <div class="form-group"><label>Endereço *</label><input type="text" v-model="endForm.endereco" required></div>
            <div class="form-group"><label>Número *</label><input type="text" v-model="endForm.numero" required></div>
          </div>
          <div class="form-group"><label>Complemento</label><input type="text" v-model="endForm.complemento"></div>
          <div class="form-grid">
            <div class="form-group"><label>Bairro *</label><input type="text" v-model="endForm.bairro" required></div>
            <div class="form-group"><label>Cidade *</label><input type="text" v-model="endForm.cidade" required></div>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label>Estado *</label>
              <select v-model="endForm.estado" required>
                <option value="">Selecione</option>
                <option v-for="uf in ufList" :key="uf" :value="uf">{{ uf }}</option>
              </select>
            </div>
            <div class="form-group"><label>País *</label><input type="text" v-model="endForm.pais" required></div>
          </div>
          <div class="form-group checkbox-group">
            <input type="checkbox" id="principal" v-model="endForm.principal">
            <label for="principal">Tornar endereço principal</label>
          </div>
          <p v-if="msgEndereco" class="msg" :class="msgEnderecoTipo">{{ msgEndereco }}</p>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="fecharModal">Cancelar</button>
            <button type="submit" class="btn-primary" :disabled="salvandoEnd">
              <i class="fas fa-save"></i> {{ salvandoEnd ? 'Salvando...' : (editandoId ? 'Atualizar' : 'Salvar') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { formatarMoeda } from '@/utils/formatters'
import { validarSenha } from '@/utils/validarSenha'

const router = useRouter()
const authStore = useAuthStore()

const carregando   = ref(true)
const aba          = ref('perfil')
const pedidoAberto = ref(null)

const usuario = reactive({ nome: '', sobrenome: '', email: '', telefone: '', cpf: '', data_nascimento: '' })
const cpfOriginal = ref('')
const enderecos = ref([])
const pedidos   = ref([])

const salvandoPerfil = ref(false)
const msgPerfil      = ref('')
const msgPerfilTipo  = ref('success')

const senhaForm = reactive({ senha_atual: '', nova_senha: '', confirmar_senha: '' })
const salvandoSenha = ref(false)
const msgSenha      = ref('')
const msgSenhaTipo  = ref('success')
const erroNovaSenha = computed(() => validarSenha(senhaForm.nova_senha))

const modalAberto  = ref(false)
const editandoId   = ref(null)
const salvandoEnd  = ref(false)
const msgEndereco  = ref('')
const msgEnderecoTipo = ref('success')
const endForm = reactive({
  cep: '', endereco: '', numero: '', complemento: '',
  bairro: '', cidade: '', estado: '', pais: 'Brasil', principal: false, tipo: 'residencial'
})

const ufList = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

const formatarData = (d) => d ? new Date(d).toLocaleDateString('pt-BR') : ''

function formatarCPF(e) {
  let v = e.target.value.replace(/\D/g, '').slice(0, 11)
  v = v.replace(/(\d{3})(\d)/, '$1.$2')
  v = v.replace(/(\d{3})(\d)/, '$1.$2')
  v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2')
  usuario.cpf = v
}

function togglePedido(id) {
  pedidoAberto.value = pedidoAberto.value === id ? null : id
}

async function carregarDados() {
  carregando.value = true
  try {
    const { data } = await api.get('/configuracoes/perfil')
    Object.assign(usuario, data.usuario)
    cpfOriginal.value = data.usuario?.cpf || ''
    enderecos.value = data.enderecos || []
    pedidos.value   = data.pedidos   || []
  } catch {
    console.error('Erro ao carregar dados.')
  } finally {
    carregando.value = false
  }
}

async function salvarPerfil() {
  salvandoPerfil.value = true
  msgPerfil.value = ''
  try {
    const { data } = await api.put('/configuracoes/perfil', {
      nome: usuario.nome,
      sobrenome: usuario.sobrenome,
      email: usuario.email,
      telefone: usuario.telefone,
      data_nascimento: usuario.data_nascimento || null,
      cpf: cpfOriginal.value ? null : (usuario.cpf || null),
    })
    usuario.cpf = data.cpf || usuario.cpf
    cpfOriginal.value = data.cpf || ''
    msgPerfil.value = 'Perfil atualizado com sucesso!'
    msgPerfilTipo.value = 'msg-success'
  } catch (err) {
    msgPerfil.value = err.response?.data?.detail || 'Erro ao salvar perfil.'
    msgPerfilTipo.value = 'msg-error'
  } finally {
    salvandoPerfil.value = false
  }
}

async function alterarSenha() {
  msgSenha.value = ''
  if (erroNovaSenha.value) {
    msgSenha.value = erroNovaSenha.value
    msgSenhaTipo.value = 'msg-error'
    return
  }
  if (senhaForm.nova_senha !== senhaForm.confirmar_senha) {
    msgSenha.value = 'As senhas não coincidem.'
    msgSenhaTipo.value = 'msg-error'
    return
  }
  salvandoSenha.value = true
  try {
    await api.put('/configuracoes/senha', {
      senha_atual: senhaForm.senha_atual,
      nova_senha: senhaForm.nova_senha,
    })
    msgSenha.value = 'Senha alterada com sucesso!'
    msgSenhaTipo.value = 'msg-success'
    senhaForm.senha_atual = ''
    senhaForm.nova_senha = ''
    senhaForm.confirmar_senha = ''
  } catch (err) {
    msgSenha.value = err.response?.data?.detail || 'Erro ao alterar senha.'
    msgSenhaTipo.value = 'msg-error'
  } finally {
    salvandoSenha.value = false
  }
}

function abrirModal(end = null) {
  msgEndereco.value = ''
  if (end) {
    editandoId.value = end.id
    Object.assign(endForm, end)
  } else {
    editandoId.value = null
    Object.assign(endForm, { cep: '', endereco: '', numero: '', complemento: '', bairro: '', cidade: '', estado: '', pais: 'Brasil', principal: false, tipo: 'residencial' })
  }
  modalAberto.value = true
}

function fecharModal() { modalAberto.value = false }

async function salvarEndereco() {
  salvandoEnd.value = true
  msgEndereco.value = ''
  try {
    if (editandoId.value) {
      await api.put(`/configuracoes/enderecos/${editandoId.value}`, { ...endForm })
    } else {
      await api.post('/configuracoes/enderecos', { ...endForm })
    }
    fecharModal()
    await carregarDados()
  } catch (err) {
    msgEndereco.value = err.response?.data?.detail || 'Erro ao salvar endereço.'
    msgEnderecoTipo.value = 'msg-error'
  } finally {
    salvandoEnd.value = false
  }
}

async function removerEndereco(id) {
  if (!confirm('Excluir este endereço?')) return
  try {
    await api.delete(`/configuracoes/enderecos/${id}`)
    await carregarDados()
  } catch (err) {
    alert(err.response?.data?.detail || 'Erro ao excluir endereço.')
  }
}

async function setPrincipal(id) {
  try {
    await api.patch(`/configuracoes/enderecos/${id}/principal`)
    await carregarDados()
  } catch (err) {
    alert(err.response?.data?.detail || 'Erro ao definir endereço principal.')
  }
}

async function buscarCep() {
  const cep = endForm.cep.replace(/\D/g, '')
  if (cep.length !== 8) return
  try {
    const r = await fetch(`https://viacep.com.br/ws/${cep}/json/`)
    const d = await r.json()
    if (!d.erro) {
      endForm.endereco = d.logradouro || ''
      endForm.bairro   = d.bairro     || ''
      endForm.cidade   = d.localidade || ''
      endForm.estado   = d.uf         || ''
    }
  } catch {}
}

onMounted(async () => {
  if (!authStore.logado) { router.push('/login?redirect=/configuracoes'); return }
  await carregarDados()
})
</script>

<style scoped>
.configuracoes-page {
  padding-top: 100px;
  padding-bottom: var(--espacamento-xl);
  min-height: 100vh;
}
.breadcrumb-nav {
  margin-bottom: var(--espacamento-md);
  font-size: 0.875rem;
  color: var(--cor-texto-secundario);
  display: flex; gap: 0.5rem; align-items: center;
}
.breadcrumb-nav a { color: var(--cor-dourado); text-decoration: none; }

.loading-spinner { text-align: center; padding: var(--espacamento-xl); color: var(--cor-dourado); font-size: 1.2rem; }

.configuracoes-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: var(--espacamento-lg);
  align-items: start;
}

.configuracoes-sidebar {
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-md);
  border: 1px solid rgba(201,168,76,0.2);
  position: sticky; top: 90px;
}
.user-profile-summary {
  display: flex; align-items: center; gap: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(201,168,76,0.2);
  margin-bottom: 1rem;
}
.user-avatar i { font-size: 3rem; color: var(--cor-dourado); flex-shrink: 0; }
.user-info { min-width: 0; }
.user-info h3, .user-info p {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.user-info h3 { color: var(--cor-texto); font-size: 1rem; margin-bottom: 0.2rem; }
.user-info p  { color: var(--cor-texto-secundario); font-size: 0.8125rem; }

.configuracoes-menu { display: flex; flex-direction: column; gap: 0.375rem; }
.menu-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: var(--borda-radius-md);
  color: var(--cor-texto-secundario);
  text-decoration: none;
  font-size: 0.9rem;
  transition: all 0.2s ease;
}
.menu-item:hover { background: rgba(201,168,76,0.08); color: var(--cor-dourado); }
.menu-item.active { background: var(--gradiente-botao); color: var(--cor-fundo); font-weight: 600; }

.configuracoes-content {
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-lg);
  border: 1px solid rgba(201,168,76,0.2);
}

.tab-header {
  margin-bottom: var(--espacamento-lg);
  padding-bottom: var(--espacamento-sm);
  border-bottom: 1px solid rgba(201,168,76,0.15);
}
.tab-header h2 { color: var(--cor-dourado); font-family: var(--fonte-principal); font-size: 1.5rem; margin-bottom: 0.25rem; }
.tab-header p  { color: var(--cor-texto-secundario); font-size: 0.875rem; }

.form-grid {
  display: grid; grid-template-columns: 1fr 1fr;
  gap: var(--espacamento-sm);
  margin-bottom: var(--espacamento-md);
}
.form-group { display: flex; flex-direction: column; gap: 0.4rem; margin-bottom: var(--espacamento-sm); }
.form-group label { font-size: 0.875rem; font-weight: 500; color: var(--cor-texto-secundario); }
.form-group input, .form-group select {
  padding: 0.625rem 0.875rem;
  background: var(--cor-fundo);
  border: 1px solid rgba(201,168,76,0.25);
  border-radius: var(--borda-radius-sm);
  color: var(--cor-texto);
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.2s;
}
.form-group input:focus, .form-group select:focus { border-color: var(--cor-dourado); }
.form-group input.readonly { opacity: 0.5; cursor: not-allowed; }
.dica-cpf { font-size: 0.78rem; color: var(--cor-texto-secundario); }
.erro-senha { color: #e57373; font-size: 0.78rem; }
.checkbox-group { flex-direction: row !important; align-items: center; gap: 0.5rem !important; }
.checkbox-group label { margin: 0; font-size: 0.9rem; color: var(--cor-texto); }

.form-actions { display: flex; gap: var(--espacamento-sm); justify-content: flex-end; margin-top: var(--espacamento-md); }

.msg { font-size: 0.875rem; padding: 0.5rem 0.75rem; border-radius: var(--borda-radius-sm); margin-bottom: var(--espacamento-sm); }
.msg-success { background: rgba(76,175,80,.15); color: #4CAF50; border: 1px solid #4CAF50; }
.msg-error   { background: rgba(244,67,54,.15); color: #f44336; border: 1px solid #f44336; }

.btn-primary {
  background: var(--gradiente-botao); color: var(--cor-fundo);
  border: none; padding: 0.625rem 1.5rem;
  border-radius: var(--borda-radius-sm); font-weight: 600; font-size: 0.9rem;
  cursor: pointer; transition: all 0.25s; display: inline-flex; align-items: center; gap: 0.5rem;
}
.btn-primary:hover:not(:disabled) { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(201,168,76,.3); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-secondary {
  background: transparent; color: var(--cor-texto);
  border: 1px solid rgba(201,168,76,0.4);
  padding: 0.625rem 1.5rem; border-radius: var(--borda-radius-sm);
  font-weight: 500; font-size: 0.9rem; cursor: pointer; transition: all 0.25s;
  display: inline-flex; align-items: center; gap: 0.5rem; text-decoration: none;
}
.btn-secondary:hover { border-color: var(--cor-dourado); color: var(--cor-dourado); }

/* ENDEREÇOS */
.enderecos-container { display: flex; flex-direction: column; gap: var(--espacamento-md); }
.endereco-card {
  background: var(--cor-fundo); border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md); border: 1px solid rgba(201,168,76,0.15);
  transition: border-color 0.2s;
}
.endereco-card.principal { border-color: var(--cor-dourado); background: rgba(201,168,76,0.04); }
.endereco-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
.endereco-header h3 { color: var(--cor-texto); font-size: 1rem; font-weight: 600; }
.badge-principal {
  background: var(--gradiente-botao); color: var(--cor-fundo);
  padding: 0.2rem 0.6rem; border-radius: var(--borda-radius-lg); font-size: 0.75rem; font-weight: 700;
}
.endereco-info p { color: var(--cor-texto-secundario); font-size: 0.875rem; margin: 0.2rem 0; }
.endereco-actions { display: flex; gap: 0.5rem; margin-top: 0.75rem; flex-wrap: wrap; }
.btn-edit, .btn-delete, .btn-set-primary {
  padding: 0.35rem 0.75rem; border-radius: var(--borda-radius-sm);
  font-size: 0.8rem; border: none; cursor: pointer;
  display: inline-flex; align-items: center; gap: 0.35rem;
  transition: all 0.2s; font-weight: 500;
}
.btn-edit       { background: rgba(33,150,243,.2); color: #64B5F6; border: 1px solid #2196F3; }
.btn-delete     { background: rgba(244,67,54,.2);  color: #f44336; border: 1px solid #f44336; }
.btn-set-primary{ background: rgba(76,175,80,.2);  color: #4CAF50; border: 1px solid #4CAF50; }
.btn-edit:hover, .btn-delete:hover, .btn-set-primary:hover { transform: translateY(-2px); filter: brightness(1.15); }

.add-endereco-card {
  border: 2px dashed rgba(201,168,76,0.3); border-radius: var(--borda-radius-md);
  padding: var(--espacamento-lg); text-align: center; cursor: pointer; transition: all 0.2s;
}
.add-endereco-card:hover { border-color: var(--cor-dourado); background: rgba(201,168,76,0.04); }
.add-endereco-content i { font-size: 2rem; color: var(--cor-dourado); margin-bottom: 0.5rem; display: block; }
.add-endereco-content h3 { color: var(--cor-texto-secundario); font-size: 1rem; }

/* SEGURANÇA */
.seguranca-card {
  max-width: 480px;
  background: var(--cor-fundo); padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-md); border: 1px solid rgba(201,168,76,0.15);
}
.seguranca-card h3 { color: var(--cor-dourado); margin-bottom: var(--espacamento-md); font-family: var(--fonte-principal); }

/* PEDIDOS */
.pedidos-lista { display: flex; flex-direction: column; gap: 0.75rem; }
.pedido-card {
  background: var(--cor-fundo); border-radius: var(--borda-radius-md);
  border: 1px solid rgba(201,168,76,0.15); overflow: hidden;
  transition: border-color 0.2s;
}
.pedido-card:hover { border-color: rgba(201,168,76,0.35); }
.pedido-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 1rem var(--espacamento-md); cursor: pointer; flex-wrap: wrap; gap: 0.5rem;
}
.pedido-header:hover { background: rgba(201,168,76,0.04); }
.pedido-header-info { display: flex; align-items: center; gap: 0.75rem; }
.pedido-id { font-family: monospace; font-weight: 700; color: var(--cor-dourado); }
.badge-status {
  padding: 0.2rem 0.6rem; border-radius: var(--borda-radius-lg);
  font-size: 0.75rem; font-weight: 700; text-transform: uppercase; border: 1px solid;
}
.badge-status.pago      { background: rgba(76,175,80,.2);  color: #4CAF50; border-color: #4CAF50; }
.badge-status.pendente  { background: rgba(255,193,7,.2);  color: #FFC107; border-color: #FFC107; }
.badge-status.cancelado { background: rgba(244,67,54,.2);  color: #f44336; border-color: #f44336; }
.badge-status.estornado { background: rgba(33,150,243,.2); color: #2196F3; border-color: #2196F3; }
.pedido-header-right { display: flex; align-items: center; gap: 1rem; }
.pedido-data  { color: var(--cor-texto-secundario); font-size: 0.875rem; }
.pedido-total { font-weight: 700; color: var(--cor-dourado); }
.pedido-header-right .fas { color: var(--cor-texto-secundario); font-size: 0.8rem; }

.pedido-detalhes { border-top: 1px solid rgba(201,168,76,0.1); padding: var(--espacamento-md); }
.cupom-info {
  display: flex; align-items: center; gap: 0.5rem;
  background: rgba(201,168,76,0.08); border: 1px solid rgba(201,168,76,0.2);
  border-radius: var(--borda-radius-sm); padding: 0.5rem 0.875rem;
  font-size: 0.875rem; color: var(--cor-texto-secundario); margin-bottom: var(--espacamento-sm);
}
.cupom-info .fas, .cupom-info strong { color: var(--cor-dourado); }
.itens-lista { display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: var(--espacamento-sm); }
.item-pedido {
  display: flex; align-items: center; gap: 0.75rem;
  background: var(--cor-fundo-secundario); border-radius: var(--borda-radius-sm);
  padding: 0.625rem 0.875rem; border: 1px solid rgba(255,255,255,0.04);
}
.item-img { width: 48px; height: 48px; object-fit: cover; border-radius: var(--borda-radius-sm); flex-shrink: 0; }
.item-info { flex: 1; display: flex; flex-direction: column; gap: 0.15rem; }
.item-info strong { color: var(--cor-texto); font-size: 0.9rem; }
.item-plano { color: var(--cor-dourado); font-size: 0.75rem; text-transform: capitalize; }
.item-qtd   { color: var(--cor-texto-secundario); font-size: 0.8rem; }
.item-total { font-weight: 700; color: var(--cor-dourado); white-space: nowrap; font-size: 0.9rem; }
.btn-recomprar {
  width: 30px; height: 30px; border-radius: 50%;
  background: rgba(201,168,76,0.1); border: 1px solid rgba(201,168,76,0.3);
  color: var(--cor-dourado); display: flex; align-items: center; justify-content: center;
  text-decoration: none; font-size: 0.75rem; transition: all 0.2s; flex-shrink: 0;
}
.btn-recomprar:hover { background: rgba(201,168,76,0.25); transform: scale(1.1); }
.pedido-resumo {
  border-top: 1px solid rgba(255,255,255,0.05);
  padding-top: 0.625rem; display: flex; flex-direction: column;
  gap: 0.3rem; align-items: flex-end;
}
.resumo-linha { display: flex; gap: 2rem; font-size: 0.875rem; }
.resumo-linha.desconto { color: #4CAF50; }
.resumo-linha.total    { font-weight: 700; color: var(--cor-dourado); font-size: 0.9375rem; }

.pedidos-vazio {
  text-align: center; padding: var(--espacamento-xl);
  display: flex; flex-direction: column; align-items: center; gap: var(--espacamento-md);
}
.pedidos-vazio .fas { font-size: 3.5rem; color: var(--cor-dourado); opacity: 0.35; }
.pedidos-vazio p    { color: var(--cor-texto-secundario); }

/* MODAL */
.modal {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.75); backdrop-filter: blur(4px);
  display: flex; align-items: center; justify-content: center; z-index: 2000;
}
.modal-content {
  background: var(--cor-fundo-secundario); border: 1px solid rgba(201,168,76,0.3);
  border-radius: var(--borda-radius-lg); width: 90%; max-width: 560px;
  max-height: 90vh; overflow-y: auto;
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 1.25rem 1.5rem; border-bottom: 1px solid rgba(201,168,76,0.15);
}
.modal-header h3 { color: var(--cor-dourado); font-family: var(--fonte-principal); }
.modal-close { background: none; border: none; color: var(--cor-texto-secundario); font-size: 1.1rem; cursor: pointer; transition: color 0.2s; }
.modal-close:hover { color: var(--cor-texto); }
.endereco-form { padding: 1.5rem; }
.modal-actions {
  display: flex; justify-content: flex-end; gap: 0.75rem;
  margin-top: 1.25rem; padding-top: 1rem;
  border-top: 1px solid rgba(201,168,76,0.15);
}

@media (max-width: 768px) {
  .configuracoes-layout { grid-template-columns: 1fr; }
  .configuracoes-sidebar { position: static; }
  .form-grid { grid-template-columns: 1fr; }
  .pedido-header { flex-direction: column; align-items: flex-start; }
  .pedido-header-right { width: 100%; justify-content: space-between; }
}
</style>