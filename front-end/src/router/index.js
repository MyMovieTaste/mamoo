import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '../views/Index.vue'
import Signup from '../views/Signup.vue'
import Login from '../views/Login.vue'
import SignupReview from '../views/SignupReview.vue'
import MyProfile from '../views/MyProfile.vue'
import Search from '../views/Search.vue'
// import MovieDetail from '../views/MovieDetail.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/index',
    name: 'Index',
    component: Index
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
    path: '/profile',
    name: 'MyProfile',
    component: MyProfile
  },
  {
    path: '/signupreview',
    name: 'SignupReview',
    component: SignupReview
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
