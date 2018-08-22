<template>
    
  <div>
    <!-- <b-btn v-b-modal.modal1>Launch demo modal</b-btn> -->

    <!-- Modal Component -->
    <b-modal modal-class="left" v-model="modalShow" ref="myModalRef" id="modalAccept" title="Bootstrap-Vue">
      <p class="my-4">Hello from modal!</p>
      <template slot="modal-cancel">
        X
      </template>
      
    </b-modal>

  </div>

</template>

<script>

  export default {
    name: 'popup-accept',
    data () {
      return {
        modalClass: 'left',
        modalShow: true
      }
    },
    mounted () {
      // this.$refs.myModalRef.show()
    }
  }
  // $("#exampleModal").modal()
</script>

<style src="./popupAccept.sass" lang="sass">


</style>
