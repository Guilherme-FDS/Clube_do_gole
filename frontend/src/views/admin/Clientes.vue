<template>
  <div class="clientes-container">
    <BotaoVoltarAdmin />

    <div class="page-header">
      <div>
        <h1><i class="fas fa-users"></i> Clientes</h1>
        <p>Cadastros, assinaturas e histórico de compras</p>
      </div>
      <div class="header-stats" v-if="!carregando">
        <span class="stat-pill">{{ clientes.length }} clientes</span>
        <span class="stat-pill ativos">{{ clientesAtivos }} ativos</span>
      </div>
    </div>

    <!-- Busca -->
    <div class="filtros-card">
      <input v-model="busca" class="input-busca" placeholder="Buscar por nome, email ou CPF..." />
    </div>

    <!-- Lista -->
    <div class="tabela-card">
      <div v-if="carregando" class="loading">
        <i class="fas fa-spinner fa-spin"></i> Carregando...
      </div>
      <table v-else>
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome</th>
            <th>Email</th>
            <th>Telefone</th>
            <th>Cadastro</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in clientesFiltrados" :key="c.id" @click="abrirDetalhe(c.id)" class="linha-clicavel">
            <td><span class="id-badge">#{{ c.id }}</span></td>
            <td class="nome-col">{{ c.nome }} {{ c.sobrenome }}</td>
            <td>{{ c.email }}</td>
            <td>{{ c.telefone || '—' }}</td>
            <td>{{ formatarData(c.criado_em) }}</td>
            <td>
              <span :class="['status-badge', c.ativo ? 'ativo' : 'inativo']">
                {{ c.ativo ? 'Ativo' : 'Inativo' }}
              </span>
            </td>
            <td><i class="fas fa-chevron-right chevron"></i></td>
          </tr>
          <tr v-if="clientesFiltrados.length === 0">
            <td colspan="7" class="sem-dados">Nenhum cliente encontrado.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal detalhe -->
    <div v-if="modalAberto" class="modal-overlay" @click.self="fecharModal">
      <div class="modal-box">
        <div class="modal-header">
          <h2><i class="fas fa-user-circle"></i> {{ detalhe?.cliente?.nome }} {{ detalhe?.cliente?.sobrenome }}</h2>
          <button class="btn-fechar" @click="fecharModal"><i class="fas fa-times"></i></button>
        </div>

        <div v-if="carregandoDetalhe" class="loading"><i class="fas fa-spinner fa-spin"></i></div>
        <div v-else-if="detalhe" class="modal-body">

          <!-- Dados pessoais -->
          <section class="secao">
            <h3><i class="fas fa-id-card"></i> Dados Pessoais</h3>
            <div class="dados-grid">
              <div class="dado"><span class="label">Email</span><span>{{ detalhe.cliente.email }}</span></div>
              <div class="dado"><span class="label">CPF</span><span>{{ detalhe.cliente.cpf || '—' }}</span></div>
              <div class="dado"><span class="label">Telefone</span><span>{{ detalhe.cliente.telefone || '—' }}</span></div>
              <div class="dado"><span class="label">Nascimento</span><span>{{ detalhe.cliente.data_nascimento ? formatarData(detalhe.cliente.data_nascimento) : '—' }}</span></div>
              <div class="dado"><span class="label">Cadastrado em</span><span>{{ formatarData(detalhe.cliente.criado_em) }}</span></div>
              <div class="dado"><span class="label">Status</span>
                <span :class="['status-badge', detalhe.cliente.ativo ? 'ativo' : 'inativo']">{{ detalhe.cliente.ativo ? 'Ativo' : 'Inativo' }}</span>
              </div>
            </div>
          </section>

          <!-- Endereços -->
          <section class="secao" v-if="detalhe.enderecos?.length">
            <h3><i class="fas fa-map-marker-alt"></i> Endereços</h3>
            <div v-for="(e, i) in detalhe.enderecos" :key="i" class="endereco-item">
              {{ e.logradouro }}, {{ e.numero }}{{ e.complemento ? ', ' + e.complemento : '' }} — {{ e.bairro }}, {{ e.cidade }}/{{ e.estado }} — CEP {{ e.cep }}
            </div>
          </section>

          <!-- Pedidos -->
          <section class="secao">
            <h3><i class="fas fa-shopping-bag"></i> Pedidos ({{ detalhe.pedidos?.length || 0 }})</h3>
            <div v-if="!detalhe.pedidos?.length" class="sem-dados">Sem compras registradas.</div>
            <table v-else class="tabela-interna">
              <thead>
                <tr>
                  <th>Venda</th>
                  <th>Produto</th>
                  <th>Plano</th>
                  <th>Total</th>
                  <th>Cupom</th>
                  <th>Data</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in detalhe.pedidos" :key="p.id_compra">
                  <td><span class="id-badge">#{{ p.id_compra }}</span></td>
                  <td>{{ p.nome_produto || '—' }}</td>
                  <td>{{ p.plano || '—' }}</td>
                  <td>{{ formatarMoeda(p.valor_total) }}</td>
                  <td>{{ p.cupom_aplicado || '—' }}</td>
                  <td>{{ formatarData(p.data) }}</td>
                </tr>
              </tbody>
            </table>
          </section>

        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import BotaoVoltarAdmin from '@/components/BotaoVoltarAdmin.vue'

const clientes = ref([])
const carregando = ref(true)
const busca = ref('')
const modalAberto = ref(false)
const detalhe = ref(null)
const carregandoDetalhe = ref(false)

const clientesAtivos = computed(() => clientes.value.filter(c => c.ativo).length)

const clientesFiltrados = computed(() => {
  const q = busca.value.toLowerCase()
  if (!q) return clientes.value
  return clientes.value.filter(c =>
    `${c.nome} ${c.sobrenome} ${c.email} ${c.cpf || ''}`.toLowerCase().includes(q)
  )
})

function formatarData(d) {
  if (!d) return '—'
  return new Date(d).toLocaleDateString('pt-BR')
}

function formatarMoeda(v) {
  return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v || 0)
}

async function abrirDetalhe(id) {
  modalAberto.value = true
  carregandoDetalhe.value = true
  detalhe.value = null
  try {
    const { data } = await api.get(`/admin/clientes/${id}`)
    detalhe.value = data
  } catch {
    detalhe.value = null
  } finally {
    carregandoDetalhe.value = false
  }
}

function fecharModal() {
  modalAberto.value = false
  detalhe.value = null
}

onMounted(async () => {
  try {
    const { data } = await api.get('/admin/clientes')
    clientes.value = data
  } catch {
    console.error('Erro ao carregar clientes.')
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
.clientes-container {
  min-height: 100vh;
  background: #F4F5F7;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
  padding: 80px max(24px, calc((100% - 1100px) / 2)) 60px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}
.page-header h1 {
  font-size: 22px;
  font-weight: 700;
  color: #1B1A19;
  margin: 0 0 4px;
}
.page-header p { color: #6B7280; font-size: 13px; margin: 0; }

.header-stats { display: flex; gap: 8px; }
.stat-pill {
  background: #fff;
  border: 1px solid #E3E5E8;
  border-radius: 20px;
  padding: 4px 14px;
  font-size: 13px;
  color: #4B5563;
}
.stat-pill.ativos { border-color: #2E8B57; color: #2E8B57; background: #EBF8F0; }

.filtros-card {
  background: #fff;
  border: 1px solid #E3E5E8;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 16px;
}
.input-busca {
  width: 100%;
  border: 1px solid #D6D9DE;
  border-radius: 8px;
  padding: 9px 14px;
  font-size: 13px;
  font-family: inherit;
  color: #1B1A19;
  background: #fff;
  box-sizing: border-box;
}
.input-busca:focus { outline: none; border-color: #C9A84C; box-shadow: 0 0 0 3px rgba(201,168,76,0.15); }

.tabela-card {
  background: #fff;
  border: 1px solid #E3E5E8;
  border-radius: 10px;
  overflow: hidden;
}
table { width: 100%; border-collapse: collapse; }
th {
  background: #F9FAFB;
  color: #6B7280;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: .05em;
  text-transform: uppercase;
  padding: 10px 16px;
  text-align: left;
  border-bottom: 1px solid #E3E5E8;
}
td { padding: 12px 16px; font-size: 13px; color: #1B1A19; border-bottom: 1px solid #F3F4F6; }
.linha-clicavel { cursor: pointer; transition: background .12s; }
.linha-clicavel:hover { background: #FAFAF8; }
.nome-col { font-weight: 600; }
.id-badge { background: #F3F4F6; border-radius: 6px; padding: 2px 8px; font-size: 12px; color: #4B5563; font-weight: 600; }
.status-badge { border-radius: 20px; padding: 3px 10px; font-size: 11px; font-weight: 600; }
.status-badge.ativo { background: #EBF8F0; color: #2E8B57; }
.status-badge.inativo { background: #FEF2F2; color: #DC2626; }
.chevron { color: #9CA3AF; font-size: 11px; }
.sem-dados { text-align: center; padding: 40px; color: #9CA3AF; font-size: 13px; }
.loading { text-align: center; padding: 40px; color: #9CA3AF; }

/* Modal */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,0.4);
  z-index: 1000;
  display: flex; align-items: center; justify-content: center;
  padding: 24px;
}
.modal-box {
  background: #fff;
  border-radius: 14px;
  width: 100%; max-width: 760px;
  max-height: 88vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.15);
}
.modal-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 20px 24px 16px;
  border-bottom: 1px solid #E3E5E8;
  position: sticky; top: 0; background: #fff; z-index: 1;
}
.modal-header h2 { font-size: 17px; font-weight: 700; color: #1B1A19; margin: 0; }
.btn-fechar { background: none; border: none; cursor: pointer; color: #9CA3AF; font-size: 18px; padding: 4px; }
.btn-fechar:hover { color: #1B1A19; }
.modal-body { padding: 20px 24px 24px; }

.secao { margin-bottom: 24px; }
.secao h3 { font-size: 13px; font-weight: 700; color: #4B5563; text-transform: uppercase; letter-spacing: .05em; margin: 0 0 12px; }
.dados-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }
.dado { display: flex; flex-direction: column; gap: 2px; }
.label { font-size: 11px; color: #9CA3AF; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }
.dado span:last-child { font-size: 13px; color: #1B1A19; }
.endereco-item { font-size: 13px; color: #4B5563; background: #F9FAFB; border-radius: 8px; padding: 10px 14px; margin-bottom: 6px; }

.tabela-interna { width: 100%; border-collapse: collapse; }
.tabela-interna th { background: #F9FAFB; color: #6B7280; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; padding: 8px 12px; text-align: left; border-bottom: 1px solid #E3E5E8; }
.tabela-interna td { padding: 10px 12px; font-size: 12px; color: #1B1A19; border-bottom: 1px solid #F3F4F6; }
</style>
