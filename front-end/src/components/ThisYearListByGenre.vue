<template>
  <div>
    <p></p>
    <h4>올해 박스오피스 순위</h4>
    <select @change="genreSelected" name="" id="">
      <option value=16>가족</option>
      <option value=4>공포</option>
      <option value=11>다큐멘터리</option>
      <option value=3>드라마</option>
      <option value=15>로맨스</option>
      <option value=0>모험</option>
      <option value=13>미스터리</option>
      <option value=10>범죄</option>
      <option value=12>SF</option>
      <option value=8>서부</option>
      <option value=9>스릴러</option>
      <option value=2>애니메이션</option>
      <option value=5 selected>액션</option>
      <option value=7>역사</option>
      <option value=14>음악</option>
      <option value=17>전쟁</option>
      <option value=6>코미디</option>
      <option value=18>TV 영화</option>
      <option value=1>판타지</option>
    </select>
    <div 
      v-if="thisYearList[0]"
      class="row row-cols-4">
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
  methods: {
    genreSelected(event) {
      this.$store.dispatch('genreSelected',event.target.value)
      // computed로 안되서 실행했다.. 으.... 왜 안될까..
      this.$store.dispatch('getThisYearList')
    }
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