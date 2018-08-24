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
        <div class="info">Depart <b>{{datenow}}</b> </div>
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
          Pris en charge colis de <strong>Agathe</strong> <b>{{datecol}}</b>
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
          Livraison colis de <strong>Agathe à Francois</strong><b>{{dateliv}}</b>
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
          Arrivée à destination<b>{{datearr}}</b>
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
            <div class="info">{{adresse1}}</div>
          </div>
        </div>
        <div class="destinationAddress">
          <div class="icon">
            <img src="static/icons/pin_map.svg" class="pinmap">
          </div>
          <div class="address">
            <div class="label">Adresse de destination</div>
            <div class="info">{{adresse2}}</div>
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
          <div class="info">{{info.price}} €</div>
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
            <div class="number">{{Math.trunc(info.time/60)}}</div>
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
            <div class="number">{{info.distance}}</div>
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
            <a  href="" class="button">C'est parti !</a>            
          </div>
        </div>
      </div>
      <div class="acceptCheck">
        <div class="icon">
          <div class="dot"><div class="dotinside"></div></div>
        </div>
        <div class="text">
          <div>
            J’accèpte qu’on me propose la livraison de colis sur mon trajet en échange d’une réduction de prix de ma course.
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
  import moment from 'moment'
  export default {
    name: 'driving-page',
    components: { GoogleMap, popupAccept },
    data () {
      return {
        info:[],
        main_path:[],
        latitudedep:'',
        longitudedep:'',
        latitudearr:'',
        longitudearr:'',
        adresse1:[],
        adresse2:[],
        datenow: '',
        datecol:'',
        dateliv:'',
        datearr:''
      }
    },
    methods: {
      open (link) {
        this.$electron.shell.openExternal(link)
      },
      time() {
  var self = this
  this.datenow = moment().format('h:mm')

  setInterval(self.time, 1000)
},
time2() {
var self = this
this.datecol = moment().add(3,'minutes').format('h:mm')

},
time3() {
var self = this
this.dateliv = moment().add(5,'minutes').format('h:mm')

},
time4() {
var self = this
this.datearr = moment().add(Math.trunc(this.info.time/60),'minutes').format('h:mm')

}
    },
    mounted () {
    this.time();

      this.$http
        .get('/ride')
        .then(response => {
    this.info=response.data;

        this.main_path = response.data.itineraries[0].itinerary.map( point =>{
          return {lat: point.x, lng: point.y}
          })

      this.latitudedep=this.main_path[0].lat;
      this.longitudedep=this.main_path[0].lng;
      axios.post('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + this.latitudedep + ',' + this.longitudedep + '&key=AIzaSyAv2KTxY9QiIaWZg8JMXc9JA46mtzV5bOM')
                .then(response => {
      this.adresse1=response.data.results[0].formatted_address;
      })
                .catch(e => {
                this.errors.push(e)
              })

    this.latitudearr=this.main_path[this.main_path.length-1].lat;
    this.longitudearr=this.main_path[this.main_path.length-1].lng;
    axios.post('https://maps.googleapis.com/maps/api/geocode/json?latlng=' + this.latitudearr + ',' + this.longitudearr + '&key=AIzaSyAv2KTxY9QiIaWZg8JMXc9JA46mtzV5bOM')
           .then(response => {
              this.adresse2=response.data.results[0].formatted_address;
              console.log(this.adresse2);
              })
                        .catch(e => {
                        this.errors.push(e)
                      })
                      this.time2();
                      this.time3();
                      this.time4();


       })







    }
  }
</script>

 <style scoped src="./driving_page.sass" lang="sass">

 </style>
