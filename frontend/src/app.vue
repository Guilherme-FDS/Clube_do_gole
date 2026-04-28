<template>
  <router-view />
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCarrinhoStore } from '@/stores/carrinho'

const auth = useAuthStore()
const carrinho = useCarrinhoStore()

onMounted(() => {
  auth.init()
  carrinho.init()
})
</script>