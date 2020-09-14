let urlMixin = {

    methods: {
        populateUrl: function (url, params) {
            for (const key in params) {
                url = url.split(':' + key).join(params[key])
            }
            return url;
        }
    }
};
export default urlMixin