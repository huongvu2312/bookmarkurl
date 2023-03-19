import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

import HomeView from '../views/HomeView.vue'
import AboutView from '../views/AboutView.vue'
import SignUpView from '../views/SignUpView.vue'
import LogInView from '../views/LogInView.vue'
import BookmarkView from '../views/BookmarkView.vue'
import BookmarkNew from '../views/BookmarkNew.vue'
import BookmarkDetail from '../views/BookmarkDetail.vue'
import CategoryView from '../views/CategoryView.vue'
import CategoryNew from '../views/CategoryNew.vue'
import CategoryDetail from '../views/CategoryDetail.vue'
import MyAccountView from '../views/MyAccountView.vue'
import ChangePassword from '../views/ChangePassword.vue'

const routes = [
  {
    path: '/',
    name: 'NoPath',
    component: HomeView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/about',
    name: 'about',
    component: AboutView
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUpView
  },
  {
    path: '/log-in',
    name: 'LogIn',
    component: LogInView
  },
  {
    path: '/bookmark',
    name: 'bookmark',
    component: BookmarkView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/bookmark/new',
    name: 'BookmarkNew',
    component: BookmarkNew,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/bookmark/:bookmark_id',
    name: 'BookmarkDetail',
    component: BookmarkDetail,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/category',
    name: 'category',
    component: CategoryView,
    meta: {
      requireLogin: true
    }
  },
  ,
  {
    path: '/category/new',
    name: 'CategoryNew',
    component: CategoryNew,
    meta: {
      requireLogin: true
    }
  },
  ,
  {
    path: '/category/:category_slug',
    name: 'CategoryDetail',
    component: CategoryDetail,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/my-account',
    name: 'MyAccount',
    component: MyAccountView,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/my-account/change-password',
    name: 'ChangePassword',
    component: ChangePassword,
    meta: {
      requireLogin: true
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'LogIn' });
  } else {
    next()
  }
})

export default router
