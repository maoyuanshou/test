<template>
    <div class="searchStack">
        <el-input placeholder="请输入内容" v-model="addressInput" class="input-with-select">
            <el-select v-model="selectType" slot="prepend" placeholder="请选择" style="width: 150px;">
                <el-option label="地名地址查询" value="1"></el-option>
                <el-option label="订单号" value="2"></el-option>
                <el-option label="用户电话" value="3"></el-option>
            </el-select>
            <el-button slot="append" icon="el-icon-search" @click.prevent="doSearch()"></el-button>
        </el-input>
    </div>
</template>

<script>
// import * as L from "leaflet";

export default {
    name: 'searchStack',
    props: {
        map: {
            type: Object,
            default: () => { }
        }
    },
    data() {
        return {
            addressInput: '',
            selectType: '地名地址查询',
            showXyInput: false,
            xy_coor: '',
        }
    },
    mounted() {
    },
    methods: {
        doSearch() {
            console.log(this.addressInput);
            
        }
    }
}
</script>

<style scoped>
.searchStack {
    z-index: 999;
    position: absolute;
    top: 30px;
    left: 30px;
    /* background-color: rgb(255, 255, 255); */
    border-radius: 8px;
    padding: 4px;
    /* width: 42px; */
    display: flex;
    align-items: center;
    flex-direction: column;

}
</style>