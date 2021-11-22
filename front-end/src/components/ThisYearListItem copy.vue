<template>
  <div class="col">
    <div class="card d-block" style="width: 18rem;"
      @click="moveToDetail"
    >
      <!-- <router-link :to="{ name: 'MovieDetail' }"> -->
        <img :src="posterPath" alt="" class="card-img-top">
        <div class="card-body">
          <h5 class="card-title">{{ movie.title }}</h5>
          <p class="card-text">Some quick example text to build on the card title and make up the bulk of the card's content.</p>
        </div>
        <ul class="list-group list-group-flush">
          <li class="list-group-item">An item</li>
        </ul>
        <!-- <div class="card-body"> -->
          <!-- <a href="#" class="card-link">Another link</a> -->
        <!-- </div> -->
      <!-- </router-link>   -->
    </div>
  </div>

</template>

<script>
export default {
  name: 'ThisYearListItem',
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
      
      this.$router.push({ name: 'MovieDetail' })
    }
  }
}
</script>

<style>

</style>