<template>
  <div class="age-gate-overlay">
    <div class="age-gate-card">
      <span class="chip">Clube do Gole</span>
      <h2>Você é maior de 18 anos?</h2>
      <p class="subtitulo">Este site contém conteúdo sobre bebidas alcoólicas e é destinado apenas a maiores de idade.</p>
      <div class="age-gate-botoes">
        <button type="button" class="btn-sim" @click="confirmarSim">Sim</button>
        <button type="button" class="btn-nao" @click="confirmarNao">Não</button>
      </div>
    </div>
  </div>
</template>

<script setup>
function confirmarSim() {
  localStorage.setItem('age_verified', 'true')
  document.body.classList.remove('age-gate-open')
  window.location.reload()
}

function confirmarNao() {
  if (window.history.length > 1) {
    window.history.back()
  } else {
    window.location.href = 'https://google.com'
  }
}
</script>

<style scoped>
.age-gate-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 1.25rem;
}

.age-gate-card {
  width: 100%;
  max-width: 380px;
  background: #0d0d0d;
  border: 1px solid #C9A84C;
  border-radius: 16px;
  padding: 2.2rem 1.8rem;
  text-align: center;
  box-shadow: 0 0 40px rgba(201, 168, 76, 0.15);
}

.chip {
  display: inline-flex;
  gap: 5px;
  font-size: 0.72rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #C9A84C;
  background: rgba(201, 168, 76, 0.08);
  border: 1px solid rgba(201, 168, 76, 0.25);
  border-radius: 999px;
  padding: 0.25rem 0.75rem;
  margin-bottom: 1rem;
}
.chip::before { content: '●'; font-size: 6px; }

.age-gate-card h2 {
  margin: 0;
  font-size: 1.4rem;
  color: #ffffff;
}

.subtitulo {
  margin-top: 0.7rem;
  font-size: 0.88rem;
  color: #aaaaaa;
  line-height: 1.5;
}

.age-gate-botoes {
  display: flex;
  gap: 0.9rem;
  margin-top: 1.6rem;
}

.btn-sim,
.btn-nao {
  flex: 1;
  padding: 0.78rem;
  border-radius: 11px;
  font-weight: 700;
  font-size: 0.92rem;
  cursor: pointer;
  border: none;
}

.btn-sim {
  background: linear-gradient(45deg, #9E7A2E, #E2C06A);
  color: #0d0d0d;
}

.btn-nao {
  background: transparent;
  color: #C9A84C;
  border: 1px solid #C9A84C;
}
</style>
