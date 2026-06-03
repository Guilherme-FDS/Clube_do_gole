import axios from 'axios'

const strapi = axios.create({
  baseURL: import.meta.env.VITE_STRAPI_URL || 'http://localhost:1337',
})

const get = (path, params = {}) =>
  strapi.get(`/api${path}`, { params: { populate: '*', ...params } })

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