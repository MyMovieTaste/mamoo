<template>
  <div>
    <h1>Signup</h1>
    <p></p>
    <input
      type="text"
      placeholder="username"
      v-model="username"
    >
    <p> </p>
    <input
      type="password"
      placeholder="password"
      v-model="password"
    >
    <p></p>
    <input
      type="password"
      placeholder="passwordConfirmation"
      v-model="passwordConfirmation"
    >
    <p></p>
    <button @click="signup" @keyup.enter="signup" class="btn btn-primary">Next</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Signup',
  data: function () {
    return {
      credentials: {
        // username: null,
        // password: null,
        // passwordConfirmation: null,
      }
    }
  },
  methods: {
    signup() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/signup/',
        data: this.credentials,
      })
        .then()
    }
    // toSignupReview () {
    //   this.$router.push( { name: 'SignupReview' } )
    // }
  }
}
</script>

<style>

</style>