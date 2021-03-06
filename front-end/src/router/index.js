import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '../views/Index.vue'
import Signup from '../views/Signup.vue'
import Login from '../views/Login.vue'
// import SignupReview from '../views/SignupReview.vue'
import Search from '../views/Search.vue'
// import MovieDetail from '../views/MovieDetail.vue'
import Profile from '../views/Profile.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '',
    name: 'Index',
    component: Index,
    // beforeEnter: function(to, from, next) {

    // }

  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup
  },
  // {
  //   path: '/movie-detail',
  //   name: 'MovieDetail',
  //   component: MovieDetail
  // },
  {
    path: '/search',
    name: 'Search',
    component: Search
  },
  {
    path: '/profile/:personname',
    name: 'Profile',
    component: Profile,
  },
  // {
  //   path: '/signupreview',
  //   name: 'SignupReview',
  //   component: SignupReview
  // }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// routes.beforeEach((to, from, next) => {

// })

export default router
