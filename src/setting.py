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
proxy_retry = 5

# 指定支持的代理类型，同时只能支持一种类型，可选值有：http、https、socks、http/https
proxy_type = 'http/https'

# 指定隧道代理的地址
server_host = '0.0.0.0'

# 指定隧道代理的端口
server_port = 1991

# 用于Spider的代理，默认为None
spider_proxy = None

# 设置测试代理的超时时间，较短的时间可以获得速度较快的代理，但可用代理数量会更少，单位：秒
test_timeout = 10

# 爬虫完成一轮爬取后，进行下一轮爬取需要间隔的时间，单位：分
idle_time = 5

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
