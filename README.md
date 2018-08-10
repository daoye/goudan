# goudan(狗蛋)

Goudan(狗蛋)is a tunnel proxy, it's support all tcp proxy(theoretically), such as http,https,socks.
By default, goudan crawl free proxies from some websites. So, you can use it out of box.

## Why do this

When I develop a spider to crawl some web sites, most time they have some defense measures.

So, I must change my IP to crawl it at a moment.

The best way is set a proxy address for a web requests libray, such as "Requests","urlib", "aiohttp" and so on.

But, I need write those code in every project. I want't to do this.

This why I start this project.

## How to use

### Use by docker(Recommend)

```bash
docker run -p 1991:1991 -d --restart always --name goudan daoye/goudan
```

or

```bash
docker run -p 1991:1991 -d --restart always --name goudan daoye/goudan --log_level 10 -r 10 -i 60 -t socks
```

If you want see some help documents:

```bash
docker run daoye/goudan -h
```

### From source(need python3.7)

```bash
git clone https://github.com/daoye/goudan.git
git checkout develop
cd goudan
python3 main.py
```

The best way is use virtualenv.

## Add your proxies

If you have some other proxies, you can add them  to the proxy pool.

To do this, you must create a new spider. For example:

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-


class MySpider():
    def run(self):
        return [
            {"host": "127.0.0.1", 'port': 1080, 'type': 'socks', 'loc': 'jp'},
            {"host": "127.0.0.1", 'port': 1087, 'type': 'http', 'loc': 'jp'}
        ]
```

This spider return an array include some proxies.

Anyway, you can collect some proxies from other web site:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-


from lxml import etree
from spiders.baseSpider import BaseSpider
import logging

class MySpider(BaseSpider):
    def __init__(self):
        BaseSpider.__init__(self)
        self.urls = [
            'http://www.xxx.xxx/'
        ]

    def _parse(self, results, text):
        # parse the result
        # then add it to "results"

        for r in rows:
            results.append({
                'host': r.ip,
                'port': r.port,
                'type': 'http',
                'loc': 'cn'
            })
```

A proxy is a dictionary, it has these key:

host: The ip address.

port: The port, __it must an integer__.

type: The proxy's type, it can be: __http,https,http/https,socks__ .

loc:   Location of proxy(not imoprtant, use for feature) .

__When you create a spider, you must add it to the "setting.py"__

Open file "setting.py",  then find the "spiders" variable, add you spider in it:

```python
spiders = [
    ......

    'spiders.mySpider.MySpider'  # This is you spider.
]
```

## The end

Enjoy!