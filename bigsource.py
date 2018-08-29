# -*- coding: utf-8 -*-
__FileName__ = 'bigsource'
__Author__ = 'Liter WU'
__Time__ = '2018/8/27 21:50'

import requests
from random import choice
from bs4 import BeautifulSoup
import xlwt


class BigSource(object):

    def __init__(self):

        self.url = 'http://www.zuida.me/?m=vod-type-id-1.html'
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
        self.title = ''
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.workbook.add_sheet('video')
        self.create_excel()
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
        total = bs.select('.xing_vb4 a')
        # print(total)
        for x in total:
            self.title = x.text
            # print(x.text)
            detail_url = 'http://www.zuida.me'+x.attrs['href']
            # print(detail_url)
            self.detail_html(detail_url)

    def detail_html(self, detail_url):

        self.url = detail_url
        self.get_html()
        bs = BeautifulSoup(self.html, 'lxml')
        score = bs.select('.vodInfo label')[0].text
        # print(score)
        detail = bs.select('.vodinfobox')[0].text.strip()
        # print(detail)

        download = bs.select('#play_2 ul li input')
        download = download[-1].attrs['value']
        # print(download)
        self.save_data(self.title, score, detail, download)

    def create_excel(self):

        self.sheet.write(0, 0, '名称')
        self.sheet.write(0, 1, '评分')
        self.sheet.write(0, 2, '详情')
        self.sheet.write(0, 3, '下载链接')

    def save_data(self, *args):

        self.count += 1

        print('正在保存:{}'.format(args[0]))

        for idx, data in enumerate(args):

            self.sheet.write(self.count, idx, data)

        self.workbook.save('BigSource.xls')

    def run(self):

        self.get_html()
        bs = BeautifulSoup(self.html, 'lxml')
        last = bs.select('.pagelink_a')[-1].attrs['href']
        total = last.split('-')[-1].split('.')[0]
        # print(total)
        for p in range(1, int(total)+1):
            self.url = 'http://www.zuida.me/?m=vod-type-id-1-pg-{}.html'.format(p)
            self.get_html()
            self.parse_html()


if __name__ == '__main__':

    p = BigSource()
    p.run()


