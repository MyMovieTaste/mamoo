<template>
  <div>
    <span v-if="!(revisingId === review.id)">
      <span>{{ review.user }}</span> | 
      <span>{{ rate }}</span> | 
      <span>{{ review.content }}</span>
    </span>
    <!-- 수정을 동시에 여러개 하지 않는다 가정; 근데 동시 여러개 수정하게 가능할듯? -->
    <button
      v-if="isOwnerAndIsRevising === 'isOwnerAndNotRevising'"
      @click="toggleRevise"
    >수정</button>
    <button
      v-if="isOwnerAndIsRevising === 'isOwnerAndNotRevising'"
      @click="toggleDeleteConfirmation"
    >삭제</button>

    <!-- 삭제확인 모달 -->
    <div class="modal" :class="{ 'showModal': deleteConfirmation }">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <!-- <h5 class="modal-title" id="staticBackdropLabel">Modal title</h5> -->
            <button 
              @click="toggleDeleteConfirmation"
              type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <p>정말 삭제하시겠습니까?</p>
            <button @click="deleteReview">예</button>
            <button @click="toggleDeleteConfirmation">아니오</button>
          </div>
        </div>
      </div>
    </div>
    <!-- 여기까지 삭제확인 모달 -->

    <div v-if="revisingId === review.id">
    <select v-model="reviseRate" name="rank" id="rate">
      <option value="5">★★★★★</option>
      <option value="4">★★★★</option>
      <option value="3">★★★</option>
      <option value="2">★★</option>
      <option value="1">★</option>
    </select>
    <textarea 
      :value="reviewReviseInput"
      @keyup="reviewReviseInputChange"
    ></textarea>
    <button @click="reviewReviseSubmit">작성</button>
    <button
      v-if="isOwnerAndIsRevising === 'isOwnerAndIsRevising'"
      @click="toggleRevise"
    >취소</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Review',
  props: {
    review: Object,
  },
  data: function () {
    return {
      reviseRate: this.review.rank,
    }
  },
  methods: {
    toggleRevise() {
      const reviseInfo = {
        reviewId: this.review.id,
        content: this.review.content
      }
      this.$store.dispatch('toggleRevise', reviseInfo)
    },
    reviewReviseInputChange(event) {
      this.$store.dispatch('reviewReviseInputChange', event.target.value)
    },
    reviewReviseSubmit() {
      this.toggleRevise()
    },
    toggleDeleteConfirmation() {
      this.$store.dispatch('toggleDeleteConfirmation')
    },
    deleteReview() {
      this.$store.dispatch('deleteReview', this.review)
    }
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
    checkIsOwner() {
      if (this.$store.state.userId === this.review.user) {
        return true
      } else {
        return false
      }
    },
    isRevising() {
      return this.$store.state.isRevising
    },
    isOwnerAndIsRevising() {
      if (this.checkIsOwner) {
        if (this.isRevising) {
          return 'isOwnerAndIsRevising'
        } else {
          return 'isOwnerAndNotRevising'
        }
      } else {
        return false
      }
    },
    reviewReviseInput() {
      return this.$store.state.reviewReviseInput
    },
    hide() {
      return true
    },
    revisingId() {
      return this.$store.state.revisingId
    },
    deleteConfirmation() {
      return this.$store.state.deleteConfirmation
    }
  },
}
</script>

<style>
  .showModal {display: block;}
</style>