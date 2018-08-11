#!/usr/bin/env python
# -*- coding:utf-8 -*-


class LocalSpider():
    def __init__(self):
        self.idle = 10
        
    def run(self):
        return [
            {"host": "127.0.0.1", 'port': 1080, 'type': 'socks', 'loc': 'jp'},
            {"host": "127.0.0.1", 'port': 1087, 'type': 'http', 'loc': 'jp'}
        ]
