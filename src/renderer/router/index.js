import Vue from 'vue'
import Router from 'vue-router'
import Menu1 from '@/components/menu1'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/go',
      path: '/',
      name: 'driving-page',
      component: require('@/components/DrivingPage').default
    },    
    {
      // path: '/',
      path: '/welcome',
      name: 'welcome-page',
      component: require('@/components/WelcomePage').default
    }, 
    {
      path: '/start',
      // path: '/',
      name: 'start-page',
      component: require('@/components/StartPage').default
    }, 
    {
      path: '*',
      redirect: '/'
    }
    ,
    {
       path: '/menu1',
       name: 'Menu1',
       component: Menu1
   }
  ]
})
