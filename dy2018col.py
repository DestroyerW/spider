# -*- coding: utf-8 -*-
__FileName__ = 'dy2018col'
__Author__ = 'Liter WU'
__Time__ = '2018/8/9 9:54'

import xlwt
from urllib import request
from random import choice
import re
import sqlite3
from cleardata import Clear


class Dy2018(object):

    def __init__(self):

        self.url = 'https://www.dy2018.com/html/gndy/dyzz/index.html'
        self.html = ''
        self.headers = self.ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 UBrowser/4.0.3214.0 Safari/537.36'
        ]
        self.download = ''
        self.retry_count = 0
        self.count = 0
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.workbook.add_sheet('dy_data')

    def get_html(self, url):

        # req = request.Request(url=url, headers=self.headers)
        # reponse = request.urlopen(req)
        # self.html = reponse.read().decode('gb2312', 'ignore')

        req = request.Request(url=url, headers={
            'User-Agent': choice(self.ua_list)
        })
        try:
            self.retry_count += 1
            response = request.urlopen(req)
            self.html = response.read().decode('gb2312', 'ignore')
        except Exception as e:
            if self.retry_count > 3:
                print('请求失败，地址：{}'.format(url))
                return
            print('请求数据失败，正在尝试重新连接...')
            self.get_html(url)
        else:
            self.retry_count = 0

    def parse_html(self):

        # 获取每一页的电影的详情地址
        detail_pattern = re.compile(r'<td height="26">.*?<a href="(.*?)"', re.S)
        detail_rs = re.findall(detail_pattern, self.html)
        # print(detail_rs)
        for d in detail_rs:
            # print(d)
            self.url = 'https://www.dy2018.com' + d
            # print(self.url)

            # 从电影的详情地址爬取信息
            self.get_html(self.url)
            # print(self.html)
            movie_info_pat = re.compile(r'<!--Content Start-->(.*?)<!--xunleiDownList Start-->.*?<td style="WORD-WRAP: break-word".*?<a href="(.*?)"', re.S)
            movie_info = re.findall(movie_info_pat, self.html)
            # print(movie_info)
            for m in movie_info:

                movie_d = m[0]
                movie_d = Clear.group(movie_d)
                print(movie_d)

                self.download = m[1]
                print('下载地址为:{}'.format(self.download))

                self.save_data(movie_d[0], movie_d[1], movie_d[2], movie_d[3], movie_d[4], movie_d[5], movie_d[6], movie_d[7], movie_d[8], movie_d[9], movie_d[10], movie_d[11], movie_d[12], movie_d[13], movie_d[14], movie_d[15], self.download)

    def write_to_excel(self, idx, data):

        # print(idx, data)
        self.sheet.write(self.count, idx, data)

    def save_data(self, *args):

        for idx, data in enumerate(args):

            self.write_to_excel(idx, data)

        self.workbook.save('电影天堂.xls')

        connect = sqlite3.connect('dy2018.db')
        sql = "CREATE TABLE IF NOT EXISTS dy2018(id integer primary key ,tran_name CHAR ,movie_title CHAR, movie_s CHAR, movie_origin CHAR,movie_cat char ,movie_lan CHAR,movie_sub char ,movie_date char,movie_grade char,movie_format char,movie_measure char,movie_size char,movie_len char,movie_director char,movie_starring char,movie_intro char ,download char )"
        cursor = connect.cursor()
        cursor.execute(sql)
        insert_sql = "insert into dy2018(tran_name, movie_title, movie_s, movie_origin, movie_cat, movie_lan, movie_sub, movie_date, movie_grade, movie_format, movie_measure, movie_size, movie_len, movie_director, movie_starring, movie_intro, download)values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % args
        cursor.execute(insert_sql)
        connect.commit()

        cursor.close()
        connect.close()
        self.count += 1

    def run(self):

        # 获取最新电影的每一页地址
        self.get_html(self.url)
        page_pattern = re.compile(r"<option value='(.*?)'", re.S)
        page_rs = re.findall(page_pattern, self.html)
        # print(page_rs)
        for p in page_rs:
            # print(p)
            url = 'https://www.dy2018.com' + p
            self.get_html(url)
            self.parse_html()


p = Dy2018()
p.run()
