# shino

## 简介
shino 是一个免费开源的无代码化分布式爬虫框架，项目使用到 mysql、rabbitmq、redis 分别作为数据存储、消息队列和缓存。利用 grpc 技术作解耦各个模块，实现多机灵活部署。灵活组合的拓展需求。

## 功能块
- 种子生成器
- 下载器
- 解析器
- 清洗器
- 存储器

## 准备
- [mysql](https://www.mysql.com/) 安装并开启
- [rabbitmq](https://www.rabbitmq.com/) 安装并开启
- [redis](https://redis.io/) 安装并开启

**备注：请确保你所使用的环境和 `resouces` 中的配置一致**


## 安装使用
- 版本要求

`python >= 3.7.0`

- 获取项目代码
```shell script
git clone https://github.com/hacksman/shino
```

- 安装依赖
```shell script
pip instal requirements.txt
```

- 运行服务
```shell script
# 开启服务 / debug 表示在 debug 配置环境下运行
sh start.sh debug
# 关闭服务
sh stop.sh
# 重启服务
sh restart.sh debug
``` 

- 原理说明

[shino 原理说明](https://github.com/hacksman/code_notes/blob/master/shino/shino%20%E5%8E%9F%E7%90%86%E8%AF%B4%E6%98%8E.md)

- 使用教程

[shino 教程 - 知乎热榜数据抓取](https://github.com/hacksman/code_notes/blob/master/shino/shino%20%E6%95%99%E7%A8%8B%20-%20%E7%9F%A5%E4%B9%8E%E7%83%AD%E6%A6%9C%E6%95%B0%E6%8D%AE%E6%8A%93%E5%8F%96.md)


## TODO-LIST
- [X] seed modifier 中间件模式改写
- [X] run.sh 运行启动脚本
    - [X] 支持 start、restart、stop
- [X] 命令行模式支持更加丰富的功能
    - [X] debug 模式
        - [X] seed 运行时间修改为 10s 执行一次
        - [X] debug 以上级别日志输出
- [X] install 脚本编写，实现 start/restart/stop 功能
- 各个地方的参数配置化
- 各模块功能及原理说明文档
    - 是什么
    - [X] 原理
    - [X] 使用说明
- 使用说明
    - [X] 基本 demo
    - 链式调用 demo
    - 动态 url demo
    - 解析 xpath demo
    - 解析内嵌结构 demo
- [X] 去掉冗余的日志
- [ ] 支持多 headers 切换形式
- 数据支持 update 操作
- ~~支持仅本地抓取~~
- 完善统计功能
- 后端接口暴露
- 前端界面

## License