<template>
    
  <div>
    <!-- Modal Component -->
    <b-modal modal-class="left popupStatus"
     v-model="modalShow" ref="popupStatusRef" id="modalStatust"
    :hide-header= "true"
    :hide-footer= "true"
     >
    <div class="content">
      <div class="textColumn">
        <div class="titre">
          <h2>Prise en charge du colis de Agathe </h2>
        </div>
        <div class="text">Le colis est chargé, nous pouvons  repartir quand vous le souhaitez.</div>
      </div>
      
      <div class="mapColumn">
        <div class="car">
          <img src="static/images/car.png" class="img">                  
        </div>
        <div class="points">
          <div class="north">N</div>
          <div class="middle">
            <div class="west">W</div>
            <div class="east">E</div>
          </div>
          <div class="south">S</div>
        </div>
      </div>

      <div class="buttonsContainer">
        <div class="goButton">
          <button type="button">
            <img src="static/icons/go.png" class="img">                  
          </button>
        </div>        
      </div>

    </div>
      
    </b-modal>

  </div>

</template>

<script>
  import GoogleMap from './GoogleMap'

  export default {
    name: 'popup-status',
    components: { GoogleMap },    
    data () {
      return {
        modalClass: 'left',
        modalShow: true
      }
    }
  }
  
</script>

<style src="./popupStatus.sass" lang="sass">


</style>
