import api from './api'

export const ver               = ()     => api.get('/carrinho/')
export const adicionar         = (data) => api.post('/carrinho/adicionar', data)
export const remover           = (ids)  => api.post('/carrinho/remover', { ids })
export const atualizarQtd      = (data) => api.post('/carrinho/quantidade', data)
export const contador          = ()     => api.get('/carrinho/contador')
export const itensSelecionados = (ids)  => api.post('/carrinho/itens_selecionados', { ids })
export const finalizar         = (data) => api.post('/carrinho/finalizar', data)
export const meusPedidos       = ()     => api.get('/carrinho/meus_pedidos')