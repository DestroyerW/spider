# -*- coding: utf-8 -*-
__FileName__ = 'wzry'
__Author__ = 'Liter WU'
__Time__ = '2018/8/15 12:00'

import requests
import json
import os

# 读取本地json文件
with open('D:\KingGlory\herolist.json', 'r', encoding='utf-8') as f:
    jsonFile = json.load(f)

# 从官网爬取json
# response = requests.get(url='http://pvp.qq.com/web201605/js/herolist.json')
# jsonFile = response.json()

# 提取json文件
for m in range(len(jsonFile)):

    # 数字名字
    ename = jsonFile[m]['ename']
    # 汉语名字
    cname = jsonFile[m]['cname']
    # 切割后是字典 列表形式
    skinName = jsonFile[m]['skin_name'].split('|')
    # 计算每个英雄的皮肤多少
    print(skinName)
    skinNumber = len(skinName)
    print(skinNumber)
    # 此次循环是为了下载图片  构造图片网址
    for bigskin in range(1, skinNumber + 1):
        # 指定图片网址
        urlPicture = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/' + str(ename) + '/' + str(
            ename) + '-bigskin-' + str(bigskin) + '.jpg'
        # 获取图片信息  图片都是二进制  content就是获取二级制信息
        picture = requests.get(urlPicture).content
        # 保存信息 保存图片
        if not os.path.exists('D:\KingGlory\imgs'):
            os.mkdir('D:\KingGlory\imgs')
        with open('D:\KingGlory\imgs\\' + cname + skinName[bigskin - 1] + '.jpg', 'wb') as f:
            f.write(picture)
