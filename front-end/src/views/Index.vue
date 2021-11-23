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
              :value="reviewInput"
              @keyup="reviewInputChange"
            ></textarea>
            <button @click="reviewSubmit">작성</button>
            <hr>
            <h4>리뷰</h4>
            <review
              v-for="review in reviews"
              :review="review"
              :key="review.id"
            ></review>
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
import Review from '@/components/Review.vue'

export default {
  name: 'Index',
  components: {
    RecommendList,
    MyRecommendList,
    ThisYearListByGenre,
    Review
  },
  data: function () {
    return {
    //   isLogin: this.$store.state.isLogin
      rate: null,
    }
  },
  methods: {
    toggleMovieDetail () {
        this.$store.dispatch('toggleMovieDetail')
    },
    reviewInputChange(event) {
      this.$store.dispatch('reviewInputChange', event.target.value)
    },
    reviewSubmit() {
      const review = {
        content: this.reviewInput,
        movie_title: this.movieDetail.title,
        rank: this.rate,
      }
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/${this.movieDetail.id}/reviews/`,
        data: review,
        headers: this.setToken()
      })
        .then(() => {
          this.$store.dispatch('getReviews', this.movieDetail.id)
          this.$store.dispatch('resetReviewInput')
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
    },
    movieDetail() {
      return this.$store.state.movieDetail
    },
    reviewInput() {
      return this.$store.state.reviewInput
    },
    reviews() {
      return this.$store.state.reviews
    },
  },
  created: function() {
    this.$store.dispatch('getThisYearList')
    if (this.isLogin) {
      this.$store.dispatch('getMyRecommendList')
    }
  }

}
</script>

<style>
  .showModal {display: block;}
</style>