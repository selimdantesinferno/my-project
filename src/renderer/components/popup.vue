<template>
  <div>
  <table>
  <td>
  <div>Partage de votre trajet<div>
  <div>Agathe souhaite partager votre trajet pour transporter un colis à François<div>
  </td>
  <td>
  <div class="stroke1">
  <div class="stroke">
    <div class="slime">
<div class="slime1">
<google-map class="ellipse" />
</div>
</div></div></div>
  </td>
  <td>
  <div>
  Durée suplémentaire
  </div>
  <div>
  +8 min
  </div>
  <div>
  Arrivée estimée
  </div>
  <div>
  {{time4();}}
  </div>
  <div>
  Prix de la course
  </div>
  <div>
  {{info.price-50%}}
  </div>
  </td>
  <td>
  <div></div>
  <div><div>
  </td>
  </table>
</div>
</template>


<script>

  import GoogleMap from './GoogleMap'
  import axios from 'axios'
  import moment from 'moment'
  export default {
    name: 'landing-page',
    components: { GoogleMap },
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


<style scoped>
  @import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');

  * {
    margin: 0;
    padding: 0;
    background-image: radial-gradient(circle at 50% 50%, #0e121c, #15243f);
}











  .slime {

    width: 306px;
    height: 306px;
    background-image: linear-gradient(116deg, #42ddbc, #00acd6 50%, #9007c5);
    background-image: linear-gradient(116deg, #42ddbc, #00acd6 50%, #9922cc);
    border-radius: 50%;


  }
  .resp{
  width: 337px;
  height: 15px;
  font-family: Raleway;
  font-size: 13px;
  font-weight: bold;

  color: #ffffff;
  }
  .slime1 {

    width: 306px;
    height: 306px;
    transform: rotate(-135deg);
    background-image: linear-gradient(116deg, #42ddbc, #00acd6 50%, #9007c5);
    background-image: linear-gradient(116deg, #42ddbc, #00acd6 50%, #9922cc);
    border-radius: 50%;

  }
  .stroke {
    width: 309px;
    height: 325px;
    transform: rotate(-75deg);
    border: solid 0.5px #ffffff;
    border-radius: 50%;
  }
  .stroke1 {
    width: 309px;
    height: 325px;
    border: solid 0.5px #ffffff;
    border-radius: 50%;
  }
  .ellipse {

  width:287px;
  height:287px;
  transform: rotate(-150deg);
  align-items: center;
  border-radius: 50%;}
  h1{
  color:white;
  width:245px;
  height:36px;
  font-family: Raleway;
  font-size: 31px;
  font-weight:bold;
  }
  h2{
  color:white;
}


</style>
