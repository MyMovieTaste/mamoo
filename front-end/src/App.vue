<template>
  <div id="app">
    <div>
      <div id="nav" class="d-flex justify-content-between">
        <router-link :to="{ name: 'Index' }">Home</router-link>
        <div v-if="!isLogin">
          <router-link :to="{ name: 'Signup' }">추천받기</router-link> |
          <router-link :to="{ name: 'Login' }">로그인</router-link>
        </div>
        <div v-else>
          <router-link :to="{ name: 'Profile'}">내 프로필</router-link> | 
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
    //   isLogin: this.$store.isLogin
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
      this.$router.push({ name: 'Login' })
    }
  },
  updated: function() {
    // 이것도 mutations에서 해야하나
    if (localStorage.getItem('jwt')) {
      const token = localStorage.getItem('jwt')
      const decodedToken = jwt_decode(token)
      this.$store.state.username = decodedToken.username
      this.$store.state.isLogin = true
    } else {
      this.$store.state.isLogin = false
    }
  },
  computed: {
    ...mapGetters([
      'isLogin'
    ])
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
