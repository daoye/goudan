#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import checker


class CheckerMiddleware():
    def input(self, data):
        checker.batch_check(data)
        for x in data:
            if x.get('success') == False:
                data.remove(x)
