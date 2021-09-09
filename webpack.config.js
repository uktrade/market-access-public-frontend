const path = require("path");
const BundleTracker = require("webpack-bundle-tracker");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CopyPlugin = require("copy-webpack-plugin");

const assetsSrcPath = path.resolve(__dirname, "apps/static/src/")
const assetsBuildPath = path.resolve(__dirname, "apps/static/dist")

const mainConfig = {
    entry: {
        main: path.resolve(assetsSrcPath, "js/index.js"),
        style: path.resolve(assetsSrcPath, "scss/index.scss")
    },
    output: {
      path: path.resolve(assetsBuildPath, "webpack_bundles"),
      publicPath: "/static/webpack_bundles/",
      filename: "[name]-[fullhash].js",
      clean: true,
      iife: false
    },
    plugins: [
        new BundleTracker({ filename: "./webpack-stats.json" }),
        new MiniCssExtractPlugin({
            filename: "[name]-[fullhash].css",
            chunkFilename: "[id]-[fullhash].css",
        }),
        new CopyPlugin({
            patterns: [
                { from: path.resolve(assetsSrcPath,"govuk-public/"), to: "../govuk-public" }
            ],
        }),
  ],
  module: {
    rules: [
    {
        test: /\.(woff2?)$/i,
        type: 'asset/resource',
        generator: {
            filename: "../fonts/[name].[ext]"
        }
    },
    {
        test: /\.(png|jpe?g|gif|svg|ico|eot)$/i,
        type: 'asset/resource',
        generator: {
            filename: "../images/[name].[ext]"
        }
    },
    {
      test: /\.s[ac]ss$/i,
      use: [
        {
          loader: MiniCssExtractPlugin.loader,
        },
        "css-loader",
        "sass-loader",
      ],
    },
        {
          test: /\.m?js$/,
          exclude: /(node_modules)/,
          use: {
            loader: 'babel-loader',
            options: {
              presets: ['@babel/preset-env']
            }
          }
        }

    ],
  },

  resolve: {
    modules: ["node_modules"],
    extensions: [".js", ".scss"],
  },

  devtool:
    process.env.NODE_ENV == "development" ? "eval-source-map" : "source-map",
}

module.exports = mainConfig
