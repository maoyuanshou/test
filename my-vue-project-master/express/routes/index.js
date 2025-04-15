const express = require('express');
const router = express.Router();
const userHandler = require('../router_handler/user')
const User = require('../API/user')
/* GET home page. */
router.get('/index', function (req, res, next) {
  res.send('??');
  console.log('1');
});

//获取用户信息的路由
router.get('/user', User.get)
router.post('/reguser', userHandler.reguser);
router.post('/login', userHandler.login);


module.exports = router;
