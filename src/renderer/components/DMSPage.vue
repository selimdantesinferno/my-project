<template>
 <div class="container-fluid dmsPage">
  <div class="row h-100 no-gutters">

    <div class="col detectionColumn">
      <div class="d-flex flex-column justify-content-center ">
        <div class="content">
          <div class="align-items-center d-flex logoIdemia">
            <img src="static/images/idemiaLogo.png" alt="">
          </div>
          <div class="row no-gutters movements">            
            <div class="col text">Face movements</div>
            
            <div class="col text-center">
              Eyes<br>
              <img src="static/images/eyes.png" class="eyes bordered"  alt="">
            </div>
            <div class="col text-center mouthText">
              Mouth<br>
              <img src="static/images/mouth.png" class="mouth bordered"  alt="">
            </div>
          </div>

          <div class="row no-gutters position">
            <div class="col text">
              Head Position
            </div>
            <div class="col headImage text-center">
              <img src="static/images/head.png" class="head bordered"  alt="">
            </div>
            <div class="col text-center">
              <div class="d-flex flex-column justify-content-center">
                <div class="coordinate">
                  <span class="cercle">x</span>
                  <span class="badge value">14.6</span>
                  <span class="unit">mm</span>
                </div>
                <div class="coordinate">
                  <span class="cercle">y</span>
                  <span class="badge value">14.6</span>
                  <span class="unit">mm</span>
                </div>
                <div class="coordinate">
                  <span class="cercle">z</span>
                  <span class="badge value">14.6</span>
                  <span class="unit">mm</span>
                </div>
              </div>
            </div>
              
          </div>
        </div>
      </div>
    </div>

    <div class="col videoColumn">
      <div class="video">
        <img :src="rotationImage" alt="">
        <div class="separator"></div>
      </div> 
      <div class="coordinates">
        <div class="coordinatesContent">
          <div class="pitch"><div>Pitch</div> <div><span>15.0</span></div><div>Dg</div> </div>
          <div class="yaw"><div>Yaw</div> <div><span>22.0</span></div><div>Dg</div> </div>
          <div class="roll"><div>Roll</div> <div><span>1.0</span></div><div>Dg</div> </div>          
        </div>
      </div>     
    </div>


    <div class="col statusColumn">
      <div class="row no-gutters h-100">
        
        <div class="col condition d-flex flex-column justify-content-between">
          <div class="titre">Physical condition</div>
          <div class="d-flex flex-column">
            <div class="feature d-flex">
              <div class="col name">Tiredness</div>
              <div class="col bar">
                <div class="progress">
                  <span class="marker"></span>
                  <div class="progress-bar vert" role="progressbar" style="width: 34%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"></div>
                  <div class="progress-bar jaune" role="progressbar" style="width: 34%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>
                  <div class="progress-bar rouge" role="progressbar" style="width: 34%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
              </div>
              <div class="col value">35%</div>
            </div>
            <div class="feature d-flex">
              <div class="col name">Stress</div>
              <div class="col bar">
                <div class="progress">
                  <span class="marker"></span>
                  <div class="progress-bar vert" role="progressbar" style="width: 34%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"></div>
                  <div class="progress-bar jaune" role="progressbar" style="width: 34%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>
                  <div class="progress-bar rouge" role="progressbar" style="width: 34%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
              </div>
              <div class="col value">35%</div>
            </div>
            <div class="feature d-flex">
              <div class="col name">Sleepness</div>
              <div class="col bar">
                <div class="progress">
                  <span class="marker"></span>
                  <div class="progress-bar vert" role="progressbar" style="width: 34%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"></div>
                  <div class="progress-bar jaune" role="progressbar" style="width: 34%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>
                  <div class="progress-bar rouge" role="progressbar" style="width: 34%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
              </div>
              <div class="col value">35%</div>
            </div>
            <div class="feature d-flex">
              <div class="col name">Vigilance</div>
              <div class="col bar">
                <div class="progress">
                  <span class="marker"></span>
                  <div class="progress-bar vert" role="progressbar" style="width: 34%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"></div>
                  <div class="progress-bar jaune" role="progressbar" style="width: 34%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>
                  <div class="progress-bar rouge" role="progressbar" style="width: 34%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
              </div>
              <div class="col value">35%</div>
            </div>
          </div>

        </div>

        <div class="col constants">
          <div class="d-flex flex-column h-100">
            <div class="logoBar"><img src="static/images/altranLogo.png" alt=""></div>
            <div class="align-items-center content d-flex flex-column h-100 text-center">
              Vital Constants
              <br>
              <div class="constantsBox d-flex flex-column">
                <div class="constant d-flex">
                  <div class="icon">
                    <img src="static/images/temperature.png" alt="">                    
                  </div>
                  <div class="text">
                    <span>36,8 °C</span>
                  </div>
                  
                </div>
                <div class="constant d-flex">
                  <div class="icon">
                    <img src="static/images/coeur.png" alt="">                    
                  </div>
                  <div class="text">
                    <span>72 bpm</span>
                  </div>
                  
                </div>
                <div class="constant d-flex">
                  <div class="icon">
                    <img src="static/images/poumon.png" alt="">                    
                  </div>
                  <div class="text">
                    <span>15 rpm</span>
                  </div>
                  
                </div>
              </div>
            </div>  
          </div> 
        </div>
      </div>

       
    </div>  

  </div>
</div>

</template>

<script>  
  export default {
    name: 'dms-page',
    data() {
      return {           
        actualRotation: "yaw",
        rotationValues: {
          center : 'static/images/center.png',
          pitch : 'static/images/pitch.png',
          yaw : 'static/images/yaw.gif',
          roll : 'static/images/roll.png'        
        }
      }      
    },
    computed: {
      rotationImage() {
        return this.rotationValues[this.actualRotation]
      }
    }
  }
</script>
 
<style scope src="./dms_page.sass" lang="sass">

</style>
