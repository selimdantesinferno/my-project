<template>
  <div class="content">
    <!-- <router-link to="/test">Go to test</router-link> -->

    <div class="travelColumn">
      <div class="travelPoint">
        <div class="icon">
          <img src="../assets/start.svg" class="start">
        </div>
        <div class="point">
          <div class="dot"></div>
        </div>
        <div class="info">Depart <br> <b>16:22</b> </div>
      </div>
      <div class="travelPoint center">
        <div class="icon">
          <img src="../assets/colis.svg" class="colis">
        </div>
        <div class="point">
          <div class="dot"></div>
        </div>
        <div class="info"></div>
      </div>
      <div class="travelPoint center">
        <div class="icon">
          <img src="../assets/colis_ok.svg" class="colis-ok">
        </div>
        <div class="point">
          <div class="dot"></div>
        </div>
        <div class="info"></div>
      </div>
      <div class="travelPoint destination">
        <div class="icon">
          <img src="../assets/pin_map.svg" class="pinmap">
        </div>
        <div class="point">
          <div class="dot"></div>
        </div>
        <div class="info"></div>
      </div>
      <div class="line"></div>      
    </div>





    <div class="addressColumn"></div>
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
  flex: 1 100%;
}

/*travel column*/

.travelColumn {
  border: 1px solid red;
  flex: 0 1 75%;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  flex-wrap: wrap;
  position: relative;
}

.travelColumn .line {
  height: 76%;
  width: 4px;
  background-image: linear-gradient(to top, transparent 50%, #223049 50%), linear-gradient(to top, #00acd7, #43debd);
  background-size: 1px 8px, 100% 100%;
  border: none;
  border-radius: 70%;
  position: absolute;
  left: 34.7%;
}

.travelPoint {
    flex: 0 1 15%;
    display: flex;
    justify-content: space-around;
    z-index: 1;
}

.travelPoint .icon {
  flex: 0 1 11%;
  display: flex;
}
.travelPoint .icon img {
  margin: auto;
}

.travelPoint .point {
  display: flex;
  flex: 0 1 15%;
}
.travelPoint .info {
  flex: 0 1 40%;
}

.travelPoint .point .dot {
    border: 2px solid #43debd;
    border-radius: 50%;
    height: 40%;
    width: 40%;
    margin: auto;
}

.travelPoint.center .point .dot {
    background-color: white;    
    border: none;
    border-radius: 50%;
    height: 30%;
    width: 30%;
}

.travelPoint.destination .point .dot {
    border: 2px solid #00acd7;    
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
    