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
      
      <div class="statusColumn">

        <div class="points">
          <div class="two">
            <div class="left">Coffre Fermé</div>
            <div class="rigth">Prêt à repartir</div>
          </div>
          <div class="one">Coffre ouvert</div>          
          <div class="two">
            <div class="left">Identification</div>
            <div class="rigth">En attente de l'expediteur</div>
          </div>
        </div>
        <div class="line">
          <div class="imgBorder">
            <img src="static/images/car.png" class="img">
          </div>
          <div class="imgCut">
            
          </div>
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
