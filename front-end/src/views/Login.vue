<template>
  <div class="container row justify-content-center">
    <div class="col-3 d-flex flex-column">
      <h1 class="mb-5 tcenter logo gradiant">Login</h1>
      <input
        type="text"
        placeholder="username"
        v-focus
        v-model="credentials.username"
        class="form-control mb-3"
      >
      <input
        @keyup.enter="login"
        type="password"
        placeholder="password"
        v-model="credentials.password"
        class="form-control mb-3"
      >
      <div class="row d-flex justify-content-center">
        <button @click="login" class="btn btn-primary col-4">로그인</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data: function() {
    return {
      credentials: {
        username: null,
        password: null,
      }
    }
  },
  methods: {
    // 이걸 actions에서 안하지 왜 흠
    login() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/api-token-auth/',
        data: this.credentials,
      })
        .then(res => {
          // console.log(res)
          sessionStorage.setItem('jwt', res.data.token)
          this.$store.dispatch('login')
          this.$router.push({ name: 'Index' })
        })
        .catch(() => {
          // if (err.status === 400) {
          alert('아이디 혹은 패스워드가 틀립니다.')
          // }
        })
    }
  },

  // mounted는 로그인 성공 시 실행 안됨
  // destroyed는 Index.vue created보다 느림 왜지 (beforeDestory도 마찬가지..)
  
  directives: {
    focus: {
      // 디렉티브 정의
      inserted: function (el) {
        el.focus()
      }
    }
  }
}
</script>

<style lang="scss" scoped>
@import '@/scss/main.scss';

h1 {
    color: $gray-100;
    font-size: 3rem;
}

.tcenter {
  text-align: center;
}

.logo {
  font-family: 'Montserrat', sans-serif;
  text-decoration: none;
  // &:hover {
  // }
}

.gradiant {
  background: linear-gradient(90deg, rgba(15,239,253,1) 30%, rgba(255,0,245,1) 52%, rgba(0,212,255,0.5088410364145659) 77%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

</style>
