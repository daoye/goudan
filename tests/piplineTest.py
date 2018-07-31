#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import MagicMock, Mock
from proxy.pipline import Pipline


class PiplineTest(unittest.TestCase):

    def setUp(self):
        self.pipline = Pipline()

    def tearDown(self):
        pass

    def test_input(self):
        data = ['item1']
        self.pipline.register(MockMiddleware())
        self.pipline.input(data)

        d_len = len(data)
        assert d_len == 2


class MockMiddleware():
    def input(self, data):
        data.append('middleware')
