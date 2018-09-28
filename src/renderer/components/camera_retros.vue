<template>
  <div class="cameraRetros">
    <img style="-webkit-user-select: none;" src="http://192.168.0.182/mjpg/video.mjpg?camera=1" width="255" height="388">
    
    <img style="-webkit-user-select: none;" src="http://192.168.0.182/mjpg/video.mjpg?camera=2" width="255" height="388">


  </div>
</template>
<script>
import GoogleMap from "./GoogleMap";
export default {
name:"camera",
components:{
GoogleMap
},
  data() {
    return {
    
      legacySystemHTML: `
      <body style="margin: 0px; background: #0e0e0e;">

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
        <div class="info">Start <b>6:00 pm</b> </div>
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
          Package picking-up for <strong>Agathe</strong> <b>6:05 pm</b>
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
          Package delivery from <strong>Agathe to Francois</strong><b>6:15 pm</b>
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
          Arrival<b>6:25 pm</b>
        </div>
      </div>
      <div class="line"></div>
    </div>
     <div class="mapColumn">
      <div class="durationColumn">
        <div class="duration">
          <div class="label">Duration</div>
          <div class="value">
            <div class="number">25</div>
            <div class="unit">min</div>
          </div>
        </div>
      </div>
      <div class="mapContainerColumn">
      
        <google-map class="googleMapDriving" />
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
            <div class="number">8.5</div>
            <div class="unit">Km</div>
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
          <div class="text">Autonomous </div>
        </div>
</body>  
      `
    }
  }
}
</script>
<style src="./camera_retros.sass" lang="sass">

</style>