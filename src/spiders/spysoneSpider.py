#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import etree
from spiders.baseSpider import BaseSpider
import logging
import re

# 在大陆，此spider需要设置二级代理才可以正常爬取
class SpysoneSpider(BaseSpider):

    def __init__(self):
        BaseSpider.__init__(self)
        self.urls = [
            'http://spys.one/en/anonymous-proxy-list/',
            'http://spys.one/en/anonymous-proxy-list/1/',
            'http://spys.one/en/anonymous-proxy-list/2/'
        ]
        self.idle = 10 * 60  # idle 10 minutes.

    def _parse(self, results, text):
        try:
            _val = {}
            m = re.search(
                r'<script type="text/javascript">([a-zA-Z0-9;=^]*)?</script>', text)
            if m:
                express = m.group(1)
                for e in express.split(';'):
                    if e:
                        item = e.split('=')
                        if '^' in item[1]:
                            _x = item[1].split('^')
                            _val[item[0]] = int(_x[0]) ^ _val[_x[1]]
                        else:
                            _val[item[0]] = int(item[1])

            html = etree.HTML(text)
            rows = html.xpath('//tr[starts-with(@class, "spy1x")]')

            for r in rows[2:]:
                port = ''
                for _x in re.finditer(r'([a-z0-9])*?\^([a-z0-9])*', r[0][1][0].text):
                    item = _x.group(0).split('^')
                    port += str(_val[item[0]] ^ _val[item[1]])
                results.append({
                    'host': r[0][1].text,
                    'port': int(port),
                    'type': 'http',#str.lower(r[1][0][0].text + r[1][0][1].text),
                    'loc': 'cn'
                })
        except Exception as e:
            logging.error("KuaidailiSpider error:%s" % e)
