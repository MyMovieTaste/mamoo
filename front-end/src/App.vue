<template>
<div id="app" class="bg">
    <div class="header">
      <logo></logo>
      <div id="nav" class="nav">
        <div class="nav-item search d-flex">
          <input
            @keydown.enter="search"
            @keyup="searchInputChange"
            :value="searchInput"
            class="form-control me-2 d-block" type="text" placeholder="영화제목을 입력해보세요">
          <router-link :to="{ name: 'Search' }">
            <img @click="search" src="@/assets/Search.svg" alt="search" class="icon">
          </router-link>
        </div>

        <div v-if="!isLogin" class="nav-item">
          <router-link :to="{ name: 'Signup' }" class="btn btn-primary me-2">추천받기</router-link>
          <router-link :to="{ name: 'Login' }" class="btn btn-outline">로그인</router-link>
        </div>
        <div v-else class="nav-item">
          <!-- 이렇게 하면 왜 계속 장고서버가 반응하는데 computed가 발생하는건가 왜지 -->
          <!-- <router-link :to="`/profile/${userInfo.username}`" class="btn btn-primary me-2">내 프로필</router-link> -->
          <!-- 내 프로필에서 내 프로필 누르면 에러가 나는데 중요한건 아니지만 없애려면 if로 하면 되려나 -->
          <a href="#" @click="toMyProfile" class="btn btn-primary me-2">내 프로필</a>
          <router-link to="#" @click.native="logout" class="btn btn-outline">로그아웃</router-link>
        </div>
      </div>
    </div>
    <div class="container">
      <router-view/>
    </div>

  </div> 
</template>

<script>
import jwt_decode from 'jwt-decode'
import { mapGetters } from 'vuex'
import Logo from '@/components/Logo.vue'

export default({
  components: {
    Logo
  },
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
      this.$router.push({ name: 'Search'})
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
    userInfo() {
      return this.$store.state.userInfo
    },
    searchInput() {
      return this.$store.state.searchInput
    },
  },
  updated: function () {
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
  },
  
})
</script>


<style lang="scss">
@import '@/scss/main.scss';


.container {
  padding-top: 40px;
  display:flex;
  align-items: center;
  flex-direction: row;
  justify-content: space-between;
}

.header {
  display:flex;
  align-items: center;
  flex-direction: row;
  justify-content: space-between;
  height: 120px;
  padding: 2rem;
  .logo {
    margin-right: 40px;
  }
}

.btn-outline {
  color: $primary;
  border-color: $primary;
}

.search {
  margin-right: 1rem;
}

.bg {
  background-color: #111;
  background-image: url('./assets/bg-tp50.svg');
  background-repeat: repeat;
  background-size: 205%;
  overflow: hidden;
  background-position: center;
  width: 100%;
  min-height: 100vh;
}

.icon {
  width: 2rem;
}


</style>
