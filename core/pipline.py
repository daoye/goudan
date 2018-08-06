#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.utils import singleton


@singleton
class Pipline():
    def __init__(self):
        self.__middlewares = []

    def input(self, data):
        '''向管道输入数据'''
        for m in self.__middlewares:
            try:
                m.input(data)
            except Exception as e:
                print(e)

    def register(self, middleware):
        '''向管道中注册中间件'''
        self.__middlewares.append(middleware)
