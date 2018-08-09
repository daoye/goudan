#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setting
from core.pipline import Pipline
from data.samplePool import SamplePool
import datetime
import time
import logging


class Dispatcher():
    def __init__(self):
        self.pipline = Pipline()

        # load middlewares
        [self.pipline.register(self.__load(name)()) for name in setting.pipeline_middlewares]

        # load  spiders
        self.spiders = [self.__load(name)() for name in setting.spiders]

    def __run_spider(self):
        # run spiders
        for spider in self.spiders:
            data = None
            try:
                data = spider.run()
            except Exception as e:
                logging.error('Spider [%s] failed: %s' % (type(spider).__name__, e))

            if data:
                    self.pipline.input(data)

            logging.debug('Spider [%s] was get %s proxies.' % (type(spider).__name__, len(data)))

    def __valid_pool(self):
        pool = SamplePool()
        self.pipline.input(pool.get_pool())

    def __load(self, name):
        sep = name.split('.')
        module_name = '.'.join(sep[0:-1])
        cls_name = sep[-1]
        module = __import__(module_name, globals(), locals(), [cls_name], 0)
        return getattr(module, cls_name)

    def run(self):
        while True:
            logging.debug('Spiders are running now...')
            self.__run_spider()
            logging.debug('Spiders run complete!' )

            time.sleep(setting.idle_time * 60)

            logging.debug('Valid proxies from pool now...')
            self.__valid_pool()
            logging.debug('Pool proxies valid complete!')
