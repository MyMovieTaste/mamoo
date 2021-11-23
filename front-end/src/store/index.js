import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import axios from 'axios'

export default new Vuex.Store({
  state: {
    isLogin: false,
    username: null,
    thisYearList: [],
    isMovieDetail: false,
    movieDetail: null,
    reviewInput: null,
    reviews: [],
    myRecommendList: [],
    token: null,
  },
  mutations: {
    LOGIN(state) {
      state.isLogin = true
    },
    SETTOKEN(state) {
      const token = localStorage.getItem('jwt')
      const headers = {
        Authorization: `JWT ${token}`
      }
      state.token = headers 
    },
    LOGOUT(state) {
      state.isLogin = false
      localStorage.removeItem('jwt')
    },
    GETTHISYEARLIST(state, movies) {
      state.thisYearList = movies
    },
    TOGGLEMOVIEDETAIL(state) {
      if (state.isMovieDetail) {
        state.isMovieDetail = false
      } else {
        state.isMovieDetail = true
      }
    },
    GETMOVIEDETAIL(state, movie) {
      state.movieDetail = movie
    },
    REVIEWINPUTCHANGE(state, value) {
      state.reviewInput = value
    },
    GETREVIEWS(state, reviews) {
      state.reviews = reviews
    },
    RESETREVIEWINPUT(state) {
      state.reviewInput = null
    },
    GETMYRECOMMENDLIST(state, movies) {
      state.myRecommendList = movies
    }
  },
  actions: {
    login({ commit }) {
      commit('LOGIN')
    },
    logout({ commit }) {
      commit('LOGOUT')
    },
    getThisYearList({ commit }) {
      const API_URL = 'http://127.0.0.1:8000/movies/'
      axios.get(`${API_URL}`)
        .then(res => {
          commit('GETTHISYEARLIST', res.data)
        })
        .catch()
    },
    toggleMovieDetail({commit}) {
      commit('TOGGLEMOVIEDETAIL')
    },
    getMovieDetail({commit}, movieId) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${movieId}/`,
      })
        .then(res => {
          commit('GETMOVIEDETAIL', res.data)
        })
    },
    reviewInputChange({commit}, value) {
      commit('REVIEWINPUTCHANGE', value)
    },
    getReviews({commit}, movieId) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/movies/${movieId}/reviews/`
      })
        .then(res => {
          commit('GETREVIEWS', res.data)
        })
    },
    resetReviewInput({commit}){
      commit('RESETREVIEWINPUT')
    },
    setToken({commit}) {
      commit('SETTOKEN')
    },
    getMyRecommendList({commit}) {
      console.log(this.state.token)
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/movie_recommend/',
        headers: this.state.token
      })
        .then(res => {
          console.log(res)
          commit('GETMYRECOMMENDLIST', res.data)
        })
    },
  },
  getters: {
    isLogin (state) {
      return state.isLogin
    }
  },
  modules: {
  }
})
