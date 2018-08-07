#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import random

import aiohttp
from lxml import etree

from data import userAgent
import setting


class BaseSpider():

    def __init__(self):
        self.urls = []
        self.loop = asyncio.get_event_loop()

    def run(self):
        results = []
        tasks = [self._feth(results, u) for u in self.urls]
        self.loop.run_until_complete(asyncio.gather(*tasks))

        return results

    def _headers(self):
        number = random.randint(0, len(userAgent.agents)-1)
        return {'user-agent': userAgent.agents[number]}

    async def _feth(self, results, url):
        try:
            html = None
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self._headers(), proxy=setting.spider_proxy) as response:
                    html = await response.text()

            self._parse(results, html)

        except Exception as e:
            print(e)

    def _parse(self, results, text):
        pass
