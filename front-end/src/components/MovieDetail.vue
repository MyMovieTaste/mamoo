<template>
  <div>
    <div class="modal" :class="{ 'showModal': clicked}"> <div class="modal_body">Modal</div> </div> <button 
    @click="openPopup"
    class="btn-open-popup">Modal 띄우기</button>
  </div>
</template>

<script>
export default {
  name: 'MovieDetail',
  data: function () {
    return {
      clicked: null,
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

<style>
  .modal { position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: none; background-color: rgba(0, 0, 0, 0.4); }
  .showModal {display: block;}
</style>