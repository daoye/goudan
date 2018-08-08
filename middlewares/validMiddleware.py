#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import setting
import urllib3
from core.samplePool import SamplePool
from data.userAgent import agents
import random


class ValidMiddleware():
    def __init__(self):
        self.pool = SamplePool()
        urllib3.disable_warnings()

    def input(self, data):
        loop = asyncio.get_event_loop()
        tasks = []
        if setting.proxy_type == 'socks':
            tasks = [self._valid_socks(p)
                     for p in data if p['type'] == 'socks']
        else:
            tasks = [loop.run_in_executor(None, self._valid, p)
                     for p in data if p['type'] != 'socks']
        loop.run_until_complete(asyncio.gather(*tasks))
        print('Have %s alive proxies.' % len(self.pool.get_pool()))
        return None

    async def _valid_socks(self, item):
        try:
            _, w = await asyncio.open_connection(item['host'], item['port'])
            print('%s:%s ok!' % (item['host'], item['port']))
            self.pool.add([item])
            w.close()
        except Exception as e:
            self.pool.remove(item)
            print(e)

    def _valid(self, item):
        https_target_url = 'https://www.ipip.net/'
        http_target_url = 'http://2018.ip138.com/ic.asp'
        types = setting.proxy_type.split('/')
        success = False
        if 'https' in types:
            success = self._test(
                https_target_url, item['host'], item['port'], item['type'])
        if 'http' in types:
            if 'https' in types and not success:
                success = False
            else:
                success = self._test(
                    http_target_url, item['host'], item['port'], item['type'])

        if success:
            print('%s:%s ok!' % (item['host'], item['port']))
            self.pool.add([item])
        else:
            self.pool.remove(item)

    def _test(self, url, proxy_host, proxy_port, proxy_type):
        proxy_addr = '%s://%s:%s' % (proxy_type, proxy_host, proxy_port)
        headers = {
            'User-Agent': agents[random.randint(0, len(agents)-1)]
        }
        try:
            req = urllib3.ProxyManager(proxy_addr)
            res = req.request('GET', url, headers=headers, timeout=setting.test_timeout)
            return res.status == 200
        except Exception as e:
            print(e)
            return False
