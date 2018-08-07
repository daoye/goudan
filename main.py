#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import dispatcher, rproxy
from threading import Thread
import time
import sys
import setting
import asyncio
import datetime


def run_dispatcher():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    _dispatcher = dispatcher.Dispatcher()

    while True:
        print('[%s] Spiders are running now...' % datetime.datetime.now())
        _dispatcher.run()
        print('[%s] Spiders run complete!' % datetime.datetime.now())
        time.sleep(5*60)


def _info():
    print('Example: python main.py -tsocks -l0.0.0.0 -p1991 -shttp://localhost:1087')
    print('-t   [http,https,socks]')
    print('-l   Tunnel host, default is "0.0.0.0"')
    print('-p   Tunnel port, default is "1991"')
    print('-s   Spider proxy address, for example: http://localhost:1087, default is None')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            for arg in sys.argv[1:]:
                if arg.startswith('-t'):
                    setting.proxy_type = arg.replace('-t', '').lower()
                elif arg.startswith('-l'):
                    setting.server_host = arg.replace('-l', '')
                elif arg.startswith('-p'):
                    setting.server_port = int(arg.replace('-p', ''))
                elif arg.startswith('-s'):
                    setting.spider_proxy = arg.replace('-s', '')
                else:
                    print('invalid argument: %s' % arg)
                    sys.exit(0)
        except:
            _info()
            sys.exit(0)
    try:
        d_thread = Thread(target=run_dispatcher,
                          daemon=True, name="dispatcher")
        d_thread.start()
    except InterruptedError:
        pass

    rproxy.start()
