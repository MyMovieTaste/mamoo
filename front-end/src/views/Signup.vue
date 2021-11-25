<template>
  <div class="container row justify-content-center">
    <div class="col-3 d-flex flex-column">
      <h1 class="mb-5 tcenter logo gradiant">Signup</h1>
      <input
        type="text"
        placeholder="username"
        v-focus
        v-model="credentials.username"
        class="form-control mb-3"
      >
      <input
        type="password"
        placeholder="password"
        v-model="credentials.password"
        class="form-control mb-3"
      >
      <input
        type="password"
        placeholder="passwordConfirmation"
        v-model="credentials.passwordConfirmation"
        @keyup.enter="signup"
        class="form-control mb-5"
      >
      <div class="row d-flex justify-content-center">
        <button @click="signup" class="btn btn-primary col-4">Next</button>
      </div>
    </div>
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
        .catch(err => {
          console.log(err)
        })
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
