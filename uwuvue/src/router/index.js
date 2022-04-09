import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('../views/HomeView.vue'),
    meta: { title: 'Home' }
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
    path: '/profile',
    name: 'profile',
    component: () => import('../views/UserView.vue'),
    meta: { title: 'User profile' }
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
    component: () => import('../views/UserFavoritesView.vue'),
    meta: { title: 'Favorites' }
  },
  {
    path: '/users/:id/readed',
    name: 'users-readed',
    component: () => import('../views/UserReadedView.vue'),
    meta: { title: 'Readed' }
  },
  {
    path: '/profile/favorites',
    name: 'profile-favorites',
    component: () => import('../views/UserFavoritesView.vue'),
    meta: { title: 'Favorites' }
  },
  {
    path: '/profile/readed',
    name: 'profile-readed',
    component: () => import('../views/UserReadedView.vue'),
    meta: { title: 'Readed' }
  },
  {
    path: '/profile/friends',
    name: 'users-friends',
    component: () => import('../views/UserFriendsView.vue'),
    meta: { title: 'Friends' }
  },
  {
    path: '/profile/requests',
    name: 'users-requests',
    component: () => import('../views/FriendRequestView.vue'),
    meta: { title: 'Requests' }
  },
  {
    path: '/mangas/add',
    name: 'add-mangas',
    component: () => import('../views/AddMangaView.vue'),
    meta: { title: 'Add manga' }
  },
  {
    path: '/mangas/:id/edit',
    name: 'modify-manga',
    component: () => import('../views/ModifyMangaView.vue'),
    meta: { title: 'Edit manga' }
  },
  {
    path: '/mangas/:id/add',
    name: 'add-chapters',
    component: () => import('../views/AddChapterView.vue'),
    meta: { title: 'Add chapter' }
  },
  {
    path: '/:catchAll(.*)',
    name: '404',
    component: () => import('../views/404View.vue'),
    meta: { title: '404' }
  }
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
