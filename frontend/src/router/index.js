import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  // Públicas
  { path: '/',             name: 'Home',          component: () => import('@/views/Home.vue') },
  { path: '/produto/:id',  name: 'ProdutoDetalhe',component: () => import('@/views/ProdutosDetalhe.vue') },
  { path: '/mixupcode',    name: 'MixUpCode',     component: () => import('@/views/Mixupcode.vue') },
  { path: '/carrinho',     name: 'Carrinho',      component: () => import('@/views/Carrinho.vue') },

  // Guest only
  { path: '/login',    name: 'Login',    component: () => import('@/views/Login.vue'),    meta: { guestOnly: true } },
  { path: '/cadastro', name: 'Cadastro', component: () => import('@/views/Cadastro.vue'), meta: { guestOnly: true } },

  // Auth required
  { path: '/checkout',      name: 'Checkout',      component: () => import('@/views/Checkout.vue'),      meta: { auth: true } },
  { path: '/meus-pedidos',  name: 'MeusPedidos',   component: () => import('@/views/MeusPedidos.vue'),   meta: { auth: true } },
  { path: '/configuracoes', name: 'Configuracoes', component: () => import('@/views/Configuracoes.vue'), meta: { auth: true } },

  // Admin
  { path: '/admin',                          name: 'Admin',              component: () => import('@/views/admin/Admin.vue'),           meta: { admin: true } },
  { path: '/admin/vendas',                   name: 'AdminVendas',        component: () => import('@/views/admin/Dashboard.vue'),       meta: { admin: true } },
  { path: '/admin/produtos',                 name: 'AdminProdutos',      component: () => import('@/views/admin/Produtos.vue'),        meta: { admin: true } },
  { path: '/admin/produtos/editar/:id',      name: 'AdminEditarProduto', component: () => import('@/views/admin/Editarprodutos.vue'),  meta: { admin: true } },
  { path: '/admin/cupons',                   name: 'AdminCupons',        component: () => import('@/views/admin/Cupons.vue'),          meta: { admin: true } },
  { path: '/admin/cupons/editar/:id',        name: 'AdminEditarCupom',   component: () => import('@/views/admin/Editarcupom.vue'),     meta: { admin: true } },
  { path: '/admin/vendas/:id',               name: 'AdminDetalhesVenda', component: () => import('@/views/admin/Detalhesvenda.vue'),   meta: { admin: true } },

  // 404 - Redirecionar para home
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  
  // Admin check
  if (to.meta.admin && auth.tipo !== 'admin') {
    return next(auth.logado ? '/' : '/login')
  }
  
  // Auth required check
  if (to.meta.auth && !auth.logado) {
    return next(`/login?redirect=${to.path}`)
  }
  
  // Guest only check (usuário logado não pode acessar login/cadastro)
  if (to.meta.guestOnly && auth.logado) {
    return next(auth.tipo === 'admin' ? '/admin' : '/')
  }
  
  next()
})

export default router
