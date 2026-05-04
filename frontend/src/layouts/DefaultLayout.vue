<template>
  <AppHeader />
  <main>
    <slot />
  </main>
  <AppFooter />
</template>

<script setup>
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
</script>