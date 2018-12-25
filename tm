# -*- coding: utf-8 -*-
__FileName__ = 'TM'
__Author__ = 'Liter WU'
__Time__ = '2018/8/23 19:55'

from selenium import webdriver
import time

driver = webdriver.Firefox()

driver.get('https://www.tmall.com/')
time.sleep(1)

input_ = driver.find_element_by_tag_name('input')
select = input('请输入要搜索的商品:')
input_.send_keys('{}'.format(select))
driver.find_element_by_tag_name('button').click()

while True:
    time.sleep(1)
    for x in range(1, 8, 1):
        j = x/10
        js = 'document.documentElement.scrollTop = document.documentElement.scrollHeight * {}'.format(j)
        driver.execute_script(js)
        time.sleep(0.5)

    divs = driver.find_elements_by_class_name('product')
    print(len(divs))

    for div in divs:
        print(div.text)
    try:
        driver.find_element_by_class_name('ui-page-next').click()
    except Exception as e:
        print('没有下一页了')
        break

time.sleep(10)
driver.quit()
