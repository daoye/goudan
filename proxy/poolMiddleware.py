#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core.samplePool import SamplePool


class PoolMiddleware():
    def input(self, data):
        pool = SamplePool()
        pool.add(data)
