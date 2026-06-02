// services/auth.js
import api from './api'

export const login    = (data) => api.post('/auth/login', data)
export const cadastro = (data) => api.post('/auth/cadastro', data)
export const logout   = ()     => api.post('/auth/logout')
export const me       = ()     => api.get('/auth/me')

export const esqueceuSenha  = (email)        => api.post('/auth/esqueceu-senha', { email })
export const redefinirSenha = (token, nova)  => api.post('/auth/redefinir-senha', { token, nova_senha: nova })

export const oauthCallback  = (code, provider, guest_carrinho = []) =>
  api.post('/auth/oauth/callback', { code, provider, guest_carrinho })

export const getGoogleAuthUrl = () => {
  const params = new URLSearchParams({
    client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
    redirect_uri: import.meta.env.VITE_GOOGLE_REDIRECT_URI,
    response_type: 'code',
    scope: 'openid email profile',
    access_type: 'offline',
    prompt: 'select_account',
  })
  return `https://accounts.google.com/o/oauth2/v2/auth?${params}`
}

export const getFacebookAuthUrl = () => {
  const params = new URLSearchParams({
    client_id: import.meta.env.VITE_FACEBOOK_APP_ID,
    redirect_uri: import.meta.env.VITE_FACEBOOK_REDIRECT_URI,
    response_type: 'code',
    scope: 'email,public_profile',
  })
  return `https://www.facebook.com/v19.0/dialog/oauth?${params}`
}