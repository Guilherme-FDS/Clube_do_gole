<template>
  <footer class="main-footer">
    <div class="footer-divisor-topo"></div>

    <div class="footer-grid">

      <!-- Coluna 1: Marca -->
      <div class="footer-col footer-col-marca">
        <router-link to="/" class="footer-logo">
          <img src="/img/logo.webp" alt="Clube do Gole" style="width:40px;height:auto;">
          <div class="logo-text">
            <span class="nome">CLUBE DO GOLE</span>
            <span class="subtitulo">Bebidas Premium</span>
          </div>
        </router-link>
        <p class="footer-descricao">Curadoria exclusiva de destilados raros entregues na sua porta todo mês.</p>
        <div class="footer-redes">
          <a href="https://www.instagram.com" target="_blank" rel="noopener noreferrer" aria-label="Instagram">
            <i class="fa-brands fa-instagram"></i>
          </a>
          <a href="#" aria-label="Facebook">
            <i class="fa-brands fa-facebook"></i>
          </a>
          <a href="mailto:contato@clubedogole.com.br" aria-label="Email">
            <i class="fa-solid fa-envelope"></i>
          </a>
        </div>
      </div>

      <!-- Coluna 2: Obtenha Ajuda -->
      <div class="footer-col">
        <h4>Obtenha Ajuda</h4>
        <ul>
          <li><router-link to="/faq">Perguntas Frequentes</router-link></li>
          <li><router-link to="/contato">Contate-nos</router-link></li>
          <li><router-link to="/envio-devolucoes">Envio e Devoluções</router-link></li>
          <li><router-link to="/politica-reembolso">Política de Reembolso</router-link></li>
          <li><router-link to="/meus-pedidos">Acompanhe seu Pedido</router-link></li>
        </ul>
      </div>

      <!-- Coluna 3: Junte-se -->
      <div class="footer-col">
        <h4>Junte-se</h4>
        <ul>
          <li><router-link to="/corporativo">Parcerias</router-link></li>
          <li>
            <a href="https://docs.google.com/forms/d/e/1FAIpQLSfy8JIXAE-M2mAVcUXJRCyCICgCzHkJNUadbtC9qygMaVzoHg/viewform"
              target="_blank" rel="noopener noreferrer">Influenciadores</a>
          </li>
          <li>
            <a href="https://tally.so/r/gDvqpD" target="_blank" rel="noopener noreferrer">
              Pesquisa de Mercado
            </a>
          </li>
        </ul>
      </div>

      <!-- Coluna 4: Clube do Gole -->
      <div class="footer-col">
        <h4>Clube do Gole</h4>
        <ul>
          <li><router-link to="/#como-funciona">Como Funciona</router-link></li>
          <li><router-link to="/corporativo">Corporativo</router-link></li>
          <li><router-link to="/blog">Blog</router-link></li>
          <li><router-link to="/sobre">Nossa História</router-link></li>
          <li><router-link to="/sobre#missao">Missão e Valores</router-link></li>
          <li><router-link to="/contato">Imprensa</router-link></li>
        </ul>
      </div>

    </div>

    <!-- Pagamentos -->
    <div class="footer-pagamentos">
      <span class="footer-pagamentos-label">Formas de pagamento</span>
      <div class="footer-pagamentos-icons">
        <span class="pgto-badge"><i class="fa-brands fa-cc-visa"></i> Visa</span>
        <span class="pgto-badge"><i class="fa-brands fa-cc-mastercard"></i> Mastercard</span>
        <span class="pgto-badge"><i class="fas fa-qrcode"></i> Pix</span>
      </div>
    </div>

    <div class="footer-divisor"></div>

    <!-- Bottom bar -->
    <div class="footer-bottom">
      <p class="footer-copyright">© 2026 Clube do Gole. Todos os direitos reservados.</p>
      <div class="footer-legais">
        <a href="#">Termos e Condições</a>
        <a href="#">Política de Privacidade</a>
        <a href="#">Política de Cookies</a>
      </div>
    </div>

  </footer>
</template>

<script setup>
</script>

<style scoped>
.main-footer {
  padding-top: var(--espacamento-md);
  padding-bottom: 0;
}

.footer-divisor-topo {
  border-top: 1px solid rgba(201,168,76,0.2);
  margin-bottom: var(--espacamento-md);
}

.footer-divisor {
  border-top: 1px solid rgba(201,168,76,0.15);
  margin: var(--espacamento-sm) auto 0;
  max-width: 1200px;
  padding: 0 var(--espacamento-sm);
}

.footer-logo {
  display: flex; align-items: center; gap: 0.625rem;
  text-decoration: none; margin-bottom: 0.75rem;
}

.footer-redes {
  margin-top: 1rem;
}

.footer-link-desabilitado {
  color: var(--cor-texto-secundario);
  opacity: 0.4;
  cursor: default;
  font-size: 0.875rem;
}

.footer-pagamentos {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--espacamento-sm) var(--espacamento-sm);
  display: flex;
  align-items: center;
  gap: 1.25rem;
  flex-wrap: wrap;
}
.footer-pagamentos-label {
  font-size: 0.8125rem;
  color: var(--cor-texto-secundario);
  font-weight: 500;
}
.footer-pagamentos-icons {
  display: flex; gap: 0.75rem; flex-wrap: wrap;
}
.pgto-badge {
  display: inline-flex; align-items: center; gap: 0.35rem;
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: var(--borda-radius-sm);
  padding: 0.3rem 0.75rem;
  font-size: 0.8125rem;
  color: var(--cor-texto-secundario);
}
.pgto-badge i { font-size: 1rem; }

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--espacamento-sm) var(--espacamento-sm);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
}
.footer-legais {
  display: flex; gap: 1.25rem; flex-wrap: wrap;
}
.footer-legais a {
  color: var(--cor-texto-secundario);
  font-size: 0.8125rem;
  text-decoration: none;
  transition: color 0.2s;
}
.footer-legais a:hover { color: var(--cor-dourado); }

@media (max-width: 768px) {
  .footer-bottom { flex-direction: column; text-align: center; }
  .footer-legais { justify-content: center; }
  .footer-pagamentos { justify-content: center; }
}
</style>