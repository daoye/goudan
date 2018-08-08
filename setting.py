#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 指定用于获取代理ip的爬虫
spiders = [
    # 'spiders.localSpider.LocalSpider',
    'spiders.freeHTTPSpider.FreeHTTPSpider',
    'spiders.freeHTTPSSpider.FreeHTTPSSpider',
    'spiders.xiciSpider.XiciSpider',
    'spiders.data5uSpider.Data5uSpider',
    'spiders.kuaidailiSpider.KuaidailiSpider',
]

# 指定中间件，中间件将按顺序被执行
pipeline_middlewares = [
    'middlewares.validMiddleware.ValidMiddleware',
]

# 指定支持的代理类型，同时只能支持一种类型，可选值有：http、https、socks、http/https
#-t
proxy_type = 'http/https'

# 指定隧道代理的地址
# -l
server_host = '0.0.0.0'

# 指定隧道代理的端口
# -p
server_port = 1991

# 用于Spider的代理，默认为None
# -s
spider_proxy = None

# 设置测试代理的超时时间，较短的时间可以获得速度较快的代理，但可用代理数量会更少，单位：秒
#-tt
test_timeout = 10

# 同时支持命令行参数配置，示例如下:
# python main.py -thttps -l0.0.0.0 -p1991 -shttp://localhost:1087 -tt5
