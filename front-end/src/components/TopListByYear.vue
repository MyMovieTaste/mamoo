<template>
  <div>
    <h4>연도별 인기 영화</h4>
    <select @change="yearSelected" name="" id="">
      <option
        v-for="i in numOfYears" 
        :key="i"
        :value=i-1>{{2021-i+1}}</option>
    </select>
    <div class="row row-cols-4">
      <top-list-item-by-year
        v-for="movie in topListByYear"
        :key="movie.id"
        :movie="movie"
      ></top-list-item-by-year>
    </div>
  </div>
</template>

<script>
import TopListItemByYear from '@/components/TopListItemByYear.vue'

export default {
  name: 'TopListByYear',
  components: {
    TopListItemByYear
  },
  methods: {
    yearSelected(event) {
      this.$store.dispatch('yearSelected', event.target.value)
      // 왜 이렇게 해야되지 리뷰삭제는 바로 반영 되는뎁
      this.$store.dispatch('getTopListByYear')
    }
  },
  computed: {
    topListByYear() {
      return this.$store.state.topListByYear
    },
    numOfYears() {
      return this.$store.state.numOfYears
    }
  },
}
</script>

<style>

</style>