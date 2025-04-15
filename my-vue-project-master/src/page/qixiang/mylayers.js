let ol = window.ol
export function createLyrTian() {
    const key = 'afb4309d6e49809778feb49ec25d96d9'
    return new ol.layer.Tile({
      properties: {
        name: 'tian',
        title: '天地图-平面',
      },
      visible: true,
      source: new ol.source.XYZ({
        projection: 'EPSG:3857',
        url: `http://t{0-7}.tianditu.gov.cn/vec_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=${key}`,
      })
    })
  }

export function createLyrTian_img() {
    const key = 'afb4309d6e49809778feb49ec25d96d9'
    return new ol.layer.Tile({
      properties: {
        name: 'tian',
        title: '天地图-平面',
      },
      visible: false,
      source: new ol.source.XYZ({
        projection: 'EPSG:3857',
        url: `http://t{0-7}.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=vec&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=${key}`,
      })
    })
  }

export function createLyrTian_cva() {
    const key = 'afb4309d6e49809778feb49ec25d96d9'
    return new ol.layer.Tile({
      properties: {
        name: 'tian',
        title: '天地图-注记',
      },
      visible: true,
      source: new ol.source.XYZ({
        projection: 'EPSG:3857',
        url: `http://t{0-7}.tianditu.gov.cn/cva_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cva&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=${key}`,
      })
    })
  }
