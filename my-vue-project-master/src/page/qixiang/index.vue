<template>
  <div class="container">
    <Header @showLeida="showLeida"></Header>
    <list :map="map"></list>
    <leftInfo :map="map" ref="leftInfo"></leftInfo>
    <globalQxInfo :map="map" ref="globalQxInfo"></globalQxInfo>
    <div class="mapContainer" id="mapContainer"></div>

    <div class="legend">
      <div class="gradient-bar"></div>
      <div class="text">
        <span>差</span>
        <span>中</span>
        <span>优</span>
      </div>
    </div>

    <el-button class="btn-play" type="success" :icon="!play ? 'el-icon-video-play' : 'el-icon-video-pause'" circle
      @click="addStaticImage"></el-button>
    <el-steps class="steps-container" :active="count">
      <el-step v-for="(item, index) in Object.keys(playUrls || {})" :key="index" :title="item / 100"
        icon="el-icon-s-flag"> </el-step>
      <!-- <el-step title="步骤 1" icon="el-icon-edit"></el-step>
      <el-step title="步骤 2" icon="el-icon-upload"></el-step>
      <el-step title="步骤 3" icon="el-icon-picture"></el-step> -->
    </el-steps>
  </div>
</template>
<!-- 该系统技术文档 https://ysp2s1zs4g.feishu.cn/docx/XnIHdc2QioN1IWxNvqScZtcsnnb -->
<script>
function formatDate() {
  const now = new Date(); // 获取当前日期和时间

  // 提取年、月、日、小时
  const year = now.getFullYear(); // 年份
  const month = String(now.getMonth() + 1).padStart(2, '0'); // 月份（从0开始，需要加1）
  const day = String(now.getDate()).padStart(2, '0'); // 日
  const hour = String(now.getHours()).padStart(2, '0'); // 小时（24小时制）

  // 拼接成指定格式
  const formattedDate = `${year}${month}${day}${hour}`;

  return formattedDate;
}
import { createLyrTian, createLyrTian_cva } from './mylayers.js'
// import axios from "axios";
let ol = window.ol;
import quxianMap from "./quxianMap.json";

export default {
  components: {
    Header: () => import('./header.vue'),
    list: () => import('./list.vue'),
    leftInfo: () => import('./leftInfo.vue'),
    globalQxInfo: () => import('./globalQxInfo.vue'),
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
      setTimeout(() => {
        this.initMap();
        this.addLayers();
      }, 1000);
    });
  },
  methods: {
    // 初始化 cesium 应用程序
    // 初始化地图
    initMap() {
      let map = new ol.Map({
        // 将地图对象绑定到id为"map"的div元素上。
        target: 'mapContainer',
        // 设置地图图层，这里用到了一个图片图层，其数据源为一个ImageWMS图层。
        layers: [
        ],
        // 视图
        view: new ol.View({
          // 中心点和缩放级别
          center: ol.proj.fromLonLat([110.17, 38.02136]),//此处替换为自己的中心点坐标
          zoom: 4.2
        }),
      });

      // let zoomslider = new ol.control.ZoomSlider();
      // map.addControl(zoomslider);

      const zoomToExtent = new ol.control.ZoomToExtent();
      map.addControl(zoomToExtent);
      this.map = map;
      window.map = map;

      // map.addLayer(createLyrTian_img())
      map.addLayer(createLyrTian())
      map.addLayer(createLyrTian_cva())

    },
    // 重置地图
    resizeMap() {
      this.map.fitBounds([this.globalEnveloped.geometry.coordinates[0].map(item => [item[1], item[0]])], { padding: [200, 200] });
    },
    // 渲染geojson数据
    renderGeojson() {
      let item = quxianMap.find(item => item['城市编码'] === this.$store.state.quxianCode)
      this.vectorLayer && this.map.removeLayer(this.vectorLayer);
      const vectorLayer = new ol.layer.Vector({
        source: new ol.source.Vector({
          // data: res,
          url: `/areas_v3/bound/${item['区县地区编码']}.json`, // 替换为你的GeoJSON文件URL
          format: new ol.format.GeoJSON()
        }),
        style: new ol.style.Style({
          fill: new ol.style.Fill({
            color: 'rgba(0, 255, 255, 0.2)' // 面填充颜色
          }),
          stroke: new ol.style.Stroke({
            color: 'green',
            width: 4
          })
        })
      });

      this.vectorLayer = vectorLayer;
      this.map.addLayer(vectorLayer);

      // 定位到GeoJSON数据的范围
      let that = this;
      vectorLayer.getSource().once('change', function () {
        if (this.getState() === 'ready') {
          const extent = this.getExtent();
          that.map.getView().fit(extent, that.map.getSize());
        }
      });
    },
  
    addLayers() {
      this.axios.get(`https://tiles.geovisearth.com/meteorology/v1/view/air/mfv/aqi_cn_bd_rt/aqi/range?start=${'2025010100'}&end=${formatDate()}`,
        {
          params: {
            // location: this.$store.state.quxianCode,
            token: '0f6a2507659fef660c63f88bb875abfd6a2314ef02aa8cc00e02d768af65dad7'
          },
        })
        .then(res => {
          if (res.status === 200) {
            let urls = res.data.result.urls
            if (Object.keys(urls).length > 0) {
              let urls = res.data.result.urls
              let keys = Object.keys(urls)
              let urlsArr = {}
              for (let i = 0; i < keys.length; i++) {
                if (parseInt(keys[i]) % 100 === 0) {
                  urlsArr[keys[i]] = urls[keys[i]]
                }
              }
              console.log(urlsArr)
              this.playUrls = urlsArr
              // this.addStaticImage()
            } else {
              this.$message.warning('暂无数据')
            }
          } else {
            this.url = ''
            // this.removeStaticImage()
            this.$message.error(res.data.message)
          }
        })
    },
    // 清除图层
    clearLayers() {
      this.playUrls = {};
      this.removeStaticImage();
      this.playTimer && window.clearInterval(this.playTimer);
    },
    // 添加静态图片 也就是
    addStaticImage() {
      if (this.play) {
        this.play = !this.play;
        this.removeStaticImage();
        window.clearInterval(this.playTimer);
        return false;
      }
      this.map.setView(new ol.View({
        // 中心点和缩放级别
        center: ol.proj.fromLonLat([110.17, 38.02136]),//此处替换为自己的中心点坐标
        zoom: 4.2
      }));
      this.play = !this.play;
      // 添加图片图层
      let keys = Object.keys(this.playUrls)
      // let count = 0;
      this.playTimer = setInterval(() => {
        this.removeStaticImage();
        this.currentTime = keys[this.count];
        this.imageLayer = new ol.layer.Image({
          source: new ol.source.ImageStatic({
            url: this.playUrls[keys[this.count]][0], // 替换为你的图片URL
            // imageSize: [4006, 2403], // 图片的尺寸（宽、高）
            imageExtent: ol.proj.transformExtent([73, 16, 136, 54], 'EPSG:4326', 'EPSG:3857') // 图片覆盖的地理范围
            // imageExtent: [-180, -90, 180, 90], // 图片覆盖的地理范围
          })
        });

        this.map.addLayer(this.imageLayer);
        this.count++;
        if (this.count === keys.length) {
          this.count = 0;
        }
      }, 2000)
    },
    // 移除静态图片
    removeStaticImage() {
      this.imageLayer && this.map.removeLayer(this.imageLayer);
    },

    showLeida(url) {
      console.log('$emit Url',url)
      url = `https://io-qos.geovisearth.com/getfile/35/visual/vucloud/mfv/nowcast/202503/2010/precipint_18202503201230a439889918dac6893b.png`
      this.removeStaticImage();
      this.imageLayer = new ol.layer.Image({
        source: new ol.source.ImageStatic({
          url, // 替换为你的图片URL
          // imageSize: [4006, 2403], // 图片的尺寸（宽、高）
          imageExtent: ol.proj.transformExtent([73, 16, 136, 54], 'EPSG:4326', 'EPSG:3857') // 图片覆盖的地理范围
          // imageExtent: [-180, -90, 180, 90], // 图片覆盖的地理范围
        })
      });

      this.map.addLayer(this.imageLayer);
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

.legend {
  position: absolute;
  bottom: 10px;
  left: 450px;

  .gradient-bar {
    width: 20px;
    /* bar条的宽度 */
    height: 250px;
    /* bar条的高度 */
    background: linear-gradient(to top, red, yellow, green);
    /* 从左到右的渐变色 */
  }

  .text {
    width: 20px;
    height: 250px;
    position: absolute;
    right: -26px;
    top: 0;
    display: flex;
    justify-content: space-between;
    flex-direction: column-reverse;
    font-size: 16px;
  }

}


.btn-play {
  position: absolute;
  bottom: 22px;
  left: 490px;
}

.steps-container {
  background-color: rgba(4, 19, 30, 0.5);
  position: absolute;
  bottom: 10px;
  left: 545px;
  width: 50%;
  text-align: center;
  padding: 10px;
}

/deep/ .my-div-icon .div-wrap {
  display: flex;
  align-items: center;
  width: 200px;
}

/deep/ .my-div-icon .div-wrap span {
  border: 3px solid #02227e;
  padding: 2px 5px;

  color: #fff;
  font-size: 16px;
}
</style>