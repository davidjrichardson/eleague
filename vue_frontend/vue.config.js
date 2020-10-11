const BundleTracker = require("webpack-bundle-tracker");

const pages = {
    'dashboard': {
        entry: './src/dashboard.js',
        chunks: ['chunk-vendors']
    },
}

module.exports = {
    pages: pages,
    filenameHashing: false,
    productionSourceMap: false,
    publicPath: process.env.NODE_ENV === 'production'
        ? ''
        : 'http://localhost:8080/',
    outputDir: '../static/vue/',

    chainWebpack: config => {

        config.optimization
            .splitChunks({
                cacheGroups: {
                    vendor: {
                        test: /[\\/]node_modules[\\/]/,
                        name: "chunk-vendors",
                        chunks: "all",
                        priority: 1
                    },
                },
            });

        Object.keys(pages).forEach(page => {
            config.plugins.delete(`html-${page}`);
            config.plugins.delete(`preload-${page}`);
            config.plugins.delete(`prefetch-${page}`);
        })

        const svgRule = config.module.rule('svg');
        svgRule.uses.clear();

        svgRule.use('vue-loader')
            .loader('vue-loader')
            .end()
            .use('vue-svg-loader')
            .loader('vue-svg-loader')

        config
            .plugin('BundleTracker')
            .use(BundleTracker, [{filename: '../../vue_frontend/webpack-stats.json'}]); // This is relative to outputDir

        config.resolve.alias
            .set('__STATIC__', 'static')

        config.devServer
            .public('http://localhost:8080')
            .host('localhost')
            .port(8080)
            .hotOnly(true)
            .watchOptions({poll: 1000})
            .https(false)
            .headers({"Access-Control-Allow-Origin": ["*"]})

    }
};