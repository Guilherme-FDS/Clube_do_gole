<template>
  <div class="venda-container">
    <BotaoVoltarAdmin to="/admin/vendas" label="Voltar ao Dashboard" />

    <div v-if="carregando" class="loading">
      <i class="fas fa-spinner fa-spin"></i> Carregando venda...
    </div>

    <div v-else-if="erro" class="erro-box">
      <i class="fas fa-exclamation-circle"></i> {{ erro }}
    </div>

    <template v-else-if="venda">
      <!-- Cabeçalho -->
      <div class="page-header">
        <div>
          <h1>Venda <span class="id-destaque">#{{ venda.id }}</span></h1>
          <p>{{ formatarDataHora(venda.data) }}</p>
        </div>
        <span :class="['status-badge', venda.status]">{{ labelStatus(venda.status) }}</span>
      </div>

      <div class="grid-principal">
        <!-- Coluna esquerda -->
        <div class="coluna">

          <!-- Itens -->
          <div class="card">
            <h3><i class="fas fa-wine-bottle"></i> Itens</h3>
            <table>
              <thead>
                <tr><th>Produto</th><th>Plano</th><th>Qtd</th><th>Unitário</th><th>Total</th></tr>
              </thead>
              <tbody>
                <tr v-for="(i, idx) in venda.itens" :key="idx">
                  <td class="nome-col">{{ i.nome_produto }}</td>
                  <td><span class="plano-badge">{{ i.plano }}</span></td>
                  <td>{{ i.quantidade }}</td>
                  <td>{{ moeda(i.valor_unitario) }}</td>
                  <td class="valor-col">{{ moeda(i.valor_total) }}</td>
                </tr>
              </tbody>
            </table>

            <!-- Resumo financeiro -->
            <div class="resumo">
              <div class="resumo-linha"><span>Subtotal</span><span>{{ moeda(venda.valor_original) }}</span></div>
              <div class="resumo-linha desconto" v-if="venda.valor_desconto > 0">
                <span>Desconto {{ venda.desconto_aplicado > 0 ? `(${venda.desconto_aplicado}%)` : '' }}
                  <span v-if="venda.cupom_aplicado" class="cupom-tag"><i class="fas fa-tag"></i> {{ venda.cupom_aplicado }}</span>
                </span>
                <span>− {{ moeda(venda.valor_desconto) }}</span>
              </div>
              <div class="resumo-linha total"><span>Total</span><span>{{ moeda(venda.valor_total) }}</span></div>
            </div>
          </div>

          <!-- Pagamentos -->
          <div class="card">
            <h3><i class="fas fa-credit-card"></i> Pagamentos</h3>
            <div v-if="!venda.pagamentos.length" class="sem-dados">Nenhum pagamento registrado.</div>
            <table v-else>
              <thead>
                <tr><th>ID</th><th>Método</th><th>Status</th><th>Valor</th><th>Pago em</th></tr>
              </thead>
              <tbody>
                <tr v-for="p in venda.pagamentos" :key="p.id">
                  <td><span class="id-badge">#{{ p.id }}</span></td>
                  <td>{{ labelMetodo(p.metodo) }}</td>
                  <td><span :class="['status-badge', 'sm', p.status]">{{ labelStatus(p.status) }}</span></td>
                  <td class="valor-col">{{ moeda(p.valor) }}</td>
                  <td>{{ p.pago_em ? formatarDataHora(p.pago_em) : '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Coluna direita -->
        <div class="coluna">

          <!-- Cliente -->
          <div class="card">
            <h3><i class="fas fa-user"></i> Cliente</h3>
            <div v-if="!venda.cliente" class="sem-dados">Cliente não identificado.</div>
            <div v-else class="info-list">
              <div class="info"><span class="label">Nome</span><span>{{ venda.cliente.nome }}</span></div>
              <div class="info"><span class="label">Email</span><span>{{ venda.cliente.email }}</span></div>
              <div class="info"><span class="label">Telefone</span><span>{{ venda.cliente.telefone || '—' }}</span></div>
              <div class="info"><span class="label">ID</span><span class="id-badge">#{{ venda.cliente.id }}</span></div>
            </div>
          </div>

          <!-- Assinatura -->
          <div class="card" v-if="venda.assinatura">
            <h3><i class="fas fa-sync-alt"></i> Assinatura Gerada</h3>
            <div class="info-list">
              <div class="info"><span class="label">ID</span><span class="id-badge">#{{ venda.assinatura.id }}</span></div>
              <div class="info"><span class="label">Plano</span><span class="plano-badge">{{ venda.assinatura.plano }}</span></div>
              <div class="info"><span class="label">Status</span>
                <span :class="['status-badge', 'sm', venda.assinatura.status]">{{ venda.assinatura.status }}</span>
              </div>
              <div class="info"><span class="label">Início</span><span>{{ formatarData(venda.assinatura.data_inicio) }}</span></div>
              <div class="info" v-if="venda.assinatura.proximo_ciclo">
                <span class="label">Próximo ciclo</span><span>{{ formatarData(venda.assinatura.proximo_ciclo) }}</span>
              </div>
            </div>
          </div>

          <!-- Endereço -->
          <div class="card" v-if="venda.endereco">
            <h3><i class="fas fa-map-marker-alt"></i> Entrega</h3>
            <p class="endereco-texto">
              {{ venda.endereco.logradouro }}, {{ venda.endereco.numero }}<template v-if="venda.endereco.complemento"> — {{ venda.endereco.complemento }}</template><br>
              {{ venda.endereco.bairro }} — {{ venda.endereco.cidade }}/{{ venda.endereco.estado }}<br>
              CEP {{ venda.endereco.cep }}
            </p>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'
import BotaoVoltarAdmin from '@/components/BotaoVoltarAdmin.vue'

const route = useRoute()
const venda = ref(null)
const carregando = ref(true)
const erro = ref('')

const moeda = (v) =>
  new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(v || 0)

const formatarDataHora = (d) =>
  d ? new Date(d).toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' }) : '—'

const formatarData = (d) => (d ? new Date(d + 'T00:00:00').toLocaleDateString('pt-BR') : '—')

const labelStatus = (s) => ({
  pendente: 'Pendente', pago: 'Pago', cancelado: 'Cancelado', estornado: 'Estornado',
  aprovado: 'Aprovado', recusado: 'Recusado', ativa: 'Ativa', pausada: 'Pausada', expirada: 'Expirada', cancelada: 'Cancelada',
}[s] || s)

const labelMetodo = (m) => ({
  cartao_credito: 'Cartão de Crédito', pix: 'PIX', boleto: 'Boleto', outro: 'Outro',
}[m] || m)

onMounted(async () => {
  try {
    const { data } = await api.get(`/admin/vendas/${route.params.id}`)
    venda.value = data
  } catch (e) {
    erro.value = e?.response?.status === 404 ? 'Venda não encontrada.' : 'Erro ao carregar detalhes da venda.'
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
.venda-container {
  min-height: 100vh;
  background: #F4F5F7;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
  padding: 80px max(24px, calc((100% - 1100px) / 2)) 60px;
}

.loading, .erro-box { text-align: center; padding: 60px 0; color: #9CA3AF; font-size: 14px; }
.erro-box { color: #DC2626; }

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.page-header h1 { font-size: 22px; font-weight: 700; color: #1B1A19; margin: 0 0 2px; }
.id-destaque { color: #C9A84C; }
.page-header p { color: #6B7280; font-size: 13px; margin: 0; }

.grid-principal {
  display: grid;
  grid-template-columns: 1.6fr 1fr;
  gap: 16px;
  align-items: start;
}
.coluna { display: flex; flex-direction: column; gap: 16px; }
@media (max-width: 900px) { .grid-principal { grid-template-columns: 1fr; } }

.card {
  background: #fff;
  border: 1px solid #E3E5E8;
  border-radius: 10px;
  padding: 18px 20px;
}
.card h3 {
  font-size: 12px;
  font-weight: 700;
  color: #4B5563;
  text-transform: uppercase;
  letter-spacing: .05em;
  margin: 0 0 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.card h3 i { color: #C9A84C; }

table { width: 100%; border-collapse: collapse; }
th {
  color: #6B7280;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: .04em;
  text-align: left;
  padding: 6px 8px;
  border-bottom: 1px solid #E3E5E8;
}
td { padding: 10px 8px; font-size: 13px; color: #1B1A19; border-bottom: 1px solid #F3F4F6; }
.nome-col { font-weight: 600; }
.valor-col { font-weight: 600; white-space: nowrap; }

.plano-badge {
  background: #FDF6E5;
  color: #8A6520;
  border-radius: 20px;
  padding: 2px 10px;
  font-size: 11px;
  font-weight: 600;
  text-transform: capitalize;
}
.id-badge { background: #F3F4F6; border-radius: 6px; padding: 2px 8px; font-size: 12px; color: #4B5563; font-weight: 600; }

.status-badge {
  border-radius: 20px;
  padding: 5px 14px;
  font-size: 12px;
  font-weight: 700;
}
.status-badge.sm { padding: 3px 10px; font-size: 11px; }
.status-badge.pago, .status-badge.aprovado, .status-badge.ativa { background: #EBF8F0; color: #2E8B57; }
.status-badge.pendente, .status-badge.pausada { background: #FEF8E7; color: #B7791F; }
.status-badge.cancelado, .status-badge.recusado, .status-badge.cancelada { background: #FEF2F2; color: #DC2626; }
.status-badge.estornado, .status-badge.expirada { background: #F3F4F6; color: #6B7280; }

.resumo { margin-top: 14px; border-top: 1px solid #E3E5E8; padding-top: 12px; }
.resumo-linha {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #4B5563;
  padding: 4px 8px;
}
.resumo-linha.desconto { color: #2E8B57; }
.cupom-tag {
  background: #EBF8F0;
  border-radius: 6px;
  padding: 1px 8px;
  font-size: 11px;
  font-weight: 600;
  margin-left: 6px;
}
.resumo-linha.total {
  font-size: 16px;
  font-weight: 700;
  color: #1B1A19;
  border-top: 1px solid #E3E5E8;
  margin-top: 6px;
  padding-top: 10px;
}

.info-list { display: flex; flex-direction: column; gap: 10px; }
.info { display: flex; justify-content: space-between; align-items: center; font-size: 13px; color: #1B1A19; }
.label { font-size: 11px; color: #9CA3AF; font-weight: 600; text-transform: uppercase; letter-spacing: .04em; }

.endereco-texto { font-size: 13px; color: #4B5563; line-height: 1.7; margin: 0; }
.sem-dados { color: #9CA3AF; font-size: 13px; padding: 8px 0; }
</style>
