#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 指定用于获取代理ip的爬虫
spiders = [
    # 'spiders.localSpider.LocalSpider',
    # 'spiders.xcspider.XcSpider',
    # 'spiders.kuaidailiSpider.KuaidailiSpider'
    'spiders.freeHTTPSpider.FreeHTTPSpider',
    # 'spiders.freeHTTPSSpider.FreeHTTPSSpider'
]

# 指定中间件，中间件将按顺序被执行
pipeline_middlewares = [
    'middlewares.checkerMiddleware.CheckerMiddleware',
    'middlewares.poolMiddleware.PoolMiddleware'
]

# 指定支持的代理类型，同时只能支持一种类型，可选值有：http、https、socks
proxy_type = 'http'

# 指定隧道代理的地址
server_host = '0.0.0.0'

# 指定隧道代理的端口
server_port = 1991

#用于Spider的代理，默认为None
spider_proxy = 'http://localhost:1087'

# example arguments for command line:
# python main.py -tsocks -l0.0.0.0 -p1991 -shttp://localhost:1087
