<template>
  <router-link :to="{ name: 'Index' }" class="logo">
    <img src="@/assets/logo.svg" alt="logo">
    <span class="gradiant">Mamoo</span>
  </router-link>
</template>

<style lang="scss" scoped>
@import '@/scss/main.scss';

.logo {
  font-family: 'Montserrat', sans-serif;
  text-decoration: none;
  font-size: 1.6rem;
  // &:hover {
  // }
}
.logo span {
  margin-left:10px;
  font-size: 2.2rem;
}

.gradiant {
  background: linear-gradient(90deg, rgba(15,239,253,1) 0%, rgba(255,0,245,1) 52%, rgba(0,212,255,0.5088410364145659) 97%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

</style>