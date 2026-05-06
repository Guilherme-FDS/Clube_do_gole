<template>
    <main class="admin-container">
      <div class="container">
        <h1 class="admin-title titulo-lg">Painel Administrativo</h1>
        <p class="admin-subtitle texto-corrido texto-centro">Gerencie todas as áreas do Clube do Gole</p>
  
        <div class="admin-grid">
          <!-- CUPONS -->
          <router-link to="/admin/cupons" class="admin-card fade-in" :class="{ visible: fadeInVisible }" @click="handleCardClick">
            <div class="card-icon">
              <i class="fas fa-tags"></i>
              <span class="card-badge" v-if="stats.cuponsAtivos > 0">{{ stats.cuponsAtivos }} Ativos</span>
            </div>
            <h3 class="card-title">Gerenciar Cupons</h3>
            <p class="card-description">Controle cupons de desconto, usos disponíveis e porcentagens</p>
            <div class="card-arrow">
              <i class="fas fa-chevron-right"></i>
            </div>
          </router-link>
  
          <!-- VENDAS -->
          <router-link to="/admin/vendas" class="admin-card fade-in" :class="{ visible: fadeInVisible }" @click="handleCardClick">
            <div class="card-icon">
              <i class="fas fa-chart-line"></i>
              <span class="card-badge">Relatórios</span>
            </div>
            <h3 class="card-title">Dashboard de Vendas</h3>
            <p class="card-description">Relatórios completos de vendas, produtos mais vendidos e faturamento</p>
            <div class="card-arrow">
              <i class="fas fa-chevron-right"></i>
            </div>
          </router-link>
  
          <!-- PRODUTOS -->
          <router-link to="/admin/produtos" class="admin-card fade-in" :class="{ visible: fadeInVisible }" @click="handleCardClick">
            <div class="card-icon">
              <i class="fas fa-wine-bottle"></i>
            </div>
            <h3 class="card-title">Gerenciar Produtos</h3>
            <p class="card-description">Adicione, edite ou remova produtos do catálogo de bebidas</p>
            <div class="card-arrow">
              <i class="fas fa-chevron-right"></i>
            </div>
          </router-link>
        </div>
      </div>
    </main>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  
  const router = useRouter()
  const authStore = useAuthStore()
  
  // Estados
  const fadeInVisible = ref(false)
  const stats = ref({
    cuponsAtivos: 0
  })
  
  // Estatísticas (opcional - pode ser carregada da API)
  const carregarEstatisticas = async () => {
    try {
      // Opcional: buscar contagem de cupons ativos
      const response = await fetch('/api/admin/stats', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })
      if (response.ok) {
        const data = await response.json()
        stats.value.cuponsAtivos = data.cupons_ativos || 0
      }
    } catch (error) {
      console.error('Erro ao carregar estatísticas:', error)
    }
  }
  
  // Feedback de clique no card
  const handleCardClick = (e) => {
    const card = e.currentTarget
    const originalContent = card.innerHTML
    
    card.innerHTML = `
      <div class="card-loading">
        <i class="fas fa-spinner fa-spin"></i>
        <span>Carregando...</span>
      </div>
    `
    
    // Restaurar após timeout (caso o redirecionamento falhe)
    setTimeout(() => {
      if (card.innerHTML !== originalContent) {
        card.innerHTML = originalContent
      }
    }, 3000)
  }
  
  // Verificar autenticação e permissão
  onMounted(async () => {
    if (!authStore.logado || authStore.tipo !== 'admin') {
      router.push('/login?redirect=/admin')
      return
    }
    
    await carregarEstatisticas()
    
    setTimeout(() => {
      fadeInVisible.value = true
    }, 100)
  })
  </script>
  
  <style scoped>
  /* ===== ESTILOS EXCLUSIVOS DO PAINEL ADMINISTRATIVO ===== */
  .admin-container {
    padding: 140px 0 var(--espacamento-xl);
    background: var(--gradiente-hero);
    min-height: 100vh;
  }
  
  .admin-title {
    color: var(--cor-dourado);
    margin-bottom: var(--espacamento-sm);
    position: relative;
    text-align: center;
  }
  
  .admin-title::after {
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
  
  .admin-subtitle {
    margin-bottom: var(--espacamento-lg);
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    text-align: center;
  }
  
  .admin-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
    gap: var(--espacamento-lg);
    max-width: 1200px;
    margin: 0 auto;
  }
  
  .admin-card {
    background: var(--cor-fundo-secundario);
    border-radius: var(--borda-radius-lg);
    padding: var(--espacamento-lg);
    text-decoration: none;
    transition: all 0.3s ease;
    border: 1px solid rgba(255, 215, 0, 0.2);
    position: relative;
    overflow: hidden;
    display: block;
    height: 100%;
    cursor: pointer;
  }
  
  .admin-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gradiente-botao);
    transform: scaleX(0);
    transition: transform 0.3s ease;
  }
  
  .admin-card:hover::before {
    transform: scaleX(1);
  }
  
  .admin-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--sombra-destaque);
    border-color: var(--cor-dourado);
  }
  
  .card-icon {
    position: relative;
    margin-bottom: var(--espacamento-md);
    text-align: center;
  }
  
  .card-icon i {
    font-size: 3.5rem;
    color: var(--cor-dourado);
    transition: all 0.3s ease;
  }
  
  .admin-card:hover .card-icon i {
    transform: scale(1.1);
    color: var(--cor-roxo-principal);
  }
  
  .card-badge {
    position: absolute;
    top: -8px;
    right: -8px;
    background: var(--gradiente-botao);
    color: var(--cor-fundo);
    padding: 0.5rem 1rem;
    border-radius: var(--borda-radius-lg);
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  
  .card-title {
    font-family: var(--fonte-secundaria);
    font-size: 1.5rem;
    color: var(--cor-dourado);
    margin-bottom: var(--espacamento-sm);
    text-align: center;
    font-weight: 600;
  }
  
  .card-description {
    color: var(--cor-texto-secundario);
    text-align: center;
    line-height: 1.6;
    margin-bottom: var(--espacamento-md);
  }
  
  .card-arrow {
    text-align: center;
    color: var(--cor-dourado);
    font-size: 1.25rem;
    transition: all 0.3s ease;
  }
  
  .admin-card:hover .card-arrow {
    transform: translateX(5px);
    color: var(--cor-roxo-principal);
  }
  
  /* Estilos para loading dos cards */
  .card-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--espacamento-md);
    color: var(--cor-dourado);
    min-height: 200px;
  }
  
  .card-loading i {
    font-size: 2rem;
    margin-bottom: var(--espacamento-xs);
  }
  
  .card-loading span {
    font-size: 0.9rem;
    font-weight: 500;
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
  
  /* Aplicar delay diferente para cada card */
  .admin-card:nth-child(1) { transition-delay: 0s; }
  .admin-card:nth-child(2) { transition-delay: 0.1s; }
  .admin-card:nth-child(3) { transition-delay: 0.2s; }
  
  /* Responsividade */
  @media (max-width: 1024px) {
    .admin-grid {
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: var(--espacamento-md);
    }
  }
  
  @media (max-width: 768px) {
    .admin-container {
      padding: 120px 0 var(--espacamento-lg);
    }
    
    .admin-grid {
      grid-template-columns: 1fr;
      gap: var(--espacamento-md);
    }
    
    .admin-card {
      padding: var(--espacamento-md);
    }
  }
  
  @media (max-width: 480px) {
    .admin-container {
      padding: 100px 0 var(--espacamento-md);
    }
    
    .admin-title {
      font-size: 2rem;
    }
    
    .admin-card {
      padding: var(--espacamento-sm);
    }
    
    .card-icon i {
      font-size: 3rem;
    }
    
    .card-title {
      font-size: 1.25rem;
    }
  }
  </style>