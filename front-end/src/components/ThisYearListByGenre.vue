<template>
  <div>
    <p>올해 박스오피스 순위</p>
    <div class="row row-cols-4">
      <this-year-list-item
        v-for="movie in thisYearList"
        :key="movie.id"
        :movie="movie"
      ></this-year-list-item>
    </div>
  </div>
</template>

<script>
import ThisYearListItem from '@/components/ThisYearListItem.vue'

export default {
  name: 'ThisYearListByGenre',
  components: {
    ThisYearListItem
  },
  computed: {
    thisYearList() {
      return this.$store.state.thisYearList
    }
  },
}
</script>

<style>

</style>