#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import asyncio
import random

import aiohttp
from lxml import etree

import setting
import logging
from pony.orm import *
from core.data import ProxyItem
from datetime import datetime, timedelta

class BaseSpider():

    def __init__(self):
        self.urls = []
        self.next= None
        self.loop = asyncio.get_event_loop()
        self.idle = 5
        self.idlePerPage = 2


    def start(self, hosting):
        logging.info("Running spider [%s] now!" % (type(self).__name__))
        results = []
        #  tasks = [self._feth(results, u) for u in self.urls]
        #  self.loop.run_until_complete(asyncio.gather(*tasks))
        for u in self.urls:
            self.loop.run_until_complete(self._feth(results, u))
            time.sleep(self.idlePerPage)

        while self.next:
            next_url = self.next
            self.next = None
            self.loop.run_until_complete(self._feth(results, next_url))

        with db_session:
            expired = int((datetime.now() + timedelta(days=360*10)).timestamp())
            for r in results:
                if not exists(x for x in ProxyItem if
                              x.protocol == r['protocol'] and x.host == r['host'] and x.port == r['port']):
                    ProxyItem(protocol=r['protocol'],
                              supportProtocol=r['supportProtocol'],
                              host=r['host'],
                              port=r['port'],
                              expired=r.get('expired', expired),
                              usr=r.get('usr', ''),
                              pwd=r.get('pwd', ''),
                              location=r.get('location', ''),
                              isok=False,
                              validCount=0,
                              failedCount=0)

    def _headers(self):
        return {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}

    async def _feth(self, results, url):
        logging.debug("Fetching page [%s]" % (url))
        try:
            html = None
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=self._headers()) as response:
                    html = await response.text()

            self._parse(results, html)

        except Exception as e:
            logging.error("Fetch page error: %s" % (e))

    def _parse(self, results, text):
        pass
