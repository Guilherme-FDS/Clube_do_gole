document.addEventListener("DOMContentLoaded", () => {
  // ---------- INICIALIZAÇÃO ----------
  initHeaderScroll();
  initCarousel();
  initScrollAnimations();
  initSmoothScroll();
  atualizarContadorCarrinho();
  initUserMenu(); // ← Adicionei esta linha

  // ---------- HEADER COM SCROLL ----------
  function initHeaderScroll() {
    const header = document.querySelector('header');
    
    if (header) {
      window.addEventListener('scroll', () => {
        if (window.scrollY > 100) {
          header.classList.add('header-scrolled');
        } else {
          header.classList.remove('header-scrolled');
        }
      });
    }
  }

  // ---------- CARROSSEL PRINCIPAL MODERNO ----------
  function initCarousel() {
    const carouselContainer = document.getElementById("carouselContainer");
    const slides = document.querySelectorAll(".carousel-slide");
    const prevSlide = document.getElementById("prevSlide");
    const nextSlide = document.getElementById("nextSlide");
    const indicatorsContainer = document.getElementById("carouselIndicators");

    if (!carouselContainer || slides.length === 0 || !prevSlide || !nextSlide || !indicatorsContainer) {
      return;
    }

    let currentIndex = 0;
    let intervalId;
    let isAnimating = false;

    function updateCarousel() {
      if (isAnimating) return;
      
      isAnimating = true;
      carouselContainer.style.transform = `translateX(-${currentIndex * 100}%)`;
      
      // Atualizar indicadores
      document.querySelectorAll(".indicador").forEach((dot, index) => {
        dot.classList.toggle("active", index === currentIndex);
      });

      // Reset da flag de animação
      setTimeout(() => {
        isAnimating = false;
      }, 500);
    }

    function startCarousel() {
      intervalId = setInterval(() => {
        currentIndex = (currentIndex + 1) % slides.length;
        updateCarousel();
      }, 5000);
    }

    function stopCarousel() {
      clearInterval(intervalId);
    }

    // Criar indicadores dinamicamente
    function createIndicators() {
      indicatorsContainer.innerHTML = '';
      slides.forEach((_, index) => {
        const dot = document.createElement("div");
        dot.classList.add("indicador");
        if (index === 0) dot.classList.add("active");
        
        dot.addEventListener("click", () => {
          if (index !== currentIndex && !isAnimating) {
            currentIndex = index;
            updateCarousel();
            stopCarousel();
            startCarousel();
          }
        });
        
        indicatorsContainer.appendChild(dot);
      });
    }

    // Event listeners para navegação
    function setupEventListeners() {
      prevSlide.addEventListener("click", () => {
        if (isAnimating) return;
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        updateCarousel();
        stopCarousel();
        startCarousel();
      });

      nextSlide.addEventListener("click", () => {
        if (isAnimating) return;
        currentIndex = (currentIndex + 1) % slides.length;
        updateCarousel();
        stopCarousel();
        startCarousel();
      });

      // Pausar carousel no hover
      carouselContainer.addEventListener("mouseenter", stopCarousel);
      carouselContainer.addEventListener("mouseleave", startCarousel);

      // Pausar carousel quando a janela perde foco
      document.addEventListener("visibilitychange", () => {
        if (document.hidden) {
          stopCarousel();
        } else {
          startCarousel();
        }
      });
    }

    // Inicializar carousel
    createIndicators();
    setupEventListeners();
    startCarousel();
  }

  // ---------- ANIMAÇÕES AO SCROLL ----------
  function initScrollAnimations() {
    const observerOptions = {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          
          // Animações específicas para diferentes elementos
          if (entry.target.classList.contains('passo')) {
            entry.target.style.transitionDelay = `${entry.target.dataset.delay || '0'}ms`;
          }
        }
      });
    }, observerOptions);

    // Observar todos os elementos com classe fade-in
    document.querySelectorAll('.fade-in').forEach((el, index) => {
      if (el.classList.contains('passo')) {
        el.dataset.delay = index * 100;
      }
      observer.observe(el);
    });
  }

  // ---------- SCROLL SUAVE ----------
  function initSmoothScroll() {
    // Scroll para links internos
    document.querySelectorAll('.scroll-link').forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
          const headerHeight = document.querySelector('header').offsetHeight;
          const targetPosition = targetElement.offsetTop - headerHeight;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    });

    // Botão "Conheça os Planos" no hero
    const btnPlanos = document.querySelector('.btn-modern');
    if (btnPlanos) {
      btnPlanos.addEventListener('click', function(e) {
        e.preventDefault();
        const targetElement = document.querySelector('#planos');
        if (targetElement) {
          const headerHeight = document.querySelector('header').offsetHeight;
          const targetPosition = targetElement.offsetTop - headerHeight;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    }
  }

  // ---------- CONTADOR DO CARRINHO ----------
  async function atualizarContadorCarrinho() {
    try {
      const response = await fetch("/carrinho/contador");
      if (!response.ok) {
        throw new Error('Erro na resposta do servidor');
      }
      
      const data = await response.json();
      const cartCountElement = document.getElementById("cartCount");
      
      if (cartCountElement) {
        cartCountElement.textContent = data.count;
        
        // Adicionar animação quando o contador muda
        if (parseInt(cartCountElement.textContent) > 0) {
          cartCountElement.classList.add('pulse');
          setTimeout(() => {
            cartCountElement.classList.remove('pulse');
          }, 300);
        }
      }
    } catch (error) {
      console.error("Erro ao atualizar contador do carrinho:", error);
    }
  }

  // ---------- MENU DO USUÁRIO MOBILE ----------
  function initUserMenu() {
    const userMenuContainers = document.querySelectorAll('.user-menu-container');
    
    userMenuContainers.forEach(container => {
      const trigger = container.querySelector('.user-menu-trigger');
      const dropdown = container.querySelector('.user-dropdown');
      
      if (trigger && dropdown) {
        // Toggle no clique
        trigger.addEventListener('click', (e) => {
          e.stopPropagation();
          const isVisible = dropdown.style.display === 'block';
          dropdown.style.display = isVisible ? 'none' : 'block';
        });
        
        // Fechar ao clicar fora
        document.addEventListener('click', (e) => {
          if (!container.contains(e.target)) {
            dropdown.style.display = 'none';
          }
        });
        
        // Fechar ao pressionar ESC
        document.addEventListener('keydown', (e) => {
          if (e.key === 'Escape') {
            dropdown.style.display = 'none';
          }
        });
      }
    });
  }

  // ---------- OTIMIZAÇÕES DE PERFORMANCE ----------
  // Debounce para eventos de scroll
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // Recalcular elementos apenas quando necessário
  window.addEventListener('resize', debounce(() => {
    // Re-inicializar animações se necessário
    initScrollAnimations();
  }, 250));

  // ---------- MENSAGENS DE CARREGAMENTO ----------
  // Mostrar loading state nos botões quando necessário
  document.addEventListener('submit', function(e) {
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    
    if (submitBtn) {
      submitBtn.classList.add('btn-loading');
      submitBtn.disabled = true;
    }
  });

  // ---------- TRATAMENTO DE ERROS ----------
  window.addEventListener('error', function(e) {
    console.error('Erro capturado:', e.error);
  });

  window.addEventListener('unhandledrejection', function(e) {
    console.error('Promise rejeitada:', e.reason);
  });
});

// ---------- FUNÇÕES GLOBAIS ÚTEIS ----------
// Função para formatar preços
function formatarPreco(preco) {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL'
  }).format(preco);
}

// Função para validar email
function validarEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}