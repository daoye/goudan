#!/usr/bin/env python
# -*- coding: utf-8 -*-


from spiders.baseSpider import BaseSpider
import json


class FreeHTTPSpider(BaseSpider):
    '''data from https://github.com/jiangxianli/ProxyIpLib'''

    def __init__(self):
        BaseSpider.__init__(self)
        self.urls = ['http://ip.jiangxianli.com/api/proxy_ips']

    def _parse(self, results, text):
        try:
            data = json.loads(text)

            if data.get('code') != 0:
                return
            data = data.get('data')

            for r in data.get('data'):
                results.append({
                    'host': r.get('ip'),
                    'port': int(r.get('port')),
                    'type': r.get('protocol'),
                    'loc': 'cn'
                })
                
            self.next = data.get('next_page_url')
        except Exception as e:
            print(e)
