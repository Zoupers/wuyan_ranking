# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File Name：     ProxyManager.py
   Description :
   Author :       JHao
   date：          2016/12/3
-------------------------------------------------
   Change Activity:
                   2016/12/3:
-------------------------------------------------
"""
# __author__ = 'JHao'

import random

from scrapy.proxies_mine.Util import EnvUtil
from scrapy.proxies_mine.DB.DbClient import DbClient
from scrapy.proxies_mine.Util.GetConfig import config
from scrapy.proxies_mine.Util.LogHandler import LogHandler
from scrapy.proxies_mine.Util.utilFunction import verifyProxyFormat
from scrapy.proxies_mine.ProxyGetter.getFreeProxy import GetFreeProxy


class ProxyManager(object):
    """
    ProxyManager
    """

    def __init__(self, mode):
        self.mode = mode
        self.db = DbClient(mode)
        self.raw_proxy_queue = 'raw_proxy'
        self.log = LogHandler('proxy_manager')
        self.useful_proxy_queue = 'useful_proxy'

    def refresh(self):
        """
        fetch proxy into Db by ProxyGetter/getFreeProxy.py
        :return:
        """
        self.db.changeTable(self.raw_proxy_queue)
        for proxyGetter in config.proxy_getter_functions:
            # fetch
            try:
                self.log.info("{func}: fetch proxy start".format(func=proxyGetter))
                for proxy in getattr(GetFreeProxy, proxyGetter.strip())():
                    # 直接存储代理, 不用在代码中排重, hash 结构本身具有排重功能
                    proxy = proxy.strip()
                    if proxy and verifyProxyFormat(proxy):
                        self.log.info('Mode:{mode} {func}: fetch proxy {proxy}'.format(mode=self.mode, func=proxyGetter, proxy=proxy))
                        self.db.put(proxy)
                    else:
                        self.log.error('Mode:{mode} {func}: fetch proxy {proxy} error'.format(mode=self.mode, func=proxyGetter, proxy=proxy))
            except Exception as e:
                self.log.error("Mode:{mode} {func}: fetch proxy fail".format(mode=self.mode, func=proxyGetter))
                continue

    def get_http(self):
        """
        return a useful proxy (http)
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        item_dict = self.db.getAll()
        if item_dict:
            if EnvUtil.PY3:
                return random.choice(list(item_dict.keys()))
            else:
                return random.choice(item_dict.keys())
        return None
        # return self.db.pop()

    def get_https(self):
        """
        return a useful proxy (https)
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        item_dict = self.db.getAll()
        if item_dict:
            if EnvUtil.PY3:
                return random.choice(list(item_dict.keys()))
            else:
                return random.choice(item_dict.keys())
        return None
        # return self.db.pop()
        

    def delete(self, proxy):
        """
        delete proxy from pool
        :param proxy:
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        self.db.delete(proxy)

    def getAll(self):
        """
        get all proxy from pool as list
        :return:
        """
        self.db.changeTable(self.useful_proxy_queue)
        item_dict = self.db.getAll()
        if EnvUtil.PY3:
            return list(item_dict.keys()) if item_dict else list()
        return item_dict.keys() if item_dict else list()

    def getNumber(self):
        self.db.changeTable(self.raw_proxy_queue)
        total_raw_proxy = self.db.getNumber()
        self.db.changeTable(self.useful_proxy_queue)
        total_useful_queue = self.db.getNumber()
        return {'raw_proxy': total_raw_proxy, 'useful_proxy': total_useful_queue}


if __name__ == '__main__':
    pp = ProxyManager('http')
    pp2 = ProxyManager('https')
    pp.refresh()
    pp2.refresh()
