#!/usr/bin/env python
# -*- coding: utf-8 -*-

from proxy import checker


class CheckerMiddleware():
    def input(self, data):
        checker.batch_check(data)
