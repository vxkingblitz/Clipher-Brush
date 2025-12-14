import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'

const routes = [
  {
    path: '/',
    name: 'LoadingScreen',
    component: () => import('../views/LoadingScreen.vue')
  },
  {
    path: '/feed/:tab?',
    name: 'Feed',
    component: () => import('../views/FeedPage.vue'),
    props: true
  },
  {
    path: '/createNew',
    name: 'CreatePainting',
    component: () => import('../views/CreatePaintingPage.vue'),
  },
  {
    path: '/profile/:tab?',
    name: 'Profile',
    component: () => import('../views/ProfilePage.vue'),
    props: true
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// router.beforeEach((to, from, next) => {
//   const auth = useAuthStore()
  
//   if (to.meta.requiresAuth && !auth.isAuthenticated) {
//     next('/')
//   } else {
//     next()
//   }
// })

export default router