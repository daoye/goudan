#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import random

import aiohttp
from lxml import etree

from data import agents
import setting
import logging

class BaseSpider():

    def __init__(self):
        self.urls = []
        self.next= None
        self.loop = asyncio.get_event_loop()

    def run(self):
        logging.debug("Running spider [%s] now!" % (type(self).__name__))
        results = []
        tasks = [self._feth(results, u) for u in self.urls]
        self.loop.run_until_complete(asyncio.gather(*tasks))

        while self.next:
            next_url = self.next
            self.next = None
            self.loop.run_until_complete(self._feth(results, next_url))

        return results

    def _headers(self):
        number = random.randint(0, len(agents)-1)
        return {'user-agent': agents[number]}

    async def _feth(self, results, url):
        logging.debug("Fetching page [%s] by spider [%s]." % (url, type(self).__name__))
        try:
            html = None
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self._headers(), proxy=setting.spider_proxy) as response:
                    html = await response.text()

            self._parse(results, html)

        except Exception as e:
            logging.error("Fetch page error:%s by spider [%s]" % (e, type(self).__name__))

    def _parse(self, results, text):
        pass
