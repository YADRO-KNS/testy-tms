const path = require("path");
const Dotenv = require('dotenv-webpack');
const webpack = require('webpack')

module.exports = (env) => {
    return (
        {
            plugins: [
                env.WEBPACK_SERVE
                    ? new Dotenv()
                    : new webpack.DefinePlugin({
                        'process.env': JSON.stringify(process.env)
                    })
            ],
            entry: {
                "test-suites-app": "./src/index.js"
            },
            output: {
                path: path.resolve(__dirname, env.WEBPACK_SERVE ? '../../dist/assets/js/apps' : 'build'),
                filename: "test-suites-app.js",
            },
            devServer: {
                devMiddleware: {
                    writeToDisk: true,
                },
            },
            module: {
                rules: [
                    {
                        test: /\.jsx?$/,
                        exclude: /(node_modules)/,
                        loader: "babel-loader",
                        options: {
                            presets: ["@babel/preset-env", "@babel/preset-react"]
                        }
                    },
                ]
            },
        })
}