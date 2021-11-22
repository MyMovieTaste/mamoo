<template>
  <div>    
    <recommend-list v-if="!isLogin"></recommend-list>
    <my-recommend-list v-else></my-recommend-list>
    <this-year-list-by-genre></this-year-list-by-genre>
  </div>
</template>

<script>
import RecommendList from '@/components/RecommendList.vue'
import MyRecommendList from '@/components/MyRecommendList.vue'
import { mapGetters } from 'vuex'
import ThisYearListByGenre from '@/components/ThisYearListByGenre.vue'

export default {
  name: 'Index',
  components: {
    RecommendList,
    MyRecommendList,
    ThisYearListByGenre
  },
  data: function () {
    return {
    //   isLogin: this.$store.state.isLogin
    }
  },
  methods: {

  },
  computed: {
    ...mapGetters([
      'isLogin'
    ]),
  },
  created: function() {
    this.$store.dispatch('getThisYearList')
  }
}
</script>

<style>

</style>