# handle url and content get request

import requests
from random import randint
from fake_useragent import UserAgent
import asyncio
from aiohttp.client import ClientSession
# import time
fake = UserAgent()
# t = time.time()
# 用文件的话太麻烦
# with open('useragent.txt', 'r', encoding='utf-8') as f:
#     useragent = [i[:-1] for i in f.readlines()]
#     print(time.time()-t)


# 使用代理的话中间会花很多不必要的时间， 但是如果是异步的话，可以一试
def get_proxies():
    http = requests.get('http://127.0.0.1:8080/get/http').text
    https = requests.get('http://127.0.0.1:8080/get/https').text
    # print({'http': 'http://'+http, 'https': 'https://'+https})
    return {'http': 'http://'+http, 'https': 'https://'+https}


# 堵塞式获取网页内容的接口
def get_content(url):
    useragent = fake.random
    headers = {'User-Agent': useragent}
    # print(time.time()-t)
    # proxies = get_proxies()
    req = requests.get(url, headers=headers)
    # req = requests.get(url, headers=headers, proxies=proxies)
    req.encoding = 'utf-8'
    return req.text


class AsyncGet(object):
    """
    异步获取urls:list的内容
    """
    def __init__(self, urls: "a list of urls",
                 # proxy=False
                 ):
        """
        :type urls: list of urls
        """
        self.urls = urls
        # 在这里用自己开代理服务器有点麻烦。。。还费时间
        # self.proxy = proxy
        # if proxy:
        #     self.open_proxy_pool()
        #     import threading
        #     threading.Thread(target=self.open_proxy_pool).run()
        #     print('Waiting 10s since proxies pool beginning!')
        #     import time
        #     time.sleep(20)
        #     del time

    # @staticmethod
    # def open_proxy_pool():
    #     from scrapy.proxies_mine.Run import main
    #     main.run()

    async def asy_do(self, url):
        async with ClientSession() as req:
            user_agent = fake.random
            kwargs = dict()
            # if self.proxy:
            #     from scrapy.proxies_mine.get_proxies import get_http
            #     kwargs['proxy'] = 'http://'+get_http()
            #     print(kwargs['proxy'])
            # print(**kwargs)
            kwargs['headers'] = {'User-Agent': user_agent}
            async with req.get(url=url, **kwargs) as response:
                # print('req', time.time() - t)
                text = await response.text()
        return text

    # 提供异步获取网页内容的接口，最好500个以上
    @property
    def get_content(self):
        loop = asyncio.get_event_loop()
        asyncio.Semaphore(300)
        tasks = []
        for url in self.urls:
            task = asyncio.ensure_future(self.asy_do(url))
            tasks.append(task)
        contents = loop.run_until_complete(asyncio.gather(*tasks))
        # print(time.time() - t)
        # 返回的是网页内容的集合
        return contents


if __name__ == '__main__':
    req = get_content('http://www.baidu.com')
    req1 = get_content('http://www.sohu.com')
    # print(time.time()-t)
    req2 = AsyncGet(urls=['http://www.baidu.com', 'http://www.sohu.com'],
                    # proxy=True
                    )
    print(req2.get_content)
    # print(time.time() - t)
