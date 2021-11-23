<template>
  <div>
    <p v-if="username">{{ username }}</p>

  </div>
</template>

<script>
export default {
  name: 'MyProfile',
  computed: {
    username() {
      return this.$store.state.username
    }
  }
}
</script>

<style>

</style>