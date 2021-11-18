<template>
  <div>    
    <recommend-list v-if="!isLogin"></recommend-list>
    <my-recommend-list v-else>다른 유저들이 추천받은 영화</my-recommend-list>
  </div>
</template>

<script>
import RecommendList from '@/components/RecommendList.vue'
import MyRecommendList from '@/components/MyRecommendList.vue'

export default {
  name: 'Index',
  components: {
    RecommendList,
    MyRecommendList,
  },
  data: function() {
    return {
      isLogin: false,
    }
  }
}
</script>

<style>

</style>