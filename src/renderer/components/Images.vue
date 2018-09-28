<template>
  <div class="container-fluid contentImages" @click.left="back" @click.right="forward">
    <img :src="currentImage" alt="" class="ihm">
    <div class="row no-gutters">
      <div class="col-2 navigation back" @click="goto"></div>
      <div class="col navigation forward" ></div>
    </div>
    <!-- <div class="row no-gutters">
      <div class="col-2 camera camLeft"></div>
      <div class="col"></div>
      <div class="col-2 camera camRight"></div>
    </div> -->
  </div>

</template>

<script>
  export default {
    name: 'images',
    data () {
      return {
        maxImg: 15,
        currentImageIndex: 1
      }
    },
    computed: {
      currentImage() {
        return "static/ihm/" + this.currentImageIndex + ".jpg"
      }
    },
    methods: {
      goto() {
        if (this.currentImageIndex == 14)
          this.$router.push ('dms')
      },
      forward() {        
        if(this.currentImageIndex == this.maxImg)
          this.currentImageIndex = 0
        this.currentImageIndex++        
      },
      back(){
        if(this.currentImageIndex == 1)
          this.currentImageIndex = this.maxImg + 1
        this.currentImageIndex--
      }
    }
    
  }
</script>

 <style src="./images.sass" lang="sass">

 </style>
