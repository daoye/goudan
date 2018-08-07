#!/usr/bin/env python
# -*- coding:utf-8 -*-


class LocalSpider():
    def run(self):
        return [
            {"host": "127.0.0.1", 'port': 1080, 'type': 'socks', 'loc': 'jp'},
            {"host": "127.0.0.1", 'port': 1099, 'type': 'socks', 'loc': 'jp'}
        ]
