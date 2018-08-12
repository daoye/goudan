#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
from spiders.baseSpider import BaseSpider
import logging

class Data5uSpider(BaseSpider):

    def __init__(self):
        BaseSpider.__init__(self)
        self.urls = [
            'http://www.data5u.com/free/index.shtml',
            'http://www.data5u.com/free/gngn/index.shtml',
            'http://www.data5u.com/free/gnpt/index.shtml',
            'http://www.data5u.com/free/gwgn/index.shtml',
            'http://www.data5u.com/free/gwpt/index.shtml'
        ]

    def _parse(self, results, text):
        try:
            html = etree.HTML(text)
            rows = html.xpath('//ul[@class="l2"]')

            for r in rows:
                ptype = str.lower(r[3][0][0].text)
                results.append({
                    'host': r[0][0].text,
                    'port': int(r[1][0].text),
                    'type': ptype if ptype != 'socks4/5' else 'socks',
                    'loc': 'cn'
                })
        except Exception as e:
            logging.error("Data5uSpider error:%s" % e)
