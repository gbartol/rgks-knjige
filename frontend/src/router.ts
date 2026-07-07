import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

import { useAuth } from '@/auth/useAuth'
import ProfileEditView from './ProfileEditView.vue'
import UserSearchView from './UserSearchView.vue'
import BookSearchView from './BookSearchView.vue'
import HomeFeedView from './HomeFeedView.vue'
import MyShelvesView from './MyShelvesView.vue'


const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'feed',
    component: HomeFeedView,
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    name: 'profile',
    component: ProfileEditView,
    meta: { requiresAuth: true },
  },
  {
    path: '/users',
    name: 'users',
    component: UserSearchView,
    meta: { requiresAuth: true },
  },
  {
    path: '/books',
    name: 'book-search',
    component: BookSearchView,
    meta: { requiresAuth: true },
  },
  {
    path: '/shelves',
    name: 'my-shelves',
    component: MyShelvesView,
    meta: { requiresAuth: true },
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Guard: rute s meta.requiresAuth zahtijevaju prijavljenog korisnika.
// initAuth() se izvršava prije mountanja aplikacije (main.ts), pa je
// isAuthenticated već točan kad guard prvi put pokrene.
router.beforeEach((to) => {
  const { isAuthenticated, login } = useAuth()
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    // Pokreće preusmjeravanje na Microsoft prijavu; trenutnu navigaciju
    // otkazujemo jer preglednik ionako napušta stranicu.
    login()
    return false
  }
})

export default router
