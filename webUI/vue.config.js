const { defineConfig } = require("@vue/cli-service");
const CompressionPlugin = require("compression-webpack-plugin");
module.exports = defineConfig({
  transpileDependencies: true,
  lintOnSave: false,
});
module.exports = {
  pages: {
    index: {
      // entry for the pages
      entry: "src/views/index/index.js",
      // the source template
      template: "src/views/index/index.html",
      // output as dist/index.html
      filename: "index.html",
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: "xxx",
      // chunks to include on this pages, by default includes
      // extracted common chunks and vendor chunks.
      //chunks: ['chunk-vendors', 'chunk-common', 'index']
    },
    burden: {
      // entry for the pages
      entry: "src/views/burden/burden.js",
      // the source template
      template: "src/views/burden/burden.html",
      // output as dist/index.html
      filename: "burden.html",
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: "Burden Analysis | xxx",
    },
    PartHub: {
      // entry for the pages
      entry: "src/views/parthub/parthub.js",
      // the source template
      template: "src/views/parthub/parthub.html",
      // output as dist/index.html
      filename: "parthub.html",
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: "PartHub | xxx",
    },
    parts: {
      // entry for the pages
      entry: "src/views/parts/parts.js",
      // the source template
      template: "src/views/parts/parts.html",
      // output as dist/index.html
      filename: "parts.html",
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: "PartHub Results | xxx",
    },
    treeMap: {
      // entry for the pages
      entry: "src/views/treeMap/treeMap.js",
      // the source template
      template: "src/views/treeMap/treeMap.html",
      // output as dist/index.html
      filename: "treeMap.html",
      // when using title option,
      // template title tag needs to be <title><%= htmlWebpackPlugin.options.title %></title>
      title: "Parts | xxx",
    },
  },
  css: {
    loaderOptions: {
      less: {
        lessOptions: {
          javascriptEnabled: true,
          modifyVars: {
            "primary-color": "#e37654",
            "pagination-font-family": "Barlow",
            "font-family": "HarmonyOS_Sans, Helvetica, Arial, sans-serif",
          },
        },
      },
    },
  },
  chainWebpack: (config) => {
    config.plugin("compressionPlugin").use(
      new CompressionPlugin({
        test: /\.(js|css|less)$/,
        threshold: 1024,
        deleteOriginalAssets: false,
        minRatio: 0.3,
      })
    );
  },
};
