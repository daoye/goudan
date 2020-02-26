#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import setting
import logging
import argparse
import asyncio
import signal
from pony.orm import *
from core.data import Pool, db_bind
from core import FILE
from core.rproxy import RProxy
from core import hosting




def parse_args():
    info = '''Goudan(狗蛋)is a tunnel proxy, it's support all tcp proxy(theoretically), such as http,https,socks.
By default, goudan crawl free proxies from some websites. So, you can use it out of box.
For more information visit: https://github.com/daoye/goudan
    '''
    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('-r', '--retry', type=int, default=5,
                        help="If proxy host connect failed, goudan will retry use another proxy. This argument tell goudan number of retries, default is 5.")
    parser.add_argument('-l', '--listen', type=str, default="http:0.0.0.0:1991,https:0.0.0.0:1992,socks4:0.0.0.0:1993,socks5:0.0.0.0:1994",
                        help="Set tunnel proxy's hosts. This can be specified more than one host. To define host use this format: protocol:ip:port,protocol:ip:port,...  The protocol could be http,https,socks4,socks5.")

    parser.add_argument('--log_level', type=int, choices=[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR],
                        default=20, help="Set log level, The optional values are: 10=DEBUG,20=INFO,30=WARNING,40=ERROR, default is 20.")
    args = parser.parse_args()
    setting.retry = args.retry
    for x in args.listen.split(','):
        (protocol, host, port) = x.split(':')
        setting.svr[protocol] = '%s:%s' %(host, port)
    setting.log_level = args.log_level


def term(sig_num, addtion):
    hosting.stop()
    exit(1)

if __name__ == '__main__':
    parse_args()
    logging.basicConfig(level=setting.log_level, format="%(asctime)s - %(levelname)s - %(message)s")
    signal.signal(signal.SIGTERM, term)
    signal.signal(signal.SIGILL, term)

    db_bind()

    try:
        loop = asyncio.get_event_loop()

        proxes = []
        pool = Pool()
        for protocol,v in setting.svr.items():
            (host, port) = v.split(':')
            r = RProxy(protocol, host, int(port), pool)
            proxes.append(r)

        # run plugin host.
        hosting.launch()

        # run RProxy server.
        for p in proxes:
            p.start()

        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        for p in proxes:
            p.stop()
        hosting.stop()
