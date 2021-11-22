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
    login() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/api-token-auth/',
        data: this.credentials,
      })
        .then(res => {
          localStorage.setItem('jwt', res.data.token)
          this.$store.dispatch('login')
          this.$router.push({ name: 'Index' })
          console.log(res)
        })
        .catch(err => {
          console.log(err)
          // if (err.status === 400) {
            alert('아이디 혹은 패스워드가 틀립니다.')
          // }
        })
    }
  },

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