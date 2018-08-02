#!/usr/bin/env python
# -*- coding: utf-8 -*-

spiders = [
    'spiders.localSpider.LocalSpider'
]

# 中间件将按顺序被执行
pipeline_middlewares = [
    'proxy.checkerMiddleware.CheckerMiddleware',
    'proxy.poolMiddleware.PoolMiddleware'
]
