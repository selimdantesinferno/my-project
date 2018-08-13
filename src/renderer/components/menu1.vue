<template>
  <div>
  <table class="table1" width="100%" height="100%">
    <tr>
    <td class="td1">
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
<google-map class="ellipse" />
</div>
</div></div></div></td>
    <td><h2 class="dure">Distance</h2>
    <br>
    <label class="resp">
{{Math.trunc(info.distance)}}
    </label>
    <h2 class="min">Km</h2>
  </td></tr>
</table>
</td>
<td>
<table>
<tr>
<td>
<div><img src="../assets/road3.png" class="image">

</div>
</td>
<td>
<img src="../assets/desert3.png" class="image">
</td>
<td>
<img src="../assets/music3.png" class="image">
</td>
<td>
<div class="columbia"></div>
</td>
</tr>
</table>
</td>
<td>

</td>
  </div>
  </template>
  <style>
  .image{
  width: 251px;
  height: 327px;
  object-fit: contain;
  background-image: linear-gradient(183deg, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0) 51%, #000000);
  }
  .columbia{
  width: 251px;
  height: 327px;
  background-image: linear-gradient(to bottom, rgba(255, 255, 255, 0.5), rgba(0, 0, 0, 0.5)), linear-gradient(224deg, #42ddbc, #00acd6 50%, #9007c5);
  }

  </style>
