// checkout.js - Versão Corrigida

// Variáveis globais
let enderecoEditando = null;
let enderecosUsuario = [];

document.addEventListener("DOMContentLoaded", () => {
    console.log("🔄 Inicializando checkout...");
    
    // Elementos DOM
    const orderItems = document.getElementById("orderItems");
    const subtotalElement = document.getElementById("subtotal");
    const totalAmountElement = document.getElementById("totalAmount");
    const paymentMethods = document.querySelectorAll('input[name="payment"]');
    const cardData = document.getElementById("cardData");
    const confirmPaymentBtn = document.getElementById("confirmPayment");
    const confirmPaymentText = document.getElementById("confirmPaymentText");
    const applyCouponBtn = document.getElementById("applyCoupon");
    const couponCodeInput = document.getElementById("couponCode");
    const discountLine = document.getElementById("discountLine");
    const discountValue = document.getElementById("discountValue");
    const enderecosContainer = document.getElementById("enderecosContainer");
    const emptyAddress = document.getElementById("emptyAddress");

    let cartItems = [];
    let discount = 0;
    let cupomAplicado = null;
    let enderecoSelecionado = null;

    // Carregar dados iniciais
    async function inicializarCheckout() {
        console.log("🚀 Inicializando checkout...");
        await loadSelectedCartItems();
        await carregarEnderecosUsuario();
        inicializarEventos();
        inicializarModalEndereco();
    }

    // Carregar itens selecionados do carrinho
    async function loadSelectedCartItems() {
        try {
            const selectedItems = JSON.parse(localStorage.getItem('checkoutItems') || '[]');
            
            console.log("🔍 Itens selecionados do localStorage:", selectedItems);

            if (selectedItems.length === 0) {
                showError("Nenhum item selecionado para checkout. Redirecionando para o carrinho...");
                setTimeout(() => window.location.href = '/carrinho', 2000);
                return;
            }

            const response = await fetch("/api/carrinho/itens_selecionados", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    itens_selecionados: selectedItems
                })
            });
            
            const data = await response.json();
            
            console.log("📦 Itens carregados da API:", data.itens);

            if (data.itens && data.itens.length > 0) {
                cartItems = data.itens;
                updateOrderSummary();
                showSuccess(`${cartItems.length} item(s) carregado(s) com sucesso!`);
            } else {
                showError("Itens selecionados não encontrados no carrinho. Redirecionando...");
                setTimeout(() => window.location.href = '/carrinho', 2000);
            }
        } catch (error) {
            console.error('Erro ao carregar itens selecionados:', error);
            showError("Erro ao carregar itens do carrinho. Tente novamente.");
        }
    }

    // Carregar endereços do usuário - CORRIGIDO
    async function carregarEnderecosUsuario() {
        try {
            console.log("🔄 Carregando endereços do usuário...");
            
            const response = await fetch("/api/enderecos");
            
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            
            const data = await response.json();
            console.log("📬 Dados recebidos da API:", data);
            
            if (data.enderecos && data.enderecos.length > 0) {
                enderecosUsuario = data.enderecos;
                console.log(`✅ ${enderecosUsuario.length} endereço(s) carregado(s):`, enderecosUsuario);
                renderizarEnderecos();
                showSuccess(`${enderecosUsuario.length} endereço(s) carregado(s)!`);
            } else {
                console.log("📭 Nenhum endereço encontrado");
                mostrarEnderecoVazio();
                showError("Nenhum endereço cadastrado. Por favor, adicione um endereço para continuar.");
            }
        } catch (error) {
            console.error('❌ Erro ao carregar endereços:', error);
            mostrarEnderecoVazio();
            showError("Erro ao carregar endereços. Tente novamente.");
        }
    }

    // Mostrar estado vazio de endereços
    function mostrarEnderecoVazio() {
        if (emptyAddress) {
            emptyAddress.style.display = 'block';
            if (enderecosContainer) {
                enderecosContainer.innerHTML = '';
                enderecosContainer.appendChild(emptyAddress);
            }
        }
        atualizarEstadoBotaoPagamento();
    }

    // Renderizar endereços na tela - CORRIGIDO
    function renderizarEnderecos() {
        console.log("🎨 Renderizando endereços...");
        if (!enderecosContainer) return;
        
        enderecosContainer.innerHTML = '';
        
        if (enderecosUsuario.length === 0) {
            mostrarEnderecoVazio();
            return;
        }
        
        if (emptyAddress) emptyAddress.style.display = 'none';
        
        enderecosUsuario.forEach((endereco, index) => {
            const addressCard = document.createElement('div');
            addressCard.className = `endereco-card ${endereco.principal === 'sim' ? 'principal' : ''}`;
            addressCard.dataset.enderecoId = endereco.id;
            
            addressCard.innerHTML = `
                <div class="endereco-header">
                    <h3>${endereco.principal === 'sim' ? 'Endereço Principal' : `Endereço ${index + 1}`}</h3>
                    ${endereco.principal === 'sim' ? '<span class="badge-principal">Principal</span>' : ''}
                </div>
                <div class="endereco-info">
                    <p><strong>${endereco.endereco}, ${endereco.numero}</strong></p>
                    ${endereco.complemento ? `<p>Complemento: ${endereco.complemento}</p>` : ''}
                    <p>${endereco.bairro} - ${endereco.cidade}/${endereco.estado}</p>
                    <p>CEP: ${endereco.cep}</p>
                </div>
                <div class="endereco-actions">
                    <button type="button" class="btn-edit" onclick="editarEnderecoCheckout('${endereco.id}')">
                        <i class="fas fa-edit"></i>
                        Editar
                    </button>
                    ${endereco.principal !== 'sim' ? `
                        <button type="button" class="btn-set-primary" onclick="definirComoPrincipalCheckout('${endereco.id}')">
                            <i class="fas fa-star"></i>
                            Tornar Principal
                        </button>
                    ` : ''}
                    ${enderecosUsuario.length > 1 ? `
                        <button type="button" class="btn-delete" onclick="excluirEnderecoCheckout('${endereco.id}')">
                            <i class="fas fa-trash"></i>
                            Excluir
                        </button>
                    ` : ''}
                </div>
            `;
            
            // Adicionar checkbox de seleção para entrega
            const checkboxContainer = document.createElement('div');
            checkboxContainer.className = 'endereco-selecao';
            checkboxContainer.innerHTML = `
                <label class="checkbox-label">
                    <input type="radio" name="endereco_entrega" value="${endereco.id}" 
                           ${endereco.principal === 'sim' ? 'checked' : ''}
                           onchange="selecionarEnderecoCheckout('${endereco.id}')">
                    <span class="checkmark"></span>
                    Usar este endereço para entrega
                </label>
            `;
            
            addressCard.appendChild(checkboxContainer);
            
            // Adicionar evento de clique para seleção
            addressCard.addEventListener('click', (e) => {
                // Não selecionar se clicar nos botões de ação
                if (!e.target.closest('.endereco-actions') && !e.target.closest('.endereco-selecao')) {
                    const radio = addressCard.querySelector('input[type="radio"]');
                    if (radio) {
                        radio.checked = true;
                        selecionarEnderecoCheckout(endereco.id);
                    }
                }
            });
            
            enderecosContainer.appendChild(addressCard);
        });
        
        // Selecionar automaticamente o endereço principal
        const enderecoPrincipal = enderecosUsuario.find(e => e.principal === 'sim');
        if (enderecoPrincipal) {
            selecionarEnderecoCheckout(enderecoPrincipal.id);
        } else if (enderecosUsuario.length > 0) {
            // Se não tem principal, selecionar o primeiro
            selecionarEnderecoCheckout(enderecosUsuario[0].id);
        }
    }

    // Inicializar eventos
    function inicializarEventos() {
        console.log("🎯 Inicializando eventos...");
        
        // Alternar dados do cartão
        if (paymentMethods.length > 0) {
            paymentMethods.forEach(method => {
                method.addEventListener('change', (e) => {
                    if (e.target.value === 'cartao' && cardData) {
                        cardData.style.display = 'block';
                        cardData.style.animation = 'slideDown 0.3s ease-out';
                    } else if (cardData) {
                        cardData.style.display = 'none';
                    }
                });
            });
        }

        // Aplicar cupom de desconto
        if (applyCouponBtn) {
            applyCouponBtn.addEventListener('click', aplicarCupomDesconto);
        }

        // Confirmar pagamento
        if (confirmPaymentBtn) {
            confirmPaymentBtn.addEventListener('click', processarPagamento);
        }

        // Formatação de inputs do cartão
        inicializarMascarasCartao();
    }

    // Inicializar modal de endereço
    function inicializarModalEndereco() {
        console.log("🏠 Inicializando modal de endereço...");
        
        // Máscara para CEP
        const cepInput = document.getElementById('cep');
        if (cepInput) {
            cepInput.addEventListener('input', function(e) {
                let value = e.target.value.replace(/\D/g, '');
                
                if (value.length <= 8) {
                    value = value.replace(/(\d{5})(\d)/, '$1-$2');
                    e.target.value = value;
                }
            });
        }

        // Submit do formulário de endereço
        const enderecoForm = document.getElementById('enderecoForm');
        if (enderecoForm) {
            enderecoForm.addEventListener('submit', salvarEndereco);
        }

        // Botão de fechar modal
        const closeBtn = document.querySelector('.close-modal');
        if (closeBtn) {
            closeBtn.addEventListener('click', fecharModalEndereco);
        }

        // Buscar CEP automático
        const cepBuscarBtn = document.getElementById('buscarCep');
        if (cepBuscarBtn) {
            cepBuscarBtn.addEventListener('click', buscarCEP);
        }
    }

    // ===== FUNÇÕES DO CHECKOUT =====

    // Selecionar endereço - CORRIGIDO
    window.selecionarEnderecoCheckout = function(enderecoId) {
        console.log(`📍 Selecionando endereço: ${enderecoId}`);
        enderecoSelecionado = enderecoId;
        
        // Atualizar todos os radios
        document.querySelectorAll('input[name="endereco_entrega"]').forEach(radio => {
            radio.checked = radio.value === enderecoId;
        });
        
        // Remover seleção visual anterior
        document.querySelectorAll('.endereco-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Adicionar seleção visual atual
        const selectedCard = document.querySelector(`[data-endereco-id="${enderecoId}"]`);
        if (selectedCard) {
            selectedCard.classList.add('selected');
        }
        
        // Habilitar botão de pagamento
        atualizarEstadoBotaoPagamento();
        showSuccess('Endereço selecionado com sucesso!');
    }

    // Atualizar estado do botão de pagamento
    function atualizarEstadoBotaoPagamento() {
        if (!confirmPaymentBtn) return;
        
        if (enderecoSelecionado) {
            confirmPaymentBtn.disabled = false;
            confirmPaymentText.textContent = 'Confirmar Pagamento';
            confirmPaymentBtn.innerHTML = '<i class="fas fa-lock"></i> Confirmar Pagamento';
        } else {
            confirmPaymentBtn.disabled = true;
            confirmPaymentText.textContent = 'Selecione um endereço para continuar';
            confirmPaymentBtn.innerHTML = '<i class="fas fa-map-marker-alt"></i> Selecione um endereço para continuar';
        }
    }

    // Atualizar resumo do pedido
    function updateOrderSummary() {
        if (!orderItems) return;
        
        orderItems.innerHTML = '';
        let subtotal = 0;

        if (cartItems.length === 0) {
            orderItems.innerHTML = `
                <div class="empty-cart">
                    <i class="fas fa-shopping-cart"></i>
                    <p>Nenhum item selecionado</p>
                </div>
            `;
            if (subtotalElement) subtotalElement.textContent = 'R$ 0,00';
            if (totalAmountElement) totalAmountElement.textContent = 'R$ 0,00';
            return;
        }

        cartItems.forEach(item => {
            const itemElement = document.createElement('div');
            itemElement.className = 'order-item fade-in';
            
            const nome = item.nome_produto || item.nome || 'Produto sem nome';
            const preco = parseFloat(item.valor_unitario || item.preco || 0);
            const quantidade = parseInt(item.quantidade || 1);
            const totalItem = parseFloat(item.valor_total || preco * quantidade);
            
            itemElement.innerHTML = `
                <div class="item-info">
                    <h4>${nome}</h4>
                    <span class="price">R$ ${preco.toFixed(2)}</span>
                </div>
                <div class="item-quantity">${quantidade}x</div>
                <div class="item-total">R$ ${totalItem.toFixed(2)}</div>
            `;
            orderItems.appendChild(itemElement);

            subtotal += totalItem;
        });

        const total = subtotal - discount;
        
        if (subtotalElement) subtotalElement.textContent = `R$ ${subtotal.toFixed(2)}`;
        if (totalAmountElement) totalAmountElement.textContent = `R$ ${total.toFixed(2)}`;
        
        setTimeout(() => {
            document.querySelectorAll('.fade-in').forEach(el => {
                el.classList.add('visible');
            });
        }, 100);
    }

    // Aplicar cupom de desconto
    async function aplicarCupomDesconto() {
        if (!couponCodeInput || !applyCouponBtn) return;
        
        const couponCode = couponCodeInput.value.trim().toUpperCase();
        
        if (!couponCode) {
            showError('Por favor, insira um código de cupom.');
            return;
        }

        applyCouponBtn.disabled = true;
        applyCouponBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Aplicando...';

        try {
            const response = await fetch("/api/cupons/validar", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    codigo: couponCode
                })
            });

            const data = await response.json();
            
            if (data.valido) {
                const subtotalText = subtotalElement.textContent.replace('R$ ', '').replace(',', '.');
                const subtotal = parseFloat(subtotalText);
                
                discount = subtotal * (data.desconto / 100);
                if (discountValue) discountValue.textContent = `-R$ ${discount.toFixed(2)}`;
                if (discountLine) discountLine.style.display = 'flex';
                updateOrderSummary();
                
                cupomAplicado = {
                    id: data.id_cupom,
                    codigo: couponCode,
                    desconto: data.desconto
                };
                
                localStorage.setItem('cupomAplicado', JSON.stringify(cupomAplicado));
                
                showSuccess(data.mensagem);
            } else {
                showError(data.mensagem);
            }
        } catch (error) {
            console.error('Erro ao validar cupom:', error);
            showError('Erro ao validar cupom. Tente novamente.');
        } finally {
            applyCouponBtn.disabled = false;
            applyCouponBtn.innerHTML = 'Aplicar';
            couponCodeInput.value = '';
        }
    }

    // Processar pagamento - CORRIGIDO
    async function processarPagamento() {
        // Validar endereço selecionado
        if (!enderecoSelecionado) {
            showError('Por favor, selecione um endereço de entrega.');
            return;
        }

        const selectedPayment = document.querySelector('input[name="payment"]:checked');
        if (!selectedPayment) {
            showError('Por favor, selecione um método de pagamento.');
            return;
        }
        
        // Validar dados do cartão se necessário
        if (selectedPayment.value === 'cartao') {
            const cardNumber = document.getElementById('cardNumber')?.value;
            const cardExpiry = document.getElementById('cardExpiry')?.value;
            const cardCVC = document.getElementById('cardCVC')?.value;
            const cardName = document.getElementById('cardName')?.value;
            
            if (!cardNumber || !cardExpiry || !cardCVC || !cardName) {
                showError('Por favor, preencha todos os dados do cartão.');
                return;
            }
        }

        confirmPaymentBtn.disabled = true;
        confirmPaymentBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processando...';

        try {
            // Aplicar cupom se existir
            if (cupomAplicado) {
                const aplicarCupomResponse = await fetch("/api/cupons/aplicar", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        id_cupom: cupomAplicado.id
                    })
                });

                const cupomData = await aplicarCupomResponse.json();
                if (!cupomData.sucesso) {
                    showError(`Erro ao aplicar cupom: ${cupomData.mensagem}`);
                    resetPaymentButton();
                    return;
                }
            }

            const formData = new FormData();
            cartItems.forEach(item => {
                formData.append('selecionar_item', item.id_carrinho);
            });

            // Adicionar dados do cupom
            if (cupomAplicado) {
                formData.append('cupom_aplicado', cupomAplicado.codigo);
                formData.append('desconto_cupom', cupomAplicado.desconto.toString());
                console.log("📦 Enviando cupom para backend:", {
                    codigo: cupomAplicado.codigo,
                    desconto: cupomAplicado.desconto
                });
            } else {
                formData.append('cupom_aplicado', '');
                formData.append('desconto_cupom', '0');
            }

            const response = await fetch("/finalizar_compra", {
                method: "POST",
                body: formData
            });

            if (response.ok) {
                localStorage.removeItem('checkoutItems');
                localStorage.removeItem('carrinho');
                localStorage.removeItem('cupomAplicado');
                
                showSuccess('Pagamento realizado com sucesso! Obrigado pela compra.', true);
                setTimeout(() => {
                    window.location.href = '/';
                }, 3000);
            } else {
                throw new Error('Erro ao processar pagamento');
            }
        } catch (error) {
            console.error('Erro ao processar pagamento:', error);
            showError('Erro ao processar pagamento. Tente novamente.');
            resetPaymentButton();
        }
    }

    // Inicializar máscaras do cartão
    function inicializarMascarasCartao() {
        const cardNumber = document.getElementById('cardNumber');
        const cardExpiry = document.getElementById('cardExpiry');
        const cardCVC = document.getElementById('cardCVC');

        if (cardNumber) {
            cardNumber.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '').replace(/(\d{4})(?=\d)/g, '$1 ').trim();
            });
        }

        if (cardExpiry) {
            cardExpiry.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '').replace(/(\d{2})(?=\d)/, '$1/');
            });
        }

        if (cardCVC) {
            cardCVC.addEventListener('input', (e) => {
                e.target.value = e.target.value.replace(/\D/g, '').substring(0, 3);
            });
        }
    }

    // Carregar cupom salvo se existir
    function carregarCupomSalvo() {
        const cupomSalvo = localStorage.getItem('cupomAplicado');
        if (cupomSalvo) {
            cupomAplicado = JSON.parse(cupomSalvo);
            if (couponCodeInput) couponCodeInput.value = cupomAplicado.codigo;
            
            const subtotalText = subtotalElement.textContent.replace('R$ ', '').replace(',', '.');
            const subtotal = parseFloat(subtotalText);
            discount = subtotal * (cupomAplicado.desconto / 100);
            if (discountValue) discountValue.textContent = `-R$ ${discount.toFixed(2)}`;
            if (discountLine) discountLine.style.display = 'flex';
            updateOrderSummary();
        }
    }

    // Funções de utilidade
    function showError(message) {
        showNotification(message, 'error');
    }

    function showSuccess(message, isSuccess = false) {
        showNotification(message, 'success');
    }

    function showNotification(message, type) {
        const existingNotification = document.querySelector('.checkout-notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        const notification = document.createElement('div');
        notification.className = `checkout-notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                <span>${message}</span>
            </div>
        `;

        document.body.appendChild(notification);

        // Animação de entrada
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 10);

        // Remover após 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.style.opacity = '0';
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.remove();
                    }
                }, 300);
            }
        }, 5000);
    }

    function resetPaymentButton() {
        if (!confirmPaymentBtn) return;
        confirmPaymentBtn.disabled = false;
        confirmPaymentBtn.innerHTML = '<i class="fas fa-lock"></i> Confirmar Pagamento';
    }

    // Inicialização
    inicializarCheckout().then(() => {
        carregarCupomSalvo();
    });
});

// ===== FUNÇÕES GLOBAIS DO MODAL DE ENDEREÇO =====

// Abrir modal de endereço
window.abrirModalEndereco = function(enderecoId = null) {
    const modal = document.getElementById('modalEndereco');
    const form = document.getElementById('enderecoForm');
    const titulo = document.getElementById('modalEnderecoTitulo');
    const botaoTexto = document.getElementById('modalEnderecoBotaoTexto');
    
    enderecoEditando = enderecoId;
    
    if (enderecoId) {
        titulo.textContent = 'Editar Endereço';
        botaoTexto.textContent = 'Atualizar Endereço';
        carregarDadosEndereco(enderecoId);
    } else {
        titulo.textContent = 'Adicionar Novo Endereço';
        botaoTexto.textContent = 'Salvar Endereço';
        if (form) form.reset();
        const paisInput = document.getElementById('pais');
        if (paisInput) paisInput.value = 'Brasil';
    }
    
    if (modal) {
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }
}

// Fechar modal de endereço
window.fecharModalEndereco = function() {
    const modal = document.getElementById('modalEndereco');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        enderecoEditando = null;
    }
}

// Fechar modal ao clicar fora
window.addEventListener('click', function(e) {
    const modal = document.getElementById('modalEndereco');
    if (e.target === modal) {
        fecharModalEndereco();
    }
});

// Buscar CEP (ViaCEP)
window.buscarCEP = async function() {
    const cepInput = document.getElementById('cep');
    if (!cepInput) return;
    
    const cep = cepInput.value.replace(/\D/g, '');
    
    if (cep.length !== 8) {
        alert('Por favor, digite um CEP válido com 8 dígitos.');
        return;
    }
    
    cepInput.disabled = true;
    
    try {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();
        
        if (!data.erro) {
            const enderecoInput = document.getElementById('endereco');
            const bairroInput = document.getElementById('bairro');
            const cidadeInput = document.getElementById('cidade');
            const estadoInput = document.getElementById('estado');
            
            if (enderecoInput) enderecoInput.value = data.logradouro || '';
            if (bairroInput) bairroInput.value = data.bairro || '';
            if (cidadeInput) cidadeInput.value = data.localidade || '';
            if (estadoInput) estadoInput.value = data.uf || '';
            
            const numeroInput = document.getElementById('numero');
            if (numeroInput) numeroInput.focus();
        } else {
            alert('CEP não encontrado. Por favor, verifique o CEP digitado.');
        }
    } catch (error) {
        console.error('Erro ao buscar CEP:', error);
        alert('Erro ao buscar CEP. Tente novamente.');
    } finally {
        cepInput.disabled = false;
    }
}

// Carregar dados do endereço para edição
window.carregarDadosEndereco = function(enderecoId) {
    // Buscar dados do endereço na lista carregada
    const endereco = window.enderecosUsuario?.find(e => e.id === enderecoId);
    
    if (endereco) {
        const enderecoIdInput = document.getElementById('endereco_id');
        const cepInput = document.getElementById('cep');
        const enderecoInput = document.getElementById('endereco');
        const numeroInput = document.getElementById('numero');
        const complementoInput = document.getElementById('complemento');
        const bairroInput = document.getElementById('bairro');
        const cidadeInput = document.getElementById('cidade');
        const estadoInput = document.getElementById('estado');
        const paisInput = document.getElementById('pais');
        const principalInput = document.getElementById('endereco_principal');
        
        if (enderecoIdInput) enderecoIdInput.value = endereco.id;
        if (cepInput) cepInput.value = endereco.cep || '';
        if (enderecoInput) enderecoInput.value = endereco.endereco || '';
        if (numeroInput) numeroInput.value = endereco.numero || '';
        if (complementoInput) complementoInput.value = endereco.complemento || '';
        if (bairroInput) bairroInput.value = endereco.bairro || '';
        if (cidadeInput) cidadeInput.value = endereco.cidade || '';
        if (estadoInput) estadoInput.value = endereco.estado || '';
        if (paisInput) paisInput.value = endereco.pais || 'Brasil';
        if (principalInput) principalInput.checked = endereco.principal === 'sim';
    }
}

// Salvar endereço
window.salvarEndereco = async function(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    let url = '/adicionar_endereco';
    
    if (enderecoEditando) {
        url = `/editar_endereco/${enderecoEditando}`;
    }
    
    try {
        const response = await fetch(url, {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(data.message);
            fecharModalEndereco();
            location.reload(); // Recarregar para atualizar os endereços
        } else {
            alert('Erro ao salvar endereço: ' + data.message);
        }
    } catch (error) {
        console.error('Erro ao salvar endereço:', error);
        alert('Erro ao salvar endereço. Tente novamente.');
    }
}

// Funções específicas para o checkout
window.editarEnderecoCheckout = function(enderecoId) {
    abrirModalEndereco(enderecoId);
}

window.excluirEnderecoCheckout = async function(enderecoId) {
    if (confirm('Tem certeza que deseja excluir este endereço?')) {
        try {
            const response = await fetch(`/excluir_endereco/${enderecoId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert(data.message);
                location.reload();
            } else {
                alert(data.message);
            }
        } catch (error) {
            console.error('Erro:', error);
            alert('Erro ao excluir endereço.');
        }
    }
}

window.definirComoPrincipalCheckout = async function(enderecoId) {
    try {
        const response = await fetch(`/definir_endereco_principal/${enderecoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.message);
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao definir endereço principal.');
    }
}