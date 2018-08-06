#!/usr/bin/env python
# -*- coding: utf-8 -*-

spiders = [
    # 'spiders.localSpider.LocalSpider',
    'spiders.xcspider.XcSpider'
]

# 中间件将按顺序被执行
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

#args:
# python main.py -tsocks -l0.0.0.0 -p1991
