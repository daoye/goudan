#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import singleton
import logging

@singleton
class Pipline():
    def __init__(self):
        self.__middlewares = []

    def input(self, data):
        for m in self.__middlewares:
            try:
                data = m.input(data)
                if not data:
                    break
            except Exception as e:
                logging.error("Input data failed: %s" % e)

    def register(self, middleware):
        self.__middlewares.append(middleware)
        logging.debug('Middleware [%s] registered!' % (type(middleware).__name__))