#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setting
from core.pipline import Pipline
from core.samplePool import SamplePool
import datetime
import time


class Dispatcher():
    def __init__(self):
        self.pipline = Pipline()

        # load middlewares
        [self.pipline.register(self.__load(name)())
         for name in setting.pipeline_middlewares]

        # load  spiders
        self.spiders = [self.__load(name)() for name in setting.spiders]

    def __run_spider(self):
        # run spiders
        for spider in self.spiders:
            data = None
            try:
                data = spider.run()
            except Exception as e:
                print('spider failed:%s' % (e))

            if data and len(data):
                    self.pipline.input(data)
            else:
                print('No have proxies.')

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
            print('[%s] Spiders are running now...' % datetime.datetime.now())
            self.__run_spider()
            print('[%s] Spiders run complete!' % datetime.datetime.now())

            time.sleep(5*60)

            print('[%s] Valid proxy from pool now...' %  datetime.datetime.now())
            self.__valid_pool()
            print('[%s] Pool proxy valid complete!' % datetime.datetime.now())
