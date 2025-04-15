/*
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2022-06-28 09:51:57
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2022-11-03 16:34:43
 * @FilePath: \shipin2\src\router\index.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import Vue from 'vue';
import VueRouter from 'vue-router';
Vue.use(VueRouter);

import Login from '../page/login.vue';
import Page1 from '../components/pages1.vue'
import Land from '../page/land/index.vue'
import QX from '../page/qixiang/index.vue'
import EEDS from '../page/eeds/index.vue'
import GeoSOT from '../page/beidou_grid_code/index.vue'

//配置路由重定向（默认加载页面）
export default new VueRouter({
    routes: [
        //加载页面，采用路由懒加载（不用将所有页面全部加载进来，而是进入哪个页面加载哪个，提高性能）
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login',
            component: Login
        },
        {
            path: '/page1',
            component: Page1
        },
        {
            path: '/land',
            component: Land
        },
        {
            path: '/qixiang',
            component: QX
        },
        {
            path: '/eeds',
            component: EEDS
        },
        {
            path: '/qixiang',
            component: QX
        },
        {
            path: '/beidou_grid_code',
            component: GeoSOT
        },
    ]
})