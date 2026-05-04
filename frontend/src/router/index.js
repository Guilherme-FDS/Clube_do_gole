import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // Públicas
  { path: '/',             name: 'Home',          component: () => import('@/views/home.vue') },
  { path: '/produto/:id',  name: 'ProdutoDetalhe',component: () => import('@/views/produtosdetalhe.vue') },
  { path: '/mixupcode',    name: 'MixUpCode',     component: () => import('@/views/mixupcode.vue') },
  { path: '/carrinho',     name: 'Carrinho',      component: () => import('@/views/carrinho.vue') },

  // Guest only
  { path: '/login',    name: 'Login',    component: () => import('@/views/login.vue'),    meta: { guestOnly: true } },
  { path: '/cadastro', name: 'Cadastro', component: () => import('@/views/cadastro.vue'), meta: { guestOnly: true } },

  // Auth required
  { path: '/checkout',      name: 'Checkout',      component: () => import('@/views/checkout.vue'),      meta: { auth: true } },
  { path: '/meus-pedidos',  name: 'MeusPedidos',   component: () => import('@/views/meuspedidos.vue'),   meta: { auth: true } },
  { path: '/configuracoes', name: 'Configuracoes', component: () => import('@/views/configuracoes.vue'), meta: { auth: true } },

  // Admin
  { path: '/admin',              name: 'AdminDashboard',    component: () => import('@/views/admin/dashboard.vue'),      meta: { admin: true } },
  { path: '/admin/produtos',     name: 'AdminProdutos',     component: () => import('@/views/admin/produtos.vue'),        meta: { admin: true } },
  { path: '/admin/produtos/:id', name: 'AdminEditarProduto',component: () => import('@/views/admin/editarprodutos.vue'),  meta: { admin: true } },
  { path: '/admin/cupons',       name: 'AdminCupons',       component: () => import('@/views/admin/cupons.vue'),          meta: { admin: true } },
  { path: '/admin/cupons/:id',   name: 'AdminEditarCupom',  component: () => import('@/views/admin/editarcupom.vue'),     meta: { admin: true } },
  { path: '/admin/vendas/:id',   name: 'AdminDetalhesVenda',component: () => import('@/views/admin/detalhesvenda.vue'),   meta: { admin: true } },

  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.admin && auth.tipo !== 'admin')
    return auth.logado ? '/' : '/login'

  if (to.meta.auth && !auth.logado)
    return `/login?redirect=${to.path}`

  if (to.meta.guestOnly && auth.logado)
    return auth.tipo === 'admin' ? '/admin' : '/'
})

export default router