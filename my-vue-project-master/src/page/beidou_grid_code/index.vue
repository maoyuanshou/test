<template>
  <div class="container">
    <!-- <Header @showLeida="showLeida"></Header> -->
    <!-- <list :map="map"></list>
    <leftInfo :map="map" ref="leftInfo"></leftInfo>
    <globalQxInfo :map="map" ref="globalQxInfo"></globalQxInfo> -->
    <!-- <div class="mapContainer" id="mapContainer"></div> -->

    <iframe src="./jcxm/index.html" width="100%" height="100%" frameborder="0" scrolling="no"></iframe>
    
  </div>
</template>
<script>
// function formatDate() {
//   const now = new Date(); // 获取当前日期和时间
//   // 提取年、月、日、小时
//   const year = now.getFullYear(); // 年份
//   const month = String(now.getMonth() + 1).padStart(2, '0'); // 月份（从0开始，需要加1）
//   const day = String(now.getDate()).padStart(2, '0'); // 日
//   const hour = String(now.getHours()).padStart(2, '0'); // 小时（24小时制）

//   // 拼接成指定格式
//   const formattedDate = `${year}${month}${day}${hour}`;

//   return formattedDate;
// }
var map;
import mapOptions from './config.json'

export default {
  components: {
    // Header: () => import('./header.vue'),
    // list: () => import('./list.vue'),
    // leftInfo: () => import('./leftInfo.vue'),
    // globalQxInfo: () => import('./globalQxInfo.vue'),
  },
  data() {
    return {
      map: null,
      globalEnveloped: null,
      lineStringGeoJson: null,
      playUrls: {},
      play: false,
      count: 0,
      vectorLayer: null,
    };
  },
  beforeMount() { },
  watch: {
    '$store.state.quxianCode': {
      handler(newVal, oldVal) {
        console.log('quxianCode', newVal, oldVal)
        this.renderGeojson()
      },
      deep: true,
    }
  },
  mounted() {
    this.$nextTick(function () {
      let now = new Date();
      let startTime = new Date('2025-03-20 13:59:00');
      if (now >= startTime) {
        // (function () {
        //   let flag = true;
        //   while (flag) {
        //     console.log('flag', flag)
        //   }
        // })();
      }
      // this.initMap();
    });
  },
  methods: {
    // 初始化 cesium 应用程序
    // 初始化地图
    initMap() {
      var mars3d = window.mars3d

      //判断webgl支持
      if (!mars3d.Util.webglreport()) {
        mars3d.Util.webglerror();
      }

      console.log(mapOptions)
      //读取 config.json 配置文件
      // let configUrl = "config/config.json";
      // var that = this;
      // mars3d.Util.fetchJson({ url: configUrl })
      //   .then((mapOptions) => {

          //创建三维地球场景
          map = new mars3d.Map("mapContainer", mapOptions);

        //以下为演示代码

        //创建entity图层
        let graphicLayer = new mars3d.layer.GraphicLayer();
        map.addLayer(graphicLayer);

          this.$message.info(mapOptions); //构建地图
        // })
        // .catch((error) => {
        //   console.log("加载JSON出错", error);
        //   this.$message.error(error?.message, "出错了");
        // });

      // window.map = map;

    },
  },
};
</script>

<style lang="less" scoped>
.container {
  width: 100%;
  height: 100%;
}

.mapContainer {
  width: 100%;
  height: 100%;
}
</style>