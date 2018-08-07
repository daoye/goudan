#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setting
from core.pipline import Pipline


class Dispatcher():
    def __init__(self):
        self.pipline = Pipline()

        # load middlewares
        [self.pipline.register(self.__load(name)()) for name in setting.pipeline_middlewares]

        # load  spiders
        self.spiders = [self.__load(name)() for name in setting.spiders]

    def run(self):
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

    def __load(self, name):
        sep = name.split('.')
        module_name = '.'.join(sep[0:-1])
        cls_name = sep[-1]
        module = __import__(module_name, globals(), locals(), [cls_name], 0)
        return getattr(module, cls_name)
