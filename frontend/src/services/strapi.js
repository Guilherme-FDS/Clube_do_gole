import axios from 'axios'

const strapi = axios.create({
  baseURL: import.meta.env.VITE_STRAPI_URL || 'http://localhost:1337',
})

// Cache em memória — persiste enquanto a aba estiver aberta, zerando entre recarregamentos
const _cache = new Map()
const CACHE_TTL = 5 * 60 * 1000 // 5 minutos

const _getCached = (key) => {
  const entry = _cache.get(key)
  if (!entry) return null
  if (Date.now() - entry.ts > CACHE_TTL) { _cache.delete(key); return null }
  return entry.data
}

const get = (path, params = {}) => {
  const key = path + JSON.stringify(params)
  const cached = _getCached(key)
  if (cached) return Promise.resolve(cached)

  const req = strapi.get(`/api${path}`, { params: { populate: '*', ...params } })
  req.then(res => _cache.set(key, { data: res, ts: Date.now() })).catch(() => {})
  return req
}

export const invalidarCacheStrapi = () => _cache.clear()

export const getBanners = () =>
  get('/banners', { filters: { ativo: true }, sort: 'ordem:asc' })

export const getFaqs = () =>
  get('/faqs', { filters: { ativo: true }, sort: 'ordem:asc' })

export const getDepoimentos = () =>
  get('/depoimentos', { filters: { ativo: true } })

export const getHome = () =>
  get('/home')

export const getPosts = (params = {}) =>
  get('/posts', { sort: 'publicado_em:desc', ...params })

export const getPost = (slug) =>
  get('/posts', { filters: { slug } })

export const getPagina = (slug) =>
  get('/paginas', { filters: { slug } })

export default strapi
export const getEntregasAnteriores = () =>
  get('/entrega-anteriores', { filters: { ativo: true }, sort: 'ordem:asc', populate: '*' })
