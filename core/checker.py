#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import setting
import threading
from concurrent.futures import ThreadPoolExecutor
import urllib
from data import userAgent


def __sock_check(item):
    if item['type'] != setting.proxy_type:
        item['success'] = False
        return True

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((item['host'], item['port']))
        s.close()
        print('%s:%s ok!' % (item['host'], item['port']))
        item['success'] = True
    except Exception as e:
        print(e)
        item['success'] = False

    return True


def __http_https_check(item):
    if item['type'] != setting.proxy_type:
        item['success'] = False
        return True

    req = None
    headers = {
        'User-Agent': userAgent.agents[0]
    }
    url = None
    try:
        if item['type'] == 'https':
            if item['loc'] == 'cn':
                url = 'https://ip.cn/'
            else:
                url = 'https://www.whatismyip.com/'
        else:
            if item['loc'] == 'cn':
                url = 'http://2018.ip138.com/ic.asp'
            else:
                url = 'http://www.whatsmyip.org/'
        req = urllib.request.Request(url, headers=headers)
        req.set_proxy('%s:%s' % (item['host'], item['port']), item['type'])
        response = urllib.request.urlopen(req, timeout=3)
        content = response.read().decode('ISO-8859-1')
        item['success'] = content.find(item['host']) != -1
        if item['success']:
            print('%s:%s ok!' % (item['host'], item['port']))
    except Exception as e:
        print(e)
        item['success'] = False

    return True


def batch_check(proxies):
    pool = ThreadPoolExecutor(128)

    threads = []
    for p in proxies:
        if p['type'] == 'socks':
            threads.append(pool.submit(__sock_check, p))
        else:
            threads.append(pool.submit(__http_https_check, p))

    for t in threads:
        t.result()

    print('%s proxy host checked!' % (len(proxies)))
