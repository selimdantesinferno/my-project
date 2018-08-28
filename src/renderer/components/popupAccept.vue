<template>
    
  <div>
    <!-- Modal Component -->
    <b-modal modal-class="left popupAccept"
     v-model="modalShow" ref="popupAcceptRef" id="modalAccept" title="Bootstrap-Vue"
    :hide-header= "true"
    :hide-footer= "true"
     >
    <div class="content">
      <div class="textColumn">
        <div class="titre">
          <h2>Partage  de votre trajet </h2>
        </div>
        <div class="text"><b>Agathe</b>  souhaite partager  votre trajet  pour transporter  un <b>colis à François.</b></div>
      </div>
      <div class="mapColumn">
        <google-map class="googleMap" />
        <div class="stroke1">
          <div class="stroke">
            <img class="transp" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
          </div>
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

      <div class="infoColumn">
        <div class="duration">
          Durée supplémentaire
          <div><b>+8</b> min</div>
        </div>
        <div class="arrival">
          Arrivée estimée
          <div><b>16:56</b></div>
        </div>
        <div class="price">
          Prix de la course
          <div><strong>17,64€ - 50%</strong></div>
          <div><b>8,82€</b></div>
        </div>
      </div>

      <div class="buttonsContainer">
        <div class="goButton">
          <button type="button">
            <img src="static/icons/go.png" class="img">                  
          </button>
        </div>

        <div class="cancelButton">
          <button type="button">
            <img src="static/icons/times.svg" class="img">      
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
    name: 'popup-accept',
    components: { GoogleMap },    
    data () {
      return {
        modalClass: 'left',
        modalShow: true
      }
    }
  }
  
</script>

<style src="./popupAccept.sass" lang="sass">


</style>
