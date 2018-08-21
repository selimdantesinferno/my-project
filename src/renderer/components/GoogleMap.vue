<template>
  <div>

    <gmap-map
      :center="center"
      :zoom="13"
      v-bind:options="mapStyle"
      >
      <gmap-polyline v-if="main_path.length > 0" :path="main_path" ref="polyline">
      </gmap-polyline>
    </gmap-map>
  </div>
</template>


<style>
.googleMap {
  width: 87%;
  height: 77%;
  display: grid;
  left: 6.5%;
  top: 12%;
  position: absolute;
  z-index: 2;
}

.googleMap .vue-map-container .vue-map {
  border-radius: 50%;
}
</style>

<script>
export default {
  name: 'GoogleMap',
  data () {
    return {
      info: [],
      center: { lat: 48.8739399, lng: 2.2946627},
      main_path: [],

      // disableDefaultUI: true,
      markers: [],
      places: [],
      currentPlace: null,
      mapStyle:{styles:[
      {
      "elementType": "geometry",
      "stylers": [
       {
         "color": "#1d2c4d"
       }
      ]
      },
      {
      "elementType": "labels.text.fill",
      "stylers": [
       {
         "color": "#8ec3b9"
       }
      ]
      },
      {
      "elementType": "labels.text.stroke",
      "stylers": [
       {
         "color": "#1a3646"
       }
      ]
      },
      {
      "featureType": "administrative.country",
      "elementType": "geometry.stroke",
      "stylers": [
       {
         "color": "#4b6878"
       }
      ]
      },
      {
      "featureType": "administrative.land_parcel",
      "elementType": "labels.text.fill",
      "stylers": [
       {
         "color": "#64779e"
       }
      ]
      },
      {
      "featureType": "administrative.province",
      "elementType": "geometry.stroke",
      "stylers": [
       {
         "color": "#4b6878"
       }
      ]
      },
      {
      "featureType": "landscape.man_made",
      "elementType": "geometry.stroke",
      "stylers": [
       {
         "color": "#334e87"
       }
      ]
      },
      {
      "featureType": "landscape.natural",
      "elementType": "geometry",
      "stylers": [
       {
         "color": "#023e58"
       }
      ]
      },
      {
      "featureType": "poi",
      "elementType": "geometry",
      "stylers": [
       {
         "color": "#283d6a"
       }
      ]
      },
      {
      "featureType": "poi",
      "elementType": "labels.text.fill",
      "stylers": [
       {
         "color": "#6f9ba5"
       }
      ]
      },
      {
      "featureType": "poi",
      "elementType": "labels.text.stroke",
      "stylers": [
       {
         "color": "#1d2c4d"
       }
      ]
      },
      {
      "featureType": "poi.park",
      "elementType": "geometry.fill",
      "stylers": [
       {
         "color": "#023e58"
       }
      ]
      },
      {
      "featureType": "poi.park",
      "elementType": "labels.text.fill",
      "stylers": [
       {
         "color": "#3C7680"
       }
      ]
      },
      {
      "featureType": "road",
      "elementType": "geometry",
      "stylers": [
       {
         "color": "#304a7d"
       }
      ]
      },
      {
      "featureType": "road",
      "elementType": "labels.text.fill",
      "stylers": [
       {
         "color": "#98a5be"
       }
      ]
      },
      {
      "featureType": "road",
      "elementType": "labels.text.stroke",
      "stylers": [
       {
         "color": "#1d2c4d"
       }
      ]
      },
      {
      "featureType": "road.highway",
      "elementType": "geometry",
      "stylers": [
       {
         "color": "#2c6675"
       }
      ]
      },
      {
      "featureType": "road.highway",
      "elementType": "geometry.stroke",
      "stylers": [
       {
         "color": "#255763"
       }
      ]
      },
      {
      "featureType": "road.highway",
      "elementType": "labels.text.fill",
      "stylers": [
       {
         "color": "#b0d5ce"
       }
      ]
      },
      {
      "featureType": "road.highway",
      "elementType": "labels.text.stroke",
      "stylers": [
       {
         "color": "#023e58"
       }
      ]
      },
      {
      "featureType": "transit",
      "elementType": "labels.text.fill",
      "stylers": [
       {
         "color": "#98a5be"
       }
      ]
      },
      {
      "featureType": "transit",
      "elementType": "labels.text.stroke",
      "stylers": [
       {
         "color": "#1d2c4d"
       }
      ]
      },
      {
      "featureType": "transit.line",
      "elementType": "geometry.fill",
      "stylers": [
       {
         "color": "#283d6a"
       }
      ]
      },
      {
      "featureType": "transit.station",
      "elementType": "geometry",
      "stylers": [
       {
         "color": "#3a4762"
       }
      ]
      },
      {
      "featureType": "water",
      "elementType": "geometry",
      "stylers": [
       {
         "color": "#0e1626"
       }
      ]
      },
      {
      "featureType": "water",
      "elementType": "labels.text.fill",
      "stylers": [
       {
         "color": "#4e6d70"
       }
      ]
      }
      ]}}},

  mounted () {
      this.$http
        .get('/ride')
        .then(response => {

          this.main_path = response.data.itineraries[0].itinerary.map( point =>{
            console.log(point)
            return {lat: point.x, lng: point.y}

          })

        })
        .catch(error => console.log(error))
      // latitude=this.info.itineraries[0].itinerary[0].x;
      // console.log(latitude);
      // this.geolocate()
  },

  methods: {
    // receives a place object via the autocomplete component

    geolocate: function () {
      navigator.geolocation.getCurrentPosition(position => {
        this.center = {
        lat: position.coords.latitude,
        lng: position.coords.longitude
        }
      })
    }
  }
}
</script>
