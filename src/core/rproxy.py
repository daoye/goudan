#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from data.samplePool import SamplePool
import setting
import socket
import functools
import logging


async def process(s_client, client_addr, loop, pool):
    logging.debug('Client %s:%s conneccted' % client_addr)
    s_remote = socket.socket()
    s_remote.setblocking(False)
    s_remote.settimeout(2)
    retry = setting.proxy_retry
    success = False
    remote_addr = None
    while retry:
        try:
            proxy = pool.get_one()
            if not proxy:
                break
            remote_addr = (proxy['host'], proxy['port'])
            await loop.sock_connect(s_remote, remote_addr)
            logging.debug('Proxy %s:%s connected!' % remote_addr)
            success = True
            break
        except:
            logging.debug("Proxy connect failed, will retry (retry %s times)." % retry)
            retry -= 1

    if not success:
        logging.info("Retry multiple times, but can't connect any one proxy.")
        s_client.close()
        return

    loop.add_reader(s_client, functools.partial(forward, loop, s_client, s_remote, client_addr, remote_addr))
    loop.add_reader(s_remote, functools.partial(forward, loop, s_remote, s_client, client_addr, remote_addr))


def forward(loop, r, w, client_addr, remote_addr):
    try:
        data = r.recv(1024)
        if data:
            loop.call_soon(w.sendall, data)
            return
    except Exception as e:
        logging.debug("Recive data error:%s" % e)

    try:
        r.shutdown(socket.SHUT_RDWR)
        r.close()
    except:
        pass
    try:
        w.shutdown(socket.SHUT_RDWR)
        w.close()
    except:
        pass
    loop.remove_reader(r)
    loop.remove_reader(w)

    logging.debug('%s:%s disconnected!' % client_addr)
    logging.debug('%s:%s disconnected!' % remote_addr)



def start():
    loop = asyncio.get_event_loop()
    pool = SamplePool()

    addr = (setting.server_host, setting.server_port)
    sock = socket.socket()
    sock.bind(addr)
    sock.listen(1)
    sock.setblocking(False)
    logging.info('Tunnel server on: %s:%s, but you must wait one of spiders work done.' % addr)

    try:
        while True:
            s_client, client_addr = loop.run_until_complete(loop.sock_accept(sock))
            asyncio.Task(process(s_client, client_addr, loop, pool))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        logging.error("Accept client error: %s" % e)

    try:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except:
        pass

    loop.close()
