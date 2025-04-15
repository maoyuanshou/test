<template>
    <div :class="{'layer': true, 'show': showPanel, 'hide':!showPanel}">
        <div class="title">地图</div>
        <div class="basemap">
            <div v-for="item in baseMaps" :key="item.title" class="basemap-item" @click.prevent="toggleBasemap(item)">
                <img :src="item.imgUrl" />
                <span>{{item.title}}</span>
            </div>
        </div>
        <!-- <el-button-group class="layer-layer">
            <el-button  @click.prevent="toggleBasemap('normal')">天地图电子地图</el-button>
            <el-button  @click.prevent="toggleBasemap('image')">天地图影像</el-button>
        </el-button-group>
        <input type="text" class="layer-xyinput" v-show="showXyInput" placeholder="输入坐标" v-model="xy_coor" v-on:keyup.enter="map.flyTo(xy_coor.split(',').map(Number).reverse(), 14);showXyInput = false">
        <el-button icon="el-icon-location-outline" @click.prevent="showXyInput = true"></el-button>
        <el-button-group  class="layer-control"  @click.prevent="">
            <el-button  icon="el-icon-monitor" @click.prevent="map.flyTo([24.97, 114.07], 13)"></el-button> 
            <el-button  icon="el-icon-plus" @click.prevent="map.zoomIn()"></el-button>
            <el-button  icon="el-icon-minus" @click.prevent="map.zoomOut()"></el-button>
        </el-button-group > -->
        <div class="layer-control" @click.prevent="showPanel = false">
            <i class="el-icon-arrow-right"></i>
            <!-- <i class="el-icon-arrow-left" v-else></i> -->
        </div>
    </div>
</template>

<script>
import * as L from "leaflet";
const esri = require('esri-leaflet');
// const xzqhLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
//   attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
// })

const image = L.tileLayer('http://t{s}.tianditu.gov.cn/img_w/wmts?tk=2e3273c0d2bf1d9f011d7beaffc3881a&SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TileMatrix={z}&TileCol={x}&TileRow={y}', {
  subdomains: [0, 1, 2, 3, 4, 5, 6, 7],
  id: 'image'
})
// const normal = L.tileLayer('http://t0.tianditu.gov.cn/vec_w/wmts?&tk=2e3273c0d2bf1d9f011d7beaffc3881a&SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={x}&TILECOL={y}', {
//   subdomains: [0, 1, 2, 3, 4, 5, 6, 7],
// })
const normal = L.tileLayer('http://t{s}.tianditu.com/DataServer?T=vec_w&X={x}&Y={y}&L=1&tk=2e3273c0d2bf1d9f011d7beaffc3881a', {
  subdomains: [0, 1, 2, 3, 4, 5, 6, 7],
})
const cia_w = L.tileLayer('http://t{s}.tianditu.gov.cn/cia_w/wmts?tk=2e3273c0d2bf1d9f011d7beaffc3881a&SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cia&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TileMatrix={z}&TileCol={x}&TileRow={y}', {
  subdomains: [0, 1, 2, 3, 4, 5, 6, 7],
  transparent: true,
  zIndex: 3,
  id: 'cia_w'
})

//天地图图组
const tiandiImageMap = L.layerGroup([image, cia_w,]);
const tiandiNormalMap = L.layerGroup([normal, cia_w])

export default {
    name: 'layers',
    props: {
        map: {
            type: Object,
            default: () => {}
        }
    },
    data() {
        return {
            showPanel: false,
            xy_coor: '',
            currentBasemap: tiandiImageMap,
            baseMaps: [
                {
                    type: 'dynamicMapLayer',
                    url: '/arcgis/rest/services/xzqh2021/MapServer',
                    imgUrl: require('./images/ght-web.png'),
                    title: '规划图202105'
                },
                {
                    type: 'dynamicMapLayer',
                    url: 'https://sampleserver6.arcgisonline.com/arcgis/rest/services/Hurricanes/MapServer/',
                    imgUrl: require('./images/ght-web.png'),
                    title: 'TEST沿海'
                },
                {
                    type: 'MapServer',
                    url: 'https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer',
                    imgUrl: require('./images/kgt-web.png'),
                    title: '控规202112'
                },
                {
                    type: 'tiledMapLayer',
                    url: 'https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer',
                    imgUrl: require('./images/kgt-web.png'),
                    title: 'TEST中国区影像'
                },
                {
                    type: 'dynamicMapLayer',
                    url: 'http://118.31.43.251:6080/arcgis/rest/services/landwgs84/MapServer',
                    imgUrl: require('./images/zgt-web.png'),
                    title: '杭州总规'
                },
                // {
                //     type: 'dynamicMapLayer',
                //     url: '/arcgis/rest/services/land20/MapServer',
                //     imgUrl: require('./images/kfbjmapimp-web.png'),
                //     title: '开发边界'
                // },
                // {
                //     type: 'tiledMapLayer',
                //     url: '',
                //     imgUrl: require('./images/jbntmapimp-web.png'),
                //     title: '基本农田'
                // },
                {
                    type: 'TDT_VEC',
                    url: '',
                    imgUrl: require('./images/map_tdt.png'),
                    title: '天地图'
                },
                {
                    type: 'TDT_IMG',
                    url: '',
                    imgUrl: require('./images/map_google.png'),
                    title: '天地影像'
                },
                {
                    type: 'MapServer',
                    url: 'http://zhtj.xiaoshan.gov.cn:6060/arcgis/rest/services/WXYX202110/MapServer',
                    imgUrl: require('./images/xzt-web.png'),
                    title: '其它底图'
                }
            ]
        }
    },
    mounted() {
        this.toggleBasemap(this.baseMaps.find(item => item.type === 'TDT_IMG'))
    },
    methods: {
        clickRightItem(item) {
            if (item === '图层') {
                this.showPanel = !this.showPanel
            }
        },
        toggleBasemap(item) {
            console.log(item)
            const { type , url } = item;
            if (type === 'TDT_VEC') {
                this.map.removeLayer(this.currentBasemap)
                this.currentBasemap = tiandiNormalMap
                this.map.addLayer(this.currentBasemap)
                this.currentBasemap.setZIndex(-1)
            } else if (type === 'TDT_IMG') {
                this.map.removeLayer(this.currentBasemap)
                this.currentBasemap = tiandiImageMap
                this.map.addLayer(this.currentBasemap)
                this.currentBasemap.setZIndex(-1)
            } 

            if (type === 'dynamicMapLayer') {
                esri.dynamicMapLayer({
                    url,
                    opacity: 1,
                    f: "image",
                    // noWrap: false,
                }).addTo(this.map);
            } else if (type === 'tiledMapLayer') {
                esri.tiledMapLayer({
                    url,
                    opacity: 1,
                    f: "image",
                    noWrap: false,
                }).addTo(this.map);
            }
        }

    }
}
</script>

<style scoped>
.layer {
    z-index: 1000;
    position: fixed;
    top: 0px;
    right: 0px;
    width: 500px;
    height: 100%;
    background: #fff;
    transition: transform .7s ease;

    &.hide{
        transform: translate(530px, 0);
    }
    &.show{
        transform: translate(0, 0);
    }

    .title {
        font-size: 20px;
        font-weight: bold;
        margin-left: 12px;
        margin-top: 8px;
    }

    .basemap {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-around;
        margin-top: 10px;

        .basemap-item {
            width: 100px;
            height: 120px;
            margin-bottom: 10px;
            position: relative;
            cursor: pointer;
            border: 1px solid #ccc;
            border-radius: 5px;
            background: #fff;
            box-shadow: 0 0 5px #ccc;

            img {
                width: 100%;
                height: 100px;
            }

            span {
                position: absolute;
                bottom: 0;
                left: 0;
                width: 100%;
                height: 24px;
                line-height: 20px;
                text-align: center;
                color: #333;
                font-size: 14px;
                /* background: rgba(0,0,0,0.5); */
                /* opacity: 0; */
                transition: all 0.3s ease-in-out;
            }

            &:hover {
                border-color: #f00;
            }

            &:hover span {
                opacity: 1;
            }
        }
    }
    .layer-layer{
        position: absolute;
        right: 0px;
        display: flex;
        bottom: 155px;
    }
    
    .layer-control{
        /* display: ; */
        /* flex-direction: column; */
        width: 30px;
        height: 60px;
        line-height: 60px;
        /* border-radius: 20px 0 0px 20px; */
        border-radius: 100% 0 0 100%;
        background: #fff;
        transform: translate(-30px, 0px);
        position: absolute;
        box-shadow: -10px 0px 10px 0px rgba(76, 69, 50, 60%);
        cursor: pointer;
        top: calc(50% - 30px);
        font-size: 30px;
    }
}
</style>