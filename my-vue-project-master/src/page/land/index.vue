<template>
  <div class="container">
    <searchStack :map="map"></searchStack>
    <layers :map="map" ref="layers"></layers>
    <toolbar :map="map" @click-right-item="clickRightItem"></toolbar>
    <div class="mapContainer" id="mapContainer"></div>
  </div>
</template>

<script>
import * as L from "leaflet";
import 'leaflet/dist/leaflet.css';
// import axios from "axios";

//如果这里不使用new L.Proj，使用L.Proj会出现报错**Error in mounted hook: "TypeError: this.callInitHooks is not a function"**
// let CRS_4490 = new L.Proj.CRS("EPSG:4490", "+proj=longlat +ellps=GRS80 +no_defs", {
//           resolutions: [
//             1.4062500068012802,
//             0.7031250000000002,
//             0.3515625000000001,
//             0.17578125000000006,
//             0.08789062500000003,
//             0.043945312500000014,
//             0.021972656250000007,
//             0.010986328125000003,
//             0.005493164062500002,
//             0.002746582031250001,
//             0.0013732910156250004,
//             6.866455078125002E-4,
//             3.433227539062501E-4,
//             1.7166137695312505E-4,
//             8.583068847656253E-5,
//             4.2915344238281264E-5,
//             2.1457672119140632E-5,
//             1.0728836059570316E-5,
//             5.364418029785158E-6,
//             2.6822090148925785E-6,
//             1.3411045074462893E-6
//           ],
//           origin: [-180.0, 90.0],
//           bounds: L.bounds([102.91070446372038, 30.040562599897378, ], [104.9786245822907, 31.472138017415993])
//           //这里可以有origin、transformation、scales、resulutions、bounds几个参数提供
//           //选择，其中scales与resolutions不能同时配置
//         });
//         //将CRS_4490添加到L.CRS中
//         L.Proj.addProjection(CRS_4490);

export default {
  components: {
    toolbar: () => import('./toolbar.vue'),
    layers: () => import('./layers.vue'),
    searchStack: () => import('./searchStack.vue'),
  },
  data() {
    return {
      map: null,

    };
  },
  beforeMount() {},
  mounted() {
    this.$nextTick(function () {
      this.initMap();
    });
  },
  methods: {
    // 初始化 cesium 应用程序
    // 初始化地图
    initMap() {
      //自定义leaflet天地图经纬度坐标
      L.CRS.CustomEPSG4490 = L.extend({}, L.CRS.Earth, {
        code: 'EPSG:4490',
        projection: L.Projection.LonLat,
        transformation: new L.Transformation(1 / 180, 1, -1 / 180, 0.5),
        scale: function (zoom) {
          return 256 * Math.pow(2, zoom - 1);
        }
      });

      var map = L.map("mapContainer", {
        center: [30.220312995943516, 120.57159530172422],
        zoom: 10,
        // crs: CRS_4490,
        // crs: L.CRS.CustomEPSG4490,
        // layers: , // 位于pulic leaflet.ChineseTmsProvider.js中
        zoomControl: false,
        worldCopyJump: false,
        attributionControl: false,
      });
      this.map = map;
      window.map = map;

      // // 创建一个 XYZ 切片图层实例  
      // var xyzLayer = L.tileLayer('http://localhost:9001/heliu/{z}/{x}/{y}.png', {  
      //     maxZoom: 16,  
      //     attribution: '© company xx'  
      // });  
        
      // // 将 XYZ 切片图层添加到地图中  
      // xyzLayer.addTo(map);

      // // 加载wms 水域业务图层
      // let wmsLayer = L.tileLayer.wms("/geoserver/shuiyu/wms?", {
      //   layers: "shuiyu:shuiyu", // 图层名，多个以逗号隔开
      //   format: "image/png",
      //   transparent: true,
      //   crs: L.CRS.EPSG3857,
      // });
      // //添加图层到地图
      // wmsLayer.addTo(map);

      // // 业务点数据，可以直接从后台取，此处模拟数据
      // let data = [{name:'建乐闸站', position:[32.3935, 119.54]}, {name:'向阳河闸', position:[32.3819, 119.654]}, {name:'砖桥河闸', position:[32.44, 119.64]}]

      // data.forEach(item=>{
      //   let divIcon = L.divIcon({
      //         html: `<div class="div-wrap"><img src="${require('../img/st.png')}" width=30 height=20/><span>${item.name}</span></<div>`,
      //         className: 'my-div-icon'
      //       });
      //       L.marker(item.position, { icon: divIcon }).bindPopup(() => {
      //         return JSON.stringify({});
      //       }).addTo(map);
      // })

    },

    // 放大
    addGeojson() {},

    clickRightItem(item) {
      console.log(item);
      this.$refs.layers.clickRightItem(item);
    }
  },
};
</script>

<style lang="less" scoped>
.container{
  width: 100%;
  height: 100%;
}
.mapContainer{
  width: 100%;
  height: 100%;
}

/deep/ .my-div-icon .div-wrap{
  display: flex;
  align-items: center;
  width: 200px;
}
/deep/ .my-div-icon .div-wrap span{
  border:  3px solid #02227e;
  padding: 2px 5px;

  color: #fff;
  font-size: 16px;
}
</style>