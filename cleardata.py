# -*- coding: utf-8 -*-
__FileName__ = 'cleardata'
__Author__ = 'Liter WU'
__Time__ = '2018/8/9 11:48'

import re


class Clear(object):

    @staticmethod
    def string_clear(string):

        lable_clear = re.compile(r'<.*?>', re.S)
        string = re.sub(lable_clear, '', string)
        string = string.strip()
        return string

    @staticmethod
    def space_clear(string):
        space_clear = string.strip()
        return space_clear

    @staticmethod
    def group(string):

        str_clear = re.compile(r'<p>(.*?)</p>|<div>(.*?)</div>', re.S)
        string = re.findall(str_clear, string)

        if not string[1][0] == '':
            tran_name = string[1][0]
            movie_title = string[2][0]
            movie_s = string[3][0]
            movie_origin = string[4][0]
            movie_cat = string[5][0]
            movie_lan = string[6][0]
            movie_sub = string[7][0]
            movie_date = string[8][0]
            movie_grade = string[9][0]
            movie_format = string[10][0]
            movie_measure = string[11][0]
            movie_size = string[12][0]
            movie_len = string[13][0]
            movie_director = string[14][0]
            movie_starring = string[15][0]
            movie_intro = string[-3][0]

            return tran_name, movie_title, movie_s, movie_origin, movie_cat, movie_lan, movie_sub, movie_date, movie_grade, movie_format, movie_measure, movie_size, movie_len, movie_director, movie_starring, movie_intro

        else:

            tran_name = string[1][1]
            movie_title = string[2][1]
            movie_s = string[3][1]
            movie_origin = string[4][1]
            movie_cat = string[5][1]
            movie_lan = string[6][1]
            movie_sub = string[7][1]
            movie_date = string[8][1]
            movie_grade = string[9][1]
            movie_format = string[10][1]
            movie_measure = string[11][1]
            movie_size = string[12][1]
            movie_len = string[13][1]
            movie_director = string[14][1]
            movie_starring = string[15][1]
            movie_intro = string[-3][1]


            return tran_name, movie_title, movie_s, movie_origin, movie_cat, movie_lan, movie_sub, movie_date, movie_grade, movie_format, movie_measure, movie_size, movie_len, movie_director, movie_starring, movie_intro

