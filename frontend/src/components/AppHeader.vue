<template>
  <header class="main-header">
    <div class="header-left">
      <div class="logo">
        <router-link to="/">
          <img src="/img/logo.png" alt="Clube do Gole" class="logo-img-small" />
        </router-link>
      </div>

      <nav class="nav-left">
        <ul>
          <!-- Admin -->
          <template v-if="isAdmin">
            <li><router-link to="/">Início</router-link></li>
            <li>
              <router-link to="/admin" class="nav-admin-btn">
                <i class="fas fa-cog"></i> Painel ADM
              </router-link>
            </li>
            <li v-if="isRotaAdmin('AdminEditarProduto')">
              <router-link to="/admin/produtos" class="nav-admin-btn">
                <i class="fas fa-box"></i> Produtos
              </router-link>
            </li>
            <li v-if="isRotaAdmin('AdminEditarCupom')">
              <router-link to="/admin/cupons" class="nav-admin-btn">
                <i class="fas fa-tag"></i> Gerenciar Cupons
              </router-link>
            </li>
          </template>

          <!-- Checkout: menu simplificado -->
          <template v-else-if="rota === 'Checkout'">
            <li><router-link to="/">Início</router-link></li>
            <li><a href="/#planos">Produtos</a></li>
            <li><router-link to="/carrinho">Carrinho</router-link></li>
          </template>

          <!-- Normal -->
          <template v-else>
            <li><a :href="linkSecao('inicio')">Início</a></li>
            <li><a :href="linkSecao('comofunciona')">Como Funciona</a></li>
            <li><a :href="linkSecao('planos')">Planos</a></li>
            <li><a :href="linkSecao('sobre')">Sobre</a></li>
            <li><a :href="linkSecao('contato')">Contato</a></li>
          </template>
        </ul>
      </nav>
    </div>

    <div class="header-right">
      <router-link to="/carrinho" class="icon-btn" id="cartBtn">
        <i class="fas fa-shopping-cart"></i> Carrinho
        <span id="cartCount">{{ carrinhoCount }}</span>
      </router-link>

      <!-- Logado -->
      <div v-if="auth.logado" class="user-menu-container">
        <div class="user-menu-trigger">
          <span class="icon-btn user-name">
            <i class="fas fa-user"></i> {{ primeiroNome }}
          </span>
          <button class="menu-sanduiche" @click="toggleMenu">
            <i class="fas fa-bars"></i>
          </button>
        </div>
        <div class="user-dropdown" :class="{ open: menuAberto }">
          <router-link v-if="isAdmin" to="/admin" class="dropdown-item" @click="fecharMenu">
            <i class="fas fa-cog"></i> Painel Administrativo
          </router-link>
          <router-link v-else to="/configuracoes" class="dropdown-item" @click="fecharMenu">
            <i class="fas fa-cog"></i> Configurações
          </router-link>
          <a href="#" class="dropdown-item" @click.prevent="sair">
            <i class="fas fa-sign-out-alt"></i> Sair
          </a>
        </div>
      </div>

      <!-- Não logado -->
      <router-link v-else to="/login" class="icon-btn">
        <i class="fas fa-user"></i> Login
      </router-link>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCarrinhoStore } from '@/stores/carrinho'

const auth     = useAuthStore()
const carrinho = useCarrinhoStore()
const route    = useRoute()
const router   = useRouter()

const menuAberto  = ref(false)
const rota        = computed(() => route.name)
const isAdmin     = computed(() => auth.tipo === 'admin')
const carrinhoCount = computed(() => carrinho.count)
const primeiroNome  = computed(() => (auth.nome || '').split(' ')[0])

function isRotaAdmin(nome) { return rota.value === nome }

function linkSecao(secao) {
  return rota.value === 'Home' ? `#${secao}` : `/#${secao}`
}

function toggleMenu() { menuAberto.value = !menuAberto.value }
function fecharMenu()  { menuAberto.value = false }

async function sair() {
  fecharMenu()
  await auth.sair()
  router.push('/login')
}
</script>