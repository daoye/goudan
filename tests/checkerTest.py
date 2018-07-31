#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import MagicMock, Mock
from proxy import checker


class CheckerTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_signalon(self):
        result = checker.check('127.0.0.1:1088', 'http')
        assert result

    def test_check_batch(self):
        proxies = [{'host': '127.0.0.1:1088', 'type': 'http'},
                   {'host': '127.0.0.1:1088', 'type': 'http'}]
        checker.batch_check(proxies)

        for x in proxies:
            assert x['success']
