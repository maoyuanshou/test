<template>
    <div class="container">
        <div class="bg-container"></div>
        <div class="login-container">
            <div class="login">
                <el-form label-position="right" label-width="80px" :model="formLogin">
                    <el-form-item label="用户名">
                        <el-input v-model="formLogin.username"></el-input>
                    </el-form-item>
                    <el-form-item label="密码">
                        <el-input v-model="formLogin.password" type="password"></el-input>
                    </el-form-item>
                    <el-form-item label="">
                        <el-button type="primary" @click="loginFunc1">登录</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </div>
    </div>
</template>
<script>
// import axios from "axios"

import { customEncrypt, secretKey } from "@/common/js/common";

export default {
    data() {
        return {
            formLogin: {
                username: '',
                password: '',
            }
        };
    },
    methods: {
        async loginFunc1() {
            let data = await this.axios({
                baseURL:'',   //  基础url地址，一般写 http协议 域名 端口
                url:'/api/user/login',   //  请求地址 ， 可以全写，也可以配合 baseURL 只写某个子页面的地址
                method:'post', // 请求方式  get是明文传参  post是密文传参
                timeout: 5000, // 请求超时  如果超时将停止请求
                data: {  // post 请求时 要传递的数据
                    username: this.formLogin.username,
                    password: customEncrypt(this.formLogin.password, secretKey)
                },
                // params:{ // get 请求时，要传递的数据
                //     id:'1'
                // }
            })
            console.log(data);

            if (data.data.success && data.data.data.user) {
                const token = data.data.data.token;
                localStorage.setItem('token', token);
                this.$router.push({ path: '/eeds' })
                this.$message({
                    // message: '恭喜你，登录成功！',
                    message: 'login success！',
                    type: 'success'
                });

            } else {
                this.$message.error('用户名密码错误！');
            }
        },
        loginFunc() {
            if (this.formLogin.username === 'admin' && this.formLogin.password === '123456') {
                this.$router.push({ path: '/eeds' })
                // this.$router.push({ path: '/beidou_grid_code' })
                this.$message({
                    message: '恭喜你，登录成功！',
                    type: 'success'
                });

            } else {
                this.$message.error('用户名密码错误！');
            }
        }
    }
}
</script>
<style scoped>
.container {
    width: 100vw;
    height: 100vh;

    .bg-container {
        width: 60%;
        height: 100%;
        background-image: url('./img/login-bg.svg');
        background-repeat: no-repeat;
        background-size: cover;
        float: left;
        background-position: center center;
    }

    .login-container {
        width: 40%;
        height: 100%;
        float: right;
        position: relative;

        .login {
            position: absolute;
            width: 300px;
            height: 200px;
            box-shadow: 0 0 30px 0px #496bba80;
            margin: auto;
            top: 0;
            bottom: 0;
            right: 0;
            left: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            padding-top: 30px;
            padding-right: 30px;
        }
    }

}

/deep/ .el-form-item__label {
    color: #606266 !important;
}
</style>