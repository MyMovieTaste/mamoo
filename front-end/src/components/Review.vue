<template>
  <div>
    <span>{{ rate }}</span> | 
    <span>{{ review.content }}</span>
  </div>
</template>

<script>
export default {
  name: 'Review',
  props: {
    review: Object,
  },
  computed: {
    rate() {
      if ( this.review.rank === 5) {
        return '★★★★★'
      } else if ( this.review.rank === 4) {
        return '★★★★'
      } else if ( this.review.rank === 3) {
        return '★★★'
      } else if ( this.review.rank === 2) {
        return '★★'
      } else {
        return '★'
      }
    },
  },
}
</script>

<style>

</style>