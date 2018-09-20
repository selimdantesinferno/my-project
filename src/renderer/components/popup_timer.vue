<template>
  <div>
    <!-- Modal Component -->
    <b-modal modal-class="left popupAccept" v-model="modalShow" ref="popupAcceptRef" id="modalAccept" title="Bootstrap-Vue" :hide-header="true" :hide-footer="true">
      <div class="content">
        <div class="textColumn">
          <div class="titre">
            <h2>Have a break</h2>
          </div>
          <div class="text">You seem to need to take a break.<br>
          You should stop or let me take control</div>
        </div>
  
      </div>
  
    </b-modal>
  
  </div>
</template>

<script>
import GoogleMap from "./GoogleMap";

export default {
  name: "popup-timer",
  components: {
    GoogleMap
  },
  data() {
    return {
      modalClass: "left",
      modalShow: true
    };
  }
};
</script>

<style src="./popup_redlight.sass" lang="sass">


</style>
