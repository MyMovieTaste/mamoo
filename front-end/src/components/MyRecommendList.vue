<template>
  <div>
    <p>{{ username }}님께 추천하는 영화</p>
  </div>
</template>

<script>
export default {
  name: 'MyRecommendList',
  data: function () {
    return {
      // username: this.$store.state.username
    }
  },
  computed: {
    username () {
      return this.$store.state.username
    }
  }
}
</script>

<style>

</style>