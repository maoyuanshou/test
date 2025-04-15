<template>
  <el-card class="box-card">
    <el-row :gutter="2">
      <el-col :span="12">
        <div>
          <el-statistic title="预警发布机构">
            <template slot="prefix">
              {{ alart?.sender || '-' }}
            </template>
          </el-statistic>
        </div>
      </el-col>
      <el-col :span="12">
        <div>
          <el-statistic group-separator="," :precision="2" :title="'生效时间'">
            <template slot="prefix">
              {{ alart?.effective || '-' }}
            </template>
          </el-statistic>
        </div>
      </el-col>
    </el-row>
    <br />
    <el-row :gutter="2">
      <el-col :span="12">
        <div>
          <el-statistic group-separator="," :precision="2" decimal-separator="." :title="'预警级别'">
            <template slot="formatter">
              <i class="el-icon-s-flag" style="color: red"></i>
              {{ alart?.level || '-' }}
            </template>
            <!-- <template slot="suffix">
              <i class="el-icon-s-flag" style="color: blue"></i>
            </template> -->
          </el-statistic>
        </div>
      </el-col>
      <el-col :span="12">
        <div>
          <el-statistic title="详情">
            <template slot="suffix">
              <i class="el-icon-star-on" style="color:red"></i>
              {{ alart?.detail || '-' }}
            </template>
          </el-statistic>
        </div>
      </el-col>
    </el-row>
    <!-- <el-row>
      <el-col :span="24">
        <el-button type="primary" size="small" @click="addLayers">播放近期全国空气质量图层</el-button>
        <el-button type="primary" size="small" @click="clearLayers">暂停清除</el-button>
        &nbsp;
        <el-tag>{{ currentTime || '-' }}</el-tag>
        
      </el-col>
    </el-row> -->

    
  </el-card>
</template>

<script>
// let map = window.map;
export default {
  props: {
    map: {
      type: Object,
      default: () => { }
    }
  },
  data() {
    return {
      
      
      // 新增设备集
      selectedNode: null,
      
      playUrls: {},
      playTimer: null,
      currentTime: null,
      alart: {
        // "geoCode": "430382",
        // "sender": "韶山市气象局",
        // "typeCode": "11B09",
        // "type": "高温",
        // "levelCode": "Yellow",
        // "level": "黄色预警",
        // "effective": "2024-08-31 09:02:00",
        // "expires": "2024-08-31 18:00:00",
        // "title": "韶山市气象局发布高温黄色预警[Ⅲ级/较重]",
        // "detail": "韶山市气象台2024年8月31日9时2分发布高温黄色预警信号：今天白天韶山市最高气温将升至35℃以上，请注意防范。"
      }
    };
  },
  watch: {
    '$store.state.quxianCode': {
      handler() {
        this.initStatisticData()
      },
      deep: true,
      immediate: true
    }
  },
  unmounted() {
    this.playTimer && window.clearInterval(this.playTimer);
  },
  mounted() {
    // this.$nextTick(() => {
    //   console.log(this.treeData);
    // });
  },
  methods: {
  // 新增设备集
  initStatisticData() {
    this.axios.get('https://tiles.geovisearth.com/meteorology/v1/weather/alert/now/data',
      {
        params: {
          location: this.$store.state.quxianCode,
          token: '0f6a2507659fef660c63f88bb875abfd6a2314ef02aa8cc00e02d768af65dad7'
        },
      })
      .then(res => {
        if (res.status === 200) {
          if (res.data.result.alerts.length > 0) {
            this.alart = res.data.result.alerts[0]
          } else {
            this.alart = {}
            this.$message.warning('暂无预警信息')
          }
        } else {
          this.alart = {}
          this.$message.error('server error')
        }
      })
  },
  submitDeviceAdd(formName) {
    this.$refs[formName].validate((valid) => {
      if (valid) {
        // 上传文件
        this.$refs.upload.submit();
        let url = '/api/deviceconfiginfo/add';
        if (this.deviceAddForm.id && this.deviceAddForm.id !== '') {
          url = '/api/deviceconfiginfo/edit';
        }
        this.axios.post(url, {
          ...this.deviceAddForm,
          device_Longitude: this.deviceAddForm.device_Longitude.toString(),
          device_Latitude: this.deviceAddForm.device_Latitude.toString(),
          device_Height: this.deviceAddForm.device_Height.toString(),
          device_MonitorRange: this.deviceAddForm.device_MonitorRange.toString(),
          device_MonitorResolution: this.deviceAddForm.device_MonitorResolution.toString()
        }).then(res => {
          if (res.data.code === 200) {
            this.$message.success('success!');
            this.refreshTree();
            this.$store.commit('refreshLeftPanel')
          } else {
            this.$message.error(res.data.message);
          }
        })
        // this.visible = false;
      } else {
        return false;
      }
    });
  },
}
};
</script>

<style scoped>
.box-card {
  background-color: rgba(4, 19, 30, 0.5);
  position: fixed;
  top: 87px;
  right: 0;
  z-index: 1000;
  width: 360px;
  height: 222px;
  border: 2px solid #2A748A;
  border-radius: 12px;
}

/deep/ .el-statistic {
  color: #fff;
}

/deep/  .el-statistic .head {
  color: #e2e5ed;
}

/deep/  .el-statistic .con {
  color: #fff;
}

/deep/ .el-card {
  border: 2px solid #2A748A;
}

.el-row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -12px;
}

.el-col {
  padding: 0 12px;
  box-sizing: border-box;
}

</style>
