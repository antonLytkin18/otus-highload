import Vue from 'vue'
import {BootstrapVue, IconsPlugin} from 'bootstrap-vue'
import urlMixin from "./mixins/urlMixin.js";
import vSelect from "vue-select";
import "vue-select/dist/vue-select.css";

Vue.mixin(urlMixin);
Vue.component('v-form', require('./components/Form.vue').default);
Vue.component('v-filter-form', require('./components/FilterForm.vue').default);
Vue.component('v-follower', require('./components/Follower.vue').default);
Vue.component('v-follower-list', require('./components/FollowerList.vue').default);
Vue.component('v-follower-actions', require('./components/FollowerActions.vue').default);
Vue.component('v-chat-message-list', require('./components/Chat/ChatMessageList.vue').default);
Vue.component('v-chat-list', require('./components/Chat/ChatList.vue').default);
Vue.component('v-chat-income-message', require('./components/Chat/ChatIncomeMessage.vue').default);
Vue.component('v-chat-outcome-message', require('./components/Chat/ChatOutcomeMessage.vue').default);
Vue.component('v-feed', require('./components/Feed/Feed.vue').default);
Vue.component('v-feed-post', require('./components/Feed/FeedPost.vue').default);
Vue.component('v-select', vSelect);

Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.config.devtools = true

window.axios = require('axios');

import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

new Vue({
    el: '#app',
});
