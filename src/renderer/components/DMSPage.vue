<template>
 <div class="container-fluid dmsPage">
  <div class="row no-gutters">
    <div class="col detectionColumn">
      <div class="d-flex flex-column justify-content-center ">
        <div class="logoBar"><img src="static/images/idemiaLogo.png" alt=""></div>
        <div class="content">
          <div class="row no-gutters movements">
            <div class="col text">Face movements</div>
            <div class="col text-center">
              Eyes<br>
              <img src="static/images/eyes.png" class="eyes"  alt="">
            </div>
            <div class="col text-center">
              Mouth<br>
              <img src="static/images/mouth.png" class="mouth"  alt="">
            </div>
          </div>
          <div class="row no-gutters position">
            <div class="col-4">
              Head Position
            </div>
            <div class="col-4">
              <img src="static/images/head.png" class="head"  alt="">
            </div>
            <div class="col-4">
              <div class="d-flex flex-column justify-content-center">
                <div class="coordinate">
                  <span class="cercle">x</span>
                  <span class="badge value">14.6</span>
                  <span class="unit">cm</span>
                </div>
                <div class="coordinate">
                  <span class="cercle">y</span>
                  <span class="badge value">14.6</span>
                  <span class="unit">cm</span>
                </div>
                <div class="coordinate">
                  <span class="cercle">z</span>
                  <span class="badge value">14.6</span>
                  <span class="unit">cm</span>
                </div>
              </div>
            </div>
              
          </div>
        </div>
      </div>
    </div>

    <div class="col videoColumn">
      <div class=""><img src="static/images/video.png" class="videoImage"  alt=""></div>      
    </div>

    <div class="col statusColumn">
      <div class="d-flex flex-column justify-content-center ">
        <div class="logoBar"><img src="static/images/altranLogo.png" alt=""></div>
        <div class="content">
          <div class="row no-gutters">
            <div class="col"></div>
            <div class="col-8"></div>
          </div>
        </div>  
      </div>  
    </div>  

  </div>
</div>

</template>

<script>  
  export default {
    name: 'dms-page'
  }
</script>
 
<style scope src="./dms_page.sass" lang="sass">

</style>
