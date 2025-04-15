// store.js
import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    count: 0,
    items: [],
    projectName: '', // 项目名称
    refreshLeftPanel: false, // 刷新左侧面板
    quxianCode: 'WTX_CH101010300' // 区域编码
  },
  mutations: {
    increment(state) {
      state.count++;
    },
    decrement(state) {
      state.count--;
    },
    addItem(state, item) {
      state.items.push(item);
    },
    updateProjectName(state, projectName) {
      state.projectName = projectName;
    },
    refreshLeftPanel(state) {
      setTimeout(() => { // 延迟1秒刷新左侧面板
        state.refreshLeftPanel = !state.refreshLeftPanel;
      }, 1000);
    },
    setQuxianCode(state, quxianCode){
      state.quxianCode = quxianCode;
    }
  },
  actions: {
    incrementAsync({ commit }) {
      setTimeout(() => {
        commit('increment');
      }, 1000);
    },
    decrementAsync({ commit }) {
      setTimeout(() => {
        commit('decrement');
      }, 1000);
    }
  },
  getters: {
    doubleCount(state) {
      return state.count * 2;
    },
    itemsCount(state) {
      return state.items.length;
    }
  }
});