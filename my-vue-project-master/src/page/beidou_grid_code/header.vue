<template>
    <div>
        <div class="header">
            <div class="header-nav">
                <span class="title">北斗网格码</span>
                <!-- <span class="title"></span> -->
                <!-- 有四个按钮，分别是 Project Information 、Device Config 、Alarm Query 、System Management , 选中哪个哪个高亮 -->
                <!-- <a v-for="(item, index) in navItems" :key="index" class="header-nav-item"
                    :class="{ 'active': index === activeIndex }" @click="clickNavItem(index)">
                    <img class="left-icon" v-show="index === activeIndex" src="./images/header/nav-left.png"
                        width="16px" height="14.5px"> {{ item }} <img class="right-icon" v-show="index === activeIndex"
                        src="./images/header/nav-right.png" width="16px" height="14.5px">
                </a> -->
            </div>
            <div class="header-middle">
                <el-cascader size="large" :options="regionData" v-model="selectedOptions" @change="addressChange">
                </el-cascader>
                <el-tree class="tree-container" :data="treeData" node-key="id"  :props="defaultProps"
                    @node-click="handleNodeClick" />

                <!-- <el-button @click="showLeida">全国降水强度雷达图</el-button> -->
            </div>
            <div class="header-right">
                <div class="timer">
                    <span>{{ currentTime }}</span>
                    <span>{{ currentDate }}</span>
                </div>
                <div class="su"></div>
                <div class="exit"><a>EXIT</a></div>
            </div>
        </div>

        <el-dialog title="图片展示" :visible.sync="visible" width="1400px" @close="handleClose">
            <el-image v-for="url in urls" :key="url" :src="url" lazy></el-image>
            <!-- <img :src="url" alt="图片加载失败" width="800px"> -->
        </el-dialog>
    </div>
</template>

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

import {
    regionData,
} from "element-china-area-data";
import quxianMap from "./quxianMap.json";

export default {
    name: 'layers',
    components: {
    },
    props: {
        map: {
            type: Object,
            default: () => { }
        }
    },
    created() {
        this.startClock();
    },
    computed: {
    },
    data() {
        return {
            visible: false,
            // treeData: [
            //     {
            //         label: '全球天气图层',
            //         children: [{
            //             label: '全球卫星云图',
            //         }, {
            //             label: '风云卫星云图',
            //         }, {
            //             label: '葵花卫星云图',
            //         }]
            //     },
            // ],
            defaultProps: {
                children: 'children',
                label: 'label'
            },
            urls: null,
            url: '',

            regionData,
            selectedOptions: ['11', '1101', '110105'],

            navItems: [
                'Project Information', 'Device Config', 'Alarm Query', 'System Management'
            ],
            activeIndex: -1,
            showPanel: false, // 没有用到
            currentTime: '',
            currentDate: '',

            deviceConfigFrom: { // 设备配置

            },
        }
    },
    mounted() {
    },
    methods: {
        addressChange(value) {
            const code = quxianMap.find(item => item['区县地区编码'] + '' === value[value.length - 1])
            if (code) {
                this.$store.commit('setQuxianCode', code['城市编码'])
            } else {
                this.$message.error('该地区没有对应的城市编码' + value)
            }
        },
        startClock() {
            setInterval(() => {
                this.currentTime = new Date().toLocaleTimeString()
                this.currentDate = new Date().toLocaleDateString()
            }, 1000)
        },
        clickNavItem(index) {
            this.activeIndex = index;
            if (index === 0) {
                this.$refs.projectInfoDialog.showDialog();
            } else if (index === 1) {
                this.$refs.deviceConfigDialog.showDialog();
            } else if (index === 2) {
                this.$refs.alertQueryDialog.showDialog();
            } else if (index === 3) {
                this.$refs.systemManagementDialog.showDialog();
            }
        },
        handleNodeClick(data) {
            this.selectedNode = data;
            let f = ''
            if (data.label === '全球天气图层') {
                console.log('全球天气图层');
            } else if (data.label === '全球卫星云图') {
                f = 'gmgsi'
            }
            else if (data.label === '风云卫星云图') {
                f = 'fy'
            } else if (data.label === '葵花卫星云图') {
                f = 'himawari9'
            }

            this.axios.get(`https://tiles.geovisearth.com/meteorology/v1/view/satellite/sev/${f}/vis/range?start=${'2025010100'}&end=${formatDate()}`,
                {
                    params: {
                        // location: this.$store.state.quxianCode,
                        token: '0f6a2507659fef660c63f88bb875abfd6a2314ef02aa8cc00e02d768af65dad7'
                    },
                })
                .then(res => {
                    if (res.status === 200) {
                        let urls = res.data.result.urls
                        this.urls = Object.values(urls).map(item => item[0])
                        if (this.urls.length > 0) {
                            this.url = urls[Object.keys(urls)[0]][0]
                            this.showList()
                        } else {
                            this.$message.warning('暂无数据')
                        }
                        // this.addStaticImage()
                    } else {
                        this.url = ''
                        // this.removeStaticImage()
                        this.$message.error(res.data.message)
                    }
                })
        },
        showList() {
            this.visible = true;
        },
        handleClose() {
            this.visible = false;
        },
        showLeida() {
            this.axios.get(`https://tiles.geovisearth.com/meteorology/v1/view/nowcast/mfv/precipint/curr`,
                {
                    params: {
                        token: '0f6a2507659fef660c63f88bb875abfd6a2314ef02aa8cc00e02d768af65dad7'
                    },
                })
                .then(res => {
                    if (res.status === 200) {
                        let urls = res.data.result.urls
                        let urlsArr = Object.keys(urls)
                        if (urlsArr.length > 0) {
                            let url = urls[urlsArr[0]][0]
                            console.log(url)
                            this.$emit('showLeida', url)
                        } else {
                            this.$message.warning('暂无数据')
                        }
                        // this.addStaticImage()
                    } else {
                        this.url = ''
                        // this.removeStaticImage()
                        this.$message.error(res.data.message)
                    }
                })
        }
    }
}
</script>

<style scoped>
.header {
    z-index: 1000;
    position: fixed;
    top: 0px;
    width: 100%;
    height: 80px;
    background: url('./images/header/line.png') no-repeat, linear-gradient(180deg, #0a1920, #224a5380);
    ;
    /* background-image: url('./images/header/header.png'); */
    background-repeat: no-repeat;
    background-size: 100% 100%;

    .header-nav {
        width: 810px;
        height: 183px;
        line-height: 77px;
        /* margin-left: 40%; */
        background-image: url('./images/header/head-bg.png');
        background-repeat: no-repeat;
        background-size: 100% 100%;

        .title {
            font-size: 36px;
            font-weight: bold;
            font-style: italic;
            color: #fff;
            margin-left: 40px;
            line-height: 80px;
        }
    }

    .header-nav-item {
        color: #fff;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        position: relative;

        .left-icon {
            position: absolute;
            top: calc(50% - 7.25px);
            left: -30px;
        }

        .right-icon {
            position: absolute;
            top: calc(50% - 7.25px);
            right: -30px;
        }
    }

    .header-nav-item:hover {
        color: #27FFFF;
    }

    .active {
        color: #27FFFF;
    }

    .header-middle {
        position: absolute;
        top: 20px;
        left: 830px;
        display: flex;
        width: 500px;
        justify-content: space-around;
    }

    .header-right {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        height: 77px;
        padding: 0 20px;
        position: absolute;
        right: 0;
        top: 0;
    }

    .tree-container{
        width: 200px;
    }

    .timer {
        display: flex;
        align-items: flex-end;
        font-size: 20px;
        color: #fff;
        margin-right: 20px;
        display: flex;
        flex-direction: column;

        span:first-child {
            font-size: 20px;
            /* font-weight: bold; */
            font-style: italic;
        }

        span:last-child {
            font-size: 11px;
        }
    }

    .su {
        width: 5px;
        height: 36px;
        background-image: url('./images/header/su.png');
        background-repeat: no-repeat;
        background-size: 100% 100%;
        margin-right: 20px;
    }

    .exit {
        display: flex;
        align-items: center;
        font-size: 20px;
        color: #fff;
        cursor: pointer;
        margin-right: 20px;
    }

    .exit a {
        text-decoration: none;
        color: #fff;
    }
}
</style>