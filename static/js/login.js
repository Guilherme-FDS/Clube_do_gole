// ===== JAVASCRIPT PARA FUNÇÕES ESTÉTICAS DO LOGIN =====
document.addEventListener("DOMContentLoaded", () => {
    // ---------- INICIALIZAÇÃO ----------
    initLoginForm();
    initSocialLogin();
    initPasswordToggle();
    initCartCounter();
    initAnimations();

    // ---------- FORMULÁRIO DE LOGIN ----------
    function initLoginForm() {
        const loginForm = document.querySelector('.login-form');
        const btnLogin = document.querySelector('.btn-login');
        
        if (loginForm) {
            loginForm.addEventListener('submit', function(e) {
                // Apenas validação visual básica, não previne o envio
                const email = document.getElementById('email').value;
                const senha = document.getElementById('senha').value;
                
                // Validação visual do email
                if (email && !validateEmail(email)) {
                    showFlashMessage('Por favor, insira um email válido.', 'error');
                    // Não previne o envio - deixa o Flask validar
                }
                
                // Validação visual da senha
                if (email && !senha) {
                    showFlashMessage('Por favor, insira sua senha.', 'error');
                    // Não previne o envio - deixa o Flask validar
                }
                
                // Mostrar estado de loading visual
                if (btnLogin && email && senha) {
                    btnLogin.classList.add('loading');
                    btnLogin.disabled = true;
                    
                    // Reativar o botão após 5 segundos (caso haja erro no servidor)
                    setTimeout(() => {
                        btnLogin.classList.remove('loading');
                        btnLogin.disabled = false;
                    }, 5000);
                }
                
                // O formulário será enviado normalmente para o Flask
                // O Flask fará a validação real e redirecionamento
            });
        }
    }

    // ---------- LOGIN SOCIAL ----------
    function initSocialLogin() {
        const googleBtn = document.querySelector('.btn-social.google');
        const facebookBtn = document.querySelector('.btn-social.facebook');
        
        // Google Login - apenas visual
        if (googleBtn) {
            googleBtn.addEventListener('click', function() {
                this.classList.add('loading');
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Conectando...</span>';
                
                // Simular loading e mostrar mensagem
                setTimeout(() => {
                    showFlashMessage('Login com Google em desenvolvimento.', 'info');
                    this.innerHTML = originalText;
                    this.classList.remove('loading');
                }, 1500);
            });
        }
        
        // Facebook Login - apenas visual
        if (facebookBtn) {
            facebookBtn.addEventListener('click', function() {
                this.classList.add('loading');
                const originalText = this.innerHTML;
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Conectando...</span>';
                
                // Simular loading e mostrar mensagem
                setTimeout(() => {
                    showFlashMessage('Login com Facebook em desenvolvimento.', 'info');
                    this.innerHTML = originalText;
                    this.classList.remove('loading');
                }, 1500);
            });
        }
    }

    // ---------- TOGGLE DE SENHA ----------
    function initPasswordToggle() {
        const passwordToggle = document.querySelector('.password-toggle');
        const passwordInput = document.getElementById('senha');
        
        if (passwordToggle && passwordInput) {
            passwordToggle.addEventListener('click', function() {
                const icon = this.querySelector('i');
                
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    icon.classList.replace('fa-eye', 'fa-eye-slash');
                    this.setAttribute('aria-label', 'Ocultar senha');
                } else {
                    passwordInput.type = 'password';
                    icon.classList.replace('fa-eye-slash', 'fa-eye');
                    this.setAttribute('aria-label', 'Mostrar senha');
                }
                
                // Feedback tátil
                this.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    this.style.transform = 'scale(1)';
                }, 150);
            });
        }
    }

    // ---------- CONTADOR DO CARRINHO ----------
    function initCartCounter() {
        const cartCountEl = document.getElementById('cartCount');
        
        if (cartCountEl) {
            // Usando a mesma lógica do script principal
            fetch('/carrinho/contador')
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Erro na requisição');
                    }
                    return response.json();
                })
                .then(data => {
                    cartCountEl.textContent = data.count || 0;
                    
                    if (parseInt(data.count) > 0) {
                        cartCountEl.classList.add('pulse');
                        setTimeout(() => {
                            cartCountEl.classList.remove('pulse');
                        }, 600);
                    }
                })
                .catch(error => {
                    console.error('Erro ao carregar contador do carrinho:', error);
                    cartCountEl.textContent = '0';
                });
        }
    }

    // ---------- ANIMAÇÕES ----------
    function initAnimations() {
        // Animar elementos com classe fade-in
        const fadeElements = document.querySelectorAll('.fade-in');
        
        fadeElements.forEach((element, index) => {
            // Delay escalonado para elementos sequenciais
            element.style.transitionDelay = `${index * 0.1}s`;
            element.classList.add('visible');
        });
        
        // Animar inputs no focus
        const inputs = document.querySelectorAll('.form-input');
        inputs.forEach(input => {
            input.addEventListener('focus', function() {
                this.parentElement.classList.add('focused');
            });
            
            input.addEventListener('blur', function() {
                if (!this.value) {
                    this.parentElement.classList.remove('focused');
                }
            });
        });

        // Animar labels dos formulários
        const formInputs = document.querySelectorAll('.form-input');
        formInputs.forEach(input => {
            // Verificar se o input já tem valor ao carregar a página
            if (input.value) {
                input.parentElement.classList.add('focused');
            }

            input.addEventListener('input', function() {
                if (this.value) {
                    this.parentElement.classList.add('focused');
                } else {
                    this.parentElement.classList.remove('focused');
                }
            });
        });
    }

    // ---------- FUNÇÕES AUXILIARES ----------
    
    // Validar email (apenas para feedback visual)
    function validateEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }
    
    // Mostrar mensagens flash (para feedback visual adicional)
    function showFlashMessage(message, type = 'info') {
        // Remover mensagens existentes criadas pelo JS
        const existingMessages = document.querySelectorAll('.flash-message.js-generated');
        existingMessages.forEach(msg => msg.remove());
        
        // Criar nova mensagem
        const flashMessage = document.createElement('div');
        flashMessage.className = `flash-message ${type} js-generated`;
        
        const icons = {
            error: 'fas fa-exclamation-circle',
            success: 'fas fa-check-circle',
            info: 'fas fa-info-circle'
        };
        
        flashMessage.innerHTML = `
            <div class="flash-icon">
                <i class="${icons[type] || icons.info}"></i>
            </div>
            <div class="flash-content">
                <p>${message}</p>
            </div>
        `;
        
        // Inserir após o header do login
        const loginHeader = document.querySelector('.login-header');
        if (loginHeader) {
            loginHeader.parentNode.insertBefore(flashMessage, loginHeader.nextSibling);
        }
        
        // Auto-remover após 5 segundos
        setTimeout(() => {
            if (flashMessage.parentNode) {
                flashMessage.style.opacity = '0';
                flashMessage.style.transform = 'translateY(-10px)';
                setTimeout(() => {
                    if (flashMessage.parentNode) {
                        flashMessage.remove();
                    }
                }, 300);
            }
        }, 5000);
    }

    // ---------- MELHORIAS DE ACESSIBILIDADE ----------
    
    // Adicionar suporte a teclado para o toggle de senha
    const passwordToggle = document.querySelector('.password-toggle');
    if (passwordToggle) {
        passwordToggle.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    }

    // Focus trap para acessibilidade
    const focusableElements = document.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    if (focusableElements.length > 0) {
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Tab') {
                if (e.shiftKey) {
                    if (document.activeElement === firstElement) {
                        e.preventDefault();
                        lastElement.focus();
                    }
                } else {
                    if (document.activeElement === lastElement) {
                        e.preventDefault();
                        firstElement.focus();
                    }
                }
            }
        });
    }

    // ---------- ANIMAÇÕES ADICIONAIS ----------
    
    // Efeito de hover suave nos botões sociais
    const socialButtons = document.querySelectorAll('.btn-social');
    socialButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Efeito de loading no formulário
    const formInputs = document.querySelectorAll('.form-input');
    formInputs.forEach(input => {
        input.addEventListener('invalid', function() {
            this.style.borderColor = 'var(--cor-erro)';
        });
        
        input.addEventListener('input', function() {
            if (this.checkValidity()) {
                this.style.borderColor = 'var(--cor-dourado)';
            } else {
                this.style.borderColor = '';
            }
        });
    });

    // ---------- OTIMIZAÇÕES DE PERFORMANCE ----------
    
    // Debounce para eventos de resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(() => {
            // Recalcular layouts se necessário
        }, 250);
    });

    // Observer para elementos que entram na viewport
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('in-viewport');
                }
            });
        }, { threshold: 0.1 });

        // Observar elementos com classe observe-me
        document.querySelectorAll('.observe-me').forEach(el => {
            observer.observe(el);
        });
    }
});

// ---------- FUNÇÕES GLOBAIS PARA REUTILIZAÇÃO ----------

// Função para mostrar/esconder loading em qualquer botão
window.showButtonLoading = function(buttonElement) {
    if (buttonElement) {
        buttonElement.classList.add('loading');
        buttonElement.disabled = true;
    }
};

window.hideButtonLoading = function(buttonElement) {
    if (buttonElement) {
        buttonElement.classList.remove('loading');
        buttonElement.disabled = false;
    }
};

// Função para validar email (pode ser usada em outros lugares)
window.validateEmailFormat = function(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
};