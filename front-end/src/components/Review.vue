<template>
  <div>
    <div class="list-group">
      <div class="list-group-item">
        <div class="">
          <span v-if="!(revisingId === review.id)">
            <span>작성자 {{ review.user }}</span>
            <span class="ms-2">평점 {{ rate }}</span> 
          </span>
        </div>
            <div class="mt-2">{{ review.content }}</div>
      </div>
    <!-- 수정을 동시에 여러개 하지 않는다 가정. 근데 동시 여러개 수정하게 가능할듯? -->
    </div>
    <div>
      <div class="mt-2 mb-2 d-flex justify-content-end">
        <button
          v-if="isOwnerAndIsRevising === 'isOwnerAndNotRevising'"
          @click="toggleRevise"
          class="btn btn-outline me-1"
        >수정</button>
        <button
          v-if="isOwnerAndIsRevising === 'isOwnerAndNotRevising'"
          @click="toggleDeleteConfirmation"
          class="btn btn-outline"
        >삭제</button>
      </div>
    </div>
    <!-- 삭제확인 모달 -->
    <div class="modal" :class="{ 'showModal': deleteConfirmation }">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
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
    <select class="form-select" v-model="reviseRate" name="rank" id="rate">
      <option value="5">★★★★★</option>
      <option value="4">★★★★</option>
      <option value="3">★★★</option>
      <option value="2">★★</option>
      <option value="1">★</option>
    </select>
    <div class="form-floating">
    <textarea 
      class="form-control mt-2 pt-3"
      :value="reviewReviseInput"
      @keyup="reviewReviseInputChange"
    ></textarea>
    </div>
    <div class="d-flex justify-content-end mt-2">
      <button
        class="btn btn-outline me-2"
        v-if="isOwnerAndIsRevising === 'isOwnerAndIsRevising'"
        @click="toggleRevise"
      >취소</button>
      <button class="btn btn-primary" @click="reviewReviseSubmit">작성</button>
    </div>
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
      const reviewReviseInfo = {
        review: this.review,
        rate: this.reviseRate,
        content: this.$store.state.reviewReviseInput
      }
      this.$store.dispatch('reviewReviseSubmit', reviewReviseInfo)
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
      if (this.$store.state.username === this.review.user) {
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

<style lang="scss" scoped>
@import '@/scss/main.scss';

.btn-outline {
  color: $primary;
  border-color: $primary;
}

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

.info {
  background-color: black;
}
</style>