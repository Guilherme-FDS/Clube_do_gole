<template>
  <div></div>
</template>

<script setup>
// Edição de produto agora acontece via modal em /admin/produtos.
// Esta rota existe apenas por compatibilidade com links antigos.
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
onMounted(() => router.replace('/admin/produtos'))
</script>
