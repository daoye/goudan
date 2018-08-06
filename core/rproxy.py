#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from core.samplePool import SamplePool
import setting


class ServerProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        proxy = SamplePool().get()
        if not proxy:
            self.no_proxy = True
            print('池中没有代理，请等待代理池刷新.')
            return None
        self.no_proxy = False
        self.proxy_ip = proxy['host']
        self.proxy_port = proxy['port']
        self.clients = {}

    def connection_made(self, transport):
        if self.no_proxy:
            transport.close()
            return
        self.peername = transport.get_extra_info('peername')
        self.transport = transport

    def data_received(self, data):
        asyncio.Task(self.task_send(data))

    @asyncio.coroutine
    def task_send(self, data):
        client = self.clients.get(self.peername)
        if not client or not client.connected:
            _, proxy_protocol = yield from self.loop.create_connection(lambda:  ProxyProtocol(self.transport), self.proxy_ip, self.proxy_port)
            self.clients[self.peername] = proxy_protocol
            client = proxy_protocol
        client.transport.write(data)

    def connection_lost(self, exc):
        if not self.no_proxy:
            for x in self.clients.values():
                try:
                    if x.connected:
                        x.transport.close()
                except:
                    pass


class ProxyProtocol(asyncio.Protocol):
    def __init__(self, server):
        self.server = server
        self.connected = False

    def connection_made(self, transport):
        self.transport = transport
        self.connected = True

    def data_received(self, data):
        self.server.write(data)

    def connection_lost(self, exc):
        self.connected = False


def start():
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: ServerProtocol(loop), setting.server_host, setting.server_port)
    server = loop.run_until_complete(coro)

    print('Tunnel server on: %s:%s' % (setting.server_host, setting.server_port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
