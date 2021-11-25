<template>
  <div class="col-2 mb-3">
    <div class="card" style="width: 18rem;"
      @click="[toggleMovieDetail(), getMovieDetail(), getReviews()]"
    >
      <!-- <router-link :to="{ name: 'MovieDetail' }"> -->
        <img :src="posterPath" alt="" class="card-img-top">
        <div class="card-body">
          <!-- <p class="card-text btn">개봉 | {{ movie.year_id }}</p> -->
          <p class="card-text btn">
            <span>평균평점</span>
            <img src="../assets/Star Fill Sec.svg" alt="" class="icon">
            <span>{{ movie.vote_average }}</span>
          </p>
          <p class="card-text btn">
            <span>50년 역대랭킹</span>
            <img src="../assets/Flag Fill Sec.svg" alt="" class="icon">
            <span>{{ movie.ranking }}</span>
          </p>
          <h5 class="card-title">{{ movie.title }}</h5>
          <!-- <p class="card-text">인기도 | {{ movie.popularity }}</p>
          <p class="card-text">투표수 | {{ movie.vote_count }}</p>
          <p class="card-text">개봉일 | {{ movie.release_date }}</p> -->
        </div>
    </div>
  </div>

</template>

<script>
// import MovieDetail from '@/components/MovieDetail.vue'
// import axios from 'axios'

export default {
  name: 'TopListItemByYear',
  components: {
    // MovieDetail,
  },
  props: {
    movie: Object
  },
  data: function () {
    const IMG_URL = 'https://image.tmdb.org/t/p/w500'
    return {
      posterPath: `${IMG_URL}/${this.movie.poster_path}`
    }
  },
  methods: {
    moveToDetail() {
      console.log(this.movie.id)
      this.$router.push({ name: 'MovieDetail' })
    },
    toggleMovieDetail () {
        this.$store.dispatch('toggleMovieDetail')
    },
    getMovieDetail() {
      this.$store.dispatch('getMovieDetail', this.movie.id)
    },
    getReviews() {
      const movieId = this.movie.id
      this.$store.dispatch('getReviews', movieId)
    }
  },
}
</script>


<style lang="scss" scoped>
@import '@/scss/main.scss';

.card {
  background-color: $gray-900;
  color: $gray-200; 
  &:hover {
    cursor: pointer;
  }
}
.card-img-top {
  height: 400px;
  object-fit: cover;
}
.card-title {
  font-size: 1.3rem;
}
.card-text {
  font-size: 0.8rem;
  color: $gray-500;
}
.btn {
  color: $secondary;
  border: $btn-border-width solid $secondary;
  border-radius: 1rem;
  &:hover {
    background-color: $gray-900;
    color: $secondary;
    text-decoration: if($link-hover-decoration == underline, none, null);
  }
}
.btn:first-child {
  margin-right:0.5rem;
}
.icon {
  width: 1rem;
}
</style>