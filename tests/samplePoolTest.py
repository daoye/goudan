#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from unittest.mock import MagicMock, Mock
from core.samplePool import SamplePool


class SamplePoolTest(unittest.TestCase):

    def setUp(self):
        self.pool = SamplePool()
        self.pool._set_pool(self.mockData())

    def tearDown(self):
        self.pool._set_pool([])

    def test_get(self):
        item = self.pool.get()
        assert item is not None

    def test_add(self):
        data = [
            {"host": '192.168.0.15', 'port': 1080, 'loc': 'jp', 'type': 'socks'},
            {"host": '192.168.0.15', 'port': 1081, 'loc': 'jp', 'type': 'socks'},
            {"host": '232.12.123.4', 'port': 1080, 'loc': 'jp', 'type': 'socks'}
        ]
        self.pool.add(data)

        actual = len(self.pool._get_pool())
        assert actual == 9

    def test_add_repeat(self):
        data = [
            {"host": '127.0.0.1', 'port': 1080, 'loc': 'jp', 'type': 'socks'},
            {"host": '127.0.0.1', 'port': 1080, 'loc': 'jp', 'type': 'socks'}
        ]
        self.pool.add(data)

        actual = len(self.pool._get_pool())
        assert actual == 6

    def test_remove(self):
        item = {"host": '127.0.0.1', 'port': 1080,
                'loc': 'jp', 'type': 'socks'}
        self.pool.remove(item)
        actual = len(self.pool._get_pool())
        assert actual == 5

    def test_remove_nobody(self):
        self.pool.remove({"host": '127.0.0.1', 'port': 1080})
        actual = len(self.pool._get_pool())
        assert actual == 6

    def mockData(self):
        return [
            {"host": '127.0.0.1', 'port': 1080,  'loc': 'jp', 'type': 'socks'},
            {"host": '192.168.26.2', 'port': 235,  'loc': 'cn', 'type': 'http'},
            {"host": '198.26.23.25', 'port': 12, 'loc': 'cn', 'type': 'http'},
            {"host": '198.26.23.25', 'port': 8099,   'loc': 'cn', 'type': 'http'},
            {"host": '223.26.56.159', 'port': 23, 'loc': 'cn', 'type': 'http'},
            {"host": '223.26.56.159', 'port': 62658, 'loc': 'cn', 'type': 'http'}
        ]
