// cupons.js - Funcionalidades específicas da gestão de cupons

document.addEventListener("DOMContentLoaded", () => {
    // Inicializar funcionalidades dos cupons
    initCuponsModal();
    initCuponsForm();
    initCuponsAnimations();
    initCuponsPerformance();
});

// Gerenciamento do Modal
function initCuponsModal() {
    const modal = document.getElementById('modalCupom');
    const btnAbrir = document.getElementById('btnAbrirModal');
    const btnFechar = document.getElementById('btnFecharModal');
    const formCupom = document.getElementById('formCupom');

    if (!modal || !btnAbrir) return;

    // Abrir modal
    btnAbrir.addEventListener('click', () => {
        modal.style.display = 'flex';
        document.getElementById('codigoCupom')?.focus();
    });

    // Fechar modal
    if (btnFechar) {
        btnFechar.addEventListener('click', fecharModal);
    }

    // Fechar modal clicando fora
    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            fecharModal();
        }
    });

    // Fechar modal com ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            fecharModal();
        }
    });

    // Auto-uppercase no código do cupom
    const codigoInput = document.getElementById('codigoCupom');
    if (codigoInput) {
        codigoInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, '');
        });
    }

    // Validação do formulário
    if (formCupom) {
        formCupom.addEventListener('submit', function(e) {
            if (!validarFormCupom()) {
                e.preventDefault();
            }
        });
    }
}

function fecharModal() {
    const modal = document.getElementById('modalCupom');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Validação do formulário de cupom
function validarFormCupom() {
    const codigo = document.getElementById('codigoCupom');
    const desconto = document.getElementById('descontoCupom');
    const usos = document.getElementById('usosCupom');

    let isValid = true;

    // Validar código (mínimo 3 caracteres)
    if (codigo && codigo.value.length < 3) {
        mostrarErro(codigo, 'Código deve ter pelo menos 3 caracteres');
        isValid = false;
    } else {
        removerErro(codigo);
    }

    // Validar desconto (1-100%)
    if (desconto && (desconto.value < 1 || desconto.value > 100)) {
        mostrarErro(desconto, 'Desconto deve ser entre 1% e 100%');
        isValid = false;
    } else {
        removerErro(desconto);
    }

    // Validar usos (mínimo 1)
    if (usos && usos.value < 1) {
        mostrarErro(usos, 'Usos máximos deve ser pelo menos 1');
        isValid = false;
    } else {
        removerErro(usos);
    }

    return isValid;
}

function mostrarErro(campo, mensagem) {
    removerErro(campo);
    campo.classList.add('input-error');
    
    let errorElement = campo.parentNode.querySelector('.field-error');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'field-error';
        campo.parentNode.appendChild(errorElement);
    }
    errorElement.textContent = mensagem;
}

function removerErro(campo) {
    campo.classList.remove('input-error');
    const errorElement = campo.parentNode.querySelector('.field-error');
    if (errorElement) {
        errorElement.remove();
    }
}

// Inicializar form
function initCuponsForm() {
    // Adicionar estilos para erros (se não existirem no CSS)
    if (!document.querySelector('#cupons-error-styles')) {
        const style = document.createElement('style');
        style.id = 'cupons-error-styles';
        style.textContent = `
            .input-error {
                border-color: #f44336 !important;
                box-shadow: 0 0 0 3px rgba(244, 67, 54, 0.1) !important;
            }
            .field-error {
                color: #f44336;
                font-size: 0.8rem;
                margin-top: 0.25rem;
                padding: 0.25rem 0.5rem;
                background: rgba(244, 67, 54, 0.1);
                border-radius: var(--borda-radius-sm);
                border: 1px solid rgba(244, 67, 54, 0.2);
            }
        `;
        document.head.appendChild(style);
    }
}

// Animações específicas
function initCuponsAnimations() {
    // Delay para as linhas da tabela
    const tableRows = document.querySelectorAll('#tbodyCupons tr.fade-in');
    
    tableRows.forEach((row, index) => {
        row.style.animationDelay = `${index * 0.05}s`;
    });
}

// Otimizações de performance
function initCuponsPerformance() {
    // Debounce para eventos
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

    // Otimizar redimensionamento
    window.addEventListener('resize', debounce(() => {
        initCuponsAnimations();
    }, 250));
}

// Funções utilitárias globais (para uso em outros lugares)
window.cuponsUtils = {
    abrirModal: () => {
        const modal = document.getElementById('modalCupom');
        if (modal) modal.style.display = 'flex';
    },
    fecharModal: () => {
        const modal = document.getElementById('modalCupom');
        if (modal) modal.style.display = 'none';
    },
    validarCodigoCupom: (codigo) => {
        return /^[A-Z0-9]{3,20}$/.test(codigo);
    }
};

// Tratamento de erros
window.addEventListener('error', function(e) {
    console.error('Erro na gestão de cupons:', e.error);
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Promise rejeitada na gestão de cupons:', e.reason);
});