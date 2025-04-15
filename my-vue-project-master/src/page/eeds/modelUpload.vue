<template>
  <div class="container">
    <div class="panel" :class="{ 'activeHide': isHideList }">
      <div class="title">
        <img :src="require('./images/title.png')" /> &nbsp;&nbsp;
        <span>模型上传</span>
      </div>
      <br />
      <!-- elementui写一个上传excel表单，填写模型编号 -->
      <el-form label-width="80px" size="small">
        <!-- <el-form-item label="模型编号">
          <el-input v-model="modelCode" placeholder="请输入模型编号" size="small" clearable></el-input>
        </el-form-item> -->
        <el-form-item label="上传文件">
          <!-- <el-upload
                      class="upload-demo"
                      action="https://jsonplaceholder.typicode.com/posts/"
                      :on-success="handleSuccess"
                      :file-list="fileList"
                      :multiple="false"
                      :limit="1"
                      :show-file-list="false"
                      :before-upload="beforeUpload"
                      :headers="headers"
                  >
                      <i class="el-icon-upload"></i>
                      <div class="el-upload__tip" slot="tip">将文件拖到此处，或点击上传</div>
                  </el-upload> -->
          <input type="file" id="file" accept=".xlsx,.xls,.csv" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">上传</el-button>
        </el-form-item>
      </el-form>

      <div class="title">
        <img :src="require('./images/title.png')" /> &nbsp;&nbsp;
        <span>模型查看</span>
      </div>
      <br />
      <!-- 写一个表单，有模型编码下拉，模型深度下拉，查看按钮 -->
      <el-form ref="form" :model="ruleForm" :rules="rules" label-width="80px" size="small">
        <el-form-item label="模型编号" prop="selectModelNum">
          <el-select v-model="ruleForm.selectModelNum" placeholder="请选择模型编号">
            <el-option v-for="(item, index) in model_num_list" :key="index" :label="item.model_num"
              :value="item.model_num"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="模型深度" prop="selectModelDepth">
          <el-select v-model="ruleForm.selectModelDepth" placeholder="请选择模型深度">
            <el-option v-for="(item, index) in depth_list" :key="index" :label="item" :value="item"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="属性字段" prop="selectModelAttr">
          <el-select v-model="ruleForm.selectModelAttr" placeholder="请选择模型属性">
            <el-option v-for="(item, index) in attr_list" :key="index" :label="item.name" :value="item.val"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitView">插值渲染</el-button>
        </el-form-item>
      </el-form>
    </div>

  </div>
</template>

<script>
let $ = window.$;
const { mars3d, turf } = window

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
      fileList: [],
      model_num_list: [],
      depth_list: [0, 5, 10, 15, 20, 30, 40, 'ALL'],
      attr_list: [{ name: '速度', val: 'vel' }, { name: '平均速度', val: 'avel' }, { name: '扰动百分比', val: 'pertub' }],
      ruleForm: {
        selectModelNum: '',
        selectModelDepth: '',
        selectModelAttr: '',
      },
      rules: {
        selectModelNum: [
          { required: true, message: '请选择模型编号', trigger: 'change' },
        ],
        selectModelDepth: [
          { required: true, message: '请选择模型深度', trigger: 'change' }
        ],
        selectModelAttr: [
          { required: true, message: '请选择模型属性', trigger: 'change' }
        ],
      },
      descData: {},

      searchText: '',
      xy_coor: '',
      res: [],
      res_temp: [],
      isHideList: false,
      selectItemRanking: '',
      tips: '',
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
    this.getModelNumList();
  },
  methods: {
    beforeUpload() {
      const isExcel = this.fileList[0].name.endsWith('.xlsx') || this.fileList[0].name.endsWith('.xls') || this.fileList[0].name.endsWith('.csv')
      if (!isExcel) {
        this.$message.error('请上传Excel格式文件')
        return false
      }
      return true
    },
    handleSuccess(res, file) {
      // 上传成功后，将文件名和文件内容保存到vuex中
      this.$store.commit('setUploadFile', { fileName: file.name, fileContent: res })
      this.$message.success('上传成功')
    },
    submitForm() {
      var fileInput = $('#file')[0];
      var file = fileInput.files[0];
      if (!file) {
        this.$message.warning("请先选择一个文件.");
        return;
      }
      // 判断是表格文件
      if (!/\.(xls|xlsx|csv)$/.test(file.name)) {
        this.$message.warning("请选择正确的表格文件！");
        return;
      }
      // if (this.modelCode.trim() == '') {
      //   this.$message.warning("请输入模型编号！");
      //   return;
      // }

      $.ajax({
        url: 'api/crud/query',
        type: 'POST',
        headers: {
          'Authorization': localStorage.getItem('token')
        },
        data: JSON.stringify({
          "sql": 'select count(distinct model_num) as count from vs_model where 1=1'
        }),
        contentType: 'application/json',
        success: function (res) {
          console.log(res);
          if (res.success) {
            if (res.data.body[0].count == 0) {
              var formData = new FormData();
              formData.append('file', file);
              formData.append('sql', 'insert into vs_model (lat,long,depth,vel,avel,pertub,model_num) values (? , ? , ? , ? , ? , ? , ?)');
              $.ajax({
                url: 'api/crud/upload2db',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false, // 告诉 jQuery 不要去设置 Content-Type 请求头 'application/x-www-form-urlencoded;charset=UTF-8',
                // dataType: 'json',
                success: function (res) {
                  console.log(res);
                  if (res === 'success') {
                    this.$message.info('添加成功', {
                      icon: 1,
                      time: 1000
                    }, function () {
                      // table.reload('userTable');
                    });
                  } else {
                    this.$message.info('添加成功', {
                      icon: 2,
                      time: 1000
                    });
                  }
                },
                error: function (err) {
                  console.log(err);
                  this.$message.info('请求失败，请稍后重试', {
                    icon: 2,
                    time: 1000
                  });
                }
              });
            } else {
              this.$message.info('项目别名已存在，不可用！')
            }

          } else {
            this.$message.info('query error')
          }
        },
        error: function (err) {
          console.log(err);
          this.$message.info('请求失败，请稍后重试', {
            icon: 2,
            time: 1000
          });
        }
      });

      this.$refs.form.validate((valid) => {
        if (valid) {
          this.$message.success('上传成功')
          this.isHideList = true
        } else {
          this.$message.error('请检查输入项')
        }
      })
    },
    getModelNumList() {
      this.axios.post('/crud/query', {
        sql: 'select distinct model_num from vs_model'
      }).then(res => {
        if (res.data.success) {
          this.model_num_list = res.data.data.body
        } else {
          this.model_num_list = []
        }
      })
    },
    submitView() {
      console.log(this.ruleForm)
      if (this.ruleForm.selectModelDepth === 'ALL') {
        this.$message.warning('请选择具体的模型深度')
        return;
      }
      this.$refs['form'].validate(async (valid) => {
        if (valid) {
          let res = await this.axios.post('/crud/query', {
            sql: "select min(vel) as min_vel, max(vel) as max_vel, min(avel) as min_avel, max(avel) as max_avel, min(pertub) as min_pertub, max(pertub) as max_pertub from vs_model where model_num = '" + this.ruleForm.selectModelNum + "' and depth = '" + this.ruleForm.selectModelDepth + "';"
          })
          this.descData = res.data.data.body[0]
          // let sql = this.ruleForm.selectModelDepth === 'ALL' ? `select * from vs_model where model_num='${this.ruleForm.selectModelNum}'`:`select * from vs_model where model_num='${this.ruleForm.selectModelNum}' and depth='${this.ruleForm.selectModelDepth}'`
          this.axios.post('/crud/query', {
            sql: `select * from vs_model where model_num='${this.ruleForm.selectModelNum}' and depth='${this.ruleForm.selectModelDepth}'`
          }).then(res => {
            if (res.data.success) {
              this.res = res.data.data.body
              console.log(this.res)
              this.rendererCz(this.res, this.ruleForm.selectModelAttr);
            } else {
              this.$message.error('查询失败')
            }
          })
        } else {
          return false;
        }
      });
      // console.log(this.selectModelNum, this.selectModelDepth, this.selectModelAttr)
    },
    rendererCz(arr, field) {
      var colors = ['#006837', "#006837", '#00904d', "#1a9850", '#5ab054', "#66bd63", "#a6d96a",  "#a6bd6a", "#d9ef8b", 
      "#ffffbf", '#fef5a3', "#fee08b", '#fdc08e', "#fdae61",'#fb7966', "#f46d43", "#d73027", "#a50026", "#f40000"]
      // colors = [
      // '#006837','#007c42','#00904d','#1a9850','#2a9d58','#3aa360','#00a458','#4aa968','#5ab070','#6ab678',
      // '#7abd80','#8ac388','#9ac990','#aad098','#bad6a0','#cadba8','#dadcb0','#eae1b8','#f9f7c0','#ffffbf',
      // '#fef5a3','#fef287','#fef06b','#fefa4f','#fef733','#fee08b','#fedc95','#fdbd70','#fec99f','#fdd6bc',
      // '#fdc9ac','#feb5ad','#fdc08e','#fdbd9d','#fdb37f','#fdae61','#fd7d70','#fc7b6b','#fb7966','#fa7761',
      // '#f9755c','#f87357','#f77152','#f66f4d','#f56e48','#f46d43',"#d73027", "#a50026"]
      var breaks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
      25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 99] // 等值面的级数
      breaks = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 99]
      var pointGrid = []

      function getColor(value) {
        for (var i = 0; i < breaks.length; i++) {
          if (breaks[i] === value) {
            return colors[i]
          }
        }
        return colors[0]
      }

      for (var i = 0, len = arr.length; i < len; i++) {
        var item = arr[i]
        pointGrid.push({
          type: "Feature",
          properties: {
            ...item,
            '_vel': (item.vel - this.descData.min_vel) / (this.descData.max_vel - this.descData.min_vel) * 10,
            '_avel': (item.avel - this.descData.min_avel) / (this.descData.max_avel - this.descData.min_avel) * 10,
            '_pertub': (item.pertub - this.descData.min_pertub) / (this.descData.max_pertub - this.descData.min_pertub) * 10,
          },
          geometry: {
            type: "Point",
            coordinates: [item.long, item.lat]
          }
        })
      }

      var points = {
        type: "FeatureCollection",
        features: pointGrid
      }

      console.log(this.descData, points)

      var geojsonPoly = turf.isobands(points, breaks, {
        zProperty: '_'+field
      })
      console.log(JSON.stringify(geojsonPoly))
      var geoJsonLayer = new mars3d.layer.GeoJsonLayer({
        name: "等值面",
        data: geojsonPoly,
        popup: "{" + field + "}",
        symbol: {
          type: "polygonC",
          styleOptions: {
            fill: true, // 是否填充
            color: "#ffff00", // 颜色
            opacity: 1 // 透明度
          },
          callback: function (attr, styleOpt) {
            console.log(attr, styleOpt)
            // 得到点的权重，计算落在那个色度带
            var val = Number(attr['_'+field].split("-")[0] || 0)
            console.log(attr['_'+field].split("-")[0], val)
            var color = getColor(val)
            return {
              color: color
              // height: 0,
              // diffHeight: val * 10000
            }
          }
        }
      })
      this.map.addLayer(geoJsonLayer)

      // 等值线
      var geojsonLine = turf.isolines(points, breaks, {
        zProperty: '_'+field
      })


      // 进行平滑处理
      // var features = geojsonLine.features;
      // for (var i = 0; i < features.length; i++) {
      //     var _coords = features[i].geometry.coordinates;
      //     var _lCoords = [];
      //     for (var j = 0; j < _coords.length; j++) {
      //         var _coord = _coords[j];
      //         var line = turf.lineString(_coord);
      //         var curved = turf.bezierSpline(line);
      //         _lCoords.push(curved.geometry.coordinates);
      //     }
      //     features[i].geometry.coordinates = _lCoords;
      // }

      var layerDZX = new mars3d.layer.GeoJsonLayer({
        name: "等值线",
        data: geojsonLine,
        popup: "{" + field + "}",
        symbol: {
          styleOptions: {
            width: 2, // 边框宽度
            color: "#000000", // 边框颜色
            opacity: 0.5, // 边框透明度
            clampToGround: false // 是否贴地
          }
        }
      })
      this.map.addLayer(layerDZX)
    }
  }
}
</script>

<style scoped>
.container {
  z-index: 999;
  position: fixed;
  top: 316.5px;
  left: 0px;
  width: 360px;
  height: calc(500px);
  /*  - 135px */

  .panel {
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

    .item-title {
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
    border-radius: 18px 0 0 18px;
    cursor: pointer;
    transition: transform 0.5s ease-in-out;

    &.activeHide {
      transform: translateX(360px);
    }
  }

}
</style>