<template>
  <div class="container-fluid contentManual">
    <div class="row no-gutters">
      <div class="col-2 camera camLeft"></div>
      <div class="col"></div>
      <div class="col-2 camera camRight"></div>
    </div>
  </div>

</template>

<script>
  import GoogleMap from './GoogleMap'
  import popupAccept from './popupAccept'
  import popupStatus from './popupStatus'
  import axios from 'axios'
  import moment from 'moment'
  export default {
    name: 'driving-page',
    components: { GoogleMap, popupAccept, popupStatus },
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

  // setInterval(self.time, 1000)
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

 <style src="./manual_page.sass" lang="sass">

 </style>
