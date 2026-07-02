<template>
  <div id="app">
    <AgeGate v-if="!idadeVerificada" />
    <AppHeader />
    <router-view />
    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCarrinhoStore } from '@/stores/carrinho'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import AgeGate from '@/components/AgeGate.vue'

const auth = useAuthStore()
const carrinho = useCarrinhoStore()

const idadeVerificada = ref(localStorage.getItem('age_verified') === 'true')

watch(idadeVerificada, (aberto) => {
  document.body.classList.toggle('age-gate-open', !aberto)
}, { immediate: true })

onMounted(() => {
  auth.init()
  carrinho.init()
})
</script>

<style>
body.age-gate-open {
  overflow: hidden;
}
</style>