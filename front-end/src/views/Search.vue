<template>
  <div class="row row-cols-4">
    <search-item
      v-for="movie in searchList"
      :key="movie.id"
      :movie="movie"
    ></search-item>
  </div>
</template>

<script>
import SearchItem from '@/components/SearchItem.vue'

export default {
  name: 'Search',
  components: {
    SearchItem,
  },
  computed: {
    searchList() {
      return this.$store.state.searchList
    }
  }
}
</script>

<style>

</style>