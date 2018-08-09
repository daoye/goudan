#!/usr/bin/env python
# -*- coding: utf-8 -*-

from core import dispatcher, rproxy
from threading import Thread
import sys
import setting
import asyncio
import logging
import argparse


def run_dispatcher():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    _dispatcher = dispatcher.Dispatcher()
    _dispatcher.run()


def parse_args():
    info = '''Goudan(狗蛋)is a tunnel proxy, it's support all tcp proxy(theoretically), such as http,https,socks.
By default, goudan crawl free proxies from some websites. So, you can use it out of box.
For more information visit: https://github.com/daoye/goudan
    '''
    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('-r', '--retry', type=int, default=5,
                        help="If proxy host connect failed, goudan will retry use another proxy. This argument tell goudan number of retries, default is 5.")
    parser.add_argument('-t', '--type', type=str, choices=['http', 'https', 'http/https', 'socks'], default="http/https",
                        help="Set tunnel proxy's type. The optional values are http,https,http/https,socks, default is http/https.")
    parser.add_argument('-l', '--host', type=str, default="0.0.0.0",
                        help="Set tunnel proxy's host. It is an ip address, default is 0.0.0.0.")
    parser.add_argument('-p', '--port', type=int, default=1991,
                        help="Set tunnel proxy's port. It is a number(0~65535), default is 1991.")
    parser.add_argument('-i', '--idle_time', type=int, default=5,
                        help="Set spider's idle time, default is 5, unit:minutes.")
    parser.add_argument('--spider_proxy', type=str,
                        help="Set the spider's proxy, like this: http://127.0.0.1:1080")
    parser.add_argument('--test_timeout', type=int, default=10,
                        help="Set timeout to valid proxy host, default is 10, unit:seconds.")
    parser.add_argument('--log_level', type=int, choices=[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR],
                        default=20, help="Set log level, The optional values are :10=DEBUG,20=INFO,30=WARNING,40=ERROR, default is 20.")
    args = parser.parse_args()
    setting.proxy_retry = args.retry
    setting.proxy_type = args.type
    setting.server_host = args.host
    setting.server_port = args.port
    setting.spider_proxy = args.spider_proxy
    setting.test_timeout = args.test_timeout
    setting.idle_time = args.idle_time
    setting.log_level = args.log_level


if __name__ == '__main__':
    parse_args()
    logging.basicConfig(level=setting.log_level, format="%(asctime)s - %(levelname)s - %(message)s")
    logging.getLogger("urllib3").setLevel(logging.FATAL)
    try:
        d_thread = Thread(target=run_dispatcher, daemon=True)
        d_thread.start()

        rproxy.start()
    except InterruptedError:
        pass
