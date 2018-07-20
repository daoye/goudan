#!/usr/bin/env python
# -*- coding: utf-8 -*-

import select
import socket
import sys
from socketserver import (BaseRequestHandler, ThreadingTCPServer, TCPServer)
from urllib.parse import urlparse


class ProxyRequestHandler(BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.conns = {}
        BaseRequestHandler.__init__(self, request, client_address, server)

    def handle(self):
        self.req_raw = self.request.recv(1024)
        self.data = self.req_raw.splitlines(False)
        command, path, httpversion = bytes.decode(self.data[0]).split(' ')

        if command == 'CONNECT':
            addr = path.split(':', 1)
            s = socket.create_connection(addr)
            res_body = str.encode(
                "%s 200 Connection Established\r\n\r\n" % httpversion)
            self.request.sendall(res_body)

            conns = [self.request, s]
            s_closed = False
            while not s_closed:
                rlist, wlist, xlist = select.select(conns, [], conns)
                if xlist or not rlist:
                    break
                for r in rlist:
                    other = conns[1] if r is conns[0] else conns[0]
                    data = r.recv(8192)
                    if not data:
                        s_closed = True
                        break
                    other.sendall(data)
        else:
            u = urlparse(path)
            origin = (u.scheme, u.netloc)
            ip = socket.gethostbyname(u.hostname)
            port = u.port or 80
            if origin not in self.conns:
                self.conns[origin] = socket.create_connection((ip, port))

            s = self.conns[origin]
            s.sendall(self.req_raw)

            while True:
                packet = s.recv(4096)
                if packet:
                    self.request.sendall(packet)
                else:
                    return


def start():
    port = len(sys.argv) < 2 and 1991 or int(sys.argv[1])
    addr = ('0.0.0.0', port)
    tcpd = ThreadingTCPServer(addr, ProxyRequestHandler)

    print("HTTP server is at: http://%s:%d/" % addr)
    tcpd.serve_forever()


if __name__ == "__main__":
    start()
