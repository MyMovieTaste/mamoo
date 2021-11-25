<template>
  <div>
    <input
      type="text"
      placeholder="username"
      v-focus
      v-model="credentials.username"
    >
    <p></p>
    <input
      type="password"
      placeholder="password"
      v-model="credentials.password"
      @keyup.enter="login"
    >
    <p></p>
    <button
      class="btn btn-success"
      @click="login"
    >Login</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Index',
  data: function() {
    return {
      credentials: {

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

<style>

</style>