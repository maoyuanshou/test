<template>
    <div class="list-container">
        <div class="list-panel" :class="{ 'activeHide': isHideList }">
            <div class="title">
                <img :src="require('./images/title.png')" /> &nbsp;&nbsp;
                <span>未来24小时降水预测</span>
            </div>
            <div class="charts-content">
                <span style="font-size: 16px;color: #fff;padding-left: 10px;">
                    {{ tips }}
                </span>
                <div class="charts" ref="charts"></div>
            </div>
            
            <div class="title">
                <img :src="require('./images/title.png')" /> &nbsp;&nbsp;
                <span>全国空气质量排行榜</span>
            </div>
            <div class="search-panel">
                <img :src="require('./images/list/search.png')" />
                <input type="text" placeholder="Search by name" v-model="searchText" @keyup.enter="searchKeywords" />
            </div>
            <div class="item-title">
                <div class="item-left"> &nbsp; &nbsp; &nbsp; 地区</div>
                <div class="item-middle">  质量 </div> 
                <div class="item-right">排名 </div>
            </div>
            <div class="list-content">
                <div class="item" :class="{ 'active': item.ranking === selectItemRanking }"
                    v-for="(item, index) in res" :key="index" @click="showDetail(item)">
                    <div class="item-left"> &nbsp; {{ item.province + item.city }} </div>
                    <div class="item-middle"> &nbsp; 
                        <!-- <img :src="item.device_SysState ? require('./images/list/online.png') : require('./images/list/offline.png')" /> -->
                        <!-- &nbsp; {{ item.device_SysState ? 'Online' : 'Offline' }} </div> -->
                        &nbsp; {{ item.aqi }} </div> 
                    <div class="item-right"
                        :class="{ 'alarm-level-0': item.ranking < 400, 'alarm-level-1': item.ranking < 300, 'alarm-level-2': item.ranking < 200, 'alarm-level-3': item.ranking < 100, 'alarm-level-4': item.ranking < 50 }">
                        &nbsp; {{ item.ranking }} </div>
                    
                </div>
            </div>
        </div>
        <div class="btn-panel" @click="isHideList = !isHideList" :class="{ 'activeHide': isHideList }">
            <img :src="isHideList ? require('./images/list/left.png') : require('./images/list/right.png')" />
        </div>
    </div>
</template>

<script>
import * as L from "leaflet";
import * as echarts from 'echarts'

export default {
    name: 'equipmentList',
    props: {
        map: {
            type: Object,
            default: () => { }
        }
    },
    data() {
        return {
            searchText: '',
            xy_coor: '',
            res: [],
            res_temp: [],
            isHideList: false,
            selectItemRanking: '',
            deviceMarkers: [],
            tips:'',
            yuces: [],
        }
    },
    watch: {
        '$store.state.quxianCode': {
            handler() {
                this.yuCe()
            },
            deep: true,
            immediate: true
        }
    },
    mounted() {
        this.getAllEquipments()
    },
    methods: {
        searchKeywords() {
            this.res = this.res_temp.filter(item => {
                return (item.province + item.city).includes(this.searchText)
            })
        },
        getAllEquipments() {
            this.axios.get('https://tiles.geovisearth.com/meteorology/v1/weather/cn/realtime/aqi/rank', {
                params: {
                    asc: true,
                    token: '0f6a2507659fef660c63f88bb875abfd6a2314ef02aa8cc00e02d768af65dad7'
                },
            }).then(res => {
                if (res.status === 200) {
                    console.log(res.data.result.datas)
                    // this.visible = false
                    this.res = res.data.result.datas;
                    this.res_temp = res.data.result.datas;
                } else {
                    this.res = []
                    this.$message.error(res.data.message)
                }
            })
        },
        showDetail(item) {
            this.selectItemRanking = item.ranking
        },
        addMarkers(data) {
            // 先清空再渲染
            this.deviceMarkers.forEach(marker => {
                marker.remove();
            });
            this.deviceMarkers = [];

            let markers = [];
            data.forEach(item => {
                markers.push(L.marker([item.device_Latitude, item.device_Longitude].map(Number), {
                    icon: L.divIcon({
                        html: `<div class="div-wrap"><img src="${require(`./images/marker/10.png`)}" width=15 height=30 /></<div>`,
                        className: 'my-div-icon'
                    }),
                    iconAnchor: [9, 42]
                }).bindPopup(() => {
                    const el = document.createElement('div');

                    ['device_AlarmState', 'device_Details',
                        'device_GroupID', 'device_Height',
                        'device_ID',
                        'device_InstallationDate',
                        'device_Latitude',
                        'device_Longitude',
                        'device_MonitorRange',
                        'device_MonitorResolution',
                        'device_Name',
                        'device_SysState',
                        'device_WorkingChannel'].forEach(key => {
                            if (item[key]) {
                                el.innerHTML += `<div>${key}: ${item[key]}</div>`;
                            }
                        });
                    return el;
                }).addTo(this.map));
            })
            this.deviceMarkers = markers;

        },
        yuCe() {
            this.axios.get('https://tiles.geovisearth.com/meteorology/v1/weather/nowcast/point/desc', {
                params: {
                    // location:'116.44231081250001,32.725437071953905',
                    location: [116.44231081250001 - Math.random() * 5, 32.725437071953905 + Math.random() * 3].join(','),
                    token: '0f6a2507659fef660c63f88bb875abfd6a2314ef02aa8cc00e02d768af65dad7'
                },
            }).then(res => {
                if (res.status === 200) {
                    this.tips = res.data.result.tips;
                    this.yuces = res.data.result.series
                    let list = []
                    if (res.data.result.series.length > 0) {
                        list = res.data.result.series;
                    } else {
                        // 快速生成一个12个元素的数组
                        for (let i = 0; i < 25; i++) {
                            list.push(Math.random() * 1 + 1.5)
                        }
                    }
                    this.initCharts(list)
                } else {
                    this.$message.error('error')
                }
            })
        },
        initCharts(list) {
            // 饼状图, 自定义颜色
            let chart = echarts.init(this.$refs.charts)
            chart.clear()
            // 从此刻算，未来24小时，只取小时
            const now = new Date()
            const data = []
            for (let i = 0; i < 24; i++) {
                const date = new Date(now.getTime() + i * 3600 * 1000)
                const hour = date.getHours()
                // const value = list[i]
                data.push(`${hour}:00`)
            }
            const option = {
                title: {
                    show: false,
                    text: '',
                    top: '0',
                    left: 'center',
                    textStyle: {
                        color: '#fff'
                    }
                },
                tooltip: {
                    trigger: 'axis',
                },
                toolbox: {
                    feature: {
                    saveAsImage: {}
                    }
                },
                legend: {
                    show: false,
                    data: ['降雨量'],
                    // orient: 'vertical', // 设置为垂直布局
                    // right: '0%', // 将 legend 放到右侧
                    top: '0%', // 垂直居中
                    textStyle: {
                        color: '#fff'
                    }
                },
                grid: {
                    // top: '1%',
                    left: '1%',
                    right: '1%',
                    bottom: '1%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    // type: 'value',
                    data,
                    // 颜色
                    axisLine: {
                        lineStyle: {
                            color: '#fff'
                        }
                    },
                    axisLabel: {
                        color: '#fff'
                    },
                    splitLine: {
                        show: false // 去掉中间的网格横线
                    }
                },
                yAxis: {
                    type: 'value',
                    // 颜色
                    axisLine: {
                        lineStyle: {
                            color: '#fff'
                        }
                    },
                    axisLabel: {
                        color: '#fff'
                    },
                    splitLine: {
                        lineStyle: {
                            color: '#fff' // 纵轴网格线颜色
                        }
                    }
                },
                series: [
                    {
                        name: '降雨量',
                        type: 'line',
                        stack: 'Total',
                        data: list,
                    },
                ]
            };
            chart.setOption(option)
        }
    }
}
</script>

<style scoped>
.list-container {
    z-index: 999;
    position: fixed;
    top: 316.5px;
    right: 0px;
    width: 360px;
    height: calc(100% - 305px);
    /*  - 135px */


    .project-name {
        color: #fff;
        font-size: 22px;
        text-align: center;
        margin-bottom: 2px;
        text-shadow: 2px 1px 7px #000;
        white-space: nowrap;
    }

    .list-panel {
        background-color: rgba(4, 19, 30, 0.5);
        border-radius: 8px;
        padding: 4px 10px;
        display: flex;
        align-items: center;
        flex-direction: column;
        border: 2px solid #2A748A;
        color: #fff;
        height: calc(100% - 32px);
        /* 抽屉效果 */
        transition: transform 0.5s ease-in-out;

        &.activeHide {
            transform: translateX(360px);
        }

        .title {
            display: flex;
            justify-content: flex-start;
            align-items: center;
            width: 100%;
            font-size: 18px;
            height: 35px;
            line-height: 35px;
            border-bottom: 1px solid #2A748A;

            img {
                width: 16px;
            }
        }

        .search-panel {
            margin-top: 10px;
            width: 100%;
            position: relative;

            img {
                position: absolute;
                left: 8px;
                top: 8px;
                width: 16px;
            }

            input {
                height: 30px;
                display: block;
                width: 308px;
                border-radius: 30px;
                background: rgba(64, 237, 255, 0.2);
                border: 0;
                padding-left: 30px;
                color: #fff;

                &:focus {
                    outline: none;
                    color: #fff;
                    caret-color: rgba(64, 237, 255, 0.5);
                }
            }
        }

        .item-title{
            width: 100%;
                display: flex;
                margin: 5px 0;
                padding: 2px 0;
                justify-content: space-between;
                align-items: center;
                cursor: pointer;

                &.active {
                    background-color: rgba(64, 237, 255, 0.2);
                }

                .item-left {
                    font-size: 16px;
                    width: 200px;
                    text-align: left;
                }

                .item-middle {
                    font-size: 14px;
                    width: 50px;
                    display: flex;
                    justify-content: flex-start;
                    align-items: center;
                }

                .item-right {
                    font-size: 14px;
                    font-weight: bold;
                    width: 50px;
                    text-align: center;
                }
        }

        .list-content {
            padding-left: 10px;
            overflow-y: auto;

            .item {
                width: 100%;
                display: flex;
                margin: 5px 0;
                padding: 2px 0;
                justify-content: space-between;
                align-items: center;
                cursor: pointer;

                &.active {
                    background-color: rgba(64, 237, 255, 0.2);
                }

                .item-left {
                    font-size: 16px;
                    width: 200px;
                    text-align: left;
                }

                .item-middle {
                    font-size: 14px;
                    width: 50px;
                    display: flex;
                    justify-content: flex-start;
                    align-items: center;
                }

                .item-right {
                    font-size: 14px;
                    font-weight: bold;
                    width: 50px;
                    text-align: center;
                    background-color: #fff;

                    &.alarm-level-0 {
                        color: #FF0100;
                    }

                    &.alarm-level-1 {
                        color: #ff8100;
                    }

                    &.alarm-level-2 {
                        color: #fefe00;
                    }

                    &.alarm-level-3 {
                        color: #98cc00;
                    }

                    &.alarm-level-4 {
                        color: #058200;
                    }
                }
            }

        }

        /* 修改滚动条样式 */
        ::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #20edde;
            border-radius: 2px;
        }

        ::-webkit-scrollbar-track {
            /* background-color: #081D32; */
            /* border-radius: 2px; */
        }
    }

    /* 按钮 */
    .btn-panel {
        position: absolute;
        right: 100%;
        top: 50%;
        background: rgba(4, 19, 30, 0.5);
        width: 16px;
        height: 32px;
        line-height: 32px;
        text-align: center;
        border-radius: 18px 0 0 18px ;
        cursor: pointer;
        transition: transform 0.5s ease-in-out;

        &.activeHide {
            transform: translateX(360px);
        }
    }

    .charts-content {
            .charts {
                width: 360px;
                height: 250px;
            }
        }
}
</style>