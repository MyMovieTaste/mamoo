<template>
  <div>
    <h1>Signup</h1>
    <p></p>
    <input
      type="text"
      placeholder="username"
      v-focus
      v-model="credentials.username"
    >
    <p> </p>
    <input
      type="password"
      placeholder="password"
      v-model="credentials.password"
    >
    <p></p>
    <input
      type="password"
      placeholder="passwordConfirmation"
      v-model="credentials.passwordConfirmation"
      @keyup.enter="signup"
    >
    <p></p>
    <button @click="signup" class="btn btn-primary">Next</button>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Signup',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
        passwordConfirmation: null,
      }
    }
  },
  methods: {
    signup() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/accounts/signup/',
        data: this.credentials,
      })
        .then(() => {
          this.$router.push({name: 'Login'})
        })
        .catch(() => {})
    }
    // toSignupReview () {
    //   this.$router.push( { name: 'SignupReview' } )
    // }
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