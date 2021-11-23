<template>
  <div>
    <p>{{ username }}님께 추천하는 영화</p>
    <my-recommend-list-item
      v-for="movie in myRecommendList"
      :key="movie.id"
      :movie="movie"
    ></my-recommend-list-item>
  </div>
</template>

<script>
import MyRecommendListItem from '@/components/MyRecommendListItem.vue'

export default {
  name: 'MyRecommendList',
  components: {
    MyRecommendListItem
  },
  data: function () {
    return {
      // username: this.$store.state.username
    }
  },
  computed: {
    username () {
      return this.$store.state.username
    },
    myRecommendList () {
      return this.$store.state.myRecommendList
    }
  }
}
</script>

<style>

</style>