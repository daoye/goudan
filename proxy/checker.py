#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib import request

__default_hit = 'http://www.baidu.com/'


def check(proxy_host, proxy_type, hit=__default_hit):
    '''检查代理是否有效，仅支持http代理'''
    req = request.Request(hit)
    req.add_header('User-Agent', 'Mozilla/6.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/8.0 Mobile/10A5376e Safari/8536.25')
    if not proxy_host or not proxy_type:
        return False
    req.set_proxy(proxy_host, proxy_type)
    try:
        with request.urlopen(req) as f:
            data = f.read()
            return data is not None
    except Exception as e:
        print(e)
        return False


def batch_check(proxies, hit=__default_hit):
    '''批量检查代理是否有效'''
    for p in proxies:
        p['success'] = check(p['host'], p['type'])
