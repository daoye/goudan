#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from core.samplePool import SamplePool
import setting
import socket
import functools


async def process(s_client, client_addr, loop, pool):
    print('client %s:%s conneccted' % client_addr)
    s_remote = socket.socket()
    s_remote.setblocking(False)
    s_remote.settimeout(2)
    retry = 5
    success = False
    remote_addr = None
    while retry:
        try:
            proxy = pool.get_one()
            if not proxy:
                break
            remote_addr = (proxy['host'], proxy['port'])
            await loop.sock_connect(s_remote, remote_addr)
            print('proxy %s:%s connected!' % remote_addr)
            success = True
            break
        except:
            retry -= 1

    if not success:
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
        print(e)
        pass

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

    print('%s:%s disconnected!' % client_addr)
    print('%s:%s disconnected!' % remote_addr)



def start():
    loop = asyncio.get_event_loop()
    pool = SamplePool()

    addr = (setting.server_host, setting.server_port)
    sock = socket.socket()
    sock.bind(addr)
    sock.listen(1)
    sock.setblocking(False)
    print('Tunnel server on: %s:%s, but you must wait one of spiders work done.' % addr)

    try:
        while True:
            s_client, client_addr = loop.run_until_complete(loop.sock_accept(sock))
            asyncio.Task(process(s_client, client_addr, loop, pool))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)

    try:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    except:
        pass

    loop.close()
