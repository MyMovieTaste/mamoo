<template>
  <div id="app">
    <div>
      <div id="nav" class="d-flex justify-content-between">
        <router-link :to="{ name: 'Index' }">Home</router-link>
        <div>
          <input @keyup.enter="search"
            @keyup="searchInputChange"
            :value="searchInput" type="text">
          <router-link :to="{ name: 'Search' }">
            <button @click="search">search</button>
          </router-link>
        </div>
        <div v-if="!isLogin">
          <router-link :to="{ name: 'Signup' }">추천받기</router-link> |
          <router-link :to="{ name: 'Login' }">로그인</router-link>
        </div>
        <div v-else>
          <a href="#" @click="toMyProfile">내 프로필</a> | 
          <router-link to="#" @click.native="logout">로그아웃</router-link>
        </div>
      </div>
      <router-view/>

    </div>
  </div>
</template>

<script>
import jwt_decode from 'jwt-decode'
import { mapGetters } from 'vuex'

export default({
  data: function() {
    return {
      // isLogin: this.$store.isLogin
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
      this.$router.push({ name: 'Login' })
    },
    search() {
      this.$store.dispatch('search', this.searchInput)
    },
    toMyProfile() {
      this.$router.push({ name: 'Profile', params: { personname: this.username }})
    },
    searchInputChange(event) {
      this.$store.dispatch('searchInputChange', event.target.value)
    }
  },
  computed: {
    ...mapGetters([
      'isLogin'
    ]),
    username() {
      return this.$store.state.username
    },
    searchInput() {
      return this.$store.state.searchInput
    }
  },
  created: function () {
    this.$store.dispatch('setToken')
    if (localStorage.getItem('jwt')) {
      const token = localStorage.getItem('jwt')
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
    console.log(this.username)
  },
})
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
