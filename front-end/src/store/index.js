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
  },
  mutations: {
    LOGIN(state) {
      state.isLogin = true
    },
    LOGOUT(state) {
      state.isLogin = false
      localStorage.removeItem('jwt')
    },
    GETTHISYEARLIST(state, movies) {
      state.thisYearList = movies
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
          console.log(res)
          commit('GETTHISYEARLIST', res.data)
        })
        .catch()
    }
  },
  getters: {
    isLogin (state) {
      return state.isLogin
    }
  },
  modules: {
  }
})
