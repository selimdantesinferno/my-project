import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'driving-page',
      component: require('@/components/DrivingPage').default
    },
     {
      path: '/test',
      name: 'old',
      component: require('@/components/itinerary').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
