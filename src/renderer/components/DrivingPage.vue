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
 
<style>
.content {
  display: flex;
  background-image: radial-gradient(circle at 50% 50%, #0e121c, #15243f);
  height: 300px;
}

[class*="Column"] {
  height: 100%;
  width: 100px;
  margin: auto;
  flex: 2 1 auto;
}

/*travel column*/

.travelColumn {
  border: 1px solid red;
  flex: 1 1 auto;
  display: flex;
  justify-content: space-around;
  flex-flow: column nowrap;
  position: relative;
}

.travelColumn .line {
  height: 76%;
  width: 2px;
  background-image: linear-gradient(to top, transparent 50%, #223049 50%), linear-gradient(to top, #00acd7, #43debd);
  background-size: 1px 8px, 100% 100%;
  border: none;
  border-radius: 70%;
  position: absolute;
  left: 35.2%;
}

.travelPoint {
    flex: 0 1 15%;
    display: flex;
    justify-content: center;
    z-index: 1;
}

.travelPoint .icon {
  flex: 0 1 11%;
  display: flex;
}
.travelPoint .icon img {
  margin: auto;
  height: 40%;
}

.travelPoint .point {
  display: flex;
  flex: 0 1 15%;
}
.travelPoint .info {
  flex: 0 1 40%;
  font-size: 50%;
}

.travelPoint .point .dot {
    border: 2px solid #43debd;
    border-radius: 50%;    
    width: 40%;
    margin: auto;
}

.travelPoint.center .point .dot {
    background-color: white;    
    border: none;
    border-radius: 50%;
    width: 25%;
}

.travelPoint.destination .point .dot {
    border: 2px solid #00acd7;    
}

.travelPoint.destination .point .dot .dotinside {
    background-color: #00acd7;
    border-radius: 50%;
    margin: 18%;
}


/*Address column*/

.addressColumn .title h1 {
  font-size: 1.5em;
  font-family: ralewaylight, Helvetica, Arial, sans-serif;    
}

.addressColumn .pathContainer [class*="Address"] {
    display: flex;
}

.addressColumn .pathContainer [class*="Address"] > .icon {
    flex: 0 1 10%;
}

.addressColumn .pathContainer [class*="Address"] > .address {
    flex: 1 1 100%;
}




.mapColumn {
    display: flex;
}
.mapColumn > * {
  border: 1px dashed red;
}

.mapContainerColumn {
  flex: 0 1 50%;
  display: flex;
}

.durationColumn {
  flex: 0 1 25%;
  text-align: right;  
}

.durationColumn .value, .distanceColumn .value {
    display: flex;
    align-items: baseline;
}

.durationColumn .value .number, .distanceColumn .value .number {
    font-size: 2em;
}

.distanceColumn {
    flex: 0 1 25%;    
}
.stroke1 {
    width: 100%;
    height: auto;
    border: solid 1px #ffffff;
    border-radius: 43%;
    margin: auto;
    display: inline-table;
}
.slime {
    width: 93%;
    background-image: linear-gradient(116deg, #42ddbc, #00acd6 22%, #9007c5 81%);
    border-radius: 40%;
    margin-left: 4%;
}
.slime1 {
    width: 92%;
    transform: rotate(-219deg);
    background-image: linear-gradient(116deg, #42ddbc, #00acd6 35%, #9007c5 80%);
    border-radius: 37%;
    display: inline-block;
    margin-left: 5%;
    margin-top: -3%;
}
.stroke {
    width: 111%;
    transform: rotate(250deg);
    border: solid 0.5px #ffffff;
    border-radius: 44%;
    margin-left: -4%;
    margin-top: -1%;
}
.stroke > img.transp, .travelPoint img.transp {
  display: block;
  height: auto;
  width: 100%;
}
</style>
    