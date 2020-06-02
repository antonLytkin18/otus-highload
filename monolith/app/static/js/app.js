import Vue from 'vue'
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
import urlMixin from "./mixins/urlMixin.js";

Vue.mixin(urlMixin);
Vue.component('v-main', require('./components/Main.vue').default);
Vue.component('v-form', require('./components/Form.vue').default);
Vue.component('v-users-list', require('./components/UsersList.vue').default);
Vue.component('v-profile', require('./components/Profile.vue').default);

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

window.axios = require('axios');

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

new Vue({
    el: '#app',
});
