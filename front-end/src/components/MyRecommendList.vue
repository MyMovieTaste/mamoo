<template>
  <div>
    <h4>{{ username }}님께 추천하는 영화</h4>
    <div class="d-flex flex-wrap">
      <my-recommend-list-item
        v-for="movie in myRecommendList"
        :key="movie.id"
        :movie="movie"
      ></my-recommend-list-item>
      </div>
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