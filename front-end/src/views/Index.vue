<template>
  <!-- esc이거 왜 제대로 작동을 안할까 -->
  <div @keyup.esc="toggleMovieDetail">
    <div class="d-flex flex-column">
      <div class="mb-3">
        <recommend-list v-if="!isLogin"></recommend-list>
        <my-recommend-list v-else></my-recommend-list>
      </div>
      <div class="mb-3">
        <this-year-list-by-genre></this-year-list-by-genre>
      </div>
      <div class="mb-3">
        <top-list-by-year></top-list-by-year>
      </div>
    </div>
    <div class="modal" :class="{ 'showModal': isMovieDetail }">
      <div v-if="movieDetail" class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <button 
              @click="toggleMovieDetail" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close">
            </button>
          </div>
          <div class="modal-body d-flex">
            <div class="me-5">
              <img :src="posterPath"  alt="" class="card-img-top">
            </div>
            <div class="">
            <div class="d-flex mt-3 justify-content-between">
              <h1> {{ movieDetail.title }} </h1>
              <div class="me-2">
                <a href="#" @click="bookmark"><img src="../assets/Bookmark.svg" class="bookmark" alt=""></a>
                <!-- <a href="#" @click="bookmark"><img src="../assets/Bookmark_fill.svg" alt=""></a> -->
              </div>
            </div>
            <div class="d-flex secondary mb-3 info">
              <p class="me-3">개봉연도  {{ movieDetail.year }}</p>
              <p>평균평점  {{ movieDetail.vote_average }}</p>
            </div>
            <div>
              <p class="mb-5">{{ movieDetail.overview }}</p>
            </div>
            <div class="d-flex flex-column">
              <h4 class="mb-3">리뷰남기기</h4>
              <!-- v-model로 하는게 맞나 -->
              <div class="mb-2 row">
                <label for="inputPassword" class="col-3 col-form-label">평점</label>
                <div class="col-9">
                  <select class="form-select" v-model="rate" name="rank" id="rate" aria-label="Default select example">
                    <option selected>이 영화 어떠셨나요?</option>
                    <option value="5">★★★★★</option>
                    <option value="4">★★★★</option>
                    <option value="3">★★★</option>
                    <option value="2">★★</option>
                    <option value="1">★</option>
                  </select>
                </div>
              </div>
              <div class="form-floating">
                <textarea class="form-control mt-2" placeholder="리뷰를 남겨보세요" id="floatingTextarea"
                  :value="reviewInput"
                  @keyup="reviewInputChange"
                ></textarea>
                <label for="floatingTextarea">Comments</label>
              </div>
              <div class="d-flex justify-content-end">
                <button @click="reviewSubmit" type="button" class="btn btn-primary mt-3">리뷰작성</button>
              </div>
            </div>
            <hr>
            <div>
              <h4>리뷰게시판</h4>
              <review
                v-for="review in reviews"
                :review="review"
                :key="review.id"
              ></review>
            </div>
            <hr>
          <div class="modal-footer">
            <button @click="toggleMovieDetail" type="button" class="btn btn-outline">닫기</button>
          </div>
          </div>
          </div>
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
        // 로그인 안했을때
        // 역시 에러 구분하는거 어떻게 하는지 잘 모르겠다
        .catch(err => {
          console.log(err)
          alert('리뷰를 남기려면 로그인해주세요.')
        })
    },
    setToken() {
      this.$store.dispatch('setToken')
    },
    bookmark() {
      this.$store.dispatch('bookmark', this.movieDetail.id)
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
    posterPath() {
      const IMG_URL = 'https://image.tmdb.org/t/p/w500'
      return `${IMG_URL}/${this.movieDetail.poster_path}`
    },    
    userInfo() {
      return this.$store.state.userInfo
    },
    isLoginAndIsBookmarked() {
      if (this.isLogin) {
        if (this.userInfo.bookmarked_movies.includes(this.movieDetail.id)) {
          return 'isLoginisBookmarked'
        } else {
          return 'isLoginNotBookmarked'
        }
      } else {
        return null
      }
    }
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


<style lang="scss" scoped>
@import '@/scss/main.scss';

.info {
  width: 350px;
}

.bookmark {
  width: 2.5rem;
}

.modal-dialog {
  max-width: 900px;
}

.card-img-top {
  width: 400px;
}

.secondary {
  color: $secondary;
}

.modal {
  color: $gray-100;

}
.modal-content {
  color: $gray-100;
}
.modal-body {
 color: $gray-100;
 padding: 0 2rem 0 2rem;
}

.modal-header{
  border-bottom: none;
}
.showModal { display: block; }

.btn-outline {
  color: $primary;
  border-color: $primary;
}
</style>