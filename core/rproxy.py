#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from core.samplePool import SamplePool
import setting
import socket


class ServerProtocol(asyncio.Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.pool = SamplePool()
        self.clients = {}
        self.closed = False

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        self.transport = transport

    def data_received(self, data):
        asyncio.Task(self.task_send(data))

    # @asyncio.coroutine
    async def task_send(self, data):
        client = await self.connect_to_proxy()
        if not client:
            self.transport.close()
        else:
            client.transport.write(data)

    async def connect_to_proxy(self):
        client = self.clients.get(self.peername)
        if client and client.connected:
            return client

        while not self.closed:
            try:
                proxy = self.pool.get_one()
                if proxy:
                    _, proxy_protocol = await self.loop.create_connection(lambda:  ProxyProtocol(self.transport), proxy['host'], proxy['port'])
                    self.clients[self.peername] = proxy_protocol
                    return proxy_protocol
                else:
                    self.transport.close()
                    print('No have alive proxy!')
                    return None
            except Exception as e:
                print(e)

            return None

    def connection_lost(self, exc):
        self.closed = True
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
        self.server.close()


def start():
    loop = asyncio.get_event_loop()
    coro = loop.create_server(lambda: ServerProtocol(
        loop), setting.server_host, setting.server_port)
    server = loop.run_until_complete(coro)

    print('Tunnel server on: %s:%s, but you must wait one of spiders work done.' % (
        setting.server_host, setting.server_port))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
