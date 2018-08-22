import Vue from 'vue'

import axios from 'axios'
import BootstrapVue from 'bootstrap-vue'

import App from './App'
import router from './router'
import store from './store'

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import './fonts/fonts.css'
import './styles/styles.css'

import * as VueGoogleMaps from 'vue2-google-maps'
// import 'bootstrap/js/dist/modal'
import 'bootstrap'



Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAv2KTxY9QiIaWZg8JMXc9JA46mtzV5bOM',

  }
})

Vue.use(BootstrapVue)

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
// Vue.http = Vue.prototype.$http = axios
Vue.http = Vue.prototype.$http = axios.create({
  baseURL: `http://localhost:8080/api`,
  // headers: {
  //   Authorization: 'Bearer {token}'
  // }
})
Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app')
