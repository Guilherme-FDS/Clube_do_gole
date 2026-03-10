// DASHBOARD VENDAS - INTERATIVIDADES E ANIMAÇÕES

document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades do dashboard
    initDashboardAnimations();
    initTableSorting();
    initRealTimeUpdates();
    initExportFunctionality();
});

// ===== ANIMAÇÕES DO DASHBOARD =====
function initDashboardAnimations() {
    // Efeito de contagem nos cards de estatísticas (VERSÃO OTIMIZADA)
    animateCounterCardsOptimized();
    
    // Highlight ao passar o mouse nas linhas da tabela
    initTableHoverEffects();
    
    // Animações de entrada
    initScrollAnimations();
}

function animateCounterCardsOptimized() {
    const counterCards = document.querySelectorAll('.card-estatistica');
    
    counterCards.forEach((card, index) => {
        // Delay escalonado para não sobrecarregar
        setTimeout(() => {
            const valorElement = card.querySelector('.card-valor');
            if (valorElement) {
                const originalText = valorElement.textContent;
                
                // Apenas mostra o valor final sem animação pesada
                // Isso resolve o problema de travamento
                valorElement.textContent = originalText;
                
                // Adiciona uma classe para efeito visual suave
                valorElement.classList.add('value-visible');
                
                // Efeito visual leve sem bloqueio
                card.style.opacity = '0';
                card.style.transform = 'translateY(20px)';
                
                setTimeout(() => {
                    card.style.transition = 'all 0.5s ease-out';
                    card.style.opacity = '1';
                    card.style.transform = 'translateY(0)';
                }, 50);
            }
        }, index * 150); // Delay de 150ms entre cada card
    });
}

// ===== ORDENAÇÃO DA TABELA =====
function initTableSorting() {
    const tableHeaders = document.querySelectorAll('.tabela-vendas th');
    
    tableHeaders.forEach((header, index) => {
        // Não aplicar ordenação na coluna de ações (última coluna)
        if (index !== tableHeaders.length - 1) {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => sortTable(index));
        }
    });
}

function sortTable(columnIndex) {
    const table = document.querySelector('.tabela-vendas');
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    // Verificar se há dados para ordenar
    const noDataRow = rows.find(row => row.querySelector('.sem-dados'));
    if (noDataRow || rows.length === 0) return;
    
    // Determinar tipo de ordenação
    const isNumeric = columnIndex === 3 || columnIndex === 4; // Quantidade e Valor
    const isDate = columnIndex === 0; // Data
    
    rows.sort((a, b) => {
        let aValue = a.cells[columnIndex].textContent.trim();
        let bValue = b.cells[columnIndex].textContent.trim();
        
        // Tratamento para valores monetários
        if (columnIndex === 4) {
            aValue = parseFloat(aValue.replace('R$', '').replace(/\./g, '').replace(',', '.').trim());
            bValue = parseFloat(bValue.replace('R$', '').replace(/\./g, '').replace(',', '.').trim());
        }
        
        // Tratamento para datas (formato DD/MM/YYYY HH:MM)
        if (columnIndex === 0) {
            const aDateStr = aValue.split(' ')[0]; // Pega apenas a data
            const bDateStr = bValue.split(' ')[0];
            aValue = new Date(aDateStr.split('/').reverse().join('-'));
            bValue = new Date(bDateStr.split('/').reverse().join('-'));
        }
        
        // Tratamento para quantidade
        if (columnIndex === 3) {
            aValue = parseInt(aValue);
            bValue = parseInt(bValue);
        }
        
        if (isNumeric || isDate) {
            return aValue - bValue;
        } else {
            return aValue.localeCompare(bValue);
        }
    });
    
    // Limpar e reordenar tabela
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
    
    // Adicionar efeito visual de reordenação
    highlightSortedRows();
}

function highlightSortedRows() {
    const rows = document.querySelectorAll('.tabela-vendas tbody tr');
    rows.forEach((row, index) => {
        row.style.animation = 'none';
        setTimeout(() => {
            row.style.animation = `fadeInUp 0.5s ease ${index * 0.1}s both`;
        }, 10);
    });
}

// ===== ATUALIZAÇÕES EM TEMPO REAL =====
function initRealTimeUpdates() {
    // Simular atualizações a cada 30 segundos (apenas para demonstração)
    setInterval(() => {
        simulateDataUpdate();
    }, 30000);
}

function simulateDataUpdate() {
    // Adicionar classe de pulso nos cards
    const cards = document.querySelectorAll('.card-estatistica');
    cards.forEach(card => {
        card.classList.add('pulse-update');
        setTimeout(() => {
            card.classList.remove('pulse-update');
        }, 1000);
    });
    
    // Mostrar notificação de atualização
    showUpdateNotification();
}

function showUpdateNotification() {
    // Verificar se já existe uma notificação
    if (document.querySelector('.update-notification')) return;
    
    const notification = document.createElement('div');
    notification.className = 'update-notification';
    notification.innerHTML = `
        <i class="fas fa-sync-alt"></i>
        Dados atualizados
    `;
    
    document.body.appendChild(notification);
    
    // Remover notificação após 3 segundos
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// ===== FUNCIONALIDADE DE EXPORTAÇÃO =====
function initExportFunctionality() {
    // Adicionar botão de exportação se necessário
    addExportButton();
}

function addExportButton() {
    const headerRight = document.querySelector('.header-right');
    if (headerRight && !document.querySelector('.export-btn')) {
        const exportBtn = document.createElement('a');
        exportBtn.className = 'icon-btn export-btn';
        exportBtn.innerHTML = '<i class="fas fa-download"></i> Exportar';
        exportBtn.href = '#';
        exportBtn.onclick = (e) => {
            e.preventDefault();
            exportToCSV();
        };
        
        headerRight.appendChild(exportBtn);
    }
}

function exportToCSV() {
    const table = document.querySelector('.tabela-vendas');
    if (!table) return;
    
    let csv = [];
    const rows = table.querySelectorAll('tr');
    
    for (let i = 0; i < rows.length; i++) {
        const row = [];
        const cols = rows[i].querySelectorAll('td, th');
        
        for (let j = 0; j < cols.length; j++) {
            // Pular coluna de ações (última coluna)
            if (j === cols.length - 1) continue;
            
            let text = cols[j].innerText;
            // Limpar texto e adicionar entre aspas para evitar problemas com vírgulas
            text = text.replace(/"/g, '""');
            row.push(`"${text}"`);
        }
        
        csv.push(row.join(','));
    }
    
    // Download do arquivo
    downloadCSV(csv.join('\n'), 'vendas_clube_do_gole.csv');
}

function downloadCSV(csv, filename) {
    // Adicionar BOM para UTF-8
    const BOM = '\uFEFF';
    const csvFile = new Blob([BOM + csv], { type: 'text/csv;charset=utf-8;' });
    const downloadLink = document.createElement('a');
    
    downloadLink.download = filename;
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = 'none';
    
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

// ===== EFEITOS VISUAIS ADICIONAIS =====
function initTableHoverEffects() {
    const tableRows = document.querySelectorAll('.tabela-vendas tbody tr');
    
    tableRows.forEach(row => {
        if (row.querySelector('.sem-dados')) return;
        
        row.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.01)';
            this.style.zIndex = '1';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.zIndex = '0';
        });
    });
}

function initScrollAnimations() {
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

    document.querySelectorAll('.fade-in').forEach(el => {
        observer.observe(el);
    });
}

// ===== UTILITÁRIOS =====
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR');
}

// ===== TRATAMENTO DE ERROS =====
window.addEventListener('error', function(e) {
    console.error('Erro no dashboard:', e.error);
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Promise rejeitada:', e.reason);
});