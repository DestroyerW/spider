# -*- coding: utf-8 -*-
__FileName__ = 'Save_DB_all'
__Author__ = 'Liter WU'
__Time__ = '2018/8/16 14:35'

import sqlite3


class SaveModel(object):

    #  类属性
    dbname = ''
    #  表名
    tablename = ''
    #  字段名
    fileds = []

    def __init__(self, *data):
        self.conn = None
        self.cursor = None
        self.data = data

    def connect_sql(self):
        """链接数据库"""
        # 根据dbname创建数据库
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

    def close_sql(self):
        """关闭数据库"""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def create_table(self):
        """创建表"""
        # 1.链接数据库
        self.connect_sql()

        s = ''
        for f in self.fileds:
            s1 = ', ' + f + ' CHAR'
            s += s1

        s += ')'
        # 拼接完整的sql语句
        sql = 'CREATE TABLE IF NOT EXISTS {}(id INTEGER PRIMARY KEY '.format(self.tablename)+s

        # 2.执行sql语句
        self.cursor.execute(sql)

        # 3.关闭数据库
        self.close_sql()

    def save(self):

        # 1.打开数据库
        self.connect_sql()

        s = ''
        v = ''
        for f in self.fileds:

            s1 = f + ','
            v1 = '"%s",'
            s += s1
            v += v1
        s = s[:-1]
        # 拼接完整的值字符串
        v = v[:-1] % self.data

        # 2.准备sql语句
        sql = """INSERT INTO {}(""".format(self.tablename) + s + """)VALUES({})""".format(v)

        # 3.执行
        self.cursor.execute(sql)

        # 4.关闭数据库
        self.close_sql()


if __name__ == '__main__':
    # 测试代码
    SaveModel.dbname = 'Test.db'
    SaveModel.tablename = 'test'
    SaveModel.fileds = ['title', 'name', 'age', 'phone', 'email', 'adreee']
    s = SaveModel('1','2','3','4','5','6')
    s.create_table()
    s.save()

