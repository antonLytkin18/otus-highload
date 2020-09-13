const path = require('path');
const PATHS = {
    app: path.resolve(__dirname, 'app/static/js'),
    build: path.resolve(__dirname, 'app/static/build')
};
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const Dotenv = require('dotenv-webpack');

module.exports = {
    entry: {
        app: PATHS.app + '/app.js'
    },
    output: {
        path: PATHS.build,
        filename: 'bundle.js'
    },
    resolve: {
        alias: {
            'vue': 'vue/dist/vue.common.js',
        }
    },
    module: {
        rules: [
            {
                test: /\.vue$/,
                loader: 'vue-loader',
            },
            {
                test: /\.css$/i,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.png$/,
                use: "url-loader?limit=100000"
            },
            {
                test: /\.jpg$/,
                use: "file-loader"
            },
            {
                test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/,
                use: 'url-loader?limit=10000&mimetype=application/font-woff'
            },
            {
                test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/,
                use: 'url-loader?limit=10000&mimetype=application/octet-stream'
            },
            {
                test: /\.eot(\?v=\d+\.\d+\.\d+)?$/,
                use: 'file-loader'
            },
            {
                test: /\.svg(\?v=\d+\.\d+\.\d+)?$/,
                use: 'url-loader?limit=10000&mimetype=image/svg+xml'
            }
        ],
    },
    plugins: [
        new Dotenv({
            safe: false,
            systemvars: true
        }),
        new VueLoaderPlugin()
    ]
};