<template>
  <div class="content">
    <!-- <router-link to="/test">Go to test</router-link> -->
    <popup-accept class="popupAccept" />
    
    <div class="travelColumn">
      <div class="travelPoint">
        <div class="icon">
          <img src="static/icons/start.svg" class="start">
        </div>
        <div class="point">
          <div class="dot">
            <img class="transp" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
          </div>
        </div>
        <div class="info">Depart <b>16:22</b> </div>
      </div>
      <div class="travelPoint center">
        <div class="icon">
          <img src="static/icons/colis.svg" class="colis">
        </div>
        <div class="point">
          <div class="dot">
            <img class="transp" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
          </div>
        </div>
        <div class="info">
          Pris en charge colis de <strong>Agathe</strong> <b>16:28</b> 
        </div>
      </div>
      <div class="travelPoint center">
        <div class="icon">
          <img src="static/icons/colis_ok.svg" class="colis-ok">
        </div>
        <div class="point">
          <div class="dot">
            <img class="transp" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
          </div>
        </div>
        <div class="info">
          Livraison colis de <strong>Agathe à Francois</strong><b>16:37</b> 
        </div>
      </div>
      <div class="travelPoint destination">
        <div class="icon">
          <img src="static/icons/pin_map.svg" class="pinmap">
        </div>
        <div class="point">
          <div class="dot">
            <div class="dotinside">
                <img class="transp" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
            </div>
          </div>
        </div>
        <div class="info">
          Arrivée à destination<b>16:42</b> 
        </div>
      </div>
      <div class="line"></div>      
    </div>


    <div class="addressColumn">
      <div class="title"><h1>Votre trajet Clara</h1></div>
      <div class="pathContainer">
        <div class="originAddress">
          <div class="icon">
            <img src="static/icons/start.svg" class="start">
          </div>
          <div class="address">
            <div class="label">Adresse de départ</div>
            <div class="info">96 Avenue Charles de Gaulle, 75015 Paris</div>
          </div>
        </div>
        <div class="destinationAddress">
          <div class="icon">
            <img src="static/icons/pin_map.svg" class="pinmap">
          </div>
          <div class="address">
            <div class="label">Adresse de destination</div>
            <div class="info">2 Place de la porte de versailles, 75015 Paris</div>
          </div>
        </div>
      </div>
      <div class="addDestination">
        <div class="icon">
          <img src="static/icons/add.png">                        
        </div>
        <div class="label">Ajouter un destination</div>
      </div>
      <div class="paymentInfo">
        <div class="price">
          <div class="label">Coût estimé de la course</div>
          <div class="info">17,64 €</div>
        </div>
        <div class="payment">
          <div class="label">Moyen de paiement</div>
          <div class="info">Clara Hugon</div>
        </div>
      </div>
    </div>
   

    <div class="mapColumn">
      <div class="durationColumn">
        <div class="duration">
          <div class="label">Durée</div>
          <div class="value">
            <div class="number">20</div>
            <div class="unit">min</div>
          </div>
        </div>
      </div>
      <div class="mapContainerColumn">        
        <google-map class="googleMap" />
        <div class="stroke1">
          <div class="slime">
            <div class="slime1">
              <div class="stroke">
                <img class="transp" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
              </div>
            </div>
          </div>
        </div>
        
      </div>
      <div class="distanceColumn">
        <div class="distance">
          <div class="label">Distance</div>
          <div class="value">
            <div class="number">4.6</div>
            <div class="unit">Km</div>
          </div>
        </div>
        <div class="footprint">
          <div class="text">Ce trajet vous permet d'économiser</div>
          <div class="info">
            <div class="number">15</div>
            <div class="unit">g Co2</div>
            <div class="icon">
              <img src="static/icons/leaf.png">              
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="buttonColumn">
      <div class="modeButtons">
        <div class="button auto active">
          <div class="roundedButton">
            <div class="icon">
              <img class="transp" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
              <img src="static/icons/car.svg" class="image">                
            </div>
          </div>
          <div class="text">Mode autonome</div>
        </div>
        <div class="button manual">
          <div class="roundedButton">
            <div class="icon">
              <img class="transp" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
              <img src="static/icons/ba_v.svg" class="image">                
            </div>
          </div>
          <div class="text">Mode manuel</div>
        </div>

      </div>
      <div class="goButton">
        <div class="stroke1">
          <div class="stroke2">
            <a href="" class="button">C'est parti !</a>            
          </div>
        </div>
      </div>
      <div class="acceptCheck">        
        <div class="icon">
          <div class="dot"><div class="dotinside"></div></div>
        </div>
        <div class="text">
          <div>
            J’accèpte qu’on me propose la livraison de colis sur mon trajet  en échange d’une réduction de prix de ma course.
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>

  import GoogleMap from './GoogleMap'
  import popupAccept from './popupAccept'
  import axios from 'axios'
  export default {
    name: 'driving-page',
    components: { GoogleMap, popupAccept },
    data () {
      return {
        info:[],
        latitude:'',
        longitude:''

      }
    },
    methods: {
      open (link) {
        this.$electron.shell.openExternal(link)
      }
    },
    mounted () {
      this.$http
        .get('/ride')
        .then(response => (this.info = response.data))
          this.latitude=this.info.itineraries[0].itinerary[0].x;
          this.longitude=this.info.itineraries[0].itinerary[0].y
      axios.post('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + this.latitude + ',' + this.longitude + '&key=AIzaSyAv2KTxY9QiIaWZg8JMXc9JA46mtzV5bOM')
                .then(response => {
                console.log(response.data);

                })
                .catch(e => {
                this.errors.push(e)
              })


    }
  }
</script>
 
 <style src="./driving_page.sass" lang="sass">
 </style>

    