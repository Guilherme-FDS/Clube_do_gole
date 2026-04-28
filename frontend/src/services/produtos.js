import api from './api'

export const listar   = ()   => api.get('/produtos/')
export const gold     = ()   => api.get('/produtos/gold')
export const premium  = ()   => api.get('/produtos/premium')
export const detalhe  = (id) => api.get(`/produtos/${id}`)