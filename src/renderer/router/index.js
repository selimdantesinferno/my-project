import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/g',
      name: 'driving-page',
      component: require('@/components/DrivingPage').default
    },    
    {
      path: '/welcome',
      name: 'welcome-page',
      component: require('@/components/WelcomePage').default
    }, 
    {
      // path: '/start',
      path: '/',
      name: 'start-page',
      component: require('@/components/StartPage').default
    }, 
    {
      path: '*',
      redirect: '/'
    }
  ]
})
