<template>
  <footer class="main-footer">
    <div class="footer-grid">

      <!-- Coluna 1: Marca -->
      <div class="footer-col footer-col-marca">
        <router-link to="/" style="display:flex;align-items:center;gap:0.625rem;text-decoration:none;margin-bottom:0.875rem;">
          <img src="/img/logo.png" alt="Clube do Gole" style="width:36px;height:auto;">
          <div class="logo-text">
            <span class="nome">CLUBE DO GOLE</span>
            <span class="subtitulo">Bebidas Premium</span>
          </div>
        </router-link>
        <p class="footer-descricao">Curadoria exclusiva de destilados raros entregues na sua porta todo mês.</p>
        <p style="margin-top:1rem;font-size:0.8rem;color:var(--cor-texto-secundario);">Maringá, PR — Brasil</p>
      </div>

      <!-- Coluna 2: Navegação -->
      <div class="footer-col">
        <h4>Navegação</h4>
        <ul>
          <li><router-link to="/#inicio">Início</router-link></li>
          <li><router-link to="/#planos">Planos</router-link></li>
          <li><router-link to="/#como-funciona">Como Funciona</router-link></li>
          <li><router-link to="/#sobre">Sobre</router-link></li>
          <li><router-link to="/#contato">Contato</router-link></li>
        </ul>
      </div>

      <!-- Coluna 3: Informações -->
      <div class="footer-col">
        <h4>Informações</h4>
        <ul>
          <li><a href="#">Política de Privacidade</a></li>
          <li><a href="#">Termos de Uso</a></li>
          <li><a href="#">Política de Entrega</a></li>
          <li><a href="#">Política de Cancelamento</a></li>
        </ul>
      </div>

      <!-- Coluna 4: Redes Sociais -->
      <div class="footer-col">
        <h4>Redes Sociais</h4>
        <div class="footer-redes">
          <a href="https://www.instagram.com" target="_blank" aria-label="Instagram">
            <i class="fa-brands fa-instagram"></i>
          </a>
          <a href="#" aria-label="Facebook">
            <i class="fa-brands fa-facebook"></i>
          </a>
          <a href="mailto:contato@clubedogole.com.br" aria-label="Email">
            <i class="fa-solid fa-envelope"></i>
          </a>
        </div>
        <p style="margin-top:1rem;font-size:0.8rem;color:var(--cor-texto-secundario);">Maringá, PR - Brasil</p>
      </div>
    </div>

    <!-- Bottom bar centralizado -->
    <div class="footer-bottom">
      <p class="footer-copyright">
        © 2026 Clube do Gole. Todos os direitos reservados.
        Created with love by
        <router-link to="/mixupcode" class="mixupcode-link">MixUpCode</router-link>
      </p>
    </div>
  </footer>
</template>

<script setup>
</script>