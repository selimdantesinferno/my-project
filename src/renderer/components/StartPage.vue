<template>
  <div class="content">
    <!-- <router-link to="/test">Go to test</router-link> -->
    <div class="centeredContent">
      <popup-accept class="popupAccept" />
      
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
        <b-btn v-b-modal.modalAccept>GO</b-btn>
      </div>

    </div>
  </div>

</template>

<script>
  import popupAccept from './popupAccept'

  export default {
    name: 'start-page',
    components: { popupAccept }

  }
</script>
 
<style src="./start_page.sass" lang="sass">

</style>
