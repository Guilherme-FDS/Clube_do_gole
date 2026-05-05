<template>
  <div id="app">
    <AppHeader />
    <router-view />
    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCarrinhoStore } from '@/stores/carrinho'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'

const auth = useAuthStore()
const carrinho = useCarrinhoStore()

onMounted(() => {
  auth.init()
  carrinho.init()
})
</script>