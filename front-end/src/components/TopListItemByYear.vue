<template>
  <div class="col">
    <div class="card d-block" style="width: 18rem;"
      @click="[toggleMovieDetail(), getMovieDetail(), getReviews()]"
    >
      <!-- <router-link :to="{ name: 'MovieDetail' }"> -->
        <img :src="posterPath" alt="" class="card-img-top">
        <div class="card-body">
          <h5 class="card-title">{{ movie.title }}</h5>
          <p class="card-text">{{ movie.popularity }}</p>
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">
            <!-- <movie-detail :movieId="movie.id"></movie-detail> -->
          </li>
        </ul>
        
        <!-- <div class="card-body"> -->
          <!-- <a href="#" class="card-link">Another link</a> -->
        <!-- </div> -->
      <!-- </router-link>   -->
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

<style>

</style>