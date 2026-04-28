import api from './api'

export const login    = (data) => api.post('/auth/login', data)
export const cadastro = (data) => api.post('/auth/cadastro', data)
export const logout   = ()     => api.post('/auth/logout')
export const me       = ()     => api.get('/auth/me')