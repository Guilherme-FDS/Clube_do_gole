export function formatarMoeda(valor) {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'BRL'
    }).format(parseFloat(valor) || 0)
  }
  
  export function formatarData(data) {
    if (!data) return ''
    return new Intl.DateTimeFormat('pt-BR').format(new Date(data))
  }
  
  export function formatarDataHora(data) {
    if (!data) return ''
    return new Intl.DateTimeFormat('pt-BR', {
      dateStyle: 'short',
      timeStyle: 'short'
    }).format(new Date(data))
  }
  
  export function formatarCPF(cpf) {
    if (!cpf) return ''
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4')
  }
  
  export function formatarTelefone(tel) {
    if (!tel) return ''
    return tel.replace(/(\d{2})(\d{5})(\d{4})/, '($1) $2-$3')
  }