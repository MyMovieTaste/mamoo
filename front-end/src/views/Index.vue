<template>
  <!-- esc이거 왜 제대로 작동을 안할까 -->
  <div @keyup.esc="toggleMovieDetail">    
    <recommend-list v-if="!isLogin"></recommend-list>
    <my-recommend-list v-else></my-recommend-list>
    <this-year-list-by-genre></this-year-list-by-genre>
    <top-list-by-year></top-list-by-year>

    <div class="modal" :class="{ 'showModal': isMovieDetail}">
      <div v-if="movieDetail" class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <!-- <h5 class="modal-title" id="staticBackdropLabel">Modal title</h5> -->
            <button 
              @click="toggleMovieDetail"
              type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <img src="" alt="">
            <div>
              <h4>{{ movieDetail.title }}
                <button @click="bookmark">소장하기</button>
                <button @click="bookmark">소장됨</button>
              </h4>
            </div>
            <p>{{ movieDetail.year }}</p>
            <p>평점: {{ movieDetail.vote_average }}</p>
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
import TopListByYear from '@/components/TopListByYear.vue'

export default {
  name: 'Index',
  components: {
    RecommendList,
    MyRecommendList,
    ThisYearListByGenre,
    Review,
    TopListByYear,
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
      this.setToken()
      axios({
        method: 'post',
        url: `http://127.0.0.1:8000/movies/${this.movieDetail.id}/reviews/`,
        data: review,
        headers: this.$store.state.token
      })
        .then(() => {
          this.$store.dispatch('getReviews', this.movieDetail.id)
          this.$store.dispatch('resetReviewInput')
        })
    },
    setToken() {
      this.$store.dispatch('setToken')
    },
    bookmark() {

      // this.$store.dispatch('')
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
    if (this.isLogin) {
      this.$store.dispatch('getMyRecommendList')
    }
    this.$store.dispatch('getThisYearList')
    this.$store.dispatch('getTopListByYear')
  }
}
</script>

<style>
  .showModal {display: block;}
</style>