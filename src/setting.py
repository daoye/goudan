#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 重连代理的重试次数
retry = 5

# 指定支持的代理类型，同时只能支持一种类型，可选值有：http、https、socks、http/https
svr = {
    'http': '0.0.0.0:1991',
    'https': '0.0.0.0:1992',
    'socks4': '0.0.0.0:1993',
    'socks5': '0.0.0.0:1994',
}

plugins = [
    # "C:\\Projects\\goudan_plugins\\src\\example.py",
    # "C:\\Projects\\goudan_plugins\\src\\spiders\\data5uSpider.py",
    # "C:\\Projects\\goudan_plugins\\src\\spiders\\freeHTTPSpider.py",
    # "C:\\Projects\\goudan_plugins\\src\\spiders\\freeHTTPSSpider.py",
    # "C:\\Projects\\goudan_plugins\\src\\spiders\\kuaidailiSpider.py",
    # "C:\\Projects\\goudan_plugins\\src\\spiders\\spysoneSpider.py",
    # "C:\\Projects\\goudan_plugins\\src\\spiders\\xiciSpider.py"
    "https://raw.githubusercontent.com/daoye/goudan_plugins/master/src/spiders/data5uSpider.py",
    "https://raw.githubusercontent.com/daoye/goudan_plugins/master/src/spiders/freeHTTPSpider.py",
    "https://raw.githubusercontent.com/daoye/goudan_plugins/master/src/spiders/kuaidailiSpider.py",
    "https://raw.githubusercontent.com/daoye/goudan_plugins/master/src/spiders/spysoneSpider.py",
    "https://raw.githubusercontent.com/daoye/goudan_plugins/master/src/spiders/xiciSpider.py"
]

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