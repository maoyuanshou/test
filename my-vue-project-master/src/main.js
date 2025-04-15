/*
 * @Author: error: git config user.name && git config user.email & please set dead value or install git
 * @Date: 2021-09-14 19:55:12
 * @LastEditors: error: git config user.name && git config user.email & please set dead value or install git
 * @LastEditTime: 2022-11-03 16:14:27
 * @FilePath: \shipin2\src\main.js
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
 */
import Vue from 'vue'
import App from './App.vue'
import router from './router/index.js'
import axios from 'axios'
import 'lib-flexible' 
// import VueAxios from 'vue-axios'
import 'element-ui/lib/theme-chalk/index.css';
import lang from 'element-ui/lib/locale/lang/en';
import locale from 'element-ui/lib/locale';
// import ElementUI from './plugins/elementui';
import ElementUI from 'element-ui';
import Echarts from 'vue-echarts';
import store from './store';
import './directives/index.js'; // 引入自定义指令
// // 引入ol样式，类文件按需引入
// import 'ol/ol.css'
// import 'ol-ext/dist/ol-ext.css'

locale.use(lang);
Vue.config.productionTip = false
Vue.use(Echarts);
Vue.use(ElementUI);
const axiosInstance = axios.create({
  baseURL: '/api',
  timeout: 1000000
})
axiosInstance.interceptors.request.use(config => {
  // Do something before request is sent
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `${token}`;
  }
  // console.log('请求拦截器', config)
  return config
}, error => {
  // Do something with request error
  return Promise.reject(error)
})
axiosInstance.interceptors.response.use(response => {
  // Do something with response data
  return response
}, error => {
  // Do something with response error
  // console.log('响应拦截器', error)
  const { response } = error;
  if (response && response.status === 401) {
    // 401 错误处理：清除登录状态，重定向到登录页面
    router.push({ path: '/' })
  } else if (response.status === 403) {
    // 403 错误处理：无权访问
    ElementUI.Message.error('no permission !');
  } else if (response.status === 500) {
    // 500 错误处理：服务器错误
    console.error('报错原因===', response)
    ElementUI.Message.error('server error !');
  } else {
    // 其他错误处理
    return Promise.reject(error);
  }
})

Vue.prototype.axios = axiosInstance;
// Vue.use(VueAxios, axios)

new Vue({
  store,
  router,
  // mode:history,
  render: h => h(App),
}).$mount('#app')
