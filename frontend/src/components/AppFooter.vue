<template>
  <footer class="main-footer">
    <div class="footer-content">
      <div class="footer-siga-nos">
        <p>Siga-nos:</p>
        <div class="redes">
          <a href="https://www.instagram.com/mixupcode" target="_blank" aria-label="Instagram">
            <i class="fa-brands fa-instagram"></i>
          </a>
          <a href="#" aria-label="Facebook">
            <i class="fa-brands fa-facebook"></i>
          </a>
          <a href="mailto:contato@clubedogole.com" aria-label="Email">
            <i class="fa-solid fa-envelope"></i>
          </a>
          <a href="https://www.linkedin.com/in/mixup-code-86492638a/" target="blank" aria-label="LinkedIn">
            <i class="fa-brands fa-linkedin"></i>
          </a>
          <a href="https://api.whatsapp.com/send/?phone=5544984385699&text=Olá+Jackson%2C+vi+seu+portfólio+e+gostaria+de+conversar%21&type=phone_number&app_absent=0" target="_blank" aria-label="WhatsApp">
            <i class="fa-brands fa-whatsapp"></i>
          </a>
        </div>
      </div>
      <p class="footer-copyright fade-in" :class="{ visible: isVisible }">
        © 2025 Clube do Gole. Todos os direitos reservados. 
        Created with love by 
        <router-link to="/mixupcode" class="mixupcode-link">
          MixUpCode
        </router-link>
      </p>
    </div>
  </footer>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const isVisible = ref(false)

onMounted(() => {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        isVisible.value = true
        observer.disconnect()
      }
    })
  }, { threshold: 0.1 })

  const element = document.querySelector('.footer-copyright')
  if (element) observer.observe(element)
})
</script>