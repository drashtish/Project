import { createRouter, createWebHistory } from 'vue-router'
import login from '../components/login.vue'
import UD from '../components/UD.vue'
import register from '../components/register.vue'
import adminlogin from '../components/adminlogin.vue'
import AD from '../components/AD.vue'
import adminsecs from '../components/adminsecs.vue'
import newsection from '../components/newsection.vue'
import updsection from '../components/updsection.vue'
import adminsbooks from '../components/adminsbooks.vue'
import newbook from '../components/newbook.vue'
import usersbooks from '../components/usersbooks.vue'
import usersnreqs from '../components/usersnreqs.vue'
import updbook from '../components/updbook.vue'
import searchsec from '../components/searchsec.vue'
import review from '../components/review.vue'
import profile from '../components/profile.vue'




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'login',
      component: login
    },
    {
      path: '/UD',
      name: 'UD',
      component: UD
    },
    {
      path: '/profile',
      name: 'profile',
      component: profile
    },
    {
      path: '/register',
      name: 'register',
      component: register
    },
    {
      path: '/adminlogin',
      name: 'adminlogin',
      component: adminlogin
    },
    {
      path: '/AD',
      name: 'AD',
      component: AD
    },
    {
      path: '/adminsecs',
      name: 'adminsecs',
      component: adminsecs
    },
    {
      path: '/newsection',
      name: 'newsection',
      component: newsection
    },
    {
      path: '/updsection/:id',
      name: 'updsection',
      component: updsection,
      props : true
    },
    {
      path: '/updbook/:id',
      name: 'updbook',
      component: updbook,
      props : true
    },
    {
      path: '/adminsbooks/:id',
      name: 'adminsbooks',
      component: adminsbooks,
      props : true
    },
    {
      path: '/newbook/:id',
      name: 'newbook',
      component: newbook,
      props : true
    },
    {
      path: '/usersbooks/:id',
      name: 'usersbooks',
      component: usersbooks,
      props : true
    },
    {
      path: '/usersnreqs/:id',
      name: 'usersnreqs',
      component: usersnreqs,
      props : true
    },
    {
      path: '/searchsec/',
      name: 'searchsec',
      component: searchsec
    },
    {
      path: '/review/:id',
      name: 'review',
      component: review,
      props : true
    }

  ]
})

export default router
