import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/go',
      name: 'driving-page',
      component: require('@/components/DrivingPage').default
    },    
    {
      path: '/',
      name: 'welcome-page',
      component: require('@/components/WelcomePage').default
    }, 
    {
      path: '*',
      redirect: '/'
    }
  ]
})
