<template>
  <div>
    <!-- Modal Component -->
    <b-modal modal-class="left popupAccept" v-model="modalShow" ref="popupAcceptRef" id="modalAccept" title="Bootstrap-Vue" :hide-header="true" :hide-footer="true">
      <div class="content">
        <div class="textColumn">
          <div class="titre">
            <h2><img src="static/images/info.png" class="info"/>Traffic light</h2>
          </div>
          <div class="text">Waiting light turn green</div>
          <div class="counter">
            <p class="timer-counter">7.s</p>
          </div>
          <div class="redlight">
            <img src="static/images/redlight.png" class="red"/>
          </div>
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
  name: "popup_redlight",
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
