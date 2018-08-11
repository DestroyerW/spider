# -*- coding: utf-8 -*-
__FileName__ = 'chuangshi'
__Author__ = 'Liter WU'
__Time__ = '2018/8/10 14:08'

import re
from urllib import request
from random import choice
import sqlite3
import xlwt


class CS_Novel(object):

    def __init__(self):

        self.url = 'http://chuangshi.qq.com/bk/'
        self.ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
        ]
        self.html = ''
        self.title = ''
        self.type = ''
        self.count = 0
        self.retry_count = 0
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.workbook.add_sheet('cs_data')
        self.create_excel()

    def create_excel(self):

        self.sheet.write(0, 0, '小说名称')
        self.sheet.write(0, 1, '小说类型')
        self.sheet.write(0, 2, '小说简介')
        self.sheet.write(0, 3, '作品标签')
        self.sheet.write(0, 4, '阅文点击')
        self.sheet.write(0, 5, '总人气')
        self.sheet.write(0, 6, '总推荐')
        self.sheet.write(0, 7, '阅文点击（月）')
        self.sheet.write(0, 8, '月人气')
        self.sheet.write(0, 9, '月推荐')
        self.sheet.write(0, 10, '阅文点击（周）')
        self.sheet.write(0, 11, '周人气')
        self.sheet.write(0, 12, '周推荐')
        self.sheet.write(0, 13, '总字数')
        self.sheet.write(0, 14, '评论数')
        self.sheet.write(0, 15, '连载状态')

    def get_html(self, url):

        req = request.Request(url=url, headers={
            'User-Agent': choice(self.ua_list)
        })
        try:
            self.retry_count += 1
            response = request.urlopen(req)
            self.html = response.read().decode('utf-8')
        except Exception as e:
            if self.retry_count > 3:
                print('请求失败，地址：{}'.format(url))
                return
            print('请求数据失败，正在尝试重新连接...')
            self.get_html(url)
        else:
            self.retry_count = 0

    def parse_html(self):

        detail_pattern = re.compile(r'<tr><td>.*?<a href=.*?">(.*?)</a>.*?<a.*?href="(.*?)".*?blank">(.*?)</a>', re.S)
        detail_rs = re.findall(detail_pattern, self.html)
        # print(detail_rs)
        for d in detail_rs:
            # print(d[0])
            self.type = (d[0])
            self.title = (d[2])
            # print(d[2])
            self.url = d[1]

            self.get_html(self.url)
            # print(self.html)
            info_pat = re.compile(
                r'<div class="info"><p.*?>(.*?)</p></div>.*?<div class="tags">(.*?)</div>.*?</td></tr><tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr><tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr><tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr><tr><td>(.*?)</td><td>(.*?)</td><td>(.*?)</td></tr>',
                re.S)
            results = re.findall(info_pat, self.html)
            # print(results)
            title = self.title
            type = self.type
            intro = results[0][0].replace('</p><p>', ' ')
            labl = results[0][1].replace('\r\n', ' ')
            click_num = results[0][2]
            peop = results[0][3]
            tot = results[0][4]
            cli_m = results[0][5]
            peop_m = results[0][6]
            tot_m = results[0][7]
            cli_w = results[0][8]
            peop_w = results[0][9]
            tot_w = results[0][10]
            toa_w = results[0][11]
            arg = results[0][12].replace('<span id="novelInfo_commentCount">0</span>', ' ')
            lia = results[0][13].replace('<span class="red2">', ' ')
            lia = lia.replace('</span>', ' ')

            self.save_data(title, type, intro, labl, click_num, peop, tot, cli_m, peop_m, tot_m, cli_w, peop_w, tot_w, toa_w, arg, lia)

    def write_to_excel(self, idx, data):

        # print(idx, data)
        self.sheet.write(self.count, idx, data)

    def save_data(self, *args):

        self.count += 1

        print('正在保存第{}本小说：{}'.format(self.count, args[0]))

        for idx, data in enumerate(args):

            self.write_to_excel(idx, data)

        self.workbook.save('创世小说.xls')

        connect = sqlite3.connect('cs.db')
        sql = "CREATE TABLE IF NOT EXISTS cs(id integer primary key ,title CHAR ,type CHAR, intro CHAR, labl CHAR,click_num char ,peop CHAR,tot char ,cli_m char,peop_m char,tot_m char,cli_w char,peop_w char,tot_w char,toa_w char,arg char,lia char )"
        cursor = connect.cursor()
        cursor.execute(sql)
        insert_sql = "insert into cs(title, type, intro, labl, click_num, peop, tot, cli_m, peop_m, tot_m, cli_w, peop_w, tot_w, toa_w, arg, lia)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % args
        cursor.execute(insert_sql)
        connect.commit()

        cursor.close()
        connect.close()

    def run(self):

        self.get_html(self.url)
        page_pattern = re.compile(r'<em>页/(.*?)页</em>', re.S)
        page_total = re.findall(page_pattern, self.html)
        # print(page_total)
        for x in range(1, int(page_total[0])):
            print('正在获取第%s页数据，请稍后....' % x)
            url = 'http://chuangshi.qq.com/bk/p/{}.html'.format(x)
            # print(url)
            self.get_html(url)
            self.parse_html()

        self.workbook.save('创世小说.xls')


p = CS_Novel()
p.run()

