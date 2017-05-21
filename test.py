# -*- coding: utf-8 -*-
# @Time    : 2017/5/21 下午 04:30
# @Author  : Yuhsuan
# @File    : test.py
# @Software: PyCharm Community Edition

from nltk.corpus import reuters
fileid = 'training/3386'
print(" ".join(reuters.words(fileids=fileid)))
print(reuters.categories(fileids=fileid))


import tfidf as ti
print(ti.tf('Portland',fileid))