// usuario_adm.js - Funcionalidades específicas do painel administrativo

document.addEventListener("DOMContentLoaded", () => {
    // Inicializar funcionalidades do admin
    initAdminAnimations();
    initAdminCards();
    initAdminPerformance();
});

// Animações específicas do painel administrativo
function initAdminAnimations() {
    // Delay específico para os cards do admin
    const adminCards = document.querySelectorAll('.admin-card.fade-in');
    
    adminCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
}

// Interações com os cards do admin
function initAdminCards() {
    const adminCards = document.querySelectorAll('.admin-card');
    
    adminCards.forEach(card => {
        // Efeito de hover com feedback tátil
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Feedback de clique
        card.addEventListener('click', function(e) {
            // Adicionar efeito de loading
            const originalContent = this.innerHTML;
            this.innerHTML = `
                <div class="card-loading">
                    <i class="fas fa-spinner fa-spin"></i>
                    <span>Carregando...</span>
                </div>
            `;
            
            // Restaurar conteúdo após um tempo (caso o redirecionamento falhe)
            setTimeout(() => {
                this.innerHTML = originalContent;
            }, 2000);
        });
    });
}

// Otimizações de performance
function initAdminPerformance() {
    // Debounce para eventos de resize
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

    // Recalcular animações no resize (com debounce)
    window.addEventListener('resize', debounce(() => {
        initAdminAnimations();
    }, 250));
}

// Tratamento de erros
window.addEventListener('error', function(e) {
    console.error('Erro no painel administrativo:', e.error);
});