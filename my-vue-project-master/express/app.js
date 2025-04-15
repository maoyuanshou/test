const express = require('express');
const app = express();
//index路由模块
const indexRouter = require('./routes/index');
//获取用户信息路由模块
// const userinfoRouter = require('./routes/userinfo')

//跨域
const cors = require('cors')
app.use(cors())
//注册解析表单数据的中间件,该过程要在路由之前
app.use(express.urlencoded({ extended: false }))

// 在路由之前 封装res.cc函数
// app.use((req,res,next)=>{
//   //status默认值为1，表示失败的情况，err的值可能是对象Error函数实例也可能是字符串
//   res.cc = function(err,status=1){
//     res.send({
//       status,
//       message:err instanceof Error ? err.message:err,
//     })
//   }
//   next()
// })


//在路由之前配置解析Token的中间件
// const expressJWT = require(express-jwt)
// const config = require('./config')
// app.use(expressJWT({
//   secret:config.jwtSecretKey
// }).unless({
//   path:[/^\/api/]
// }))

//添加路由
// app.use('/api', userinfoRouter)
app.use('/api', indexRouter);
app.listen(3030, function () {
  console.log('server start!');
});
//导出
module.exports = app;
