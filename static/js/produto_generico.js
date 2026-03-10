// produto_generico.js - Adicionar ao carrinho sem redirecionar
document.addEventListener('DOMContentLoaded', function() {
    console.log('🛒 Produto Generico JS carregado');
    
    // Variáveis globais
    let planoSelecionado = 'mensal';
    let quantidade = 1;

    // Inicializar eventos
    initEventos();
    initPlanoSelecionado();

    function initEventos() {
        // Eventos dos botões de quantidade
        document.querySelectorAll('.btn-quantidade').forEach(btn => {
            btn.addEventListener('click', function() {
                const operacao = this.querySelector('.fa-plus') ? 1 : -1;
                alterarQuantidade(operacao);
            });
        });

        // Eventos dos botões de plano
        document.querySelectorAll('.btn-plano').forEach(btn => {
            btn.addEventListener('click', function() {
                if (this.disabled) return;
                
                const plano = this.getAttribute('data-plano');
                selecionarPlano(plano);
                
                // Adicionar ao carrinho imediatamente
                adicionarAoCarrinho();
            });
        });

        // Input de quantidade - eventos para entrada manual
        const quantidadeInput = document.getElementById('quantidade_input');
        if (quantidadeInput) {
            // Evento quando o valor é alterado
            quantidadeInput.addEventListener('change', function() {
                quantidade = parseInt(this.value) || 1;
                validarQuantidade();
            });
            
            // Evento quando o usuário digita
            quantidadeInput.addEventListener('input', function() {
                // Atualiza a variável global em tempo real
                quantidade = parseInt(this.value) || 1;
            });
            
            // Prevenir entrada de valores não numéricos
            quantidadeInput.addEventListener('keypress', function(e) {
                const charCode = e.which ? e.which : e.keyCode;
                if (charCode > 31 && (charCode < 48 || charCode > 57)) {
                    e.preventDefault();
                    return false;
                }
                return true;
            });
            
            // Garantir que o valor seja válido ao perder o foco
            quantidadeInput.addEventListener('blur', function() {
                validarQuantidade();
            });
        }
    }

    function initPlanoSelecionado() {
        // Selecionar primeiro plano por padrão
        const primeiroPlano = document.querySelector('.btn-plano:not([disabled])');
        if (primeiroPlano) {
            const plano = primeiroPlano.getAttribute('data-plano');
            selecionarPlano(plano);
        }
    }

    function alterarQuantidade(operacao) {
        const input = document.getElementById('quantidade_input');
        if (!input) return;

        let novaQuantidade = parseInt(input.value) + operacao;
        const estoqueMax = parseInt(input.getAttribute('max')) || 999;

        // Validar limites
        if (novaQuantidade < 1) novaQuantidade = 1;
        if (novaQuantidade > estoqueMax) novaQuantidade = estoqueMax;

        input.value = novaQuantidade;
        quantidade = novaQuantidade;
        
        // Feedback visual
        input.classList.add('pulse');
        setTimeout(() => input.classList.remove('pulse'), 300);
    }

    function validarQuantidade() {
        const input = document.getElementById('quantidade_input');
        if (!input) return;
        
        const estoqueMax = parseInt(input.getAttribute('max')) || 999;
        const valorAtual = parseInt(input.value) || 1;

        // Validar limites
        if (valorAtual < 1) {
            input.value = 1;
            quantidade = 1;
        } else if (valorAtual > estoqueMax) {
            input.value = estoqueMax;
            quantidade = estoqueMax;
            
            // Mostrar mensagem se exceder estoque
            if (estoqueMax > 0) {
                mostrarMensagemErro(`Quantidade máxima disponível: ${estoqueMax} unidades`);
            }
        } else {
            quantidade = valorAtual;
        }
    }

    function selecionarPlano(plano) {
        planoSelecionado = plano;

        // Remover seleção anterior
        document.querySelectorAll('.plano-card').forEach(card => {
            card.classList.remove('selecionado');
        });

        // Adicionar seleção atual
        const cardSelecionado = document.querySelector(`.plano-card[data-plano="${plano}"]`);
        if (cardSelecionado) {
            cardSelecionado.classList.add('selecionado');
        }

        console.log(`📅 Plano selecionado: ${plano}`);
    }

    async function adicionarAoCarrinho() {
        const form = document.getElementById('form-carrinho');
        if (!form) {
            console.error('❌ Formulário não encontrado');
            return;
        }

        // Validar quantidade antes de enviar
        validarQuantidade();

        const botaoClicado = document.querySelector(`.btn-plano[data-plano="${planoSelecionado}"]`);
        if (!botaoClicado) {
            console.error('❌ Botão do plano não encontrado');
            return;
        }

        // Salvar estado original do botão
        const textoOriginal = botaoClicado.innerHTML;
        const estadoOriginal = botaoClicado.disabled;

        // Mostrar loading
        botaoClicado.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adicionando...';
        botaoClicado.disabled = true;

        try {
            // Criar FormData com todos os campos do formulário
            const formData = new FormData(form);
            formData.append('plano', planoSelecionado);
            formData.append('quantidade', quantidade.toString());

            console.log('📦 Enviando para carrinho:', {
                produto: formData.get('id_produto'),
                plano: planoSelecionado,
                quantidade: quantidade
            });

            // Fazer requisição AJAX
            const response = await fetch("/adicionar_carrinho", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                // ✅ Sucesso - mostrar mensagem
                mostrarMensagemSucesso(data.message);
                console.log(`✅ ${data.message} | Itens no carrinho: ${data.count}`);
                
                // Atualizar contador do carrinho no header
                atualizarContadorHeader(data.count);
                
            } else {
                // ❌ Erro - mostrar mensagem de erro
                mostrarMensagemErro(data.message);
                console.error('❌ Erro ao adicionar ao carrinho:', data.message);
            }

        } catch (error) {
            console.error('❌ Erro na requisição:', error);
            mostrarMensagemErro('Erro ao adicionar produto ao carrinho.');
        } finally {
            // Restaurar estado do botão
            botaoClicado.innerHTML = textoOriginal;
            botaoClicado.disabled = estadoOriginal;
        }
    }

    function mostrarMensagemSucesso(mensagem) {
        mostrarToast(mensagem, 'success');
    }

    function mostrarMensagemErro(mensagem) {
        mostrarToast(mensagem, 'error');
    }

    function mostrarToast(mensagem, tipo) {
        // Remover toasts existentes
        const toastsExistentes = document.querySelectorAll('.toast-message');
        toastsExistentes.forEach(toast => toast.remove());

        // Criar novo toast
        const toast = document.createElement('div');
        toast.className = `toast-message toast-${tipo}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas ${tipo === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                <span>${mensagem}</span>
                <button class="toast-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        // Adicionar ao container
        const container = document.getElementById('toast-container');
        if (container) {
            container.appendChild(toast);
        } else {
            // Criar container se não existir
            const newContainer = document.createElement('div');
            newContainer.id = 'toast-container';
            newContainer.appendChild(toast);
            document.body.appendChild(newContainer);
        }

        // Mostrar animação
        setTimeout(() => toast.classList.add('show'), 100);

        // Auto-remover após 5 segundos
        setTimeout(() => {
            if (toast.parentNode) {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }
        }, 5000);
    }

    function atualizarContadorHeader(count) {
        const cartCountElement = document.getElementById("cartCount");
        if (cartCountElement) {
            cartCountElement.textContent = count;
            
            // Animação
            cartCountElement.classList.add('pulse');
            setTimeout(() => {
                cartCountElement.classList.remove('pulse');
            }, 500);
        }
    }

    // Expor funções globais se necessário
    window.alterarQuantidade = alterarQuantidade;
});

// Função global para compatibilidade com onclick HTML
function alterarQuantidade(operacao) {
    const event = new Event('DOMContentLoaded');
    document.dispatchEvent(event);
}