// carrinho.js - Funcionalidades do carrinho de compras - ATUALIZADO COM INPUT MANUAL

class CarrinhoManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.atualizarContadorCarrinho();
        this.setupAutoRefresh();
        this.setupAddToCartButtons();
        this.setupQuantidadeInputs(); // ← NOVA LINHA ADICIONADA
        console.log('✅ CarrinhoManager inicializado - INPUT MANUAL HABILITADO');
    }

    setupEventListeners() {
        // Event listener para verificar se há itens selecionados antes de excluir
        const formExcluir = document.querySelector('button[formaction*="excluir_item_carrinho"]');
        if (formExcluir) {
            formExcluir.addEventListener('click', (e) => {
                const checkboxes = document.querySelectorAll('input[name="selecionar_item"]:checked');
                if (checkboxes.length === 0) {
                    e.preventDefault();
                    this.mostrarMensagem('Por favor, selecione pelo menos um item para excluir.', 'error');
                }
            });
        }
    }

    // NOVO MÉTODO ADICIONADO
    setupQuantidadeInputs() {
        document.querySelectorAll('.quantidade-input').forEach(input => {
            // Prevenir entrada de valores não numéricos
            input.addEventListener('keypress', function(e) {
                const charCode = e.which ? e.which : e.keyCode;
                if (charCode > 31 && (charCode < 48 || charCode > 57)) {
                    e.preventDefault();
                    return false;
                }
                return true;
            });

            // Validar ao perder o foco
            input.addEventListener('blur', function() {
                const itemId = this.id.replace('quantidade-', '');
                const valor = this.value;
                
                if (valor === '' || parseInt(valor) < 1) {
                    this.value = this.getAttribute('data-valor-anterior') || '1';
                    window.carrinhoManager.mostrarMensagem('Quantidade deve ser maior que zero.', 'error');
                }
            });

            // Salvar valor inicial como backup
            input.setAttribute('data-valor-anterior', input.value);
        });
    }

    setupAddToCartButtons() {
        const addToCartButtons = document.querySelectorAll('[id^="adicionarCarrinho"], .btn-adicionar-carrinho, button[onclick*="adicionarCarrinho"]');

        addToCartButtons.forEach(button => {
            button.replaceWith(button.cloneNode(true));
        });

        const refreshedButtons = document.querySelectorAll('[id^="adicionarCarrinho"], .btn-adicionar-carrinho, button[onclick*="adicionarCarrinho"]');

        refreshedButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleAddToCart(button);
            });
        });

        console.log(`🛒 ${refreshedButtons.length} botões de adicionar ao carrinho configurados`);
    }

    async handleAddToCart(button) {
        const form = button.closest('form');
        if (!form) {
            console.error('❌ Formulário não encontrado para o botão');
            return;
        }

        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Adicionando...';
        button.disabled = true;

        try {
            const formData = new FormData(form);

            const response = await fetch("/adicionar_carrinho", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (data.success) {
                this.atualizarContadorCarrinho();
                this.mostrarMensagemProduto(data.message, 'success', button);
                console.log(`✅ ${data.message} | Itens no carrinho: ${data.count}`);
            } else {
                this.mostrarMensagemProduto(data.message, 'error', button);
                console.error('❌ Erro ao adicionar ao carrinho:', data.message);
            }
        } catch (error) {
            console.error('❌ Erro na requisição:', error);
            this.mostrarMensagemProduto('Erro ao adicionar produto ao carrinho.', 'error', button);
        } finally {
            button.innerHTML = originalText;
            button.disabled = false;
        }
    }

    mostrarMensagemProduto(mensagem, tipo, elementoReferencia) {
        const existingMessages = document.querySelectorAll('.produto-mensagem');
        existingMessages.forEach(msg => msg.remove());

        const messageElement = document.createElement('div');
        messageElement.className = `produto-mensagem ${tipo}`;
        messageElement.innerHTML = `
            <div class="mensagem-conteudo">
                <i class="fas ${tipo === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
                <span>${mensagem}</span>
                <button class="fechar-mensagem" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        document.body.appendChild(messageElement);

        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.remove();
            }
        }, 5000);
    }

    async abrirCheckout() {
        const checkboxes = document.querySelectorAll('input[name="selecionar_item"]:checked');
        if (checkboxes.length === 0) {
            this.mostrarMensagem('Por favor, selecione pelo menos um item para finalizar a compra.', 'error');
            return;
        }

        const selectedItems = Array.from(checkboxes).map(checkbox => checkbox.value);

        console.log("🛒 Itens selecionados para checkout:", selectedItems);

        localStorage.setItem('checkoutItems', JSON.stringify(selectedItems));

        try {
            const response = await fetch('/carrinho/contador');
            const data = await response.json();

            if (data.is_guest) {
                this.mostrarMensagem('Faça login para finalizar a compra! Use o botão "Fazer Login" acima.', 'info');

                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });

                console.log('👤 Usuário deslogado - Mostrando mensagem de login');
            } else {
                console.log('👤 Usuário logado - Redirecionando para checkout');
                window.location.href = "/checkout";
            }
        } catch (error) {
            console.error('Erro ao verificar status:', error);
            window.location.href = "/checkout";
        }
    }

    // MÉTODOS ATUALIZADOS PARA INPUT MANUAL
    async aumentarQuantidade(itemId) {
        const input = document.getElementById(`quantidade-${itemId}`);
        const novaQuantidade = parseInt(input.value) + 1;
        input.value = novaQuantidade;
        await this.atualizarQuantidadeNoServidor(itemId, novaQuantidade);
    }

    async diminuirQuantidade(itemId) {
        const input = document.getElementById(`quantidade-${itemId}`);
        const novaQuantidade = parseInt(input.value) - 1;

        if (novaQuantidade < 1) {
            this.mostrarMensagem('Quantidade deve ser maior que zero.', 'error');
            return;
        }

        input.value = novaQuantidade;
        await this.atualizarQuantidadeNoServidor(itemId, novaQuantidade);
    }

    // NOVO MÉTODO PARA ATUALIZAÇÃO MANUAL
    async atualizarQuantidadeManual(itemId, novaQuantidade) {
        // Validar quantidade
        const quantidadeNum = parseInt(novaQuantidade);
        if (isNaN(quantidadeNum) || quantidadeNum < 1) {
            this.mostrarMensagem('Quantidade deve ser maior que zero.', 'error');
            
            // Restaurar valor anterior
            const input = document.getElementById(`quantidade-${itemId}`);
            const valorAnterior = input.getAttribute('data-valor-anterior') || '1';
            input.value = valorAnterior;
            return;
        }

        await this.atualizarQuantidadeNoServidor(itemId, quantidadeNum);
    }

    // MÉTODO ATUALIZADO COM ANIMAÇÃO E ROLLBACK
    async atualizarQuantidadeNoServidor(itemId, novaQuantidade) {
        try {
            const input = document.getElementById(`quantidade-${itemId}`);
            
            // Salvar valor atual para possível rollback
            input.setAttribute('data-valor-anterior', input.value);
            
            // Animação de feedback
            input.classList.add('pulse');
            setTimeout(() => input.classList.remove('pulse'), 300);

            const formData = new FormData();
            formData.append('item_id', itemId);
            formData.append('quantidade', novaQuantidade);

            const response = await fetch("/atualizar_quantidade", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (data.success) {
                // Atualizar totais
                document.getElementById(`total-${itemId}`).textContent = data.novo_total_item;
                document.getElementById('total-carrinho').innerHTML =
                    `<span class="total-label">💰 Total do Carrinho:</span>
                     <span class="total-valor">${data.total_carrinho}</span>`;

                this.atualizarContadorCarrinho();
                this.mostrarMensagem('Quantidade atualizada com sucesso!', 'success');
            } else {
                this.mostrarMensagem(data.message, 'error');
                // Rollback em caso de erro
                const valorAnterior = input.getAttribute('data-valor-anterior');
                if (valorAnterior) {
                    input.value = valorAnterior;
                }
            }
        } catch (error) {
            console.error('Erro ao atualizar quantidade:', error);
            this.mostrarMensagem('Erro ao atualizar quantidade.', 'error');
            
            // Rollback em caso de erro
            const input = document.getElementById(`quantidade-${itemId}`);
            const valorAnterior = input.getAttribute('data-valor-anterior');
            if (valorAnterior) {
                input.value = valorAnterior;
            }
        }
    }

    async excluirItem(itemId) {
        if (!confirm('Tem certeza que deseja remover este item do carrinho?')) {
            return;
        }

        try {
            const formData = new FormData();
            formData.append('item_id', itemId);

            const response = await fetch("/excluir_item_carrinho", {
                method: "POST",
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            const data = await response.json();

            if (data.success) {
                document.getElementById(`item-${itemId}`).remove();
                document.getElementById('total-carrinho').innerHTML =
                    `<span class="total-label">💰 Total do Carrinho:</span>
                 <span class="total-valor">${data.total_carrinho}</span>`;

                this.atualizarContadorCarrinho();
                this.mostrarMensagem(data.message, 'success');

                // Verificar se o carrinho ficou vazio
                const itensRestantes = document.querySelectorAll('.cart-item');
                if (itensRestantes.length === 0) {
                    setTimeout(() => {
                        location.reload();
                    }, 1500);
                }
            } else {
                this.mostrarMensagem(data.message, 'error');
            }
        } catch (error) {
            console.error('Erro ao excluir item:', error);
            this.mostrarMensagem('Erro ao excluir item.', 'error');
        }
    }

    // Funções mantidas para compatibilidade (caso ainda sejam usadas em outros lugares)
    editarQuantidade(itemId) {
        document.getElementById(`quantidade-${itemId}`).style.display = 'none';
        document.getElementById(`editar-${itemId}`).style.display = 'flex';
        document.getElementById(`item-${itemId}`).classList.add('editando');

        setTimeout(() => {
            document.getElementById(`input-${itemId}`).focus();
        }, 100);
    }

    cancelarEdicao(itemId) {
        document.getElementById(`quantidade-${itemId}`).style.display = 'inline';
        document.getElementById(`editar-${itemId}`).style.display = 'none';
        document.getElementById(`item-${itemId}`).classList.remove('editando');
    }

    async salvarQuantidade(itemId) {
        const novaQuantidade = document.getElementById(`input-${itemId}`).value;

        if (novaQuantidade < 1) {
            this.mostrarMensagem('Quantidade deve ser maior que zero.', 'error');
            return;
        }

        try {
            const formData = new FormData();
            formData.append('item_id', itemId);
            formData.append('quantidade', novaQuantidade);

            const response = await fetch("/atualizar_quantidade", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();

            if (data.success) {
                document.getElementById(`quantidade-${itemId}`).textContent = novaQuantidade;
                document.getElementById(`total-${itemId}`).textContent = data.novo_total_item;
                document.getElementById('total-carrinho').innerHTML =
                    `<span class="total-label">💰 Total do Carrinho:</span>
                     <span class="total-valor">${data.total_carrinho}</span>`;

                this.cancelarEdicao(itemId);
                this.atualizarContadorCarrinho();
                this.mostrarMensagem(data.message, 'success');
            } else {
                this.mostrarMensagem(data.message, 'error');
            }
        } catch (error) {
            console.error('Erro ao atualizar quantidade:', error);
            this.mostrarMensagem('Erro ao atualizar quantidade.', 'error');
        }
    }

    async atualizarContadorCarrinho() {
        try {
            const response = await fetch("/carrinho/contador");
            const data = await response.json();
            const cartCountElement = document.getElementById("cartCount");
            if (cartCountElement) {
                cartCountElement.textContent = data.count;

                if (data.count > 0) {
                    cartCountElement.classList.add('pulse');
                    setTimeout(() => {
                        cartCountElement.classList.remove('pulse');
                    }, 500);
                }
            }
        } catch (error) {
            console.error("Erro ao atualizar contador:", error);
        }
    }

    setupAutoRefresh() {
        setInterval(() => {
            this.atualizarContadorCarrinho();
        }, 15000);
    }

    mostrarMensagem(mensagem, tipo) {
        const existingMessage = document.querySelector('.acao-mensagem');
        if (existingMessage) {
            existingMessage.remove();
        }

        const messageElement = document.createElement('div');
        messageElement.className = `acao-mensagem ${tipo}`;
        messageElement.textContent = mensagem;

        const cartContainer = document.querySelector('.cart-container');
        const firstChild = cartContainer.firstChild;
        cartContainer.insertBefore(messageElement, firstChild);

        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.remove();
            }
        }, 5000);
    }
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 Carrinho.js carregado - INPUT MANUAL HABILITADO');

    window.carrinhoManager = new CarrinhoManager();

    // Expor funções globais para o HTML
    window.abrirCheckout = () => window.carrinhoManager.abrirCheckout();
    window.aumentarQuantidade = (itemId) => window.carrinhoManager.aumentarQuantidade(itemId);
    window.diminuirQuantidade = (itemId) => window.carrinhoManager.diminuirQuantidade(itemId);
    window.excluirItem = (itemId) => window.carrinhoManager.excluirItem(itemId);
    window.editarQuantidade = (itemId) => window.carrinhoManager.editarQuantidade(itemId);
    window.cancelarEdicao = (itemId) => window.carrinhoManager.cancelarEdicao(itemId);
    window.salvarQuantidade = (itemId) => window.carrinhoManager.salvarQuantidade(itemId);
    window.adicionarAoCarrinho = (botao) => window.carrinhoManager.handleAddToCart(botao);
    window.atualizarQuantidadeManual = (itemId, valor) => window.carrinhoManager.atualizarQuantidadeManual(itemId, valor); // ← NOVA FUNÇÃO
});