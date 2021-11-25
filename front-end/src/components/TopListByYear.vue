<template>
  <div>
    <div class="d-flex mb-3">
      <h4 class="mb-3">연도별 인기 영화</h4>
      <div class="ms-3">
        <select @change="yearSelected" class="form-select">
          <option
            v-for="i in numOfYears" 
            :key="i"
            :value=i-1>{{2021-i+1}}</option>
        </select>
      </div>
    </div>
    <div class="d-flex flex-wrap">
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

<style lang="scss" scoped>
@import '@/scss/main.scss';
h4 {
  line-height: 1;
  font-size: 30px;
  color: $gray-100;
}

.card-deck {
  position: relative;
  width: 100%;
  overflow: hidden;
  @include clearfix();

}
.card {
  background-color: $gray-900;
  color: $gray-200; 
  &:hover {
    cursor: pointer;
  }
}

</style>