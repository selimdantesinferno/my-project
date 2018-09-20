<template>
  <div class="content">
    <!-- <router-link to="/test">Go to test</router-link> -->
    <div class="centeredContent">

      <div class="avatarColumn">
        <div class="avatarImage">
          <img src="static/icons/profile.png" class="image">
        </div>

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
      <div class="textColumn">
        <b>Reconnaisance faciale</b>
        <br>
        en cours
      </div>

    </div>
  </div>

</template>

<script>

import axios from 'axios'
import popupAccept from './popupAccept'

  export default {
    name: 'start-page',
    components: { popupAccept },
    data () {
      return {
        notification:[],

        }
        },
        mounted(){
        let self=this;
        self.demo();
        /*axios.get('http://localhost:5000/pull/car/notifications')
      .then(function (response) {
        // handle success
        console.log(response.data.notifications[0].userId);
        if(response.data.notifications[0].userId=='123456')
         {
         
         self.demo();

         }
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      });
axios.get('http://localhost:5000/pull/car/biometrydata')
      .then(function (response) {
        // handle success
        var biometry=response.data.biometrydata;
        for(var i in biometry)
        {
        if(Math.abs(biometry[i].headPosition.s32XInMm)>20)
         {
         console.log("PITCH");

         }
        if(Math.abs(biometry[i].headPosition.s32YInMm)>20)
         {
         console.log("YAW");

         }
   if(Math.abs(biometry[i].headPosition.s32ZInMm)>20)
         {
         console.log("ROLL");

         }
         }
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      });*/
        },
        methods:{
        sleep: function(ms) {
          return new Promise(resolve => setTimeout(resolve, ms));
        },
        demo:async function() {

          await this.sleep(5000);
          this.$router.push('/welcome');
        }
/*
        canconnect:function(){
  var can = require('socketcan');
  var fs = require('fs');

  // Parse database
  var network = can.parseNetworkDescription("samples/can_definition.kcd");
  var channel = can.createRawChannel("can0");
  var db      = new can.DatabaseService(channel, network.buses["Motor"]);

  channel.start();

  // Register a listener to get any value changes
  db.messages["unlock_door_confirm"].signals["SpeedKm"].onChange(function(s) {
    console.log("SpeedKm " + s.value);
  });



// Unlock door
db.messages["unlock_door_request"].signals["open"].update(1);

// Trigger sending this message
db.send("unlock_door_request");
}*/

        }
      }




</script>

<style src="./start_page.sass" lang="sass">
</style>
