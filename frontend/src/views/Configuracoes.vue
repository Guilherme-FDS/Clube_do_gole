<template>
  <DefaultLayout>
    <div class="container" style="margin-top: 120px; min-height: 60vh; padding-bottom: 4rem;">
      <nav class="breadcrumb-nav">
        <router-link to="/">Início</router-link>
        <span>/</span>
        <span>Configurações</span>
      </nav>

      <div class="configuracoes-layout">
        <!-- Sidebar -->
        <div class="configuracoes-sidebar">
          <div class="user-profile-summary">
            <div class="user-avatar"><i class="fas fa-user-circle"></i></div>
            <div class="user-info" v-if="usuario">
              <h3>{{ usuario.nome }} {{ usuario.sobrenome }}</h3>
              <p>{{ usuario.email }}</p>
            </div>
          </div>
          <nav class="configuracoes-menu">
            <a v-for="tab in tabs" :key="tab.id" href="#"
               class="menu-item" :class="{ active: abaAtiva === tab.id }"
               @click.prevent="abaAtiva = tab.id">
              <i :class="tab.icone"></i> {{ tab.label }}
            </a>
          </nav>
        </div>

        <!-- Conteúdo -->
        <div class="configuracoes-content">

          <!-- Perfil -->
          <div v-if="abaAtiva === 'perfil'" class="tab-content active">
            <div class="tab-header">
              <h2>Meu Perfil</h2>
              <p>Gerencie suas informações pessoais</p>
            </div>
            <div v-if="msgPerfil" :class="`config-notification ${msgPerfilTipo}`" style="position:static;transform:none;opacity:1;margin-bottom:1rem;">{{ msgPerfil }}</div>
            <form class="perfil-form" @submit.prevent="salvarPerfil">
              <div class="form-grid">
                <div class="form-group"><label>Nome *</label><input v-model="formPerfil.nome" type="text" required /></div>
                <div class="form-group"><label>Sobrenome *</label><input v-model="formPerfil.sobrenome" type="text" required /></div>
              </div>
              <div class="form-grid">
                <div class="form-group"><label>Email *</label><input v-model="formPerfil.email" type="email" required /></div>
                <div class="form-group"><label>Telefone *</label><input v-model="formPerfil.telefone" type="tel" required /></div>
              </div>
              <div class="form-grid">
                <div class="form-group"><label>CPF</label><input :value="usuario?.cpf" type="text" readonly class="readonly" /></div>
                <div class="form-group"><label>Data de Nascimento</label><input v-model="formPerfil.data_nascimento" type="date" /></div>
              </div>
              <div class="form-actions">
                <button type="button" class="btn-secondary" @click="resetPerfil">Cancelar</button>
                <button type="submit" class="btn-primary"><i class="fas fa-save"></i> Salvar Alterações</button>
              </div>
            </form>
          </div>

          <!-- Endereços -->
          <div v-if="abaAtiva === 'enderecos'" class="tab-content active">
            <div class="tab-header">
              <h2>Meus Endereços</h2>
              <p>Gerencie seus endereços de entrega</p>
            </div>
            <div class="enderecos-container">
              <div v-for="e in enderecos" :key="e.id" class="endereco-card" :class="{ principal: e.principal === 'sim' }">
                <div class="endereco-header">
                  <h3>{{ e.principal === 'sim' ? 'Endereço Principal' : 'Endereço' }}</h3>
                  <span v-if="e.principal === 'sim'" class="badge-principal">Principal</span>
                </div>
                <div class="endereco-info">
                  <p><strong>{{ usuario?.nome }} {{ usuario?.sobrenome }}</strong></p>
                  <p>{{ e.endereco }}, {{ e.numero }}</p>
                  <p v-if="e.complemento">Complemento: {{ e.complemento }}</p>
                  <p>{{ e.bairro }} - {{ e.cidade }}/{{ e.estado }}</p>
                  <p>CEP: {{ e.cep }}</p>
                </div>
                <div class="endereco-actions">
                  <button class="btn-edit" @click="abrirModal(e)"><i class="fas fa-edit"></i> Editar</button>
                  <button v-if="e.principal !== 'sim'" class="btn-set-primary" @click="tornarPrincipal(e.id)">
                    <i class="fas fa-star"></i> Tornar Principal
                  </button>
                  <button class="btn-delete" @click="excluirEndereco(e.id)">
                    <i class="fas fa-trash"></i> Excluir
                  </button>
                </div>
              </div>

              <div class="add-endereco-card" @click="abrirModal()">
                <div class="add-endereco-content">
                  <i class="fas fa-plus-circle"></i>
                  <h3>Adicionar Novo Endereço</h3>
                  <p>Clique para cadastrar um novo endereço</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Segurança -->
          <div v-if="abaAtiva === 'seguranca'" class="tab-content active">
            <div class="tab-header">
              <h2>Segurança</h2>
              <p>Gerencie a segurança da sua conta</p>
            </div>
            <div v-if="msgSenha" :class="`config-notification ${msgSenhaTipo}`" style="position:static;transform:none;opacity:1;margin-bottom:1rem;">{{ msgSenha }}</div>
            <div class="seguranca-card">
              <h3>Alterar Senha</h3>
              <form class="senha-form" @submit.prevent="alterarSenha">
                <div class="form-group"><label>Senha Atual</label><input v-model="formSenha.senha_atual" type="password" required /></div>
                <div class="form-group"><label>Nova Senha</label><input v-model="formSenha.nova_senha" type="password" required /></div>
                <div class="form-group"><label>Confirmar Nova Senha</label><input v-model="formSenha.confirmar" type="password" required /></div>
                <button type="submit" class="btn-primary"><i class="fas fa-key"></i> Alterar Senha</button>
              </form>
            </div>
          </div>

          <!-- Pedidos -->
          <div v-if="abaAtiva === 'pedidos'" class="tab-content active">
            <div class="tab-header">
              <h2>Meus Pedidos</h2>
              <p>Acompanhe seus pedidos</p>
            </div>
            <div v-if="pedidos.length" class="pedidos-container">
              <div v-for="pedido in pedidos" :key="pedido.id_compra" class="pedido-card">
                <div class="pedido-header">
                  <div class="pedido-info">
                    <h3>Pedido #{{ pedido.id_compra?.slice(0,8) }}...</h3>
                    <span class="pedido-data">{{ pedido.data }}</span>
                  </div>
                  <div class="pedido-status"><span class="status-entregue">Entregue</span></div>
                </div>
                <div class="pedido-detalhes">
                  <div class="produto-info">
                    <div v-if="pedido.imagem_produto" class="produto-imagem">
                      <img :src="pedido.imagem_produto" :alt="pedido.nome_produto" />
                    </div>
                    <div class="produto-detalhes">
                      <h4>{{ pedido.nome_produto }}</h4>
                      <p>Quantidade: {{ pedido.quantidade }}</p>
                      <p><strong>Plano:</strong> <span :class="`plano-tag ${pedido.plano}`">{{ pedido.plano }}</span></p>
                    </div>
                  </div>
                  <div class="pedido-valores">
                    <div class="valor-item">
                      <span class="valor-label">Valor Original:</span>
                      <span class="valor-original">R$ {{ fmt(pedido.valor_sem_desconto) }}</span>
                    </div>
                    <div class="valor-item">
                      <span class="valor-label">Valor Pago:</span>
                      <span class="valor-desconto">R$ {{ fmt(pedido.valor_com_desconto) }}</span>
                    </div>
                    <div v-if="pedido.cupom_aplicado?.trim()" class="valor-item">
                      <span class="valor-label">Cupom:</span>
                      <span style="color:#007bff;font-weight:bold">{{ pedido.cupom_aplicado }}</span>
                    </div>
                  </div>
                </div>
                <div class="pedido-actions">
                  <router-link :to="`/produto/${pedido.id_produto}`" class="btn-secondary">
                    <i class="fas fa-redo"></i> Comprar Novamente
                  </router-link>
                </div>
              </div>
            </div>
            <div v-else class="pedidos-vazios">
              <div class="vazio-content">
                <i class="fas fa-shopping-bag"></i>
                <h3>Nenhum pedido encontrado</h3>
                <p>Você ainda não realizou nenhuma compra.</p>
                <a href="/#planos" class="btn-primary"><i class="fas fa-shopping-cart"></i> Fazer Compras</a>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <ModalEndereco
      :aberto="modalAberto"
      :endereco="enderecoEditando"
      @fechar="fecharModal"
      @salvo="onEnderecoSalvo"
    />
  </DefaultLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DefaultLayout from '@/layouts/DefaultLayout.vue'
import ModalEndereco from '@/components/ModalEndereco.vue'
import api from '@/services/api'

const tabs = [
  { id: 'perfil',    label: 'Perfil',        icone: 'fas fa-user' },
  { id: 'enderecos', label: 'Endereços',     icone: 'fas fa-map-marker-alt' },
  { id: 'seguranca', label: 'Segurança',     icone: 'fas fa-shield-alt' },
  { id: 'pedidos',   label: 'Meus Pedidos',  icone: 'fas fa-shopping-bag' },
]

const abaAtiva        = ref('perfil')
const usuario         = ref(null)
const enderecos       = ref([])
const pedidos         = ref([])
const modalAberto     = ref(false)
const enderecoEditando = ref(null)
const msgPerfil       = ref(''); const msgPerfilTipo = ref('success')
const msgSenha        = ref(''); const msgSenhaTipo  = ref('success')
const formPerfil = ref({ nome: '', sobrenome: '', email: '', telefone: '', data_nascimento: '' })
const formSenha  = ref({ senha_atual: '', nova_senha: '', confirmar: '' })

function fmt(v) { return parseFloat(v || 0).toFixed(2).replace('.', ',') }
function abrirModal(e = null) { enderecoEditando.value = e; modalAberto.value = true }
function fecharModal()        { modalAberto.value = false; enderecoEditando.value = null }
function resetPerfil()        { if (usuario.value) Object.assign(formPerfil.value, usuario.value) }

async function salvarPerfil() {
  try {
    const { data } = await api.put('/configuracoes/perfil', formPerfil.value)
    msgPerfil.value = data.message; msgPerfilTipo.value = data.success ? 'success' : 'error'
  } catch { msgPerfil.value = 'Erro ao salvar'; msgPerfilTipo.value = 'error' }
}

async function alterarSenha() {
  if (formSenha.value.nova_senha !== formSenha.value.confirmar) {
    msgSenha.value = 'As senhas não coincidem'; msgSenhaTipo.value = 'error'; return
  }
  try {
    const { data } = await api.put('/configuracoes/senha', formSenha.value)
    msgSenha.value = data.message; msgSenhaTipo.value = data.success ? 'success' : 'error'
    if (data.success) formSenha.value = { senha_atual: '', nova_senha: '', confirmar: '' }
  } catch { msgSenha.value = 'Erro ao alterar senha'; msgSenhaTipo.value = 'error' }
}

async function onEnderecoSalvo(dados) {
  if (enderecoEditando.value?.id)
    await api.put(`/configuracoes/enderecos/${enderecoEditando.value.id}`, dados)
  else
    await api.post('/configuracoes/enderecos', dados)
  await carregarDados(); fecharModal()
}

async function excluirEndereco(id) {
  if (!confirm('Excluir este endereço?')) return
  await api.delete(`/configuracoes/enderecos/${id}`)
  await carregarDados()
}

async function tornarPrincipal(id) {
  await api.patch(`/configuracoes/enderecos/${id}/principal`)
  await carregarDados()
}

async function carregarDados() {
  const { data } = await api.get('/configuracoes/perfil')
  usuario.value   = data.usuario
  enderecos.value = data.enderecos
  pedidos.value   = data.pedidos
  Object.assign(formPerfil.value, data.usuario)
}

onMounted(carregarDados)
</script>

<style scoped>
/* Layout */
.configuracoes-layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: var(--espacamento-lg, 2rem);
  margin-top: var(--espacamento-lg, 2rem);
}

.breadcrumb-nav {
  display: flex; align-items: center; gap: 0.5rem;
  margin-bottom: 1rem; font-size: 0.9rem; color: #666;
}
.breadcrumb-nav a { color: #FFD700; text-decoration: none; }
.breadcrumb-nav a:hover { text-decoration: underline; }

/* Sidebar */
.configuracoes-sidebar {
  background: #fff; border-radius: 12px; padding: 1.5rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1); height: fit-content;
  position: sticky; top: 140px;
}

.user-profile-summary {
  display: flex; align-items: center; gap: 1rem;
  padding-bottom: 1.5rem; border-bottom: 1px solid #e1e5e9; margin-bottom: 1rem;
}
.user-avatar { font-size: 2.5rem; color: #FFD700; }
.user-info h3 { margin: 0; font-size: 1.1rem; color: #333; }
.user-info p  { margin: 0.25rem 0 0; color: #666; font-size: 0.9rem; }

.configuracoes-menu { display: flex; flex-direction: column; gap: 0.5rem; }
.menu-item {
  display: flex; align-items: center; gap: 0.75rem;
  padding: 1rem; text-decoration: none; color: #666;
  border-radius: 8px; transition: all 0.3s;
}
.menu-item:hover  { background: black; color: #FFD700; }
.menu-item.active { background: #FFD700; color: black; }

/* Conteúdo */
.configuracoes-content {
  background: #fff; border-radius: 12px;
  padding: 2rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.tab-content { display: block; }
.tab-header { margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 1px solid #e1e5e9; }
.tab-header h2 { margin: 0 0 0.5rem; color: #333; }
.tab-header p  { margin: 0; color: #666; }

/* Forms */
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem; }
.form-group { margin-bottom: 1.5rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; color: #333; }
.form-group input {
  width: 100%; padding: 0.75rem;
  border: 1px solid #e1e5e9; border-radius: 8px; font-size: 1rem;
  transition: border-color 0.3s; background: #fff; color: #333;
}
.form-group input:focus { outline: none; border-color: #FFD700; }
.form-group input.readonly { background: #f8f9fa; color: #666; cursor: not-allowed; }

.form-actions { display: flex; gap: 1rem; justify-content: flex-end; margin-top: 2rem; }

/* Botões */
.btn-primary {
  background: #FFD700; color: black; border: none;
  padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer;
  font-size: 1rem; font-weight: 500; transition: all 0.3s;
  display: flex; align-items: center; gap: 0.5rem; text-decoration: none;
}
.btn-primary:hover { background: #E6C200; transform: translateY(-2px); }

.btn-secondary {
  background: #6c757d; color: #fff; border: none;
  padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer;
  font-size: 1rem; font-weight: 500; transition: all 0.3s; text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem;
}
.btn-secondary:hover { background: #5a6268; }

/* Endereços */
.enderecos-container { display: grid; gap: 1.5rem; }
.endereco-card {
  background: #f8f9fa; border-radius: 12px; padding: 1.5rem;
  border: 2px solid transparent; transition: all 0.3s;
}
.endereco-card.principal { border-color: #FFD700; background: #f0f7ff; }
.endereco-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; }
.endereco-header h3 { margin: 0; color: #333; }
.badge-principal { background: #FFD700; color: black; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }
.endereco-info p { margin: 0.5rem 0; color: #666; }
.endereco-info p strong { color: #333; }
.endereco-actions { margin-top: 1rem; display: flex; gap: 1rem; flex-wrap: wrap; }

.btn-edit       { background: #007bff; color: #fff; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; font-size: 0.9rem; display: flex; align-items: center; gap: 5px; transition: background 0.3s; }
.btn-edit:hover { background: #0056b3; }
.btn-delete       { background: #dc3545; color: #fff; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; font-size: 0.9rem; display: flex; align-items: center; gap: 5px; transition: background 0.3s; }
.btn-delete:hover { background: #c82333; }
.btn-set-primary       { background: #28a745; color: #fff; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; font-size: 0.9rem; display: flex; align-items: center; gap: 5px; transition: background 0.3s; }
.btn-set-primary:hover { background: #218838; }

.add-endereco-card {
  background: #f8f9fa; border: 2px dashed #e1e5e9;
  border-radius: 12px; padding: 2rem; text-align: center; cursor: pointer; transition: all 0.3s;
}
.add-endereco-card:hover { border-color: #FFD700; background: #f0f7ff; }
.add-endereco-content i  { font-size: 2.5rem; color: #FFD700; margin-bottom: 1rem; }
.add-endereco-content h3 { margin: 0 0 0.5rem; color: #333; }
.add-endereco-content p  { margin: 0; color: #666; }

/* Segurança */
.seguranca-card { background: #f8f9fa; border-radius: 12px; padding: 2rem; max-width: 500px; }
.seguranca-card h3 { margin: 0 0 1.5rem; color: #333; }

/* Pedidos */
.pedidos-container { display: flex; flex-direction: column; gap: 1.5rem; }
.pedido-card { background: #fff; border-radius: 12px; padding: 1.5rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border: 1px solid #e1e5e9; }
.pedido-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #e1e5e9; }
.pedido-info h3 { margin: 0; color: #2d3748; }
.pedido-data    { color: #718096; font-size: 0.9rem; }
.status-entregue { background: #48bb78; color: #fff; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.8rem; font-weight: 500; }
.pedido-detalhes { display: grid; grid-template-columns: 1fr auto; gap: 2rem; margin-bottom: 1rem; }
.produto-info { display: flex; gap: 1rem; align-items: flex-start; }
.produto-imagem { width: 80px; height: 80px; border-radius: 8px; overflow: hidden; flex-shrink: 0; }
.produto-imagem img { width: 100%; height: 100%; object-fit: cover; }
.produto-detalhes h4 { margin: 0 0 0.5rem; color: #2d3748; }
.produto-detalhes p  { margin: 0; color: #718096; font-size: 0.9rem; }
.pedido-valores { display: flex; flex-direction: column; gap: 0.5rem; min-width: 200px; }
.valor-item { display: flex; justify-content: space-between; align-items: center; }
.valor-label    { color: #718096; font-size: 0.9rem; }
.valor-original { color: #a0aec0; text-decoration: line-through; font-size: 0.9rem; }
.valor-desconto { color: #2d3748; font-weight: 600; font-size: 1.1rem; }
.pedido-actions { display: flex; gap: 1rem; justify-content: flex-end; }

.pedidos-vazios { text-align: center; padding: 3rem 2rem; background: #fff; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.vazio-content i    { font-size: 4rem; color: #cbd5e0; margin-bottom: 1rem; display: block; }
.vazio-content h3   { color: #4a5568; margin-bottom: 0.5rem; }
.vazio-content p    { color: #718096; margin-bottom: 2rem; }

/* Notificação inline */
.config-notification {
  border-radius: 8px; padding: 1rem 1.5rem;
  font-weight: 500; color: #333;
  border-left: 4px solid #007bff;
  background: #fff;
}
.config-notification.success { border-left-color: #28a745; color: #28a745; background: rgba(40,167,69,0.05); }
.config-notification.error   { border-left-color: #dc3545; color: #dc3545; background: rgba(220,53,69,0.05); }

/* Responsivo */
@media (max-width: 768px) {
  .configuracoes-layout { grid-template-columns: 1fr; }
  .configuracoes-sidebar { position: static; }
  .form-grid { grid-template-columns: 1fr; }
  .form-actions { flex-direction: column; }
  .pedido-detalhes { grid-template-columns: 1fr; }
  .produto-info { flex-direction: column; align-items: center; text-align: center; }
}

@media (max-width: 480px) {
  .configuracoes-content { padding: 1rem; }
}
</style>