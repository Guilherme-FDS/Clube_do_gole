import axios from 'axios'
const api = axios.create({ 
  baseURL: import.meta.env.VITE_API_URL || 'https://clube-do-gole-backend.onrender.com/api'
})
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  const guestId = localStorage.getItem('guest_id')
  if (guestId) config.headers['X-Guest-Id'] = guestId
  return config
})
api.interceptors.response.use(
  res => res,
  err => {
    // Só redireciona em 401 de sessão expirada (já estava logado), nunca numa
    // tentativa de login/cadastro — senão o erro "senha incorreta" some no reload.
    const url = err.config?.url || ''
    const ehEndpointAuth = /\/auth\/(login|cadastro|oauth)/.test(url)
    const tinhaToken = !!localStorage.getItem('token')
    if (err.response?.status === 401 && tinhaToken && !ehEndpointAuth) {
      localStorage.removeItem('token')
      localStorage.removeItem('nome')
      localStorage.removeItem('tipo')
      localStorage.removeItem('user_id')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)
export default api
