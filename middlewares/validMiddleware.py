#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import setting
from data import userAgent
from core.samplePool import SamplePool


class ValidMiddleware():
    def __init__(self):
        self.pool = SamplePool()

    def input(self, data):
        tasks = [self._valid(p) for p in data]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(asyncio.gather(*tasks))
        print('Have %s alive proxies.' % len(self.pool.get_pool()))
        return None

    async def _valid(self, item):
        try:
            r, w = await asyncio.open_connection(item['host'], item['port'])
            success = False
            if setting.proxy_type == 'https':
                w.write(b'CONNECT ip.cn:443 HTTP/1.1\r\n\r\n')
                text = await r.read()
                text = text.lower()
                if text.find(b'connection established') != -1:
                    success = True
            elif setting.proxy_type == 'http':
                w.write(
                    b'GET  http://2018.ip138.com/ic.asp HTTP/1.1\r\nHost:2018.ip138.com\r\nConnection: Close\r\n\r\n')
                text = await r.read()
                text = text.lower()
                if text.find(item['host']) != -1:
                    success = True
            elif item['type'] == 'socks':
                success = True

            if success:
                print('%s:%s ok!' % (item['host'], item['port']))
                self.pool.add([item])
            else:
                self.pool.remove(item)
            w.close()
        except Exception as e:
            self.pool.remove(item)
            print(e)
