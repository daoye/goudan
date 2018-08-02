#!/usr/bin/env python
# -*- coding: utf-8 -*-

from proxy import dispatcher
from threading import Thread
import rproxy
import time


def runProxyDispatcher():
    while True:
        dispatcher.run()
        time.sleep(10 * 60 * 1000)


def runTunnel():
    rproxy.start()


if __name__ == '__main__':
    proxThread = Thread(target=runProxyDispatcher)
    # proxThread.daemon = True
    proxThread.start()
    print('proxy spider started.')

    tunnelThread = Thread(target=runTunnel)
    tunnelThread.run()
