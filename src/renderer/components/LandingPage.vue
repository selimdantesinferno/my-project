<template>
  <div class>






      <table class="table1" width="100%" height="100%">
        <tr>
        <td>
<ul>
  <li>
<img src="../assets/start.svg"
             class="start">
  </li>
  <li>
<img src="../assets/colis.svg" class="colis">
</li>
<li>
<img src="../assets/colis_ok.svg" class="colis-ok">
</li>
<li>

<img src="../assets/pin_map.svg" class="pinmap">

</li>
</ul>
</td>
<td>
<ul>
<li>
<span class="dot1"></span>
</li>


<li>
<div class="Line-2"></div>
<span class="Fill-340"></span>
</li>

</ul>
<td>
<ul>
<li>
<label class="resp">Depart</label>
</li>
<li>
<label class="resp">{{datenow}}</label>
</li>
<li>
<label class="resp">Prise en charge du colis</label>
</li>
<li>
<label class="resp">{{datecol}}</label>
</li>
<li>
<label class="resp">Livraison de colis</label>
</li>
<li>
<label class="resp">{{dateliv}}</label>
</li>
<li>
<label class="resp">Arrivée à destination</label>
</li>
<li>
<label class="resp">{{datearr}}</label>
</li>
</ul>
</td>
</td>
<td class="td2">
<h1>Votre trajet Clara</h1>
<br>
      <h5>Adresse de départ</h5>
      <br>
      <svg xmlns="http://www.w3.org/2000/svg" width="10" height="22" viewBox="0 0 10 22">
          <g fill="none" fill-rule="evenodd" stroke="#FFF" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5">
              <path d="M5 9v12M9 5a4 4 0 1 1-8 0 4 4 0 0 1 8 0z"/>
          </g>
      </svg>
      <label class="resp">{{adresse1}}</label>
<br>
      <span class="dot2"></span>
      <br>
      <span class="dot2"></span>
      <br>
        <span class="dot2"></span>
        <br>
        <span class="dot2"></span>
        <br>
        <span class="dot2"></span>
        <br>
        <span class="dot2"></span>
        <br>
        <span class="dot2"></span>
        <br><br>
      <h5>Adresse de destination</h5>
<br>
      <svg xmlns="http://www.w3.org/2000/svg" width="17" height="23" viewBox="0 0 17 23">
          <path fill="none" fill-rule="evenodd" stroke="#FFF" stroke-width="1.5" d="M8.5 1C12.637 1 16 4.312 16 8.383a7.28 7.28 0 0 1-1.059 3.782L9.14 21.701a.627.627 0 0 1-.532.299h-.004a.627.627 0 0 1-.531-.29L2.12 12.264A7.284 7.284 0 0 1 1 8.383C1 4.313 4.364 1 8.5 1zm0 5A2.504 2.504 0 0 0 6 8.5C6 9.87 7.103 11 8.5 11 9.914 11 11 9.854 11 8.5 11 7.122 9.878 6 8.5 6z"/>
      </svg>
      <label class="resp">{{adresse2}}</label>
      <br><br>
      <h5>Coût estimé de la course</h5>
      <br>
      <label class="resp">{{info.price}}</label>
</td>
          <td>
          <table>
          <tr>
          <td>
          <h2 class="dure">Durée</h2>
          <br>
          <label class="resp">
            {{ Math.trunc(info.time/60)}}
          </label>
          <h2 class="min">min</h2>
          </td>
            <td>
              <div class="stroke1">
              <div class="stroke">
                <div class="slime">
        <div class="slime1">
      <google-map class=google-map></google-map>
        </div>
        </div></div></div></td>
              <td><h2 class="dure">Distance</h2>
              <br>
              <label class="resp">
         {{info.distance}}
              </label>
              <h2 class="min">Km</h2>
            </td></tr>
</table>
</td>
<td>
<table>
        <tr>
          <td>
      <svg xmlns="http://www.w3.org/2000/svg" width="44" height="42" viewBox="0 0 44 42">
          <g fill="none" fill-rule="evenodd" stroke="#FFF" stroke-linecap="round" stroke-linejoin="round">
              <path stroke-width="1.5" d="M1.968 36.316c-.548-.365-1.19-2.026-1.19-5.27 0-3.706 1.15-3.267 1.417-3.753.266-.487 2.23-8.042 7.596-10.57 2.266-1.065 4.365-1.101 7.54-1.155 3.038-.051 6.784-.114 10.955 1.816 4.154 1.923 6.72 4.894 8.092 6.827 0 0 4.624 1.325 5.862 5.119 1.239 3.794-1.734 6.027-1.734 6.027l-.711.314M31.114 36.394H10.672"/>
              <path stroke-width="1.5" d="M37.28 24.706H29.86s-3.186-1.593-3.544-8.104M23.773 21.877c0 2.464-3.168 2.04-7.073 2.04-3.906 0-7.073.424-7.073-2.04s3.166-4.46 7.072-4.46 7.073 1.996 7.073 4.46z"/>
              <path stroke-width="2" d="M12.91 27.843h2.13"/>
              <path stroke-width="1.5" d="M15.017 15.609a2.601 2.601 0 1 1 4.724-.075M17.195 8.175a7.963 7.963 0 0 1 4.314 2.488M17.232 4.827a11.242 11.242 0 0 1 6.168 3.04M17.191 1.577a14.446 14.446 0 0 1 8.47 3.998M10.653 36.054a4.35 4.35 0 1 1-8.699 0 4.35 4.35 0 0 1 8.7 0z"/>
              <path stroke-width="1.5" d="M7.975 36.054a1.67 1.67 0 1 1-3.341 0 1.67 1.67 0 0 1 3.34 0zM39.812 36.054a4.35 4.35 0 1 1-8.7 0 4.35 4.35 0 0 1 8.7 0z"/>
              <path stroke-width="1.5" d="M37.133 36.054a1.67 1.67 0 1 1-3.341 0 1.67 1.67 0 0 1 3.34 0zM1.956 27.623s1.305.392 1.257 3.62l.001 1.752M40.583 26.703s-1.494 1.214-.771 2.737c.722 1.523 2.664.867 2.664.867"/>
          </g>
      </svg>
    </td>
    <td>
      <svg xmlns="http://www.w3.org/2000/svg" width="29" height="30" viewBox="0 0 29 30">
          <g fill="#999" fill-rule="evenodd">
              <path d="M4.064 1.421a2.539 2.539 0 0 0-2.535 2.535 2.538 2.538 0 0 0 2.535 2.535 2.537 2.537 0 0 0 2.534-2.535 2.538 2.538 0 0 0-2.534-2.535m0 6.367A3.836 3.836 0 0 1 .232 3.956 3.836 3.836 0 0 1 4.064.126a3.836 3.836 0 0 1 3.832 3.83 3.836 3.836 0 0 1-3.832 3.832M13.32 1.421a2.539 2.539 0 0 0-2.535 2.535 2.538 2.538 0 0 0 2.535 2.535 2.537 2.537 0 0 0 2.535-2.535 2.538 2.538 0 0 0-2.535-2.535m0 6.367a3.836 3.836 0 0 1-3.832-3.832A3.836 3.836 0 0 1 13.32.126a3.836 3.836 0 0 1 3.832 3.83 3.836 3.836 0 0 1-3.832 3.832M4.064 23.001a2.539 2.539 0 0 0-2.535 2.535 2.538 2.538 0 0 0 2.535 2.535 2.537 2.537 0 0 0 2.534-2.535 2.538 2.538 0 0 0-2.534-2.535m0 6.367a3.836 3.836 0 0 1-3.832-3.832 3.836 3.836 0 0 1 3.832-3.83 3.836 3.836 0 0 1 3.832 3.83 3.836 3.836 0 0 1-3.832 3.832M13.32 23.001a2.539 2.539 0 0 0-2.535 2.535 2.538 2.538 0 0 0 2.535 2.535 2.537 2.537 0 0 0 2.535-2.535 2.538 2.538 0 0 0-2.535-2.535m0 6.367a3.836 3.836 0 0 1-3.832-3.832 3.836 3.836 0 0 1 3.832-3.83 3.836 3.836 0 0 1 3.832 3.83 3.836 3.836 0 0 1-3.832 3.832M24.94 1.421a2.538 2.538 0 0 0-2.536 2.535 2.537 2.537 0 0 0 2.535 2.535 2.538 2.538 0 0 0 2.535-2.535 2.539 2.539 0 0 0-2.535-2.535m0 6.367a3.836 3.836 0 0 1-3.831-3.832 3.836 3.836 0 0 1 3.831-3.83 3.836 3.836 0 0 1 3.831 3.83 3.836 3.836 0 0 1-3.83 3.832"/>
              <path d="M3.415 22.354h1.297V7.14H3.415zM12.672 22.354h1.297V7.14h-1.297z"/>
              <path d="M24.94 14.674H4.063v-1.297h20.228V7.14h1.296v6.886a.65.65 0 0 1-.648.648M25.035 21.807h-1.619v2.382h1.572c.422 0 .776-.036 1.064-.11.287-.073.506-.197.66-.372.15-.175.226-.417.226-.724 0-.239-.06-.45-.183-.635a1.107 1.107 0 0 0-.508-.41c-.205-.087-.609-.13-1.212-.13m-1.005 3.64h-.614v2.783c0 .366-.08.636-.242.81a.822.822 0 0 1-.632.26c-.28 0-.497-.092-.65-.272-.154-.182-.23-.448-.23-.798v-6.666c0-.378.084-.653.253-.82.17-.17.443-.255.821-.255h2.855c.393 0 .73.016 1.01.05.28.033.532.101.756.204a2.176 2.176 0 0 1 1.198 1.232c.108.281.162.58.162.894 0 .647-.183 1.163-.547 1.55-.364.385-.916.658-1.657.821.311.165.608.41.892.732.283.323.536.667.76 1.031.222.365.395.694.52.988.123.293.185.495.185.605a.618.618 0 0 1-.109.34.769.769 0 0 1-.298.266.945.945 0 0 1-.438.097.848.848 0 0 1-.496-.139 1.329 1.329 0 0 1-.346-.35 15.565 15.565 0 0 1-.393-.627l-.703-1.17c-.252-.43-.478-.757-.677-.98-.198-.226-.4-.379-.605-.462-.205-.083-.463-.124-.775-.124"/>
          </g>
      </svg>
    </td></tr>
    <tr>
      <td><label class="resp">Mode autonome</label></td>
      <td><label class="resp">Mode manuel</label></td></tr>
      <tr>
      <td>
 <router-link to="/menu1">menu1</router-link>

      </td>
      </tr>
      </table>
</td>
</tr>
        </table>
        </div>



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


</style>
