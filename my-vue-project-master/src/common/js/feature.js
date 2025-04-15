let featureObj = {
    // feature 类型判定
    typeJudge: function (feature) {
        if (feature.get('typhoonPoint')) {
            return 'typhoonPoint';
        } else if(feature.get('typhoonSolar')) {
            return 'typhoonSolar';
        } else {
            return 'isFeatureButDontNeedTodo';
        }
    },

    /**
     * 台风点 相关 
     */
    typhoonPointClick: function (feature) {
        console.log('click typhoonPoint');
        console.log(feature);
    },
    typhoonPointHover: function (feature) {
        let points = feature.get('points');
        this.setTFINFOPostion(points);
        this.typhoonData = points;
        console.log('typhoonPointHover');
        this.map.getTargetElement().style.cursor = "pointer";
        this.clearPointZoomStyle();
        feature.getStyle().getImage().setRadius(8);
        feature.changed();
        this.lastZoomPoint = feature;
    },

    /**
     * 风圈 相关
     * 
     */
    typhoonSolarClick: function (feature) {
        console.log('typhoonSolarClick',feature);
    },
    typhoonSolarHover: function (feature) {
        console.log('typhoonSolarHover', feature);
    },


    /**
     * 
     * @啥也不做
     */
    isFeatureButDontNeedTodoClick: function () {
        return;
    },
    isFeatureButDontNeedTodoHover: function () {
        console.log('is feature Hover');
        return;
    },

};
export default featureObj;