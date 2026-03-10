// cadastro.js - Integração com ViaCEP e validações

class ViaCEPIntegration {
    constructor() {
        this.baseURL = 'https://viacep.com.br/ws';
        this.init();
    }

    init() {
        this.setupCEPListeners();
        this.setupFormValidation();
        this.setupMasks();
    }

    setupMasks() {
        // Máscara para CPF
        const cpfField = document.getElementById('cpf');
        if (cpfField) {
            cpfField.addEventListener('input', (e) => this.formatarCPF(e.target));
        }

        // Máscara para telefone
        const telefoneField = document.querySelector('input[name="telefone"]');
        if (telefoneField) {
            telefoneField.addEventListener('input', (e) => this.formatarTelefone(e.target));
        }
    }

    formatarCPF(cpfInput) {
        let cpf = cpfInput.value.replace(/\D/g, '');
        cpf = cpf.substring(0, 11);
        
        if (cpf.length > 3) {
            cpf = cpf.substring(0, 3) + '.' + cpf.substring(3);
        }
        if (cpf.length > 7) {
            cpf = cpf.substring(0, 7) + '.' + cpf.substring(7);
        }
        if (cpf.length > 11) {
            cpf = cpf.substring(0, 11) + '-' + cpf.substring(11);
        }
        
        cpfInput.value = cpf;
    }

    formatarTelefone(telefoneInput) {
        let value = telefoneInput.value.replace(/\D/g, '');
        if (value.length <= 11) {
            if (value.length <= 2) {
                value = value.replace(/^(\d{0,2})/, '($1');
            } else if (value.length <= 7) {
                value = value.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
            } else {
                value = value.replace(/^(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
            }
        }
        telefoneInput.value = value;
    }

    setupCEPListeners() {
        // Listener para CEP principal
        const cepInput = document.getElementById('cep');
        if (cepInput) {
            cepInput.addEventListener('blur', () => this.buscarCEP('cep'));
            cepInput.addEventListener('input', (e) => this.formatarCEP(e.target));
        }
    }

    formatarCEP(cepInput) {
        let cep = cepInput.value.replace(/\D/g, '');
        cep = cep.substring(0, 8);
        if (cep.length > 5) {
            cep = cep.substring(0, 5) + '-' + cpf.substring(5);
        }
        cepInput.value = cep;
    }

    validarCEP(cep) {
        const cepNumerico = cep.replace(/\D/g, '');
        return cepNumerico.length === 8;
    }

    async buscarCEP(tipoCEP) {
        const cepInput = document.getElementById(tipoCEP);
        const cep = cepInput.value.replace(/\D/g, '');
        
        if (!this.validarCEP(cep)) {
            this.mostrarFeedback(tipoCEP, 'CEP inválido. Digite 8 dígitos.', 'error');
            return;
        }

        this.mostrarFeedback(tipoCEP, 'Buscando endereço...', 'loading');

        try {
            const response = await fetch(`${this.baseURL}/${cep}/json/`);
            const data = await response.json();
            
            if (data.erro) {
                this.mostrarFeedback(tipoCEP, 'CEP não encontrado.', 'error');
                return;
            }

            this.preencherEndereco(data);
            this.mostrarFeedback(tipoCEP, 'Endereço encontrado!', 'success');
        } catch (error) {
            console.error('Erro ao buscar CEP:', error);
            this.mostrarFeedback(tipoCEP, 'Erro na busca. Tente novamente.', 'error');
        }
    }

    preencherEndereco(data) {
        const campos = {
            'endereco': data.logradouro,
            'bairro': data.bairro,
            'cidade': data.localidade,
            'estado': data.uf,
            'pais': 'Brasil'
        };

        Object.keys(campos).forEach(campoId => {
            const campo = document.getElementById(campoId);
            if (campo && !campo.value) {
                campo.value = campos[campoId];
                // Adiciona classe para feedback visual
                campo.classList.add('auto-filled');
                setTimeout(() => campo.classList.remove('auto-filled'), 2000);
            }
        });

        // Foca no campo número após preencher
        const numeroField = document.getElementById('numero');
        if (numeroField) {
            numeroField.focus();
        }
    }

    mostrarFeedback(tipoCEP, mensagem, tipo) {
        const feedbackElement = document.getElementById(`${tipoCEP}Feedback`);
        if (!feedbackElement) return;
        
        feedbackElement.textContent = mensagem;
        feedbackElement.className = `cep-feedback ${tipo}`;
        
        if (tipo !== 'loading') {
            setTimeout(() => {
                feedbackElement.textContent = '';
                feedbackElement.className = 'cep-feedback';
            }, 3000);
        }
    }

    setupFormValidation() {
        const form = document.getElementById('cadastroForm');
        if (form) {
            form.addEventListener('submit', (e) => this.validarFormulario(e));
        }
    }

    validarFormulario(event) {
        const requiredFields = document.querySelectorAll('input[required]');
        let isValid = true;

        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                this.mostrarErroCampo(field, 'Este campo é obrigatório');
            } else {
                this.removerErroCampo(field);
            }
        });

        // Validação específica do CPF
        const cpfField = document.getElementById('cpf');
        if (cpfField && cpfField.value) {
            const cpfNumerico = cpfField.value.replace(/\D/g, '');
            if (cpfNumerico.length !== 11) {
                isValid = false;
                this.mostrarErroCampo(cpfField, 'CPF deve ter 11 dígitos');
            }
        }

        // Validação específica do CEP
        const cepField = document.getElementById('cep');
        if (cepField && cepField.value) {
            const cepNumerico = cepField.value.replace(/\D/g, '');
            if (cepNumerico.length !== 8) {
                isValid = false;
                this.mostrarErroCampo(cepField, 'CEP deve ter 8 dígitos');
            }
        }

        if (!isValid) {
            event.preventDefault();
            this.mostrarMensagemGeral('Por favor, preencha todos os campos obrigatórios corretamente.', 'error');
        }
    }

    mostrarErroCampo(campo, mensagem) {
        this.removerErroCampo(campo);
        campo.classList.add('error');
        
        let errorElement = campo.parentNode.querySelector('.field-error');
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'field-error';
            campo.parentNode.appendChild(errorElement);
        }
        errorElement.textContent = mensagem;
    }

    removerErroCampo(campo) {
        campo.classList.remove('error');
        const errorElement = campo.parentNode.querySelector('.field-error');
        if (errorElement) {
            errorElement.remove();
        }
    }

    mostrarMensagemGeral(mensagem, tipo) {
        const existingMessage = document.querySelector('.form-message');
        if (existingMessage) {
            existingMessage.remove();
        }

        const messageElement = document.createElement('div');
        messageElement.className = `form-message ${type}`;
        messageElement.textContent = mensagem;
        
        const form = document.getElementById('cadastroForm');
        form.insertBefore(messageElement, form.firstChild);

        setTimeout(() => {
            messageElement.remove();
        }, 5000);
    }
}

// Inicialização quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    new ViaCEPIntegration();
});