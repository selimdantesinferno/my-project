<template>
  <div>
    <!-- Modal Component -->
    <b-modal modal-class="left popupAccept" v-model="modalShow" ref="popupAcceptRef" id="modalAccept" title="Bootstrap-Vue" :hide-header="true" :hide-footer="true">
      <div class="content">
        <div class="textColumn">
          <div class="titre">
            <h2><img src="static/images/info.png" class="info"/>You are tired</h2>
          </div>
          <div class="text">Be careful! You are in a bad driving condition. Please take a rest and come back later.</div>
        </div>
  
        <div class="buttonsContainer">
          <div class="cancelButton">
              <img src="static/icons/refuse.svg" class="img">      
          </div>
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
