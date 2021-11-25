<template>
<div class="pf f-white">
  <div v-if="personInfo" class="d-flex flex-column align-items-center">
    <!-- {{ personInfo }} -->
    <h1>{{ personInfo.username }} 님 환영합니다!</h1>
    <div class="d-flex mt-4">
      <h5 class="secondary me-3">팔로워 {{ personInfo.followers_count }} 명</h5>
      <h5 class="secondary"> 팔로잉 {{ personInfo.followings_count }} 명</h5>
    </div>
    <button 
      class="btn btn-primary mt-3"
      v-if="isSelfAndIsFollowing === 'NotFollowing'"
      @click="follow">팔로우</button>
    <button
      class="btn btn-outline mt-3"
      v-if="isSelfAndIsFollowing === 'isFollowing'"
      @click="follow">언팔로우</button>
    <p>bookmarked:</p>
    <bookmarked-item
      v-for="movie in personInfo.bookmarked_movies"
      :key="movie.id"
      :movie="movie"
    ></bookmarked-item>
  </div>
</div>
</template>

<script>
import BookmarkedItem from '@/components/BookmarkedItem.vue'
import jwt_decode from 'jwt-decode'

export default {
  name: 'Profile',
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
    this.$store.dispatch('setToken')
    if (sessionStorage.getItem('jwt')) {
      const token = sessionStorage.getItem('jwt')
      const decodedToken = jwt_decode(token)
      const userInfo = {
        username: decodedToken.username,
        userId: decodedToken.user_id
      }
      this.$store.dispatch('login')
      this.$store.dispatch('getUserInfo', userInfo)
    } else {
      this.$store.dispatch('logout')
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/scss/main.scss';
.secondary {
  color: $secondary;
}

.pf {
  margin:0 auto;

}
.f-white {
  color: $gray-100;
}

.btn-primary{
  color: $gray-100;
  background-color: $primary;
  
}
.secondary {
  color: $secondary;
}

.btn-outline {
  color: $primary;
  border-color: $primary;
}

</style>