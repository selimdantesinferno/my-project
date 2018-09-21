<template>
 <div class="container-fluid dmsPage">
 <popup_timer v-if="time_tired==180000"/>
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
              <img src="static/images/repere.png" class="head bordered"  alt="">
            </div>
            <div class="col text-center">
              <div class="d-flex flex-column justify-content-center">
                <div class="coordinate">
                  <span class="cercle">x</span>
                  <span class="badge value">{{x}}</span>
                  <span class="unit">mm</span>
                </div>
                <div class="coordinate">
                  <span class="cercle">y</span>
                  <span class="badge value">{{y}}</span>
                  <span class="unit">mm</span>
                </div>
                <div class="coordinate">
                  <span class="cercle">z</span>
                  <span class="badge value">{{z}}</span>
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
          <div class="pitch"><div>Pitch</div> <div><span>{{pitch}}</span></div><div>Dg</div> </div>
          <div class="yaw"><div>Yaw</div> <div><span>{{yaw}}</span></div><div>Dg</div> </div>
          <div class="roll"><div>Roll</div> <div><span>{{roll}}</span></div><div>Dg</div> </div>          
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
              <div class="col value">{{fatigue}}%</div>
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
              <div class="col value">{{stress}}%</div>
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
              <div class="col value">{{somnolence}}%</div>
            </div>
            <div class="feature d-flex">
              <div class="col name">Vigilance</div>
              <div class="col bar">
                <div class="progress">
                  <span class="marker"></span>
                 <div v-if="vigilance>50" class="progress-bar vert" role="progressbar" style="width: 34%" aria-valuenow="15" aria-valuemin="0" aria-valuemax="100"></div>
                  <div v-if="vigilance<=50 && vigilance>=20" class="progress-bar jaune" role="progressbar" style="width: 34%" aria-valuenow="30" aria-valuemin="0" aria-valuemax="100"></div>
                  <div v-if="vigilance<20" class="progress-bar rouge" role="progressbar" style="width: 34%" aria-valuenow="20" aria-valuemin="0" aria-valuemax="100"></div>
                </div>
              </div>
              <div class="col value">{{vigilance}}%</div>
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
                    <span>60 bpm</span>
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
import axios from 'axios' 
import popup_timer from "./popup-timer";

  export default {
    name: 'dms-page',
    components: {
      popup_timer
    },
    data() {
      return {           
        actualRotation: "yaw",
        rotationValues: {
          center : 'static/images/fix-head.png',
          pitch : 'static/images/pitch-1.gif',
          yaw : 'static/images/yaw-1.gif',
          roll : 'static/images/roll-1.gif'        
        },
        timer_eyes_off:0,
        timer_eyes_closed:0,
  speed:[],
  biometry:[],
  nyaw:0,
  npitch:0,
  nroll:0,
  yaw:0,
  pitch:0,
  roll:0,
  x:0,
  y:0,
  z:0,
  max_x:0,
  max_y:0,
  max_z:0,
  nx:0,
  ny:0,
  nz:0,
  vigilance:100,
  timeLeft:60,
  time_tired:0,
  timer_stress:0,
  timerId:null,
  somnolence:0,
  fatigue:0,
  stress:0,
  timer_drow:0,
  interval:null
      }      
    },
    computed: {
      rotationImage() {
        return this.rotationValues[this.actualRotation]
      }
    },

 methods:
  {
  request(){
  self=this;
  axios.get('http://localhost:5000/pull/car/biometrydata')
      .then(function (response) {
        // handle success
        self.biometry=response.data.biometrydata;
       
       for(var i=0;i<100;i++)
       {
        self.x=self.biometry[i].headPosition.s32XInMm;
        self.y=self.biometry[i].headPosition.s32YInMm;
        self.z=self.biometry[i].headPosition.s32ZInMm;
        self.pitch=self.biometry[i].headPose.f32PitchInDegrees;
        self.yaw=self.biometry[i].headPose.f32YawInDegrees;
        self.roll=self.biometry[i].headPose.f32RollInDegrees;
        
        //estimate vigilance
        if(i==0)
        {
         self.max_x=Math.abs(self.biometry[i].headPosition.s32XInMm);
        self.max_y=Math.abs(self.biometry[i].headPosition.s32YInMm);
        self.max_z=Math.abs(self.biometry[i].headPosition.s32ZInMm);
        }
        else
        {
        self.max_x=Math.max(Math.abs(self.biometry[i].headPosition.s32XInMm),Math.abs(self.biometry[i+1].headPosition.s32XInMm))
        self.max_y=Math.max(Math.abs(self.biometry[i].headPosition.s32YInMm),Math.abs(self.biometry[i+1].headPosition.s32YInMm))
        self.max_z=Math.max(Math.abs(self.biometry[i].headPosition.s32ZInMm),Math.abs(self.biometry[i+1].headPosition.s32ZInMm))
        }        
        if(self.max_x>20)
         {
                self.nx++;
                
                self.ny=0;
                self.nz=0;
                
                this.timerId = setInterval(countdown, 1000);
                self.nyaw++;  
               if(self.nx>=2)       
                
                self.actualRotation="yawg";
         }
        else if(self.max_y>20)
         {
            self.ny++;
             
            self.nx=0;
            self.nz=0;
            this.timerId = setInterval(countdown, 1000);
            self.npitch++;  
            if(self.ny>=2)     
            self.actualRotation="pitchg";

         }
      else if(self.max_z>20)
         {
                self.nz++; 
                
                self.nx=0;
                self.ny=0;
                
                var timerId = setInterval(countdown, 1000);
                self.nroll++;   
              if(self.nz>=2)        

         self.actualRotation="rollg";
         
         }

        else if(Math.abs(self.biometry[i].eyesDirection.f32YawInDegree)>15 || Math.abs(self.biometry[i].eyesDirection.f32PitchInDegree)>15 || (self.biometry[i].eyelidOpening.f32LeftOpeningLevel<=4 &&  self.biometry[i].eyelidOpening.f32RightOpeningLevel<=4))
        {
         setInterval(function(){self.timer_eyes_off++},4000);
         if(self.timer_eyes_off<=1)
         { 
                  self.vigilance=self.vigilance-10;
         }
                  if(self.timer_eyes_off>1 && self.timer_eyes_off<=2)
         {
                  self.vigilance=self.vigilance-30;
         }
                  if(self.timer_eyes_off>2 && self.timer_eyes_off<=4)
         {
                  self.vigilance=vigilance-50;
         }
                 if(self.timer_eyes_off>4 || self.vigilance<0)
         {
                  self.vigilance=0;
         }
         
         
         
         
        }

        else{
        self.vigilance=100;}
         
      
         }
          
          // Algo Drowsiness

         if(self.biometry[i].eyelidOpening.f32LeftOpeningLevel<=4 &&  self.biometry[i].eyelidOpening.f32RightOpeningLevel<=4)
         {
          self.timer_drow = setInterval(countup, 1000);
           if(self.timer_drow>1)
            self.somnolence+=30;
           if(self.timer_drow>2 && self.timer_drow<=4)
            self.somnolence+=30
           if(self.timer_drow==4 || self.somnolence>100)
            self.somnolence=100;
          if(this.timer_drow>4)
            self.somnolence=0;

           
         }
         // Algo fatigue
         

      })
  .catch(function (error) {
        // handle error
        console.log(error);
      });
       },
  countdown() {
    if (this.timeLeft == -1) {
        clearTimeout(this.timerId);
        
    } else {
       
        this.timeLeft--;
    }
  },
    countup() {
    if (this.timer_eyes_closed >4) {
        this.timer_eyes_closed=0;
        clearTimeout(this.timer_drow);
        
    } else {
       
        this.timer_eyes_closed++;
    }
},
countuppop() {
    if (this.time_tired >180000) {
        this.time_tired=0;
        
        
    } else {
       
        this.time_tired++;
    }
}
 

        
      },
      computed: {
      rotationImage() {
        return this.rotationValues[this.actualRotation]
      }
    },
mounted () {
setInterval(countuppop, 1000)
this.request();
this.interval=setInterval(function(){
this.request();}.bind(this),1000);
this.time_tired=setInterval(countuppop,1000);
      
  },
  computed: {
    rotationImage() {
      return this.rotationValues[this.actualRotation];
    }
  },
  beforeDestroy: function() {
    clearInterval(this.interval);
  }
};
</script>
 
<style scope src="./dms_page.sass" lang="sass">

</style>
