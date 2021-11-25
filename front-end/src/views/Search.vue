<template>
  <div class="container justify-content-center">
    <div>
      <div v-if="searchList.length" class="row row-cols-4">
        <search-item
          v-for="movie in searchList"
          :key="movie.id"
          :movie="movie"
        ></search-item>
      </div>
      <div v-else>
        <!-- 검색결과 없을때 input바꾸면 계속 computed됨 흠.. -->
        <p>"{{ searchInput }}" 검색 결과가 없습니다.</p>
      </div>
    </div>
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
    },
    searchInput() {
      return this.$store.state.searchInput
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/scss/main.scss';

p {
    color: $gray-100;
    font-size: 2rem;
}

</style>