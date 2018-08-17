<template>
  <div class="content">
    <!-- <router-link to="/test">Go to test</router-link> -->

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
        <div class="info">Depart <br> <b>16:22</b> </div>
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
          Pris en charge colis de <b>Agathe</b> <br> <b>16:28</b> 
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
          Livraison colis de <b>Agathe à Francois</b> <br> <b>16:37</b> 
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
          Arrivée à destination<br> <b>16:42</b> 
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
        <div class="icon"></div>
        <div class="label">Ajouter un destination</div>
      </div>
      <div class="paymentInfo">
        <div class="label"></div>
        <div class="info"></div>
      </div>
    </div>
   


    <div class="mapColumn">
      <div class="durationColumn">
        <div class="label">Durée</div>
        <div class="value">
          <div class="number">20</div>
          <div class="unit">min</div>
        </div>
      </div>
      <div class="mapContainerColumn">        
        <div class="stroke1">
          <div class="slime">
            <div class="slime1">
              <div class="stroke">
                <img class="transp" src="data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7">
              </div>
            </div>
          </div>
        </div>
        <google-map class="googleMap" />
      </div>
      <div class="distanceColumn">
        <div class="label">Distance</div>
        <div class="value">
          <div class="number">4.6</div>
          <div class="unit">Km</div>
        </div>
      </div>
      
    </div>
    <div class="buttonColumn"></div>
  </div>

</template>

<script>

  import GoogleMap from './GoogleMap'
  import axios from 'axios'
  export default {
    name: 'driving-page',
    components: { GoogleMap },
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

    