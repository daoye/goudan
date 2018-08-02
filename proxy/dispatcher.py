#!/usr/bin/env python
# -*- coding: utf-8 -*-

import importlib
import setting
from proxy.pipline import Pipline
from proxy import checker


def run():
    pipline = Pipline()

    # register middlewares
    for name in setting.pipeline_middlewares:
        cls = __load_cls(name)
        pipline.register(cls())

    # run spiders
    for name in setting.spiders:
        try:
            s = __load_cls(name)
            data = s().run()
            if data:
                pipline.input(data)
        except Exception as e:
            raise e
            print('spider [%s], run failed.' % name)
            pass


def __load_cls(name):
    sep = name.split('.')
    module_name = '.'.join(sep[0:-1])
    cls_name = sep[-1]
    module = __import__(module_name, globals(), locals(), [cls_name], 0)
    return getattr(module, cls_name)
