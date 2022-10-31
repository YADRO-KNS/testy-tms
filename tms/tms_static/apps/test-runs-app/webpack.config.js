const path = require("path");
const Dotenv = require('dotenv-webpack');

module.exports = (env) => {
    return (
        {
            plugins: [
                new Dotenv({
                    path: `.env.${env.goal}`
                }),
            ],
            entry: {
                "test-runs-app": "./src/index.js"
            },
            output: {
                path: path.resolve(__dirname, '../../dist/assets/js/apps'),
                filename: "test-runs-app.js",
                clean: true,
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