<template>
  <div v-if="personInfo">
    {{ personInfo }}
    <p>{{ personInfo.username }}</p>
    <span>팔로워: {{ personInfo.followers_count }}</span> | 
    <span>팔로잉: {{ personInfo.followings_count }}</span>
    <button 
      v-if="isSelfAndIsFollowing === 'NotFollowing'"
      @click="follow">팔로우</button>
    <button
      v-if="isSelfAndIsFollowing === 'isFollowing'"
      @click="follow">언팔로우</button>
    <p>bookmarked:</p>
    <bookmarked-item
      v-for="movieId in personInfo.bookmarked_movies"
      :key="movieId"
      :movieId="movieId"
    ></bookmarked-item>
  </div>
</template>

<script>
import BookmarkedItem from '@/components/BookmarkedItem.vue'

export default {
  name: 'MyProfile',
  components: {
    BookmarkedItem,
  },
  // data: function () {
  //   return {
  //     personInfo: this.$store.state.person
  //   }    
  // },
  methods: {
    follow() {
      this.$store.dispatch('follow', this.personInfo)
    }
  },
  computed: {
    userInfo() {
      return this.$store.state.userInfo
    },
    personInfo() {
      return this.$store.state.person
    },
    isSelfAndIsFollowing() {
      if (this.userInfo.username == this.personInfo.username) {
        return 'isSelf'
      } else {
        if (this.personInfo.followers.includes(this.userInfo.username)) {
          return 'isFollowing'
        } else {
          return 'NotFollowing'
        }
      }
    }
  },
  created: function () {
    this.$store.dispatch('getProfile', this.$route.params.personname)
  }
}
</script>

<style>

</style>