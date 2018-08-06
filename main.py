#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import dispatcher, rproxy
from threading import Thread
import time
import sys
import setting


def run_dispatcher():
    print('Spiders are running...')
    while True:
        dispatcher.run()
        time.sleep(5 * 60 * 1000)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        setting.proxy_type = sys.argv[1]
    try:
        d_thread = Thread(target=run_dispatcher, daemon=True)
        d_thread.start()
    except InterruptedError:
        pass

    rproxy.start()
