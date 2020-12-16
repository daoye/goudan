import os
import hashlib
import shutil
import tempfile
import logging
import asyncio
import functools
import time
from multiprocessing import Pool
from subprocess import PIPE, Popen

import requests
import setting

from core import PATH, FILE
from core.data import db_bind, ProxyItem
from pony.orm import *

_pool = None

def launch():
    logging.info('Detected [%d] plugins.' % len(setting.plugins))
    global _pool
    _pool = Pool(1)
    #  _pool.apply_async(_run_process, ("`".join(setting.plugins),))
    _pool.apply(_run_process, ("`".join(setting.plugins),))


def stop():
    global _pool
    if _pool:
        _pool.terminate()


def _run_process(items):
    logging.basicConfig(level=setting.log_level,
                        format="%(asctime)s - %(levelname)s - %(message)s")

    h = Hosting(items)
    h.start()


class Hosting():
    def __init__(self, items):
        self.names = items.split('`')
        self.plugin_dir = FILE('plugins')
        self.plugins = []
        self.loop = asyncio.get_event_loop()

    def start(self):
        if not os.path.exists(self.plugin_dir):
            os.mkdir(self.plugin_dir)
            with open(os.path.join(self.plugin_dir, '__init__.py'), 'wb') as r:
                r.write(b'# this is plugin dir.')

        self._load()

        if not len(self.plugins):
            exit(0)

        self._run_plugin()
        self._run_check()

        logging.info('Plugin host launched.')
        self.loop.run_forever()

    def _run_plugin(self):
        for p in self.plugins:
            try:
                p.start(self)
            except:
                logging.exception('[%s] run failed!' % p)

        if self.loop.is_running():
            self.loop.call_later(
                15 * 60, functools.partial(self._run_plugin, self))

    def _run_check(self):
        logging.info('Start checking proxies availability ...')
        procs = []
        valid_size = 0
        results = []
        with db_session:
            items = ProxyItem.select()[:]
            for p in items:
                procs.append(self._valid_bycurl(p))
            results = self.loop.run_until_complete(asyncio.gather(*procs))

            
            for i in range(0, len(items)):
                isok = results[i]
                d = items[i]
                if isok:
                    d.isok = True
                    d.validCount = 0
                    valid_size += 1
                else:
                    d.isok = False
                    d.validCount += 1
                    if d.validCount > 2:
                        d.delete()


        logging.info('Valid done. %s proxies are available.' % valid_size)
        if self.loop.is_running():
            self.loop.call_later(60, functools.partial(self._run_check, self))

    def _load(self):
        for x in self.names:
            try:
                md5 = hashlib.md5(x.encode('utf8')).hexdigest()
                filename = md5 + '.py'
                fullpath = os.path.join(self.plugin_dir, filename)

                #  if not os.path.exists(fullpath):
                if x.startswith('http'):
                    self._download_remote_plugin(fullpath, x)
                else:
                    shutil.copy(x, fullpath)

                p = self._load_cls(md5)
                self.plugins.append(p())

                logging.info('Plugin load completed [%s]' % x)
            except:
                logging.exception("Plugin load failed [%s]" % x)

    def _download_remote_plugin(self, filename, url):
        r = requests.get(url)
        r.raise_for_status()

        with open(filename, 'wb') as f:
            f.write(r.content)

    def _load_cls(self, name):
        module_name = 'plugins.%s' % name
        cls_name = 'Plugin'
        module = __import__(module_name, globals(), locals(), [cls_name], 0)
        return getattr(module, cls_name)

    async def _valid_bycurl(self, item):
        cmd = 'curl -L -x %s://%s:%d --connect-timeout 5 https://ifconfig.me' % (item.protocol, item.host, item.port)

        proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, _ = await proc.communicate()

        val = item.host in stdout.decode()
        if val:
            logging.info('[OK] %s://%s:%s' %
                         (item.protocol, item.host, item.port))
        else:
            logging.debug("[Invalid] %s://%s:%s" %
                          (item.protocol, item.host, item.port))
        return val


    async def _valid_socks(self, item):
        try:
            _, w = await asyncio.open_connection(item.host, item.port)
            w.close()
            logging.info('ok: %s://%s:%s' %
                         (item.protocol, item.host, item.port))
            return True
        except:
            logging.debug("invalid: %s://%s:%s" %
                          (item.protocol, item.host, item.port))

        return False

    async def _valid_http(self, item):
        target_url = 'https://www.ipip.net/'
        proxy_addr = '%s://%s:%s' % (item.protocol, item.host, item.port)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                        AppleWebKit/537.36 (KHTML, like Gecko) \
                        Chrome/79.0.3945.130 Safari/537.36'
        }
        try:
            req = urllib3.ProxyManager(proxy_addr)
            res = req.request('GET', target_url, headers=headers, timeout=5)
            isok = res.status == 200
            if isok:
                logging.info('ok: %s://%s:%s' %
                             (item.protocol, item.host, item.port))
            return isok
        except Exception as e:
            logging.debug("invalid: %s://%s:%s" %
                          (item.protocol, item.host, item.port))

        return False
