<template>
  <div>
    <h4>Mamoo만의 추천 리스트를 받아보세요</h4>
    <div class="reco">
      <p>재밌게 본 영화의 리뷰 5개를 입력해보세요!</p>
      <p>여러분의 취향과 비슷한 분들을 찾아서, 그분들이 좋아한 영화를 추천해 드릴게요!</p>
    </div>
  </div>
</template>

<script>

export default {
  name: 'RecommendList',
  
}
</script>

<style lang="scss" scoped>
@import '@/scss/main.scss';
h4 {
  line-height: 1;
  font-size: 30px;
  color: $gray-100;
};

p {
  margin-bottom: 0;
};

.reco {
  color: $gray-100;
  font-size: 1.2rem;
  margin: 2rem 0 2rem;
  background-color: rgba(0, 0, 0, 0.351);
  padding: 2rem;
  border-radius: 2rem;
}

</style>