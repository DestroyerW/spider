# -*- coding: utf-8 -*-
__FileName__ = 'SDMan'
__Author__ = 'Liter WU'
__Time__ = '2018/8/24 10:45'

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from YDMDemo import YDMHttp

driver = webdriver.Firefox()

url = 'http://jw.shengda.edu.cn/jwweb/default.aspx'
driver.get(url=url)
driver.find_element_by_id('m14').click()
time.sleep(2)
driver.switch_to.frame(driver.find_element_by_css_selector('iframe'))

# with open('1.html', 'w', encoding='utf-8') as f:
#     f.write(driver.page_source)


driver.find_element_by_class_name('tx1').clear()
driver.find_element_by_id('txt_asmcdefsddsd').send_keys('201505040152')
driver.find_element_by_id('txt_pewerwedsdfsdff').send_keys('Devil2233')
driver.find_element_by_id('txt_pewerwedsdfsdff').send_keys(Keys.TAB)
captcha = driver.find_element_by_id('imgCode')
captcha.screenshot('getimage.png')

ydm = YDMHttp()
uid = ydm.login()
if uid > 0:
    print('云打码登录成功...')
    balance = ydm.balance()
    print('账户余额:{}'.format(balance))

    cid, result = ydm.decode('getimage.png', 3000, 30)
    if cid > 0:
        driver.find_element_by_id('txt_sdertfgsadscxcadsads').send_keys(result)
        driver.find_element_by_id('txt_sdertfgsadscxcadsads').send_keys(Keys.ENTER)
        time.sleep(1)
        try:
            if result:
                print('登录成功！')
            else:
                print('登录失败！重试！')
                driver.find_element_by_id('txt_sdertfgsadscxcadsads').send_keys(Keys.ENTER)

                ydm.report(cid)

        except Exception as e:
            driver.find_element_by_id('txt_sdertfgsadscxcadsads').send_keys(Keys.ENTER)





