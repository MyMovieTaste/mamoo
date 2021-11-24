<template>
  <div>
    {{ movie.title }}
  </div>
</template>

<script>
export default {
  name: 'SearchItem',
  props: {
    movie: Object,
  }
}
</script>

<style>

</style>