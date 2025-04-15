import fetch from '../common/js/fetch';

// 请求台风数据
export function getTyphoonData(){
    let url = 'datacache/typhoon.json';
    return fetch({
        method: 'GET',
        url,
    }).then(res=>{
        return res;
    })
}

// 请求 雷达回波数据
export function getRadarListData(){
    let url = 'datacache/radarlist.json';
    return fetch({
        method: 'GET',
        url,
    }).then(res=>{
        return res;
    })
}

// 请求相对湿度 数据
export function getHumidityData(){
    let url = 'datacache/humidity.json';
    return fetch({
        method: 'GET',
        url,
    }).then(res=>{
        return res;
    })
}