import requests
from random import choice
from bs4 import BeautifulSoup


class MyProxies(object):

    def __init__(self):

        self.url = 'http://31f.cn/http-proxy/'
        self.ua_list = [
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
        ]
        self.retry_count = 0
        self.html = ''
        self.proxies_list = []
        self.count = 0

    def get_html(self):

            try:
                self.retry_count += 1
                response = requests.get(url=self.url, headers={'User-Agent': choice(self.ua_list)})
                self.html = response.content.decode('utf-8')
            except Exception as e:
                if self.retry_count > 3:
                    print('请求失败，地址：{}'.format(self.url))
                    return
                print('请求数据失败，正在尝试重新连接...')
                self.get_html()
            else:
                self.retry_count = 0

    def parse_html(self):

        bs = BeautifulSoup(self.html, 'lxml')
        table = bs.select('table')[0]
        total = table.select('tr')
        for x in total:
            if x.select('td'):

                ip = "http://"+x.select('td')[1].text +":"+ x.select('td')[2].text
                self.proxies_list.append(ip)

        return self.proxies_list

    @property
    def random_proxies(self):

        self.get_html()
        ip_list = self.parse_html()
        random_ip = choice(ip_list)
        # print(random_ip)
        return random_ip


if __name__ == '__main__':

    p = MyProxies()
    p.random_proxies
    print(p.random_proxies)
