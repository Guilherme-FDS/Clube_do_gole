// ==========================
// GERENCIAMENTO DE PRODUTOS
// ==========================

// Funções globais para o onclick do HTML
function abrirModal() {
    const modal = document.getElementById('modalProduto');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function fecharModal() {
    const modal = document.getElementById('modalProduto');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = '';
    }
}

document.addEventListener('DOMContentLoaded', function() {
    inicializarGerenciadorProdutos();
    inicializarUploadImagens(); // Nova inicialização
});

function inicializarGerenciadorProdutos() {
    const modal = document.getElementById('modalProduto');
    const formProduto = document.querySelector('#modalProduto form');

    // Fechar modal clicando fora
    if (modal) {
        modal.addEventListener('click', function(event) {
            if (event.target === modal) {
                fecharModal();
            }
        });
    }

    // Fechar modal com ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            fecharModal();
        }
    });

    // Validação do formulário
    if (formProduto) {
        formProduto.addEventListener('submit', validarFormulario);
    }

    // Inicializar animações
    inicializarAnimacoes();
}

// ==========================
// COMPRESSÃO DE IMAGENS - FUNÇÃO PRINCIPAL
// ==========================

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
                compressedSize: Math.round((base64.length * 3) / 4), // Estimativa tamanho Base64
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
        settings.quality = 0.8; // PNG mantém melhor qualidade
    } else if (file.type === 'image/jpeg') {
        settings.quality = 0.7;
    }
    
    // Ajusta qualidade baseado no tamanho original
    if (file.size > 2 * 1024 * 1024) { // > 2MB
        settings.quality = 0.6;
        settings.maxWidth = 600;
        settings.maxHeight = 400;
    } else if (file.size > 1 * 1024 * 1024) { // > 1MB
        settings.quality = 0.7;
    }
    
    return settings;
}

// ==========================
// UPLOAD E GERENCIAMENTO DE IMAGENS
// ==========================

function inicializarUploadImagens() {
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
                    mostrarNotificacao('Por favor, selecione apenas imagens!', 'error');
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
                    mostrarNotificacao('Comprimindo imagem...', 'info');
                    
                    // Comprime a imagem
                    const result = await compressImage(file, settings.maxWidth, settings.maxHeight, settings.quality);
                    
                    // Salva no campo hidden
                    base64Input.value = result.base64;
                    
                    // Limpa o campo URL para evitar conflito
                    if (urlInput) urlInput.value = '';
                    
                    console.log(`Imagem comprimida: ${result.originalSize} → ${result.compressedSize} bytes (${result.compressionRatio}% redução)`);
                    mostrarNotificacao(`Imagem comprimida com sucesso! (${result.compressionRatio}% menor)`, 'success');
                    
                } catch (error) {
                    console.error('Erro ao processar imagem:', error);
                    mostrarNotificacao('Erro ao processar a imagem', 'error');
                }
            }
        });
    }

    // Se o usuário preencher o campo URL, limpa o Base64
    if (urlInput) {
        urlInput.addEventListener('input', function() {
            if (this.value) {
                if (base64Input) base64Input.value = '';
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

// ==========================
// VALIDAÇÃO DO FORMULÁRIO
// ==========================

function validarFormulario(event) {
    event.preventDefault();
    
    const nome = document.getElementById('nomeProduto')?.value.trim();
    const tipo = document.getElementById('tipoProduto')?.value;
    const descricao = document.getElementById('descricaoProduto')?.value.trim();
    const preco = parseFloat(document.getElementById('precoProduto')?.value);
    const estoque = parseInt(document.getElementById('estoqueProduto')?.value);

    // Validações básicas
    let isValid = true;

    if (!nome) {
        mostrarErro('nomeProduto', 'Nome do produto é obrigatório');
        isValid = false;
    }

    if (!descricao) {
        mostrarErro('descricaoProduto', 'Descrição é obrigatória');
        isValid = false;
    }

    if (isNaN(preco) || preco <= 0) {
        mostrarErro('precoProduto', 'Preço deve ser um valor positivo');
        isValid = false;
    }

    if (isNaN(estoque) || estoque < 0) {
        mostrarErro('estoqueProduto', 'Estoque deve ser um número não negativo');
        isValid = false;
    }

    if (isValid) {
        // Se válido, enviar formulário
        this.submit();
    }
}

function mostrarErro(campoId, mensagem) {
    const campo = document.getElementById(campoId);
    if (!campo) return;
    
    const formGroup = campo.closest('.form-group');
    if (!formGroup) return;
    
    // Remove erros anteriores
    const erroAnterior = formGroup.querySelector('.mensagem-erro');
    if (erroAnterior) {
        erroAnterior.remove();
    }
    
    // Adiciona estilo de erro
    campo.style.borderColor = '#ff6b6b';
    
    // Cria mensagem de erro
    const mensagemErro = document.createElement('span');
    mensagemErro.className = 'mensagem-erro';
    mensagemErro.style.color = '#ff6b6b';
    mensagemErro.style.fontSize = '0.875rem';
    mensagemErro.style.marginTop = '0.25rem';
    mensagemErro.style.display = 'block';
    mensagemErro.textContent = mensagem;
    
    formGroup.appendChild(mensagemErro);
    
    // Foca no campo com erro
    campo.focus();
}

// ==========================
// ANIMAÇÕES
// ==========================

function inicializarAnimacoes() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
            }
        });
    }, observerOptions);

    // Observar elementos com fade-in
    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });
}

// ==========================
// NOTIFICAÇÕES
// ==========================

function mostrarNotificacao(message, type = 'success') {
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

// ==========================
// UTILITÁRIOS
// ==========================

function formatarPreco(preco) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(preco);
}