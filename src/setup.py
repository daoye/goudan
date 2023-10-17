#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='goudan',
    version='0.0.0.1',
    description=(
        '''Goudan(狗蛋)is a tunnel proxy, it's support all tcp proxy(theoretically), such as http,https,socks.
By default, goudan crawl free proxies from some websites. So, you can use it out of box.
For more information visit: https://github.com/daoye/goudan
    '''
    ),
    long_description=open('../README.md').read(),
    author='daoye',
    author_email='daoye.more@outlook.com',
    maintainer='daoye',
    maintainer_email='daoye.more@outlook.com',
    license='MIT License',
    # packages=find_packages(),
    platforms=["all"],
    url='https://github.com/daoye/goudan',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7'
    ],
    install_requires=[
        "aiohttp==3.8.5",
        "lxml==4.9.1",
        "urllib3==1.24.2",
        "pony==0.7.12",
        "requests==2.22.0"
    ],
    py_modules=['goudan']
)
