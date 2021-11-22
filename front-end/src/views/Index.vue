<template>
  <div>    
    <recommend-list v-if="!isLogin"></recommend-list>
    <my-recommend-list v-else></my-recommend-list>
    <this-year-list-by-genre></this-year-list-by-genre>

    <div class="modal" :class="{ 'showModal': isMovieDetail}">
    
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <!-- <h5 class="modal-title" id="staticBackdropLabel">Modal title</h5> -->
            <button 
              @click="toggleMovieDetail"
              type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <img src="" alt="">
            <h4 v-if="movieDetail">{{ movieDetail.title }}</h4>
            <!-- v-model로 하는게 맞나 -->
            <select v-model="rate" name="rank" id="rate">
              <option value="5">★★★★★</option>
              <option value="4">★★★★</option>
              <option value="3">★★★</option>
              <option value="2">★★</option>
              <option value="1">★</option>
            </select>
            <textarea 
              :review-input="reviewInput"
              @keyup="reviewInputChange"
            ></textarea>
            <button @click="reviewSubmit">작성</button>
          </div>
          <!-- <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary">Understood</button>
          </div> -->
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import RecommendList from '@/components/RecommendList.vue'
import MyRecommendList from '@/components/MyRecommendList.vue'
import { mapGetters } from 'vuex'
import ThisYearListByGenre from '@/components/ThisYearListByGenre.vue'
import axios from 'axios'

export default {
  name: 'Index',
  components: {
    RecommendList,
    MyRecommendList,
    ThisYearListByGenre
  },
  data: function () {
    return {
    //   isLogin: this.$store.state.isLogin
      rate: null,
    }
  },
  methods: {
    toggleMovieDetail () {
      // if (this.$store.state.isMovieDetail) {
        this.$store.state.isMovieDetail = false
      // } else {
      //   this.$store.state.isMovieDetail = true
      // }
      // console.log(this.$store.state.isMovieDetail)
    },
    reviewInputChange(event) {
      this.$store.state.reviewInput = event.target.value
      console.log(this.$store.state.reviewInput)
    },
    reviewSubmit() {
      const review = {
        content: this.reviewInput,
        movie_title: this.movieDetail.id,
        rank: this.rate,
      }
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/${this.movieDetail.id}/reviews/`,
        data: review,
        headers: this.setToken()

      })
    },
    setToken() {
      const token = localStorage.getItem('jwt')
      const headers = {
        Authorization: `JWT ${token}`
      }
      return headers
    }
  },
  computed: {
    ...mapGetters([
      'isLogin'
    ]),
    isMovieDetail() {
      return this.$store.state.isMovieDetail
    }
    ,movieDetail() {
      return this.$store.state.movieDetail
    },
    reviewInput() {
      return this.$store.state.reviewInput
    }
  },
  created: function() {
    this.$store.dispatch('getThisYearList')
  }
}
</script>

<style>
  .showModal {display: block;}
</style>