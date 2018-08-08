#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
from core.utils import singleton


@singleton
class SamplePool():
    def __init__(self):
        self.__pool = []

    def get_one(self):
        total = len(self.__pool)
        if not total:
            return None

        index = random.randint(0, total-1)
        return self.__pool[index]

    def add(self, items):
        self.__pool.extend([x for x in items if x not in self.__pool])

    def remove(self, item):
        if item in self.__pool:
            self.__pool.remove(item)

    def get_pool(self):
        return self.__pool
