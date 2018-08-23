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
        Bienvenue Clara à bord de votre véhicule autonome Columbia.
        <br>
        <i>
          <b>"Nous allons faire un bout de chemin ensemble"</b>
        </i>
      </div>

    </div>
  </div>

</template>

<script>

  export default {
    name: 'welcome-page',
      mounted(){
      this.gotodrive();


      },
      methods:{
      gotodrive(){
      for(var i=0;i<=100;i++)
      if(i==100)
      this.$router.push('/go');
      }

      }
  }
</script>

<style src="./welcome_page.sass" lang="sass">
</style>
