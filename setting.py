#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 指定用于获取代理ip的爬虫
spiders = [
    # 'spiders.localSpider.LocalSpider',
    'spiders.freeHTTPSpider.FreeHTTPSpider',
    'spiders.freeHTTPSSpider.FreeHTTPSSpider',
    'spiders.xiciSpider.XiciSpider',
    'spiders.data5uSpider.Data5uSpider',
    'spiders.kuaidailiSpider.KuaidailiSpider'
]

# 指定中间件，中间件将按顺序被执行
pipeline_middlewares = [
    'middlewares.validMiddleware.ValidMiddleware'
]

# 重连代理的重试次数
# -r --retry=5
proxy_retry = 5

# 指定支持的代理类型，同时只能支持一种类型，可选值有：http、https、socks、http/https
#-t --type=http/https
proxy_type = 'http/https'

# 指定隧道代理的地址
# -h --host=0.0.0.0
server_host = '0.0.0.0'

# 指定隧道代理的端口
# -p --port=1991
server_port = 1991

# 用于Spider的代理，默认为None
# --spider_proxy=http://127.0.0.1
spider_proxy = None

# 设置测试代理的超时时间，较短的时间可以获得速度较快的代理，但可用代理数量会更少，单位：秒
#--test_timeout=10
test_timeout = 10

# 日志级别
# --log_level=20
# CRITICAL = 50
# FATAL = CRITICAL
# ERROR = 40
# WARNING = 30
# INFO = 20
# DEBUG = 10
# NOTSET = 0
log_level= 20

# 同时支持命令行参数配置，示例如下:
# python main.py -thttps -l0.0.0.0 -p1991 -shttp://localhost:1087 -tt5
