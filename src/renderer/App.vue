<template>

  <div id="app">
  	<video autoplay="" muted="" loop="" id="background_video">
  	  <source src="static/video/background_wave.mp4" type="video/mp4">
  	</video>
  	<div class="routerView">
  	  <router-view></router-view>
  	</div>

  </div>
</template>

<script>
  export default {
    name: 'my-project'
  }
</script>

<style>

body {
	color: white
}

</style>
