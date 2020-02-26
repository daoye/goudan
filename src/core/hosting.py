import requests
import os
import hashlib
import shutil
import tempfile
import logging
import asyncio
import setting
import functools
import time

from multiprocessing import Process
from core import PATH, FILE
from core.data import db_bind, ProxyItem
from pony.orm import *

__host_process = None

def launch():
    logging.info('Plugin host launched.')
    global __host_process
    __host_process = Process(target=_start_host_process, args=("`".join(setting.plugins),))
    __host_process.daemon = True
    __host_process.start()

def stop():
    global __host_process
    while __host_process.is_alive():
        try:
            __host_process.kill()
        except:
            pass
        time.sleep(0.1)

    try:
        __host_process.close()
    except:
        pass

def _start_host_process(items):
    logging.basicConfig(level=setting.log_level, format="%(asctime)s - %(levelname)s - %(message)s")

    db_bind()

    h = Hosting(items)
    h.start()

class Hosting():
    def __init__(self, items):
        self.list = items.split('`')
        self.plugin_dir = FILE('plugins')
        self.plugins = []
        self.loop = asyncio.get_event_loop()

    def start(self):
        if not os.path.exists(self.plugin_dir):
            os.mkdir(self.plugin_dir)
            with open(os.path.join(self.plugin_dir, '__init__.py') , 'wb') as r:
                r.write(b'# this is plugin dir.')
        self._load()

        self._run_plugin()
        self._run_check()

        self.loop.run_forever()


    def _run_plugin(self):
        for p in self.plugins:
            try:
                p.start(self)
            except:
                logging.exception('[%s] run failed!' % p)

        if self.loop.is_running():
            self.loop.call_later(15 * 60, functools.partial(self._run_plugin, self))

    def _run_check(self):
        logging.info('Start checking proxies availability ...')
        procs = []
        items =  ProxyItem.select()[:]
        for p in items:
            procs.append(self._valid_socks(p))

        results = self.loop.run_until_complete(asyncio.gather(*procs))
        
        with db_session:
            for i in range(0, len(items)):
                isok = results[i]
                d = items[i]
                if isok:
                    d.isok=True
                else:
                    d.isok=False
                    d.validCount += 1

        logging.info('Proxies availability check done ...')
        if self.loop.is_running():
            self.loop.call_later(60, functools.partial(self._run_check, self))


    def _load(self):
        m = hashlib.md5()
        for x in self.list:
            logging.info('Loading [%s]' % x)

            try:
                m.update(bytes(x, 'utf8'))
                md5 = m.hexdigest()
                filename = md5 + '.py'
                fullpath = os.path.join(self.plugin_dir, filename)

                if not os.path.exists(fullpath):
                    if x.startswith('http'):
                        self._download_remote_plugin(fullpath, x)
                    else:
                        shutil.copy(x, fullpath)
                p = self._load_cls(md5)
                self.plugins.append(p())

                logging.info('Load completed [%s]' % x)
            except:
                logging.exception("Load failed [%s]" % x)


    def _download_remote_plugin(self, filename, url):
        file_name = os.path.join(tempfile.gettempdir(), filename)
        r = requests.get(url)
        r.raise_for_status()
        with open(file_name, 'wb') as f:
            f.write(r.content)


    def _load_cls(self, name):
        # sep = name.split('.')
        # module_name = '.'.join(sep[0:-1])
        # cls_name = sep[-1]
        module_name = 'plugins.%s' % name
        cls_name='Plugin'
        module = __import__(module_name, globals(), locals(), [cls_name], 0)
        return getattr(module, cls_name)



    async def _valid_socks(self, item):
        try:
            _, w = await asyncio.open_connection(item.host, item.port)
            w.close()
            logging.info('ok: %s://%s:%s' % (item.protocol, item.host, item.port))
            return True
        except Exception as e:
            logging.debug("invalid: %s://%s:%s" % (item.protocol, item.host, item.port))

        return False

    async def _valid_http(self, item):
        target_url = 'https://www.ipip.net/'
        proxy_addr = '%s://%s:%s' % (item.protocol, item.host, item.port)
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
        }
        try:
            req = urllib3.ProxyManager(proxy_addr)
            res = req.request('GET', target_url, headers=headers, timeout=5)
            isok = res.status == 200
            if isok:
                logging.info('ok: %s://%s:%s' % (item.protocol, item.host, item.port))
            return isok
        except Exception as e:
            logging.debug("invalid: %s://%s:%s" % (item.protocol, item.host, item.port))

        return False