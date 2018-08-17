<template>
  <div class="dim" id="app">

    <router-view></router-view>
  </div>
</template>

<script>
  export default {
    name: 'my-project'
  }
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Source+Sans+Pro');
.dim{
width: 1920px;
height: 388px;
}
* {



}
.table1{

background-image: radial-gradient(circle at 50% 50%, #0e121c, #15243f);
}
.google-map{
width:287px;
height:287px;
transform: rotate(-150deg);
align-items: center;
border-radius: 50%;

}

.dot1 {
height: 25px;
width: 25px;
border:2px solid #43debd;
border-radius: 50%;
display: inline-block;
}
ul{
list-style-type: none;
margin: 0;
padding: 0;
}
.vl {
border-left: 6px solid green;
height: 500px;
}
.start {
width: 10px;
height: 22px;
object-fit: contain;
}
.colis {
width: 20px;
height: 22px;
object-fit: contain;
}
.colis-ok {
width: 29px;
height: 27px;
object-fit: contain;
}
.pinmap {
width: 15px;
height: 21px;
object-fit: contain;

}
.Line-2 {
border-left-width: 3px;
height: 295px;
border-left-style: dotted;
border-image-source: linear-gradient(to bottom, #42ddbc, #00acd6);
border-image-slice: 1;
}
.Fill-340 {
width: 9px;
height: 9px;
background-color: #ffffff;
}
.dot2{
  height: 5px;
  width: 5px;
  border-radius: 50%;
  background-color: #ffffff;
  display: inline-block;
  }

.dure {

  font-family: Raleway;
  font-size: 15px;
  font-weight: 300;
  font-style: normal;
  font-stretch: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: right;
  color: #ffffff;
}
.min {

  font-family: Raleway;
  font-size: 20px;
  font-weight: 300;
  font-style: normal;
  font-stretch: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: right;
  color: #ffffff;

}

.time {
  font-size: 30px;
  font-weight: bold;
  color: #ffffff;
}
.slime {

  width: 306px;
  height: 306px;
  background-image: linear-gradient(116deg, #42ddbc, #00acd6 50%, #9007c5);
  background-image: linear-gradient(116deg, #42ddbc, #00acd6 50%, #9922cc);
  border-radius: 50%;


}
.resp{

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
h5{
color:white;
width:77px;
height:10px;
font-family: Raleway;
font-size: 9px;
}

.columbia{
width: 251px;
 height: 327px;
background-image: linear-gradient(to bottom, rgba(255, 255, 255, 0.5), rgba(0, 0, 0, 0.5)), linear-gradient(224deg, #42ddbc, #00acd6 50%, #9007c5);
-webkit-transform: skew(-5deg);
   -moz-transform: skew(-5deg);
     -o-transform: skew(-5deg);
     border-radius:10px;
}
.main{
width: 1920px;
height: 388px;
background-image: radial-gradient(circle at 52% 50%, #15243f, #0e121c);
}
</style>
