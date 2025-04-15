<template>
    <div>
        <div class="toolbar-left">
            <img src="./images/comp.png" width="29" height="94" />
            <img src="./images/ic_zoom_out.png" width="42" @click.prevent="map.flyTo([24.97, 114.07], 13)" />
            <img src="./images/ic_add.png" width="42" @click.prevent="map.zoomIn()" />
            <img src="./images/ic_remove.png" width="42" @click.prevent="map.zoomOut()" />
            <!-- <input type="text" class="toolbar-xyinput" v-show="showXyInput" placeholder="输入坐标" v-model="xy_coor" v-on:keyup.enter="map.flyTo(xy_coor.split(',').map(Number).reverse(), 14);showXyInput = false">
            <el-button icon="el-icon-location-outline" @click.prevent="showXyInput = true"></el-button>
            <el-button-group  class="toolbar-control"  @click.prevent="">
                 <el-button  icon="el-icon-monitor" @click.prevent="map.toggleFullscreen()"></el-button>
                <el-button  icon="el-icon-monitor" @click.prevent="map.flyTo([24.97, 114.07], 13)"></el-button> 
                <el-button  icon="el-icon-plus" @click.prevent="map.zoomIn()"></el-button>
                <el-button  icon="el-icon-minus" @click.prevent="map.zoomOut()"></el-button>
            </el-button-group > -->
        </div>
        <div class="toolbar-right">
            <div class="item" @click.prevent="clickRightItem('图层')">
                <img src="./images/ic_filter2-web.png" width="50" />
                <span>图层</span>
            </div>
            <div class="item">
                <img src="./images/overlayanalysispng-web.png" width="50" />
                <span>分析</span>
            </div>
            <div class="item">
                <img src="./images/shp2-web.png" width="50" @click.prevent="map.flyTo([24.97, 114.07], 13)" />
                <span>SHP</span>
            </div>
            <div class="item">
                <img src="./images/tool_line-web.png" width="50" @click.prevent="map.zoomIn()" />
                <span>测距</span>
            </div>
            <div class="item">
                <img src="./images/ic_remove.png" width="50" @click.prevent="map.zoomOut()" />
                <span>图层</span>
            </div>
        </div>
    </div>
</template>

<script>
// import * as L from "leaflet";


export default {
    name: 'toolbar',
    props: {
        map: {
            type: Object,
            default: () => { }
        }
    },
    data() {
        return {
            showXyInput: false,
            xy_coor: '',
        }
    },
    mounted() {
    },
    methods: {
        clickRightItem(type) {
            this.$emit('click-right-item', type);
            console.log('点击右侧图层');
        }
    }
}
</script>

<style scoped>
.toolbar-left {
    z-index: 999;
    position: absolute;
    top: 100px;
    left: 30px;
    background-color: rgb(255, 255, 255);
    border-radius: 8px;
    padding: 4px;
    width: 42px;
    display: flex;
    align-items: center;
    flex-direction: column;
    /* box-shadow: 0px 0px 2px 2px rgb(250, 250, 250); */

    /* .toolbar-xyinput{
        position: absolute;
        right: 50px;
        top: 6px;
    }
    .toolbar-basemap{
        position: absolute;
        right: 0px;
        display: flex;
        bottom: 155px;
    }
    
    .toolbar-control{
        display: flex;
        flex-direction: column;
    } */
}

.toolbar-right {
    z-index: 999;
    position: absolute;
    top: 60px;
    right: 30px;
    background-color: rgb(255, 255, 255);
    border-radius: 8px;
    padding: 4px 10px;
    width: 42px;
    display: flex;
    align-items: center;
    flex-direction: column;

    .item {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        margin-bottom: 4px;
        cursor: pointer;
        border-bottom: 1px solid #ccc;
    }

    /* box-shadow: 0px 0px 2px 2px rgb(250, 250, 250); */

    /* .toolbar-xyinput{
        position: absolute;
        right: 50px;
        top: 6px;
    }
    .toolbar-basemap{
        position: absolute;
        right: 0px;
        display: flex;
        bottom: 155px;
    }
    
    .toolbar-control{
        display: flex;
        flex-direction: column;
    } */
}
</style>