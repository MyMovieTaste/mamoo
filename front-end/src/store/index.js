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
    genreSelected: 5,
    yearSelected: 0,
    topListByYear: [],
    numOfYears: null,
    userId: null,
    isRevising: false,
    reviewReviseInput: null,
    revisingId: null,
    deleteConfirmation: false,
    searchList: [],
    userInfo: [],
    person: null,
    searchInput: null,
    // bookmarkedId: []
    isBookmarked: false,
  },
  mutations: {
    LOGIN(state) {
      state.isLogin = true
    },
    GETUSERINFO(state, userInfo) {
      state.username = userInfo.username
      state.userId = userInfo.userId
    },
    GETUSERINFO2(state, userInfo) {
      state.userInfo = userInfo
    },
    SETTOKEN(state) {
      const token = sessionStorage.getItem('jwt')
      const headers = {
        Authorization: `JWT ${token}`
      }
      state.token = headers 
    },
    LOGOUT(state) {
      state.isLogin = false
      sessionStorage.removeItem('jwt')
      state.username = null
      state.userId = null
      state.userInfo = []
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
      console.log(movie)
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
    },
    GENRESELECTED(state, genreNum) {
      state.genreSelected = genreNum
    },
    GETTOPLISTBYYEAR(state, movies) {
      state.topListByYear = movies
    },
    GETNUMOFYEARS(state, numOfYears) {
      state.numOfYears = numOfYears
    },
    YEARSELECTED(state, year) {
      state.yearSelected = year
    },
    TOGGLEREVISE(state, reviseInfo) {
      if (state.isRevising) {
        state.isRevising = false
        state.revisingId = null
      } else {
        state.isRevising = true
        state.reviewReviseInput = reviseInfo.content
        state.revisingId = reviseInfo.reviewId
      }
    },
    REVIEWREVISEINPUTCHANGE(state, value) {
      state.reviewReviseInput = value
    },
    REVIEWREVISESUBMIT(state, reviewReviseInfo) {
      // todo?????? ?????? ????????? forEach??? === id ????????? ??? ????????? ?????? ?????????
      const idx = state.reviews.indexOf(reviewReviseInfo.review)
      state.reviews[idx].content = state.reviewReviseInput
    },
    DELETEREVIEW(state, review){
      state.deleteConfirmation = false
      const idx = state.reviews.indexOf(review)
      state.reviews.splice(idx, 1)
    },
    TOGGLEDELETECONFIRMATION(state) {
      if (state.deleteConfirmation) {
        state.deleteConfirmation = false
      } else {
        state.deleteConfirmation = true
      }
    },
    SEARCH(state, movies){
      state.searchList = movies
    },
    BOOKMARK(state, movieId){
      if (state.userInfo.bookmarked_movies.includes(movieId)) {
        const idx = state.userInfo.bookmarked_movies.indexOf(movieId)
        state.userInfo.bookmarked_movies.splice(idx, 1)
      } else {
        state.userInfo.bookmarked_movies.push(movieId)
      }
    },
    GETPROFILE(state, person) {
      state.person = person
    },
    FOLLOW(state) {
      if (state.person.followers.includes(state.username)) {
        const idx = state.person.followings.indexOf(state.username)
        state.person.followers.splice(idx, 1)
        state.person.followers_count -= 1
      } else {
        state.person.followers.push(state.username)
        state.person.followers_count += 1
      }
    },
    SEARCHINPUTCHANGE(state, value) {
      state.searchInput = value
      if (state.searchInput === '') {
        state.searchInput = null
      }
    },
    // BOOKMARKEDID(state, movies) {
    //   movies.forEach(movie => {
    //     state.bookmarkedId.push(movie.id)
    //   })
    // }
    GETISBOOKMARKED(state, movieAndUser) {
      console.log(movieAndUser)
      if (movieAndUser.movie.bookmarked_users.includes(movieAndUser.user.id)) {
        state.isBookmarked = true
      } else {
        state.isBookmarked = false
      }
    },
    CHANGEBOOKMARKED(state) {
      if (state.isBookmarked === true) {
        state.isBookmarked = false
      } else {
        state.isBookmarked = true
      }
    }
  },
  actions: {
    login({ commit }) {
      commit('LOGIN')
    },
    logout({ commit }) {
      commit('LOGOUT')
    },
    changeIsLogin({commit}) {
      commit('CHANGEISLOGIN')
    },
    getUserInfo({commit}, userInfo) {
      commit('GETUSERINFO', userInfo)
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/${userInfo.username}/`,
      })
        .then(res => {
          commit('GETUSERINFO2', res.data)
        })
    },
    getThisYearList({ commit }) {
      const API_URL = 'http://127.0.0.1:8000/movies/recent_movie_by_genre/'
      axios.get(`${API_URL}`)
        .then(res => {
          const genreNum = this.state.genreSelected
          commit('GETTHISYEARLIST', res.data[genreNum].movies_by_genre)
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
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/movie_recommend/',
        headers: this.state.token
      })
        .then(res => {
          commit('GETMYRECOMMENDLIST', res.data)
        })
    },
    genreSelected({commit}, genreNum) {
      commit('GENRESELECTED', genreNum)
    },
    getTopListByYear({commit}) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/best_vote_movie_by_year/'
      })
        .then(res => {
          commit('GETNUMOFYEARS', res.data.length)
          commit('GETTOPLISTBYYEAR', res.data[this.state.yearSelected].movies_by_year)
        })
    },
    yearSelected({commit}, year) {
      commit('YEARSELECTED', year)
    },
    toggleRevise({commit}, reviseInfo) {
      commit('TOGGLEREVISE', reviseInfo)
    },
    reviewReviseInputChange({commit}, value) {
      commit('REVIEWREVISEINPUTCHANGE', value)
    },
    reviewReviseSubmit({commit}, reviewReviseInfo) {
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/movies/reviews/${reviewReviseInfo.review.id}/`,
        data: { rank: reviewReviseInfo.rate, content: reviewReviseInfo.content },
        headers: this.state.token
      })
        .then(() => {
          commit('REVIEWREVISESUBMIT', reviewReviseInfo)
        })
    },
    deleteReview({commit}, review) {
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/movies/reviews/${review.id}/`,
        headers: this.state.token
      })
        .then(() => {
          commit('DELETEREVIEW', review)
        })
    },
    toggleDeleteConfirmation({commit}) {
      commit('TOGGLEDELETECONFIRMATION')
    },
    search({commit}, input) {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/movies/search/',
        params: { keyword: input }
      })
        .then(res => {
          console.log(res)
          commit('SEARCH', res.data)
        })
        .catch(() => {
          alert('???????????? ???????????????.')
        })
    },
    bookmark({commit}, movieId) {
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/${movieId}/bookmarks/`,
        headers: this.state.token
      })
        .then(() => {
          commit('BOOKMARK', movieId)
          commit('CHANGEBOOKMARKED')
        })
    },
    getProfile({commit}, personname) {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/${personname}/`,
      })
        .then(res => {
          commit('GETPROFILE', res.data)
        })
        .catch(err => {
          alert(err)
        })
    },
    follow({commit}, personInfo) {
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/accounts/${personInfo.id}/follow/`,
        // headers ?????? ??????!!!! ????????? ?????????????????? ?????? ???????????????!! 
        headers: this.state.token
      })
        .then(() => {
          commit('FOLLOW')
        })
    },
    searchInputChange({commit}, value) {
      commit('SEARCHINPUTCHANGE', value)
    },
    // bookmarkedId({commit}, movies) {
    //   commit('BOOKMARKEDID', movies)
    // }
    getIsBookmarked({commit}, movieAndUser) {
      commit('GETISBOOKMARKED', movieAndUser)
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
