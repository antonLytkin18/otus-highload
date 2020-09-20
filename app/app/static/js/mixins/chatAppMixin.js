let chatAppMixin = {
    data: () => ({
        chatAppUrl: process.env.CHAT_APP_URL,
    }),
    methods: {
        makeChatAppRequest: function (method, path, data, url) {
            path = path ? path : ''
            return axios
                .request({
                    url: url ? url + path : this.chatAppUrl + path,
                    method: method,
                    headers: {
                        'Authorization': 'JWT ' + this.$cookies.get('auth_token'),
                    },
                    data: data,
                });
        }
    }
};
export default chatAppMixin