<template>
  <div>
    <div class="modal" :class="{'showModal': clicked }">
      <div class="modal-header">
        <h5 class="modal-title">Modal title</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal_body">
        <img :src="posterPath" alt="" class="card-img-top">
        <p>ddddddd</p>
      </div>
      <div class="modal-footer">
        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-primary">Save changes</button>
      </div>
    </div>
    <button 
    @click="openPopup"
    class="btn-open-popup">Modal 띄우기
    </button>
  </div>
</template>

<script>
export default {
  name: 'MovieDetail',
  data: function () {
    const IMG_URL = 'https://image.tmdb.org/t/p/w500'
    return {
      clicked: null,
      posterPath: `${IMG_URL}/${this.movie.poster_path}`,
    }
  },
  props: {
    movidId: Number,
  },
  methods: {
    showConsole() {
      console.log(this.movidId)
    },
    openPopup () {
      if (this.clicked) {
        this.clicked = false
      } else {
        this.clicked = true
      }
    }
  }
}

// btnOpenPopup.addEventListener('click', () => { modal.style.display = 'block'; });

</script>

<style lang="scss" scoped>
@import '@/scss/main.scss';
.modal {
  color: $gray-100;
}
.modal-content {
  color: $gray-100;
}
.modal-body {
 color: $gray-100;
}

.modal-header{
  border-bottom: none;
}
.showModal { display: block; }


</style>