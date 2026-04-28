import api from './api'

export const validar = (codigo) => api.post('/cupons/validar', { codigo })
export const aplicar = (codigo) => api.post('/cupons/aplicar', { codigo })