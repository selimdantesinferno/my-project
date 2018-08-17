import Vue from 'vue'
import Router from 'vue-router'
import Menu1 from '@/components/menu1'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'landing-page',
      component: require('@/components/LandingPage').default
    },
    {
      path: '*',
      redirect: '/'
    },
    {
       path: '/menu1',
       name: 'Menu1',
       component: Menu1
   }
  ]
})
