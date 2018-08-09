#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import dispatcher, rproxy
from threading import Thread
import sys
import setting
import asyncio
import logging


def run_dispatcher():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    _dispatcher = dispatcher.Dispatcher()
    _dispatcher.run()


def info():
    print('Example: python main.py -tsocks -l0.0.0.0 -p1991 -shttp://localhost:1087')
    print('-t   [http,https,socks]')
    print('-l   Tunnel host, default is "0.0.0.0"')
    print('-p   Tunnel port, default is "1991"')
    print('-s   Spider proxy address, for example: http://localhost:1087, default is None')
    print('-tt   Test proxy timeout default is 5')


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
                elif arg.startswith('-tt'):
                    setting.test_timeout = int(arg.replace('-tt', ''))
                else:
                    print('invalid argument: %s' % arg)
                    sys.exit(0)
        except:
            info()
            sys.exit(0)

    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.getLogger("urllib3").setLevel(logging.FATAL)
    try:
        d_thread = Thread(target=run_dispatcher, daemon=True)
        d_thread.start()
    except InterruptedError:
        pass

    rproxy.start()
