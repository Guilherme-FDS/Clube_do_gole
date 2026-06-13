import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // Públicas
  { path: '/',                  name: 'Home',             component: () => import('@/views/Home.vue') },
  { path: '/produto/:id',       name: 'ProdutoDetalhe',   component: () => import('@/views/ProdutosDetalhe.vue') },

  { path: '/carrinho',          name: 'Carrinho',         component: () => import('@/views/Carrinho.vue') },
  { path: '/faq',               name: 'FAQ',              component: () => import('@/views/FAQ.vue') },
  { path: '/blog',              name: 'Blog',             component: () => import('@/views/Blog.vue') },
  { path: '/blog/:slug',        name: 'BlogPost',         component: () => import('@/views/BlogPost.vue') },

  // Institucionais
  { path: '/sobre',             name: 'Sobre',            component: () => import('@/views/Sobre.vue') },
  { path: '/contato',           name: 'Contato',          component: () => import('@/views/Contato.vue') },
  { path: '/corporativo',       name: 'Corporativo',      component: () => import('@/views/Corporativo.vue') },
  { path: '/envio-devolucoes',  name: 'EnvioDevolucoes',  component: () => import('@/views/EnvioDevolucoes.vue') },
  { path: '/politica-reembolso',name: 'PoliticaReembolso',component: () => import('@/views/PoliticaReembolso.vue') },

  // Guest only
  { path: '/login',                    name: 'Login',           component: () => import('@/views/Login.vue'),           meta: { guestOnly: true } },
  { path: '/auth/google/callback',     name: 'GoogleCallback',  component: () => import('@/views/OAuthCallback.vue'),   meta: { guestOnly: true } },
  { path: '/auth/facebook/callback',   name: 'FacebookCallback',component: () => import('@/views/OAuthCallback.vue'),   meta: { guestOnly: true } },
  { path: '/reset-password',           name: 'ResetPassword',   component: () => import('@/views/ResetPassword.vue'),   meta: { guestOnly: true } },

  // Auth required
  { path: '/checkout',       name: 'Checkout',      component: () => import('@/views/Checkout.vue'),      meta: { auth: true } },
  { path: '/meus-pedidos',   name: 'MeusPedidos',   component: () => import('@/views/MeusPedidos.vue'),   meta: { auth: true } },
  { path: '/configuracoes',  name: 'Configuracoes', component: () => import('@/views/Configuracoes.vue'), meta: { auth: true } },

  // Admin
  { path: '/admin',                     name: 'Admin',              component: () => import('@/views/admin/Admin.vue'),          meta: { admin: true } },
  { path: '/admin/vendas',              name: 'AdminVendas',        component: () => import('@/views/admin/Dashboard.vue'),      meta: { admin: true } },
  { path: '/admin/produtos',            name: 'AdminProdutos',      component: () => import('@/views/admin/Produtos.vue'),       meta: { admin: true } },

  { path: '/admin/cupons',              name: 'AdminCupons',        component: () => import('@/views/admin/Cupons.vue'),         meta: { admin: true } },
  { path: '/admin/cupons/editar/:id',   name: 'AdminEditarCupom',   component: () => import('@/views/admin/Editarcupom.vue'),    meta: { admin: true } },
  { path: '/admin/vendas/:id',          name: 'AdminDetalhesVenda', component: () => import('@/views/admin/Detalhesvenda.vue'),  meta: { admin: true } },
  { path: '/admin/assinaturas',         name: 'AdminAssinaturas',   component: () => import('@/views/admin/Assinaturas.vue'),    meta: { admin: true } },
  { path: '/admin/pagamentos',          name: 'AdminPagamentos',    component: () => import('@/views/admin/Pagamentos.vue'),     meta: { admin: true } },
  { path: '/admin/estoque',             name: 'AdminEstoque',       component: () => import('@/views/admin/Estoque.vue'),        meta: { admin: true } },
  { path: '/admin/clientes',            name: 'AdminClientes',      component: () => import('@/views/admin/Clientes.vue'),       meta: { admin: true } },

  // 404
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: (to) => {
    if (to.hash) return { el: to.hash, top: 80, behavior: 'smooth' }
    return { top: 0 }
  }
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.admin && auth.tipo !== 'admin') {
    return next(auth.logado ? '/' : '/login')
  }

  if (to.meta.auth && !auth.logado) {
    return next(`/login?redirect=${to.path}`)
  }

  if (to.meta.guestOnly && auth.logado) {
    return next(auth.tipo === 'admin' ? '/admin' : '/')
  }

  next()
})

export default router