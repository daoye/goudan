#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import select
from concurrent.futures import ThreadPoolExecutor
from core.samplePool import SamplePool


def process(conn, addr):
    host = SamplePool().get()
    if not host:
        return None

    host_sep = host['host'].split(':')
    ip = host_sep[0]
    port = int(host_sep[1])

    proxy_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_conn.connect((ip, port))
    conn.setblocking(socket.MSG_DONTWAIT)
    proxy_conn.setblocking(socket.MSG_DONTWAIT)
    closed = False
    while not closed:
        rlist, _, _ = select.select([conn, proxy_conn], [], [])
        for r in rlist:
            w = proxy_conn if r is conn else conn
            try:
                d = r.recv(1024)
                if not d:
                    closed = True
                    break
                w.sendall(d)
            except:
                closed = True
                break

    try:
        proxy_conn.shutdown(socket.SHUT_RDWR)
        proxy_conn.close()
    except:
        pass

    try:
        conn.shutdown(socket.SHUT_RDWR)
        conn.close()
    except:
        pass


def start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 1991))
    s.listen(10)
    pool = ThreadPoolExecutor(128)
    print('Server listen on 0.0.0.0:1991')
    while True:
        conn, addr = s.accept()
        pool.submit(process, conn, addr)


if __name__ == '__main__':
    start()
