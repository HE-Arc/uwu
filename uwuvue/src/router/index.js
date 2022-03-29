import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: 'Home' }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import('../views/AboutView.vue'),
    meta: { title: 'About' }
  },
  {
    path: '/mangas/:id',
    name: 'manga',
    component: () => import('../views/MangaView.vue'),
    meta: { title: 'Mangas' }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../views/LoginView.vue'),
    meta: { title: 'Login' }
  },
  {
    path: '/signup',
    name: 'signup',
    component: () => import('../views/SignupView.vue'),
    meta: { title: 'Signup' }
  },
  {
    path: '/search/:query?',
    name: 'search',
    component: () => import('../views/SearchView.vue'),
    meta: { title: 'Manga search' }
  },
  {
    path: '/users/search/:query?',
    name: 'users-search',
    component: () => import('../views/UserSearchView.vue'),
    meta: { title: 'User search' }
  },
  {
    path: '/users/:id',
    name: 'users',
    component: () => import('../views/UserView.vue'),
    meta: { title: 'User' }
  },
  {
    path: '/users/:id/favorites',
    name: 'users-favorites',
    component: () => import('../views/UserFavorites.vue'),
    meta: { title: 'Favorites' }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
  linkActiveClass: 'active'
})

router.beforeEach(to => {
  document.title = `${to.meta.title} – uwu`
})

export default router
