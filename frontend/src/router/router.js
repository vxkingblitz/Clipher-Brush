import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'LoadingScreen',
    component: () => import('../views/LoadingScreen.vue')
  },
  {
    path: '/home',
    name: 'HomePage',
    component: () => import('../views/HomePage.vue'),
    meta: { requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/')
  } else {
    next()
  }
})

export default router