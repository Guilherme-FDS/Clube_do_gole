<template>
  <div class="container configuracoes-page">
    <!-- Breadcrumb -->
    <nav class="breadcrumb-nav">
      <router-link to="/">Início</router-link>
      <span>/</span>
      <span>Configurações</span>
    </nav>

    <div class="configuracoes-layout">
      <!-- Sidebar Menu -->
      <aside class="configuracoes-sidebar">
        <div class="user-profile-summary">
          <div class="user-avatar">
            <i class="fas fa-user-circle"></i>
          </div>
          <div class="user-info">
            <h3>{{ usuario.nome }} {{ usuario.sobrenome }}</h3>
            <p>{{ usuario.email }}</p>
          </div>
        </div>

        <nav class="configuracoes-menu">
          <a href="#" class="menu-item" :class="{ active: abaAtiva === 'perfil' }" @click.prevent="mudarAba('perfil')">
            <i class="fas fa-user"></i> Perfil
          </a>
          <a href="#" class="menu-item" :class="{ active: abaAtiva === 'enderecos' }" @click.prevent="mudarAba('enderecos')">
            <i class="fas fa-map-marker-alt"></i> Endereços
          </a>
          <a href="#" class="menu-item" :class="{ active: abaAtiva === 'seguranca' }" @click.prevent="mudarAba('seguranca')">
            <i class="fas fa-shield-alt"></i> Segurança
          </a>
          <a href="#" class="menu-item" :class="{ active: abaAtiva === 'pedidos' }" @click.prevent="mudarAba('pedidos')">
            <i class="fas fa-shopping-bag"></i> Meus Pedidos
          </a>
        </nav>
      </aside>

      <!-- Conteúdo Principal -->
      <div class="configuracoes-content">
        <!-- Aba Perfil -->
        <div v-show="abaAtiva === 'perfil'" class="tab-content">
          <div class="tab-header">
            <h2>Meu Perfil</h2>
            <p>Gerencie suas informações pessoais</p>
          </div>
          <form @submit.prevent="salvarPerfil" class="perfil-form">
            <div class="form-grid">
              <div class="form-group">
                <label for="nome">Nome *</label>
                <input type="text" id="nome" v-model="usuario.nome" required>
              </div>
              <div class="form-group">
                <label for="sobrenome">Sobrenome *</label>
                <input type="text" id="sobrenome" v-model="usuario.sobrenome" required>
              </div>
            </div>
            <div class="form-grid">
              <div class="form-group">
                <label for="email">Email *</label>
                <input type="email" id="email" v-model="usuario.email" required>
              </div>
              <div class="form-group">
                <label for="telefone">Telefone *</label>
                <input type="tel" id="telefone" v-model="usuario.telefone" @input="mascararTelefone" required>
              </div>
            </div>
            <div class="form-grid">
              <div class="form-group">
                <label for="cpf">CPF</label>
                <input type="text" id="cpf" v-model="usuario.cpf" readonly class="readonly">
              </div>
              <div class="form-group">
                <label for="data_nascimento">Data de Nascimento</label>
                <input type="date" id="data_nascimento" v-model="usuario.data_nascimento">
              </div>
            </div>
            <div class="form-actions">
              <button type="button" class="btn-secondary" @click="resetarFormPerfil">Cancelar</button>
              <button type="submit" class="btn-primary"><i class="fas fa-save"></i> Salvar Alterações</button>
            </div>
          </form>
        </div>

        <!-- Aba Endereços -->
        <div v-show="abaAtiva === 'enderecos'" class="tab-content">
          <div class="tab-header">
            <h2>Meus Endereços</h2>
            <p>Gerencie seus endereços de entrega</p>
          </div>
          <div class="enderecos-container">
            <!-- Endereço Principal -->
            <div v-if="enderecoPrincipal" class="endereco-card principal" :data-endereco-id="enderecoPrincipal.id">
              <div class="endereco-header">
                <h3>Endereço Principal</h3>
                <span class="badge-principal">Principal</span>
              </div>
              <div class="endereco-info">
                <p><strong>{{ usuario.nome }} {{ usuario.sobrenome }}</strong></p>
                <p>{{ enderecoPrincipal.endereco }}, {{ enderecoPrincipal.numero }}</p>
                <p v-if="enderecoPrincipal.complemento">Complemento: {{ enderecoPrincipal.complemento }}</p>
                <p>{{ enderecoPrincipal.bairro }} - {{ enderecoPrincipal.cidade }}/{{ enderecoPrincipal.estado }}</p>
                <p>CEP: {{ enderecoPrincipal.cep }}</p>
              </div>
              <div class="endereco-actions">
                <button class="btn-edit" @click="editarEndereco(enderecoPrincipal.id)"><i class="fas fa-edit"></i> Editar</button>
                <button v-if="outrosEnderecos.length" class="btn-delete" @click="excluirEndereco(enderecoPrincipal.id)"><i class="fas fa-trash"></i> Excluir</button>
              </div>
            </div>

            <!-- Outros Endereços -->
            <div v-for="(end, idx) in outrosEnderecos" :key="end.id" class="endereco-card" :data-endereco-id="end.id">
              <div class="endereco-header">
                <h3>Endereço {{ idx + 1 }}</h3>
              </div>
              <div class="endereco-info">
                <p><strong>{{ usuario.nome }} {{ usuario.sobrenome }}</strong></p>
                <p>{{ end.endereco }}, {{ end.numero }}</p>
                <p v-if="end.complemento">Complemento: {{ end.complemento }}</p>
                <p>{{ end.bairro }} - {{ end.cidade }}/{{ end.estado }}</p>
                <p>CEP: {{ end.cep }}</p>
              </div>
              <div class="endereco-actions">
                <button class="btn-edit" @click="editarEndereco(end.id)"><i class="fas fa-edit"></i> Editar</button>
                <button class="btn-set-primary" @click="definirPrincipal(end.id)"><i class="fas fa-star"></i> Tornar Principal</button>
                <button class="btn-delete" @click="excluirEndereco(end.id)"><i class="fas fa-trash"></i> Excluir</button>
              </div>
            </div>

            <!-- Botão Adicionar Novo Endereço -->
            <div class="add-endereco-card" @click="abrirModalEndereco()">
              <div class="add-endereco-content">
                <i class="fas fa-plus-circle"></i>
                <h3>Adicionar Novo Endereço</h3>
                <p>Clique para cadastrar um novo endereço de entrega</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Aba Segurança -->
        <div v-show="abaAtiva === 'seguranca'" class="tab-content">
          <div class="tab-header">
            <h2>Segurança</h2>
            <p>Gerencie a segurança da sua conta</p>
          </div>
          <div class="seguranca-card">
            <h3>Alterar Senha</h3>
            <form @submit.prevent="alterarSenha">
              <div class="form-group">
                <label for="senha_atual">Senha Atual</label>
                <input type="password" id="senha_atual" v-model="senhaForm.senha_atual" required>
              </div>
              <div class="form-group">
                <label for="nova_senha">Nova Senha</label>
                <input type="password" id="nova_senha" v-model="senhaForm.nova_senha" required>
              </div>
              <div class="form-group">
                <label for="confirmar_senha">Confirmar Nova Senha</label>
                <input type="password" id="confirmar_senha" v-model="senhaForm.confirmar_senha" required>
              </div>
              <button type="submit" class="btn-primary"><i class="fas fa-key"></i> Alterar Senha</button>
            </form>
          </div>
        </div>

        <!-- Aba Pedidos -->
        <div v-show="abaAtiva === 'pedidos'" class="tab-content">
          <div class="tab-header">
            <h2>Meus Pedidos</h2>
            <p>Acompanhe seus pedidos e histórico de compras</p>
          </div>
          <div v-if="pedidos.length" class="pedidos-container">
            <div v-for="pedido in pedidos" :key="pedido.id_compra" class="pedido-card">
              <!-- ... conteúdo do pedido, similar ao original, mas otimizado -->
              <div class="pedido-header">
                <div class="pedido-info">
                  <h3>Pedido #{{ pedido.id_compra.slice(0,8) }}...</h3>
                  <span class="pedido-data">{{ pedido.data }}</span>
                </div>
                <div class="pedido-status"><span class="status-entregue">Entregue</span></div>
              </div>
              <div class="pedido-detalhes">
                <div class="produto-info">
                  <div class="produto-imagem" v-if="pedido.imagem_produto">
                    <img :src="pedido.imagem_produto" :alt="pedido.nome_produto" @error="hideImage">
                  </div>
                  <div class="produto-detalhes">
                    <h4>{{ pedido.nome_produto }}</h4>
                    <p>Quantidade: {{ pedido.quantidade }}</p>
                    <p class="plano-info"><strong>Plano:</strong> <span :class="['plano-tag', pedido.plano]">{{ pedido.plano | capitalize }}</span></p>
                  </div>
                </div>
                <div class="pedido-valores">
                  <div class="valor-item"><span class="valor-label">Valor Original:</span><span class="valor-original">{{ formatarMoeda(pedido.valor_sem_desconto) }}</span></div>
                  <div class="valor-item"><span class="valor-label">Valor Pago:</span><span class="valor-desconto">{{ formatarMoeda(pedido.valor_com_desconto) }}</span></div>
                  <div v-if="pedido.desconto_aplicado > 0" class="valor-item"><span class="valor-label">Desconto Total:</span><span class="desconto-total">{{ pedido.desconto_aplicado }}%</span></div>
                  <div v-if="pedido.cupom_aplicado" class="valor-item"><span class="valor-label">Cupom Utilizado:</span><span class="cupom-info">{{ pedido.cupom_aplicado }}</span></div>
                  <div v-if="pedido.valor_sem_desconto > pedido.valor_com_desconto" class="valor-item economia"><span class="valor-label">Você economizou:</span><span class="valor-economia">{{ formatarMoeda(pedido.valor_sem_desconto - pedido.valor_com_desconto) }}</span></div>
                </div>
              </div>
              <div class="pedido-actions">
                <router-link :to="`/produto/${pedido.id_produto}`" class="btn-secondary"><i class="fas fa-redo"></i> Comprar Novamente</router-link>
                <button class="btn-primary" @click="verDetalhesPedido(pedido.id_compra)"><i class="fas fa-eye"></i> Ver Detalhes</button>
              </div>
            </div>
          </div>
          <div v-else class="pedidos-vazios">
            <div class="vazio-content">
              <i class="fas fa-shopping-bag"></i>
              <h3>Nenhum pedido encontrado</h3>
              <p>Você ainda não realizou nenhuma compra. Que tal explorar nossos produtos?</p>
              <router-link to="/#planos" class="btn-primary"><i class="fas fa-shopping-cart"></i> Fazer Compras</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Endereço -->
    <div v-if="modalEnderecoAberto" class="modal" @click.self="fecharModalEndereco">
      <div class="modal-content">
        <div class="modal-header">
          <h3>{{ editandoEndereco ? 'Editar Endereço' : 'Adicionar Novo Endereço' }}</h3>
          <button class="modal-close" @click="fecharModalEndereco"><i class="fas fa-times"></i></button>
        </div>
        <form class="endereco-form" @submit.prevent="salvarEndereco">
          <div class="form-group">
            <label for="cep">CEP *</label>
            <input type="text" id="cep" v-model="enderecoForm.cep" @blur="buscarCep" required maxlength="9">
          </div>
          <div class="form-grid">
            <div class="form-group"><label for="endereco">Endereço *</label><input type="text" id="endereco" v-model="enderecoForm.endereco" required></div>
            <div class="form-group"><label for="numero">Número *</label><input type="text" id="numero" v-model="enderecoForm.numero" required></div>
          </div>
          <div class="form-group"><label for="complemento">Complemento</label><input type="text" id="complemento" v-model="enderecoForm.complemento" placeholder="Apartamento, bloco, etc."></div>
          <div class="form-grid">
            <div class="form-group"><label for="bairro">Bairro *</label><input type="text" id="bairro" v-model="enderecoForm.bairro" required></div>
            <div class="form-group"><label for="cidade">Cidade *</label><input type="text" id="cidade" v-model="enderecoForm.cidade" required></div>
          </div>
          <div class="form-grid">
            <div class="form-group">
              <label for="estado">Estado *</label>
              <select v-model="enderecoForm.estado" required>
                <option value="">Selecione</option>
                <option v-for="uf in ufList" :key="uf.sigla" :value="uf.sigla">{{ uf.nome }}</option>
              </select>
            </div>
            <div class="form-group"><label for="pais">País *</label><input type="text" v-model="enderecoForm.pais" required></div>
          </div>
          <div class="form-group checkbox-group">
            <input type="checkbox" id="endereco_principal" v-model="enderecoForm.principal">
            <label for="endereco_principal">Tornar este endereço principal</label>
          </div>
          <div class="modal-actions">
            <button type="button" class="btn-secondary" @click="fecharModalEndereco">Cancelar</button>
            <button type="submit" class="btn-primary"><i class="fas fa-save"></i> {{ editandoEndereco ? 'Atualizar Endereço' : 'Salvar Endereço' }}</button>
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
import { formatarMoeda } from '@/utils/formatters'

const router = useRouter()
const authStore = useAuthStore()

// Dados do usuário (mock, substituir por API)
const usuario = reactive({
  id: null,
  nome: '',
  sobrenome: '',
  email: '',
  telefone: '',
  cpf: '',
  data_nascimento: ''
})

// Endereços
const enderecoPrincipal = ref(null)
const outrosEnderecos = ref([])
const enderecos = ref([])

// Pedidos
const pedidos = ref([])

// Controle de abas
const abaAtiva = ref('perfil')

// Formulário de senha
const senhaForm = reactive({
  senha_atual: '',
  nova_senha: '',
  confirmar_senha: ''
})

// Modal endereço
const modalEnderecoAberto = ref(false)
const editandoEndereco = ref(false)
const enderecoForm = reactive({
  id: null,
  cep: '',
  endereco: '',
  numero: '',
  complemento: '',
  bairro: '',
  cidade: '',
  estado: '',
  pais: 'Brasil',
  principal: false
})

// Lista de estados brasileiros
const ufList = [
  { sigla: 'AC', nome: 'Acre' }, { sigla: 'AL', nome: 'Alagoas' }, { sigla: 'AP', nome: 'Amapá' },
  { sigla: 'AM', nome: 'Amazonas' }, { sigla: 'BA', nome: 'Bahia' }, { sigla: 'CE', nome: 'Ceará' },
  { sigla: 'DF', nome: 'Distrito Federal' }, { sigla: 'ES', nome: 'Espírito Santo' }, { sigla: 'GO', nome: 'Goiás' },
  { sigla: 'MA', nome: 'Maranhão' }, { sigla: 'MT', nome: 'Mato Grosso' }, { sigla: 'MS', nome: 'Mato Grosso do Sul' },
  { sigla: 'MG', nome: 'Minas Gerais' }, { sigla: 'PA', nome: 'Pará' }, { sigla: 'PB', nome: 'Paraíba' },
  { sigla: 'PR', nome: 'Paraná' }, { sigla: 'PE', nome: 'Pernambuco' }, { sigla: 'PI', nome: 'Piauí' },
  { sigla: 'RJ', nome: 'Rio de Janeiro' }, { sigla: 'RN', nome: 'Rio Grande do Norte' }, { sigla: 'RS', nome: 'Rio Grande do Sul' },
  { sigla: 'RO', nome: 'Rondônia' }, { sigla: 'RR', nome: 'Roraima' }, { sigla: 'SC', nome: 'Santa Catarina' },
  { sigla: 'SP', nome: 'São Paulo' }, { sigla: 'SE', nome: 'Sergipe' }, { sigla: 'TO', nome: 'Tocantins' }
]

// Funções de utilidade
function mostrarMensagem(texto, tipo = 'success') {
  // Implementar notificação (ex.: toast)
  alert(`${tipo.toUpperCase()}: ${texto}`)
}

function mascararTelefone(e) {
  let value = e.target.value.replace(/\D/g, '')
  if (value.length <= 11) {
    if (value.length <= 2) value = value.replace(/(\d{0,2})/, '($1')
    else if (value.length <= 6) value = value.replace(/(\d{2})(\d{0,4})/, '($1) $2')
    else value = value.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3')
    e.target.value = value
  }
}

// Carregar dados da API
async function carregarDados() {
  try {
    // Perfil
    const perfilResp = await fetch('/api/perfil')
    const perfilData = await perfilResp.json()
    Object.assign(usuario, perfilData)

    // Endereços
    const endResp = await fetch('/api/enderecos')
    const endData = await endResp.json()
    enderecos.value = endData.enderecos || []
    enderecoPrincipal.value = enderecos.value.find(e => e.principal === 'sim') || null
    outrosEnderecos.value = enderecos.value.filter(e => e.principal !== 'sim')

    // Pedidos
    const pedResp = await fetch('/api/pedidos')
    const pedData = await pedResp.json()
    pedidos.value = pedData.pedidos || []
  } catch (err) {
    console.error(err)
    mostrarMensagem('Erro ao carregar dados', 'error')
  }
}

// Salvar perfil
async function salvarPerfil() {
  try {
    const response = await fetch('/atualizar_perfil', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(usuario)
    })
    const data = await response.json()
    if (data.success) {
      mostrarMensagem('Perfil atualizado com sucesso!', 'success')
    } else {
      mostrarMensagem(data.message, 'error')
    }
  } catch (error) {
    mostrarMensagem('Erro ao salvar perfil', 'error')
  }
}

function resetarFormPerfil() {
  carregarDados() // recarrega os dados originais
}

// Alterar senha
async function alterarSenha() {
  if (senhaForm.nova_senha !== senhaForm.confirmar_senha) {
    mostrarMensagem('As senhas não coincidem', 'error')
    return
  }
  try {
    const response = await fetch('/alterar_senha', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ senha_atual: senhaForm.senha_atual, nova_senha: senhaForm.nova_senha })
    })
    const data = await response.json()
    if (data.success) {
      mostrarMensagem('Senha alterada com sucesso', 'success')
      senhaForm.senha_atual = ''
      senhaForm.nova_senha = ''
      senhaForm.confirmar_senha = ''
    } else {
      mostrarMensagem(data.message, 'error')
    }
  } catch (error) {
    mostrarMensagem('Erro ao alterar senha', 'error')
  }
}

// Endereços
function abrirModalEndereco(endereco = null) {
  if (endereco) {
    editandoEndereco.value = true
    Object.assign(enderecoForm, endereco)
    enderecoForm.principal = endereco.principal === 'sim'
  } else {
    editandoEndereco.value = false
    enderecoForm.id = null
    enderecoForm.cep = ''
    enderecoForm.endereco = ''
    enderecoForm.numero = ''
    enderecoForm.complemento = ''
    enderecoForm.bairro = ''
    enderecoForm.cidade = ''
    enderecoForm.estado = ''
    enderecoForm.pais = 'Brasil'
    enderecoForm.principal = false
  }
  modalEnderecoAberto.value = true
}

function fecharModalEndereco() {
  modalEnderecoAberto.value = false
}

async function salvarEndereco() {
  const url = enderecoForm.id ? `/editar_endereco/${enderecoForm.id}` : '/adicionar_endereco'
  const payload = { ...enderecoForm, principal: enderecoForm.principal ? 'sim' : 'nao' }
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await response.json()
    if (data.success) {
      mostrarMensagem('Endereço salvo com sucesso', 'success')
      fecharModalEndereco()
      await carregarDados() // recarrega a lista
    } else {
      mostrarMensagem(data.message, 'error')
    }
  } catch (error) {
    mostrarMensagem('Erro ao salvar endereço', 'error')
  }
}

async function excluirEndereco(id) {
  if (!confirm('Tem certeza que deseja excluir este endereço?')) return
  try {
    const response = await fetch(`/excluir_endereco/${id}`, { method: 'POST' })
    const data = await response.json()
    if (data.success) {
      mostrarMensagem('Endereço excluído', 'success')
      await carregarDados()
    } else {
      mostrarMensagem(data.message, 'error')
    }
  } catch (error) {
    mostrarMensagem('Erro ao excluir endereço', 'error')
  }
}

async function definirPrincipal(id) {
  try {
    const response = await fetch(`/definir_endereco_principal/${id}`, { method: 'POST' })
    const data = await response.json()
    if (data.success) {
      mostrarMensagem('Endereço definido como principal', 'success')
      await carregarDados()
    } else {
      mostrarMensagem(data.message, 'error')
    }
  } catch (error) {
    mostrarMensagem('Erro ao definir endereço principal', 'error')
  }
}

function editarEndereco(id) {
  const end = enderecos.value.find(e => e.id == id)
  if (end) abrirModalEndereco(end)
}

// Buscar CEP via ViaCEP
async function buscarCep() {
  const cep = enderecoForm.cep.replace(/\D/g, '')
  if (cep.length !== 8) return
  try {
    const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`)
    const data = await response.json()
    if (!data.erro) {
      enderecoForm.endereco = data.logradouro || ''
      enderecoForm.bairro = data.bairro || ''
      enderecoForm.cidade = data.localidade || ''
      enderecoForm.estado = data.uf || ''
    } else {
      mostrarMensagem('CEP não encontrado', 'error')
    }
  } catch (error) {
    mostrarMensagem('Erro ao buscar CEP', 'error')
  }
}

// Navegação entre abas
function mudarAba(aba) {
  abaAtiva.value = aba
  // Opcional: salvar no localStorage ou query param para persistir
}

// Ver detalhes do pedido (exemplo)
function verDetalhesPedido(id) {
  router.push(`/admin/vendas/${id}`)
}

// Lifecycle
onMounted(async () => {
  // Verifica se o usuário está logado
  if (!authStore.logado) {
    router.push('/login?redirect=configuracoes')
    return
  }
  await carregarDados()
})
</script>

<style scoped>
/* ===== ESTILOS EXCLUSIVOS DA PÁGINA DE CONFIGURAÇÕES ===== */
/* (Os estilos globais já fornecem botões, formulários básicos, cores, etc.) */

.configuracoes-layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: var(--espacamento-lg);
  margin-top: var(--espacamento-lg);
}

.breadcrumb-nav {
  margin-bottom: var(--espacamento-sm);
  font-size: 0.9rem;
  color: var(--cor-texto-secundario);
}
.breadcrumb-nav a { color: var(--cor-dourado); text-decoration: none; }

.configuracoes-sidebar {
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-md);
  border: 1px solid rgba(255, 215, 0, 0.2);
  position: sticky;
  top: 100px;
  height: fit-content;
}

.user-profile-summary {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  margin-bottom: 1rem;
}
.user-avatar i { font-size: 3rem; color: var(--cor-dourado); }
.user-info h3 { color: var(--cor-texto); margin-bottom: 0.25rem; }
.user-info p { color: var(--cor-texto-secundario); font-size: 0.85rem; }

.configuracoes-menu {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem;
  border-radius: var(--borda-radius-md);
  transition: all 0.3s;
  color: var(--cor-texto-secundario);
  text-decoration: none;
}
.menu-item:hover, .menu-item.active {
  background: var(--cor-dourado);
  color: var(--cor-fundo);
}

.configuracoes-content {
  background: var(--cor-fundo-secundario);
  border-radius: var(--borda-radius-lg);
  padding: var(--espacamento-lg);
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.tab-header {
  margin-bottom: var(--espacamento-lg);
  border-bottom: 1px solid rgba(255, 215, 0, 0.2);
  padding-bottom: var(--espacamento-sm);
}
.tab-header h2 { color: var(--cor-dourado); margin-bottom: 0.25rem; }

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--espacamento-sm);
  margin-bottom: var(--espacamento-md);
}
.form-group input.readonly {
  background: rgba(255,255,255,0.05);
  cursor: not-allowed;
}

.enderecos-container {
  display: flex;
  flex-direction: column;
  gap: var(--espacamento-md);
}
.endereco-card {
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  border: 1px solid rgba(255, 215, 0, 0.2);
}
.endereco-card.principal {
  border-color: var(--cor-dourado);
  background: rgba(255, 215, 0, 0.05);
}
.endereco-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--espacamento-sm);
}
.endereco-info p { margin: 0.25rem 0; color: var(--cor-texto-secundario); }
.endereco-actions {
  display: flex;
  gap: 0.5rem;
  margin-top: 1rem;
  flex-wrap: wrap;
}
.btn-edit, .btn-delete, .btn-set-primary {
  padding: 0.4rem 0.8rem;
  border-radius: var(--borda-radius-sm);
  font-size: 0.85rem;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: all 0.3s;
}
.btn-edit { background: #2196F3; color: white; }
.btn-delete { background: #f44336; color: white; }
.btn-set-primary { background: #4caf50; color: white; }
.btn-edit:hover, .btn-delete:hover, .btn-set-primary:hover { transform: translateY(-2px); filter: brightness(0.9); }

.add-endereco-card {
  border: 2px dashed rgba(255, 215, 0, 0.3);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-lg);
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
}
.add-endereco-card:hover { border-color: var(--cor-dourado); background: rgba(255,215,0,0.05); }
.add-endereco-content i { font-size: 2.5rem; color: var(--cor-dourado); margin-bottom: 0.5rem; }

.seguranca-card {
  max-width: 500px;
  background: var(--cor-fundo);
  padding: var(--espacamento-lg);
  border-radius: var(--borda-radius-md);
}

.pedido-card {
  background: var(--cor-fundo);
  border-radius: var(--borda-radius-md);
  padding: var(--espacamento-md);
  margin-bottom: var(--espacamento-md);
}
.pedido-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.pedido-detalhes {
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
}
.produto-info { display: flex; gap: 1rem; align-items: flex-start; }
.produto-imagem { width: 60px; height: 60px; border-radius: 8px; overflow: hidden; }
.produto-imagem img { width: 100%; height: 100%; object-fit: cover; }
.pedido-valores { min-width: 200px; }
.valor-item { display: flex; justify-content: space-between; margin-bottom: 0.25rem; }
.pedido-actions { display: flex; gap: 0.5rem; justify-content: flex-end; margin-top: 1rem; }

.status-entregue { background: #4caf50; color: white; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.75rem; }

.pedidos-vazios { text-align: center; padding: 3rem; }
.pedidos-vazios i { font-size: 4rem; color: var(--cor-dourado); opacity: 0.5; margin-bottom: 1rem; }

.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}
.modal-content {
  background: var(--cor-fundo-secundario);
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  border-radius: var(--borda-radius-lg);
  border: 1px solid var(--cor-dourado);
}
.modal-header {
  display: flex;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(255,215,0,0.2);
}
.modal-close { background: none; border: none; color: var(--cor-texto); font-size: 1.2rem; cursor: pointer; }
.endereco-form { padding: 1.5rem; }
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid rgba(255,215,0,0.2);
}

@media (max-width: 768px) {
  .configuracoes-layout { grid-template-columns: 1fr; }
  .configuracoes-sidebar { position: static; }
  .form-grid { grid-template-columns: 1fr; }
  .pedido-detalhes { flex-direction: column; }
}
</style>