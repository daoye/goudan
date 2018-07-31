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

    def test_get(self):
        pass