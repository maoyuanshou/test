<template>
    <div class="left-container">
        <div class="siteInfo">
            <div class="title">
                <img :src="require('./images/title.png')" /> &nbsp;&nbsp;
                <span>天气概况</span>
            </div>
            <div class="list-content">
                <div class="item">
                    <div class="item-middle"> 地面气压</div>
                    <div class="item-right"> {{ tqsk?.prs || '' }} hPa</div>
                </div>
                <div class="item">
                    <div class="item-middle"> 相对湿度 </div>
                    <div class="item-right"> {{ tqsk.rh || '' }} % </div>
                </div>
                <div class="item">
                    <div class="item-middle"> 温度 </div>
                    <div class="item-right"> {{ tqsk.tem || '' }} ℃</div>
                </div>
                <div class="item">
                    <div class="item-middle"> 体感温度 </div>
                    <div class="item-right"> {{ tqsk.real_tem || '' }} ℃</div>
                </div>
                <div class="item">
                    <div class="item-middle"> 风向描述 </div>
                    <div class="item-right"> {{ tqsk.wd_desc || '' }} m</div>
                </div>
                <div class="item">
                    <div class="item-middle"> 天气现象 </div>
                    <div class="item-right"> {{ tqsk.wp || '' }} </div>
                </div>
                <div class="item">
                    <div class="item-middle"> 风速 </div>
                    <div class="item-right"> {{ tqsk.ws || '' }} m/s</div>
                </div>
                <div class="item">
                    <div class="item-middle"> 风力 </div>
                    <div class="item-right"> {{ tqsk.ws_desc || '' }} </div>
                </div>
            </div>
            <div class="title">
                <img :src="require('./images/title.png')" /> &nbsp;&nbsp;
                <span>城市空气质量</span>
            </div>
            <div class="list-content">
                <div class="item">
                    <div class="item-middle"> 空气质量指数（AQI）</div>
                    <div class="item-right"> {{ kqzl?.aqi || '' }} hPa</div>
                </div>
                <div class="item">
                    <div class="item-middle"> 一氧化碳浓度</div>
                    <div class="item-right"> {{ kqzl.co || '' }} ug/m³ </div>
                </div>
                <div class="item">
                    <div class="item-middle"> 臭氧浓度 </div>
                    <div class="item-right"> {{ kqzl.o3 || '' }} ug/m³</div>
                </div>
                <div class="item">
                    <div class="item-middle"> 二氧化氮浓度 </div>
                    <div class="item-right"> {{ kqzl.no2 || '' }} ug/m³</div>
                </div>
                <div class="item">
                    <div class="item-middle"> 二氧化硫浓度 </div>
                    <div class="item-right"> {{ kqzl.so2 || '' }} ug/m³</div>
                </div>
                <div class="item">
                    <div class="item-middle"> pm10颗粒浓度 </div>
                    <div class="item-right"> {{ kqzl.pm10 || '' }} ug/m³</div>
                </div>
                <div class="item">
                    <div class="item-middle"> pm25颗粒浓度 </div>
                    <div class="item-right"> {{ kqzl.pm25 || '' }} ug/m³</div>
                </div>
            </div>
        </div>

        <div class="alarmLevel">
            <!-- <div class="title">
                <img :src="require('./images/title.png')" /> &nbsp;&nbsp;
                <span>未来7天预报</span>
            </div>
            <div class="level-content">
                <div class="item"> &nbsp;
                    Current Alarm Level: &nbsp;<span class="alarm-level">11</span>
                </div>
                <div class="legend">
                    <div class="lg item1">NRM</div>
                    <div class="lg item2">Level 4</div>
                    <div class="lg item3">Level 3</div>
                    <div class="lg item4">Level 2</div>
                    <div class="lg item5">Level 1</div>
                </div>
            </div> -->
            <div class="title">
                <img :src="require('./images/title.png')" />
                &nbsp;&nbsp;
                <span>未来7天预报</span>
            </div>
            <div class="charts-content">
                <div class="charts" ref="charts"></div>
            </div>
        </div>

    </div>
</template>

<script>
import * as echarts from 'echarts'

export default {
    name: 'siteInfo',
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
            tqsk: {
            },
            kqzl: {},
        }
    },
    watch: {
        '$store.state.quxianCode': {
            handler() {
                this.getQuanguoTianqi()
                this.getCityKQZL()
                this.yubao()
            },
            deep: true,
            immediate: true
        }
    },
    mounted() {
        // this.getQuanguoTianqi()
        // this.initCharts()
    },
    methods: {
        getQuanguoTianqi() {
            this.axios.get('https://tiles.geovisearth.com/meteorology/v1/weather/cn/realtime/area',
                {
                    params: {
                        location: this.$store.state.quxianCode,
                        token: '0f6a2507659fef660c63f88bb875abfd6a2314ef02aa8cc00e02d768af65dad7'
                    },
                })
                .then(res => {
                    if (res.status === 200) {
                        this.tqsk = res.data.result
                    } else {
                        this.tqsk = {}
                        this.$message.error(res.data.message)
                    }
                })
        },
        getCityKQZL() {
            this.axios.get('https://tiles.geovisearth.com/meteorology/v1/weather/cn/realtime/aqi/desc',
                {
                    params: {
                        location: this.$store.state.quxianCode,
                        token: '0f6a2507659fef660c63f88bb875abfd6a2314ef02aa8cc00e02d768af65dad7'
                    },
                })
                .then(res => {
                    if (res.status === 200) {
                        this.kqzl = res.data.result
                    } else {
                        this.kqzl = {}
                        this.$message.error(res.data.message)
                    }
                })
        },
        yubao() {
            this.axios.get('https://tiles.geovisearth.com/meteorology/v1/weather/cn/forecast/day/area', {
                params: {
                    location: this.$store.state.quxianCode,
                    token: '0f6a2507659fef660c63f88bb875abfd6a2314ef02aa8cc00e02d768af65dad7'
                },
            }).then(res => {
                if (res.status === 200) {
                    this.initCharts(res.data.result.datas.slice(0, 7))
                } else {
                    this.$message.error('error')
                }
            })
        },
        initCharts(list) {
            // 饼状图, 自定义颜色
            let chart = echarts.init(this.$refs.charts)
            chart.clear()
            const option = {
                title: {
                    text: '',
                    top: '16px',
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
                    show: true,
                    data: ['最高气温', '最低气温'],
                    // orient: 'vertical', // 设置为垂直布局
                    // right: '0%', // 将 legend 放到右侧
                    top: '1%', // 垂直居中
                    textStyle: {
                        color: '#fff'
                    }
                },
                grid: {
                    left: '1%',
                    right: '1%',
                    bottom: '1%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    // type: 'value',
                    data: list.map(item => item.week),
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
                        name: '最高气温',
                        type: 'line',
                        stack: 'Total',
                        data: list.map(item => item.tem_max),
                    },
                    {
                        name: '最低气温',
                        type: 'line',
                        stack: 'Total',
                        data: list.map(item => item.tem_min),
                    }
                ]
            };
            chart.setOption(option)
        }
    }
}
</script>

<style scoped>
.left-container {
    z-index: 999;
    position: absolute;
    top: 66.5px;
    left: 0px;
    height: 100%;

    .siteInfo {
        position: absolute;
        left: 0px;
        top: 30px;
        width: 400px;
        background-color: rgba(4, 19, 30, 0.5);
        border-radius: 8px;
        padding: 4px 10px;
        border: 2px solid #2A748A;
        color: #fff;

        &.active {
            display: block;
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

        .list-content {
            padding-left: 10px;
            overflow-y: auto;

            .item {
                width: calc(100% - 10px);
                display: flex;
                /* margin: 5px 0; */
                justify-content: space-between;
                align-items: center;
                cursor: pointer;
                padding: 5px;

                &:nth-child(odd) {
                    background-color: rgba(4, 19, 30, 0.5);
                }

                &:nth-child(even) {
                    /* background-color: rgba(4, 19, 30, 0.3); */
                }

                .item-left {
                    font-size: 16px;
                    width: 24px;
                    text-align: left;
                    display: flex;
                }

                .item-middle {
                    font-size: 14px;
                    width: 160px;
                }

                .item-right {
                    font-size: 14px;
                    width: 220px;
                    text-align: right;
                    word-wrap: break-word;
                }
            }

        }
    }

    .alarmLevel {
        position: absolute;
        bottom: 75px;
        left: 0px;
        width: 400px;
        background-color: rgba(4, 19, 30, 0.5);
        border-radius: 8px;
        padding: 4px 10px;
        border: 2px solid #2A748A;
        color: #fff;

        &.active {
            display: block;
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

        .level-content {
            padding-left: 10px;
            overflow-y: auto;

            .item {
                width: calc(100% - 30px);
                padding-left: 20px;
                display: flex;
                margin: 5px 0;
                justify-content: flex-start;
                align-items: center;
                padding: 5px;
                font-size: 16px;
            }

            .legend {
                display: flex;
                justify-content: space-evenly;
                align-items: center;
                margin-top: 10px;
                font-size: 14px;
                color: #fff;


                .lg {
                    width: 60px;
                    height: 30px;
                    line-height: 30px;
                    text-align: center;
                    color: #000;
                    border-radius: 10px;
                }

                .item1 {
                    background-color: #47FF88;
                }

                .item2 {
                    background-color: #0070C0;
                }

                .item3 {
                    background-color: #FFFF00;
                }

                .item4 {
                    background-color: #FEC000;
                }

                .item5 {
                    background-color: #FF0100;
                }
            }

        }

        .charts-content {
            .charts {
                width: 400px;
                height: 250px;
            }
        }
    }
}
</style>