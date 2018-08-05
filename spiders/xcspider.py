#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from lxml import etree

from spider import Spider


class XcSpider(Spider):
    '''爬取西刺免费代理'''

    def run(self):
        urls = ['http://www.xicidaili.com/',
                'http://www.xicidaili.com/nn/',
                'http://www.xicidaili.com/nt/',
                'http://www.xicidaili.com/wn/',
                'http://www.xicidaili.com/wt/']
        results = []
        for u in urls:
            try:
                r = self._get(u)
                if r:
                    results.extend(r)
            except:
                print('%s failed!' % u)
        print(results)
        return results

    def _get(self, url):
        headers = {'user-agent': self.userAgents[1]}
        r = requests.get(url, headers=headers)
        html = etree.HTML(r.content)
        rows = html.xpath('//table[@id="ip_list"]/tr[@class!="subtitle"]')

        results = []
        for r in rows:
            try:
                ptype = str.lower(r[5].text)
                results.append({
                    'host': r[1].text,
                    'port': int(r[2].text),
                    'type': ptype if ptype != 'socks4/5' else ptype,
                    'location': 'cn'
                })
            except:
                pass

        return results


if __name__ == '__main__':
    s = XcSpider()
    s.run()
