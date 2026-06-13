<template>
  <main class="admin-hub">
    <div class="hub-container">

      <header class="hub-header">
        <div>
          <h1 class="hub-title">Painel Administrativo</h1>
          <p class="hub-subtitle">Gestão do Clube do Gole</p>
        </div>
        <span class="hub-data">{{ dataHoje }}</span>
      </header>

      <div class="hub-grid">
        <router-link
          v-for="mod in modulos"
          :key="mod.rota"
          :to="mod.rota"
          class="hub-card"
        >
          <div class="card-icone" :style="{ background: mod.bg, color: mod.cor }">
            <i :class="mod.icone"></i>
          </div>
          <div class="card-texto">
            <h3>{{ mod.titulo }}</h3>
            <p>{{ mod.descricao }}</p>
          </div>
          <i class="fas fa-chevron-right card-seta"></i>
        </router-link>
      </div>

    </div>
  </main>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const dataHoje = new Date().toLocaleDateString('pt-BR', {
  weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
})

const modulos = [
  {
    rota: '/admin/vendas',
    icone: 'fas fa-chart-line',
    titulo: 'Dashboard de Vendas',
    descricao: 'Faturamento, relatórios e produtos mais vendidos',
    bg: '#EEF4FF', cor: '#3B6FD4'
  },
  {
    rota: '/admin/produtos',
    icone: 'fas fa-wine-bottle',
    titulo: 'Produtos & Planos',
    descricao: 'Catálogo, planos de assinatura e preços',
    bg: '#FDF6E5', cor: '#A8842C'
  },
  {
    rota: '/admin/assinaturas',
    icone: 'fas fa-sync-alt',
    titulo: 'Assinaturas',
    descricao: 'Assinaturas ativas, pausadas e ciclos',
    bg: '#F3EEFD', cor: '#7B2FE0'
  },
  {
    rota: '/admin/cupons',
    icone: 'fas fa-tags',
    titulo: 'Cupons',
    descricao: 'Descontos, usos disponíveis e validade',
    bg: '#EBF8F0', cor: '#2E8B57'
  },
  {
    rota: '/admin/pagamentos',
    icone: 'fas fa-credit-card',
    titulo: 'Pagamentos',
    descricao: 'Transações, aprovações e status do gateway',
    bg: '#FDEEEE', cor: '#C0504D'
  },
  {
    rota: '/admin/estoque',
    icone: 'fas fa-boxes',
    titulo: 'Estoque',
    descricao: 'Entradas, saídas e movimentações',
    bg: '#EDF7FA', cor: '#2A7F8E'
  },
  {
    rota: '/admin/clientes',
    icone: 'fas fa-users',
    titulo: 'Clientes',
    descricao: 'Cadastros, histórico e assinaturas',
    bg: '#F0EEFF', cor: '#5B4FCF'
  },
]

onMounted(() => {
  if (!authStore.logado || authStore.tipo !== 'admin') {
    router.push('/login?redirect=/admin')
  }
})
</script>

<style scoped>
.admin-hub {
  min-height: 100vh;
  background: #F4F5F7;
  padding: 110px 0 60px;
  font-family: 'DM Sans', 'Segoe UI', sans-serif;
}

.hub-container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Header */
.hub-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 28px;
  padding-bottom: 18px;
  border-bottom: 1px solid #E3E5E8;
}

.hub-title {
  font-size: 22px;
  font-weight: 700;
  color: #1B1A19;
  margin: 0 0 2px;
  letter-spacing: -0.01em;
}

.hub-subtitle {
  font-size: 13px;
  color: #6B7280;
  margin: 0;
}

.hub-data {
  font-size: 13px;
  color: #9CA3AF;
  text-transform: capitalize;
}

/* Grid de módulos */
.hub-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 14px;
}

.hub-card {
  display: flex;
  align-items: center;
  gap: 14px;
  background: #FFFFFF;
  border: 1px solid #E3E5E8;
  border-radius: 10px;
  padding: 18px 16px;
  text-decoration: none;
  transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s;
}

.hub-card:hover {
  border-color: #C9A84C;
  box-shadow: 0 4px 14px rgba(27, 26, 25, 0.07);
  transform: translateY(-2px);
}

.card-icone {
  width: 42px;
  height: 42px;
  border-radius: 9px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 17px;
  flex-shrink: 0;
}

.card-texto { flex: 1; min-width: 0; }

.card-texto h3 {
  font-size: 14px;
  font-weight: 600;
  color: #1B1A19;
  margin: 0 0 3px;
}

.card-texto p {
  font-size: 12px;
  color: #6B7280;
  margin: 0;
  line-height: 1.4;
}

.card-seta {
  font-size: 11px;
  color: #C4C8CE;
  transition: color 0.15s, transform 0.15s;
}

.hub-card:hover .card-seta {
  color: #C9A84C;
  transform: translateX(3px);
}

/* Responsivo */
@media (max-width: 900px) {
  .hub-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 600px) {
  .hub-grid { grid-template-columns: 1fr; }
  .hub-header { flex-direction: column; align-items: flex-start; gap: 6px; }
  .admin-hub { padding-top: 130px; }
}
</style>
