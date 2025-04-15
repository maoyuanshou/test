module.exports = {
    configureWebpack: {
        module: {
            rules: [{
                test: /\.(frag|vert|glsl)$/,
                use: [
                    {
                        loader: 'glsl-shader-loader',
                        options: {}
                    }
                ]
            }]
        }
    },
    devServer:{
        proxy:{
            '/geoserver': { // 匹配所有以'/api1'开头的请求路径
              target: "http://localhost:8081", // 代理目标的基础路径
            //   target: "http://47.115.201.167:8081", // 代理目标的基础路径
              changeOrigin: true, // 用于控制请求头中的host值，默认也为true，可以不设置
            //   pathRewrite: {'^/api1':''}  
            },
            '/mars3d': { 
                target: "http://data1.mars3d.cn", 
                changeOrigin: true, 
                pathRewrite: {'^/mars3d':''}  
            },
            // '/api': { 
            //     target: "http://localhost:8008", 
            //     changeOrigin: true, 
            //     // pathRewrite: {'^/mars3d':''}  
            // },
            '/areas_v3': { 
                target: 'https://geo.datav.aliyun.com', 
                changeOrigin: true, 
                // pathRewrite: {'^/mars3d':''}  
            },
            '/arcgis': {
                // target: 'http://zhtj.xiaoshan.gov.cn:6060',
                target: 'http://118.31.43.251:6080',
                changeOrigin: true,
            },
            '/fiber-optic': {
                target: 'http://1.95.79.36:5004',
                changeOrigin: true,
                pathRewrite: { '^/fiber-optic': '' },
            },
            '/api': {
                target: 'http://localhost:8008',
                changeOrigin: true,
            },
          }
    }
}