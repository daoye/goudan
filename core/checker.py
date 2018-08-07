#!/usr/bin/env python
# -*- coding: utf-8 -*-


import asyncio

import aiohttp

import setting
from data import userAgent


async def __socket_valid(item):
    if item['type'] != setting.proxy_type:
        item['success'] = False
        return True

    try:
        _, w = await asyncio.open_connection(item['host'], item['port'])
        w.close()
        print('%s:%s ok!' % (item['host'], item['port']))
        item['success'] = True
    except Exception as e:
        print(e)
        item['success'] = False

    return True


# async def __http_https_check(item):
#     if item['type'] != setting.proxy_type:
#         item['success'] = False
#         return True

#     headers = {
#         'User-Agent': userAgent.agents[0]
#     }
#     url = None
#     try:
#         if item['type'] == 'https':
#             if item['loc'] == 'cn':
#                 url = 'https://ip.cn/'
#             else:
#                 url = 'https://www.whatismyip.com/'
#         else:
#             if item['loc'] == 'cn':
#                 url = 'http://2018.ip138.com/ic.asp'
#             else:
#                 url = 'http://www.whatsmyip.org/'

#         html = None
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url, headers=headers, proxy='%s://%s:%s' % (item['type'], item['host'], item['port'])) as response:
#                 html = await response.text()

#         item['success'] = html.find(item['host']) != -1
#         if item['success']:
#             print('%s:%s ok!' % (item['host'], item['port']))
#     except Exception as e:
#         print(e)
#         item['success'] = False

#     return True


def valid(proxies):
    tasks = [__socket_valid(p) for p in proxies]
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(*tasks))

    print('%s proxies has valid!' % (len(proxies)))
