// ===== FUNÇÕES ESPECÍFICAS PARA EDIÇÃO DE PRODUTOS COM COMPRESSÃO =====

// Função de compressão de imagens (igual à do produtos.js)
function compressImage(file, maxWidth = 800, maxHeight = 600, quality = 0.7) {
    return new Promise((resolve, reject) => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();
        
        img.onload = function() {
            // Calcula novas dimensões mantendo proporção
            let width = img.width;
            let height = img.height;
            
            if (width > maxWidth || height > maxHeight) {
                const ratio = Math.min(maxWidth / width, maxHeight / height);
                width = Math.round(width * ratio);
                height = Math.round(height * ratio);
            }
            
            canvas.width = width;
            canvas.height = height;
            
            // Configura qualidade da renderização
            ctx.imageSmoothingEnabled = true;
            ctx.imageSmoothingQuality = 'high';
            
            // Desenha imagem comprimida
            ctx.drawImage(img, 0, 0, width, height);
            
            // Converte para Base64 com qualidade reduzida
            const base64 = canvas.toDataURL('image/jpeg', quality);
            
            resolve({
                base64: base64,
                width: width,
                height: height,
                originalSize: file.size,
                compressedSize: Math.round((base64.length * 3) / 4),
                compressionRatio: Math.round((1 - (base64.length * 3) / (4 * file.size)) * 100)
            });
        };
        
        img.onerror = function() {
            reject(new Error('Erro ao carregar imagem'));
        };
        
        img.src = URL.createObjectURL(file);
    });
}

// Função para detectar tipo de imagem e otimizar compressão
function getOptimalCompressionSettings(file) {
    const settings = {
        maxWidth: 800,
        maxHeight: 600,
        quality: 0.7
    };
    
    // Ajusta configurações baseado no tipo e tamanho da imagem
    if (file.type === 'image/png') {
        settings.quality = 0.8;
    } else if (file.type === 'image/jpeg') {
        settings.quality = 0.7;
    }
    
    // Ajusta qualidade baseado no tamanho original
    if (file.size > 2 * 1024 * 1024) {
        settings.quality = 0.6;
        settings.maxWidth = 600;
        settings.maxHeight = 400;
    } else if (file.size > 1 * 1024 * 1024) {
        settings.quality = 0.7;
    }
    
    return settings;
}

// Gerenciar upload de imagem e preview
function initImageUpload() {
    const fileInput = document.getElementById('imagemProdutoFile');
    const urlInput = document.getElementById('imagemProdutoUrl');
    const base64Input = document.getElementById('imagemBase64');
    const preview = document.getElementById('imagePreview');

    // Quando selecionar uma imagem no campo de arquivo
    if (fileInput) {
        fileInput.addEventListener('change', async function(e) {
            const file = e.target.files[0];
            
            if (file) {
                // Verifica se é uma imagem
                if (!file.type.startsWith('image/')) {
                    showNotification('Por favor, selecione apenas imagens!', 'error');
                    this.value = '';
                    return;
                }
                
                try {
                    // Mostra preview da imagem
                    preview.src = URL.createObjectURL(file);
                    preview.style.display = 'block';
                    
                    // Obtém configurações ótimas de compressão
                    const settings = getOptimalCompressionSettings(file);
                    
                    // Mostra indicador de processamento
                    showNotification('Comprimindo imagem...', 'info');
                    
                    // Comprime a imagem
                    const result = await compressImage(file, settings.maxWidth, settings.maxHeight, settings.quality);
                    
                    // Salva no campo hidden
                    base64Input.value = result.base64;
                    
                    // Limpa o campo URL para evitar conflito
                    urlInput.value = '';
                    
                    console.log(`Imagem comprimida: ${result.originalSize} → ${result.compressedSize} bytes (${result.compressionRatio}% redução)`);
                    showNotification(`Imagem comprimida com sucesso! (${result.compressionRatio}% menor)`, 'success');
                    
                } catch (error) {
                    console.error('Erro ao processar imagem:', error);
                    showNotification('Erro ao processar a imagem', 'error');
                }
            }
        });
    }

    // Se o usuário preencher o campo URL, limpa o Base64
    if (urlInput) {
        urlInput.addEventListener('input', function() {
            if (this.value) {
                base64Input.value = '';
                if (fileInput) fileInput.value = '';
                
                // Atualiza o preview se for uma URL válida
                if (this.value.startsWith('http')) {
                    preview.src = this.value;
                    preview.style.display = 'block';
                } else if (this.value === '') {
                    preview.style.display = 'none';
                }
            }
        });
    }
}

// Configurar preview inicial baseado na imagem atual
function setupInitialPreview() {
    const imagemAtual = document.getElementById('imagemProdutoUrl')?.value || '';
    const preview = document.getElementById('imagePreview');
    const base64Input = document.getElementById('imagemBase64');
    
    if (imagemAtual && imagemAtual.startsWith('data:image')) {
        // Se a imagem atual é Base64, garante que o campo URL esteja vazio
        document.getElementById('imagemProdutoUrl').value = '';
        preview.src = imagemAtual;
        preview.style.display = 'block';
    } else if (imagemAtual && imagemAtual.startsWith('http')) {
        // Se é URL, mostra no preview
        preview.src = imagemAtual;
        preview.style.display = 'block';
    }
    
    // Se já tem Base64 (em caso de edição), mantém o valor
    if (!base64Input.value && imagemAtual.startsWith('data:image')) {
        base64Input.value = imagemAtual;
    }
}

// Validação de formulário de produtos
function initAdminFormValidation() {
    const forms = document.querySelectorAll('.admin-form');
    
    forms.forEach(form => {
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
                
                // Validação específica para preço
                if (input.type === 'number' && input.name === 'preco' && input.value) {
                    const price = parseFloat(input.value);
                    if (price < 0) {
                        showFormError(input, 'O preço não pode ser negativo');
                        isValid = false;
                    }
                }
                
                // Validação específica para estoque
                if (input.type === 'number' && input.name === 'estoque' && input.value) {
                    const estoque = parseInt(input.value);
                    if (estoque < 0) {
                        showFormError(input, 'O estoque não pode ser negativo');
                        isValid = false;
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Por favor, preencha todos os campos obrigatórios corretamente.', 'error');
            }
        });
    });
}

// Mostrar erro no formulário
function showFormError(input, message) {
    clearFormError(input);
    
    const errorElement = document.createElement('div');
    errorElement.className = 'form-error';
    errorElement.textContent = message;
    
    input.style.borderColor = '#ff6b6b';
    input.parentNode.appendChild(errorElement);
}

// Limpar erro do formulário
function clearFormError(input) {
    const existingError = input.parentNode.querySelector('.form-error');
    if (existingError) {
        existingError.remove();
    }
    input.style.borderColor = '';
}

// Notificações para ações admin
function showNotification(message, type = 'success') {
    // Remove notificação existente
    const existingNotification = document.querySelector('.admin-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = `admin-notification admin-notification-${type}`;
    
    const icons = {
        success: 'check',
        error: 'exclamation',
        info: 'info',
        warning: 'exclamation-triangle'
    };
    
    notification.innerHTML = `
        <i class="fas fa-${icons[type] || 'info'}"></i>
        <span>${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Adicionar animação de entrada
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // Remover após 5 segundos
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 5000);
}

// Inicializar todas as funcionalidades quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    initAdminFormValidation();
    initImageUpload();
    setupInitialPreview();
    
    // Adicionar classe para página admin no body
    if (window.location.pathname.includes('editar_produto') || 
        window.location.pathname.includes('produtos')) {
        document.body.classList.add('admin-page');
    }
    
    console.log('Funcionalidades de edição de produto inicializadas!');
});