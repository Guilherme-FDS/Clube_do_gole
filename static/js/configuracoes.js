// configuracoes.js - Funcionalidades específicas da página de configurações

document.addEventListener("DOMContentLoaded", () => {
    console.log("🔧 Inicializando página de configurações...");
    
    // Inicializar funcionalidades
    inicializarNavegacaoAbas();
    inicializarFormularioPerfil();
    inicializarFormularioSenha();
    inicializarModalEndereco();
    inicializarMascaraTelefone();
});

// Navegação entre abas
function inicializarNavegacaoAbas() {
    const menuItems = document.querySelectorAll('.menu-item');
    const tabContents = document.querySelectorAll('.tab-content');

    menuItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Remover classe active de todos
            menuItems.forEach(i => i.classList.remove('active'));
            tabContents.forEach(tab => tab.classList.remove('active'));
            
            // Adicionar classe active ao item clicado
            item.classList.add('active');
            
            // Mostrar aba correspondente
            const tabId = item.getAttribute('data-tab') + '-tab';
            const tabToShow = document.getElementById(tabId);
            if (tabToShow) {
                tabToShow.classList.add('active');
            }
        });
    });
}

// Máscara para telefone
function inicializarMascaraTelefone() {
    const telefoneInput = document.getElementById('telefone');
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            
            // Aplicar máscara: (11) 99999-9999
            if (value.length <= 11) {
                if (value.length <= 2) {
                    value = value.replace(/(\d{0,2})/, '($1');
                } else if (value.length <= 6) {
                    value = value.replace(/(\d{2})(\d{0,4})/, '($1) $2');
                } else if (value.length <= 10) {
                    value = value.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
                } else {
                    value = value.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
                }
                e.target.value = value;
            }
        });
    }
}

// Formulário de Perfil
function inicializarFormularioPerfil() {
    const perfilForm = document.getElementById('perfilForm');
    
    if (perfilForm) {
        // Salvar estado original dos campos para detectar mudanças
        const camposOriginais = {
            nome: document.getElementById('nome').value,
            sobrenome: document.getElementById('sobrenome').value,
            email: document.getElementById('email').value,
            telefone: document.getElementById('telefone').value,
            data_nascimento: document.getElementById('data_nascimento').value
        };

        perfilForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(perfilForm);
            const dadosAtuais = Object.fromEntries(formData);
            
            // Detectar quais campos foram alterados
            const camposAlterados = [];
            
            if (dadosAtuais.nome !== camposOriginais.nome) camposAlterados.push('Nome');
            if (dadosAtuais.sobrenome !== camposOriginais.sobrenome) camposAlterados.push('Sobrenome');
            if (dadosAtuais.email !== camposOriginais.email) camposAlterados.push('Email');
            if (dadosAtuais.telefone !== camposOriginais.telefone) camposAlterados.push('Telefone');
            if (dadosAtuais.data_nascimento !== camposOriginais.data_nascimento) camposAlterados.push('Data de Nascimento');

            try {
                const response = await fetch('/atualizar_perfil', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    if (camposAlterados.length > 0) {
                        showNotification(`${camposAlterados.join(', ')} atualizado(s) com sucesso!`, 'success');
                    } else {
                        showNotification('Nenhuma alteração foi feita.', 'info');
                    }
                    
                    // Atualizar estado original
                    Object.assign(camposOriginais, dadosAtuais);
                    
                    // Não recarregar a página - manter na aba atual
                    setTimeout(() => {
                        // Atualizar nome na sidebar se necessário
                        const nomeCompleto = `${dadosAtuais.nome} ${dadosAtuais.sobrenome}`;
                        const userInfo = document.querySelector('.user-info h3');
                        if (userInfo) {
                            userInfo.textContent = nomeCompleto;
                        }
                    }, 1000);
                } else {
                    showNotification(data.message, 'error');
                }
            } catch (error) {
                console.error('Erro ao atualizar perfil:', error);
                showNotification('Erro ao atualizar perfil. Tente novamente.', 'error');
            }
        });
    }
}

// Formulário de Senha
function inicializarFormularioSenha() {
    const senhaForm = document.querySelector('.senha-form');
    
    if (senhaForm) {
        senhaForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(senhaForm);
            
            try {
                const response = await fetch('/alterar_senha', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showNotification('Senha alterada com sucesso!', 'success');
                    senhaForm.reset();
                    
                    // Manter na aba de segurança
                    manterAbaAtiva('seguranca');
                } else {
                    showNotification(data.message, 'error');
                }
            } catch (error) {
                console.error('Erro ao alterar senha:', error);
                showNotification('Erro ao alterar senha. Tente novamente.', 'error');
            }
        });
    }
}

// Modal de Endereço
function inicializarModalEndereco() {
    const modal = document.getElementById('modalEndereco');
    const form = document.getElementById('enderecoForm');
    
    if (!modal || !form) return;
    
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
    
    // Submit do formulário
    form.addEventListener('submit', salvarEnderecoConfiguracoes);
}

async function salvarEnderecoConfiguracoes(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    let url = '/adicionar_endereco';
    let mensagemSucesso = 'Endereço adicionado com sucesso!';
    
    if (window.enderecoEditando) {
        url = `/editar_endereco/${window.enderecoEditando}`;
        mensagemSucesso = 'Endereço atualizado com sucesso!';
    }
    
    try {
        const response = await fetch(url, {
            method: "POST",
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(mensagemSucesso, 'success');
            fecharModalEndereco();
            
            // Recarregar mantendo na aba de endereços
            setTimeout(() => {
                recarregarMantendoAba('enderecos');
            }, 1500);
        } else {
            showNotification('Erro: ' + data.message, 'error');
        }
    } catch (error) {
        console.error('Erro ao salvar endereço:', error);
        showNotification('Erro ao salvar endereço. Tente novamente.', 'error');
    }
}

// Funções para manter a aba ativa
function manterAbaAtiva(aba) {
    // Atualizar menu
    document.querySelectorAll('.menu-item').forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('data-tab') === aba) {
            item.classList.add('active');
        }
    });
    
    // Atualizar conteúdo
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
        if (tab.id === `${aba}-tab`) {
            tab.classList.add('active');
        }
    });
}

function recarregarMantendoAba(aba) {
    // Salvar aba atual no sessionStorage
    sessionStorage.setItem('abaAtivaConfiguracoes', aba);
    location.reload();
}

// Função de notificação melhorada
function showNotification(message, type = 'info') {
    const existingNotification = document.querySelector('.config-notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    const notification = document.createElement('div');
    notification.className = `config-notification ${type}`;
    
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        info: 'info-circle',
        warning: 'exclamation-triangle'
    };
    
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${icons[type] || 'info-circle'}"></i>
            <span>${message}</span>
        </div>
    `;

    document.body.appendChild(notification);

    // Animação de entrada
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateY(0)';
    }, 10);

    // Remover após 5 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.opacity = '0';
            notification.style.transform = 'translateY(-100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }, 5000);
}

// Funções globais do modal
function abrirModalEndereco(enderecoId = null) {
    const modal = document.getElementById('modalEndereco');
    const form = document.getElementById('enderecoForm');
    const titulo = document.getElementById('modalEnderecoTitulo');
    const botaoTexto = document.getElementById('modalEnderecoBotaoTexto');
    
    window.enderecoEditando = enderecoId;
    
    if (enderecoId) {
        titulo.textContent = 'Editar Endereço';
        botaoTexto.textContent = 'Atualizar Endereço';
        carregarDadosEndereco(enderecoId);
    } else {
        titulo.textContent = 'Adicionar Novo Endereço';
        botaoTexto.textContent = 'Salvar Endereço';
        form.reset();
        document.getElementById('pais').value = 'Brasil';
    }
    
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function fecharModalEndereco() {
    const modal = document.getElementById('modalEndereco');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        window.enderecoEditando = null;
    }
}

function carregarDadosEndereco(enderecoId) {
    const enderecoElement = document.querySelector(`[data-endereco-id="${enderecoId}"]`);
    
    if (enderecoElement) {
        document.getElementById('cep').value = enderecoElement.dataset.cep || '';
        document.getElementById('endereco').value = enderecoElement.dataset.endereco || '';
        document.getElementById('numero').value = enderecoElement.dataset.numero || '';
        document.getElementById('complemento').value = enderecoElement.dataset.complemento || '';
        document.getElementById('bairro').value = enderecoElement.dataset.bairro || '';
        document.getElementById('cidade').value = enderecoElement.dataset.cidade || '';
        document.getElementById('estado').value = enderecoElement.dataset.estado || '';
        document.getElementById('pais').value = enderecoElement.dataset.pais || 'Brasil';
        document.getElementById('endereco_principal').checked = enderecoElement.dataset.principal === 'true';
    }
}

// Funções de endereço com notificações específicas
async function editarEndereco(enderecoId) {
    abrirModalEndereco(enderecoId);
}

async function excluirEndereco(enderecoId) {
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
                showNotification('Endereço excluído com sucesso!', 'success');
                setTimeout(() => {
                    recarregarMantendoAba('enderecos');
                }, 1500);
            } else {
                showNotification(data.message, 'error');
            }
        } catch (error) {
            console.error('Erro:', error);
            showNotification('Erro ao excluir endereço.', 'error');
        }
    }
}

async function definirComoPrincipal(enderecoId) {
    try {
        const response = await fetch(`/definir_endereco_principal/${enderecoId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Endereço definido como principal!', 'success');
            setTimeout(() => {
                recarregarMantendoAba('enderecos');
            }, 1500);
        } else {
            showNotification(data.message, 'error');
        }
    } catch (error) {
        console.error('Erro:', error);
        showNotification('Erro ao definir endereço principal.', 'error');
    }
}

function resetForm() {
    const perfilForm = document.getElementById('perfilForm');
    if (perfilForm) {
        perfilForm.reset();
        showNotification('Formulário resetado.', 'info');
    }
}

// Buscar CEP
async function buscarCEP() {
    const cepInput = document.getElementById('cep');
    const cep = cepInput.value.replace(/\D/g, '');
    
    if (cep.length !== 8) {
        return;
    }
    
    cepInput.disabled = true;
    showNotification('Buscando CEP...', 'info');
    
    try {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();
        
        if (!data.erro) {
            document.getElementById('endereco').value = data.logradouro || '';
            document.getElementById('bairro').value = data.bairro || '';
            document.getElementById('cidade').value = data.localidade || '';
            document.getElementById('estado').value = data.uf || '';
            document.getElementById('numero').focus();
            showNotification('CEP encontrado! Preencha o número.', 'success');
        } else {
            showNotification('CEP não encontrado. Verifique o CEP digitado.', 'error');
        }
    } catch (error) {
        console.error('Erro ao buscar CEP:', error);
        showNotification('Erro ao buscar CEP. Tente novamente.', 'error');
    } finally {
        cepInput.disabled = false;
    }
}

// Fechar modal ao clicar fora
window.addEventListener('click', function(e) {
    const modal = document.getElementById('modalEndereco');
    if (e.target === modal) {
        fecharModalEndereco();
    }
});

// Restaurar aba ativa ao carregar a página
window.addEventListener('load', function() {
    const abaSalva = sessionStorage.getItem('abaAtivaConfiguracoes');
    if (abaSalva) {
        manterAbaAtiva(abaSalva);
        sessionStorage.removeItem('abaAtivaConfiguracoes');
    }
});