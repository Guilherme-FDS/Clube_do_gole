// ===== FUNÇÕES ESPECÍFICAS PARA EDIÇÃO DE CUPONS =====

document.addEventListener('DOMContentLoaded', function() {
    initCupomFormValidation();
    initAutoUppercase();
    initUsosValidation();
});

// Validação do formulário de cupons
function initCupomFormValidation() {
    const form = document.querySelector('form');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            const inputs = this.querySelectorAll('input[required], select[required]');
            let isValid = true;
            
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    showFormError(input, 'Este campo é obrigatório');
                    isValid = false;
                } else {
                    clearFormError(input);
                }
                
                // Validação específica para desconto
                if (input.name === 'desconto_percentual' && input.value) {
                    const desconto = parseInt(input.value);
                    if (desconto < 1 || desconto > 100) {
                        showFormError(input, 'O desconto deve estar entre 1% e 100%');
                        isValid = false;
                    }
                }
                
                // Validação específica para usos máximos
                if (input.name === 'usos_maximos' && input.value) {
                    const usos = parseInt(input.value);
                    if (usos < 1) {
                        showFormError(input, 'Os usos máximos devem ser pelo menos 1');
                        isValid = false;
                    }
                }
                
                // Validação específica para código do cupom
                if (input.name === 'codigo' && input.value) {
                    const codigo = input.value.trim();
                    if (codigo.length < 3) {
                        showFormError(input, 'O código deve ter pelo menos 3 caracteres');
                        isValid = false;
                    }
                    
                    // Verifica se contém apenas letras, números e hífens
                    const regex = /^[A-Z0-9\-_]+$/;
                    if (!regex.test(codigo)) {
                        showFormError(input, 'O código deve conter apenas letras, números, hífens e underlines');
                        isValid = false;
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Por favor, corrija os erros no formulário antes de enviar.', 'error');
            } else {
                showNotification('Cupom atualizado com sucesso!', 'success');
            }
        });
    }
}

// Auto uppercase no código do cupom
function initAutoUppercase() {
    const codigoInput = document.getElementById('codigoCupom');
    
    if (codigoInput) {
        codigoInput.addEventListener('input', function(e) {
            e.target.value = e.target.value.toUpperCase();
        });
        
        // Também aplica ao carregar a página
        codigoInput.value = codigoInput.value.toUpperCase();
    }
}

// Validação inteligente de usos
function initUsosValidation() {
    const usosInput = document.getElementById('usosCupom');
    
    if (usosInput) {
        usosInput.addEventListener('change', function() {
            const novosUsos = parseInt(this.value);
            const usosAtuais = parseInt('{{ cupom.usos_restantes }}');
            
            if (novosUsos < usosAtuais) {
                showNotification(`Atenção: Os usos máximos (${novosUsos}) são menores que os usos restantes atuais (${usosAtuais}).`, 'error');
            }
        });
    }
}

// Mostrar erro no formulário
function showFormError(input, message) {
    clearFormError(input);
    
    const errorElement = document.createElement('div');
    errorElement.className = 'form-error';
    errorElement.textContent = message;
    
    input.classList.add('invalid');
    input.parentNode.appendChild(errorElement);
}

// Limpar erro do formulário
function clearFormError(input) {
    const existingError = input.parentNode.querySelector('.form-error');
    if (existingError) {
        existingError.remove();
    }
    input.classList.remove('invalid');
}

// Notificações para ações com cupons
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `cupom-notification cupom-notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check' : 'exclamation'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Remover após 5 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Preview de alterações em tempo real
function initRealTimePreview() {
    const codigoInput = document.getElementById('codigoCupom');
    const descontoInput = document.getElementById('descontoCupom');
    
    if (codigoInput && descontoInput) {
        const updatePreview = () => {
            console.log('Alterações preview:', {
                codigo: codigoInput.value,
                desconto: descontoInput.value
            });
        };
        
        codigoInput.addEventListener('input', updatePreview);
        descontoInput.addEventListener('input', updatePreview);
    }
}

// Confirmação antes de sair da página com alterações não salvas
function initUnsavedChangesWarning() {
    let formChanged = false;
    const form = document.querySelector('form');
    const initialData = new FormData(form);
    
    form.addEventListener('input', () => {
        formChanged = true;
    });
    
    window.addEventListener('beforeunload', (e) => {
        if (formChanged) {
            e.preventDefault();
            e.returnValue = 'Você tem alterações não salvas. Tem certeza que deseja sair?';
        }
    });
    
    // Remove o aviso quando o formulário é enviado
    form.addEventListener('submit', () => {
        formChanged = false;
    });
}

// Inicializar todas as funcionalidades
document.addEventListener('DOMContentLoaded', function() {
    initCupomFormValidation();
    initAutoUppercase();
    initUsosValidation();
    initRealTimePreview();
    initUnsavedChangesWarning();
});