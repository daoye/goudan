#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import setting
import socket
import functools
import logging

class RProxy():
    def __init__(self, protocol, host, port, pool):
        self.protocol = protocol
        self.host = host
        self.port = port
        self.pool = pool
        self.loop = asyncio.get_event_loop()
        self.sock = None


    def start(self):
        addr = (self.host, self.port)
        self.sock = socket.socket()
        self.sock.bind(addr)
        self.sock.listen(1)
        self.sock.setblocking(False)
        logging.info('%s:%s is %s server' % (self.host, self.port, self.protocol))

        asyncio.Task(self._accept())


    def stop(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
        except:
            pass


    async def _accept(self):
        s_client, client_addr = await self.loop.sock_accept(self.sock)
        asyncio.Task(self._process(s_client, client_addr))
        if self.loop.is_running():
            asyncio.Task(self._accept())


    async def _process(self, s_client, client_addr):
        s_client.setblocking(False)
        logging.debug('Client %s:%s connected' % client_addr)
        
        retry = setting.retry
        success = False

        s_remote = None
        remote_addr = None
        while retry:
            proxy = self.pool.get(self.protocol)
            if not proxy:
                break

            logging.debug('Try connect to [%s://%s:%s]' % (proxy.protocol, proxy.host, proxy.port))
            try:
                remote_addr = (proxy.host, proxy.port)
                s_remote = socket.socket()
                s_remote.setblocking(False)
                s_remote.settimeout(2)

                await self.loop.sock_connect(s_remote, remote_addr)

                logging.info('Connect success [%s://%s:%s]' % (proxy.protocol, proxy.host, proxy.port))
                success = True
                break
            except:
                # logging.exception("Connect failed  [%s://%s:%s] will retry (retry [%s] times)." % (proxy.protocol, proxy.host, proxy.port, retry))
                retry -= 1

        if not success:
            logging.info("Retry multiple times, but can't connect any one proxy.")
            s_client.close()
            return

        self.loop.add_reader(s_client, functools.partial(self._forward, s_client, s_remote, client_addr, remote_addr))
        self.loop.add_reader(s_remote, functools.partial(self._forward, s_remote, s_client, remote_addr, client_addr))


    def _forward(self, r, w, r_addr, w_addr):
        try:
            data = r.recv(4096)
            if data:
                asyncio.Task(self.loop.sock_sendall(w, data))
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

        self.loop.remove_reader(r)
        self.loop.remove_reader(w)

        logging.debug('%s:%s disconnected!' % w_addr)
        logging.debug('%s:%s disconnected!' % r_addr)

