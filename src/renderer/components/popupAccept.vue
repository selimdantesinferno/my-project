<template>
    
  <div>
    <!-- <b-btn v-b-modal.modal1>Launch demo modal</b-btn> -->

    <!-- Modal Component -->
    <b-modal ref="myModalRef" id="modalAccept" title="Bootstrap-Vue">
      <p class="my-4">Hello from modal!</p>
      <!-- <template slot="header">
        <h1>Here might be a page title</h1>
      </template> -->
      
    </b-modal>

  </div>

</template>

<script>

  export default {
    name: 'popup-accept',
    
    mounted () {
      // this.$refs.myModalRef.show()
    }
  }
  // $("#exampleModal").modal()
</script>

<style src="./popupAccept.sass" lang="sass">


</style>
