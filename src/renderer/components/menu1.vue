<template>
  <div class="main">
  
  
    <table class="table1" width="100%" height="100%">
      <modal v-if="connected" role="dialog">
        <div class="modal-content">
  
          <div>Partage de votre trajet</div>
          <div>Agathe souhaite partager votre trajet pour transporter un colis à François</div>
  
          <div class="stroke1">
            <div class="stroke">
              <div class="slime">
                <div class="slime1">
                  <google-map class="ellipse" />
                </div>
              </div>
            </div>
          </div>
  
          <div>
            Durée supplémentaire
          </div>
          <div>
            +8 min
          </div>
          <div>
            Arrivée estimée
          </div>
          <div>
            {{time4()}}
          </div>
          <div>
            Prix de la course
          </div>
          <div>
            {{info.price}}
          </div>
  
  
  
        </div>
  
      </modal>
  
  
      <tr>
  
        <td class="progress">
          <table width="100%" height="100%">
            <tr>
              <td>
                <ul>
                  <li>
                    <img src="../assets/start.svg" class="start">
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
  
              </td>
            </tr>
          </table>
        </td>
        <td class="map">
  
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
              </td>
  
              <td>
                <h2 class="dure">Distance</h2>
                <br>
                <label class="resp">
  {{Math.trunc(info.distance)}}
      </label>
                <h2 class="min">Km</h2>
  
              </td>
            </tr>
            <tr>
              <td></td>
              <td>
                <div class="stroke1">
                  <div class="stroke">
                    <div class="slime">
                      <div class="slime1">
                        <google-map class="ellipse" />
                      </div>
                    </div>
                  </div>
                </div>
              </td>
              <td></td>
            </tr>
          </table>
        </td>
        <table>
  
          <td>
            <img src="../assets/road.png" class="image">
          </td>
          <td>
            <img src="../assets/desert.png" class="image">
          </td>
          <td>
  
  
            <img src="../assets/music.png" class="image">
  
  
          </td>
          <td>
  
            <div class="columbia"></div>
  
          </td>
  
        </table>
        </td>
        <td>
          <table>
          </table>
        </td>
      </tr>
    </table>
  </div>
</template>


<script>
  import GoogleMap from './GoogleMap'
  import axios from 'axios'
  import moment from 'moment'
  
  import SockJS from 'sockjs-client'
  import Stomp from 'webstomp-client'
  
  export default {
    name: 'menu1',
    components: {
      GoogleMap
    },
    data() {
      return {
        info: [],
        main_path: [],
        latitudedep: '',
        longitudedep: '',
        latitudearr: '',
        longitudearr: '',
        adresse1: [],
        adresse2: [],
        datenow: '',
        datecol: '',
        dateliv: '',
        datearr: '',
        received_messages: [],
        send_message: null,
        connected: false
      }
    },
    methods: {
      open(link) {
        this.$electron.shell.openExternal(link)
      },
      time() {
        var self = this
        this.datenow = moment().format('h:mm')
  
        setInterval(self.time, 1000)
      },
      time2() {
        var self = this
        this.datecol = moment().add(3, 'minutes').format('h:mm')
  
      },
      time3() {
        var self = this
        this.dateliv = moment().add(5, 'minutes').format('h:mm')
  
      },
      time4() {
        var self = this
        this.datearr = moment().add(Math.trunc(this.info.time / 60), 'minutes').format('h:mm')
  
      },
      send() {
        console.log('Send message:' + this.send_message)
        if (this.stompClient && this.stompClient.connected) {
          this.stompClient.send('/app-receive/from-client', this.send_message, {})
        }
      },
      connect() {
        this.socket = new SockJS('http://localhost:8080/websocket-endpoint')
        this.stompClient = Stomp.over(this.socket)
        this.stompClient.connect({}, (frame) => {
          this.connected = true
          console.log(frame)
          this.stompClient.subscribe('/global-message/tick', (tick) => {
            console.log(tick)
            this.received_messages.push(tick)
          })
        }, (error) => {
          console.log(error)
          this.connected = false
        })
      },
      disconnect() {
        if (this.stompClient) {
          this.stompClient.disconnect()
        }
        this.connected = false
      },
      tickleConnection() {
        this.connected ? this.disconnect() : this.connect()
      }
  
  
    },
    mounted() {
      this.connect();
      /*this.time();
  
  
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
  
  
  
  
  
  
  
  
      */
  
  
    }
  
  
  }
</script>

<style>
  modal {
    width: 675px;
    height: 319px;
    background-color: #ffffff;
  }
  
  .compo {
    width: 675px;
    height: 388px;
  }
  
  .progress {
    width: 156px;
    height: 335px;
    background-color: rgba(0, 0, 0, 0);
  }
  
  .map {
    width: 305px;
    height: 305px;
  }
</style>
