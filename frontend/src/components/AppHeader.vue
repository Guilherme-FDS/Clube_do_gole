<template>
  <header class="main-header" :class="{ 'header-scrolled': isScrolled }">
    <div class="header-left">
      <div class="logo">
        <img src="/img/logo.png" alt="Clube do Gole" class="logo-img-small">
      </div>
      <nav class="nav-left">
        <ul>
          <!-- CHECKOUT -->
          <template v-if="$route.name === 'checkout'">
            <li><router-link to="/">Início</router-link></li>
            <li><router-link to="/carrinho">Carrinho</router-link></li>
          </template>

          <!-- ADMIN -->
          <template v-else-if="isAdminRoute">
            <li><router-link to="/">Início</router-link></li>
            <li>
              <router-link to="/admin" class="nav-admin-btn">
                <i class="fas fa-cog"></i> Painel ADM
              </router-link>
            </li>
            <li v-if="$route.name === 'editar-produto'">
              <router-link to="/admin/produtos" class="nav-admin-btn">
                <i class="fas fa-box"></i> Produtos
              </router-link>
            </li>
            <li v-if="$route.name === 'editar-cupom'">
              <router-link to="/admin/cupons" class="nav-admin-btn">
                <i class="fas fa-tag"></i> Gerenciar Cupons
              </router-link>
            </li>
          </template>

          <!-- NORMAL -->
          <template v-else>
            <li><a href="#" @click.prevent="scrollTo('inicio')">Início</a></li>
            <li><a href="#" @click.prevent="scrollTo('como-funciona')">Como Funciona</a></li>
            <li><a href="#" @click.prevent="scrollTo('planos')">Planos</a></li>
            <li><a href="#" @click.prevent="scrollTo('sobre')">Sobre</a></li>
            <li><a href="#" @click.prevent="scrollTo('contato')">Contato</a></li>
          </template>
        </ul>
      </nav>
    </div>

    <div class="header-right">
      <router-link to="/carrinho" class="icon-btn">
        <i class="fas fa-shopping-cart"></i> Carrinho
        <span class="cart-count">{{ cartCount }}</span>
      </router-link>

      <div v-if="logado" class="user-menu-container" ref="userMenu">
        <div class="user-menu-trigger" @click="toggleUserMenu">
          <span class="icon-btn user-name">
            <i class="fas fa-user"></i>
            {{ nomeExibicao }}
          </span>
          <button class="menu-sanduiche">
            <i class="fas fa-bars"></i>
          </button>
        </div>
        <div class="user-dropdown" v-show="isUserMenuOpen">
          <template v-if="isAdmin">
            <router-link to="/admin" class="dropdown-item">
              <i class="fas fa-cog"></i> Painel Administrativo
            </router-link>
          </template>
          <template v-else>
            <router-link to="/configuracoes" class="dropdown-item">
              <i class="fas fa-cog"></i> Configurações
            </router-link>
          </template>
          <a href="#" @click.prevent="logout" class="dropdown-item">
            <i class="fas fa-sign-out-alt"></i> Sair
          </a>
        </div>
      </div>

      <router-link v-else to="/login" class="icon-btn">
        <i class="fas fa-user"></i> Login
      </router-link>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCarrinhoStore } from '@/stores/carrinho'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const carrinhoStore = useCarrinhoStore()

const isScrolled = ref(false)
const isUserMenuOpen = ref(false)
const userMenu = ref(null)

const logado = computed(() => authStore.logado)
const isAdmin = computed(() => authStore.tipo === 'admin')
const nomeExibicao = computed(() => authStore.nome?.split(' ')[0] || 'Usuário')
const cartCount = computed(() => carrinhoStore.count)

const isAdminRoute = computed(() => {
  const adminRoutes = ['usuario_adm', 'cupons', 'dashboard_vendas', 'produtos', 'editar_cupom', 'editar_produto']
  return adminRoutes.includes(route.name)
})

const handleScroll = () => { isScrolled.value = window.scrollY > 100 }

const scrollTo = (sectionId) => {
  if (route.name !== 'home') {
    router.push('/').then(() => {
      setTimeout(() => {
        const el = document.getElementById(sectionId)
        if (el) {
          const offset = document.querySelector('.main-header')?.offsetHeight || 72
          window.scrollTo({ top: el.offsetTop - offset, behavior: 'smooth' })
        }
      }, 350)
    })
  } else {
    const el = document.getElementById(sectionId)
    if (el) {
      const offset = document.querySelector('.main-header')?.offsetHeight || 72
      window.scrollTo({ top: el.offsetTop - offset, behavior: 'smooth' })
    }
  }
}

const toggleUserMenu = () => { isUserMenuOpen.value = !isUserMenuOpen.value }

const closeUserMenu = (e) => {
  if (userMenu.value && !userMenu.value.contains(e.target)) isUserMenuOpen.value = false
}

const logout = async () => {
  await authStore.sair()
  router.push('/')
  isUserMenuOpen.value = false
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  document.addEventListener('click', closeUserMenu)
  handleScroll()
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  document.removeEventListener('click', closeUserMenu)
})
</script>