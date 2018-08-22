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

  export default {
    name: 'start-page',
    data () {
      return {
        notification:[],

        }
        },
        mounted(){
        let self=this;
        axios.get('http://localhost:5000/pull/car/notifications')
      .then(function (response) {
        // handle success
        console.log(response.data.notifications[0].userId);
        if(response.data.notifications[0].userId=='123456')
         self.$router.push('/welcome');
      })
      .catch(function (error) {
        // handle error
        console.log(error);
      });
        }

  }
</script>

<style src="./start_page.sass" lang="sass">
</style>
