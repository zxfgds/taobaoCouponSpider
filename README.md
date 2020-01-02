##版本需求
python 2.7,php7.1,mysql5.7

##简要说明
* spider目录下为采集程序
* admin-php.7z 为简单的后台管理;laravel框架搭建;[laravel说明文档](https://docs.golaravel.com/docs/5.6/installation/ "laravel说明文档")

##安装步骤
* 安装 mongodb
  * ubuntu debian 请运行  : apt install mongodb
  * centos redhat 运行: yum install mongodb
* 安装依赖
  * 程序目录下运行: pip install -r requirements.txt
   以及 pip install  pymongo  pymysql

## 修改数据库链接
    编辑config.py 修改数据库信息

## 后台配置
*  配置淘宝分类ID 及关键词
    * 你的域名/admin/tbcates
     * 淘宝分类id 必须跟淘宝官方分类ID匹配
     * 关键词尽量不重叠,且分布均匀能将该分类下所有商品匹配到
    * 配置appkey
     * 阿里妈妈后台申请媒体ID ,申请后下方有个权限申请,可申请到;
     * appkey 尽量多个,如果数量比较少,请增加下面的sleeptime
    * 配置启动时间和sleeptime
     * 启动时间为每天几点开始采集,根据情况设置
     * sleeptime 为每个关键词采集间隔  建议 0.5  到 1 秒;

## 开始采集
    开始采集工作
*  采集程序目录下运行 : python start.py
*  到达你指定的采集时间后,自然会开始采集

## 关于mongodb的索引
    mongodb 用于商品去重;单核cpu机器可能效率很低;请自行注意
    另外,一定要指定索引 num_iid,否则cpu会爆
    本程序设定的 db名为: taobao  collection:itemsLog
    请为itemsLog 增加索引 num_iid
    db.itemsLog.ensureIndex({'num_iid':1})
    linux下运行:
```javascript
    mongo
    use taobao
     db.itemsLog.ensureIndex({'num_iid':1})
```
## 其他问题

* 数据库导入失败
    * 建议安装mysql5.7
    * 数据库编码指定为utf8mb4

* 入门用户建议使用面板操作
    * 宝塔面板  bt.cn
    * lnmp  lnmp.org (无面板)
    * wdcp  wdlinux.cn (不建议,居然给面板单独跑一套Apache 也是邪了门)
    * 另外 小内存机器 建议  安装 nginx 而不是Apache



## 建议
采集程序后台运行
	* nohup python start.py &
	* 建议采用 supervisor 进行后台运行;[supervisor说明文档](https://github.com/Supervisor/supervisor)




##有问题反馈
在使用中有任何问题，欢迎反馈给我们，可以用以下联系方式交流

* QQ群: 772162360
