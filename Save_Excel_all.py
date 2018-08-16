# -*- coding: utf-8 -*-
__FileName__ = 'Save_Excel_all'
__Author__ = 'Liter WU'
__Time__ = '2018/8/16 14:38'

import xlwt


class SaveExcel(object):

    filename = ''
    sheetname = ''
    fields = []

    @classmethod
    def init_work(cls):

        cls.workbook = xlwt.Workbook(encoding='utf-8')
        cls.sheet = cls.workbook.add_sheet(cls.sheetname)
        for idx, f in enumerate(cls.fields):
            cls.sheet.write(0, idx, f)

    @classmethod
    def save(cls, count, *data):
        print('正在写入第{}条数据，请稍后....'.format(count))
        """保存数据"""
        for idx, f in enumerate(data):
            # 写入数据
            cls.sheet.write(count, idx, f)

        # 保存文件
        cls.workbook.save(cls.filename)


if __name__ == '__main__':
    # 测试代码
    SaveExcel.filename = '测试.xls'
    SaveExcel.sheetname = 'test'
    SaveExcel.fields = ['title', 'name', 'age']
    SaveExcel.init_work()

    SaveExcel.save(1, '2', '3', '4')
