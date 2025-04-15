var express = require('express');
var app = express();

app.use(function (req, res, next) {
    console.log('这是最简单的中间件');
    //获取到请求到达服务器的时间
    const time = Date.now()
    //为req对象，挂载自定义属性，从而把时间共享给后面的所有路由
    req.startTime = time
    next()
})
app.use(function (req, res, next) {
    console.log('这是最简单的中间件2');

    next()
})
app.get('/', (req, res, next) => {
    res.send('homepage' + req.startTime)
})
app.get('/user', (req, res, next) => {
    res.send('userpage' + req.startTime)
})
app.listen(8881, function () {
    console.log('server start!');
});

