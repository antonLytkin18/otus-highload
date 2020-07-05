import Vue from 'vue'
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
import urlMixin from "./mixins/urlMixin.js";

Vue.mixin(urlMixin);
Vue.component('v-form', require('./components/Form.vue').default);
Vue.component('v-filter-form', require('./components/FilterForm.vue').default);
Vue.component('v-follower', require('./components/Follower.vue').default);
Vue.component('v-follower-list', require('./components/FollowerList.vue').default);
Vue.component('v-follower-actions', require('./components/FollowerActions.vue').default);

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)

window.axios = require('axios');

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

new Vue({
    el: '#app',
});
