# -*- coding: utf-8 -*-
# @Time    : 2017/5/21 下午11:54
# @Author  : Yuhsuan
# @File    : cos.py
# @Software: PyCharm Community Edition
# 計算相似度

import codecs
import numpy as np
import csv
from scipy import spatial


class cos():
    def __init__(self):
        self.raw_matrix=np.array
        self.word_count=0
        self.sg_count=0

    def readfile(self,input):
        csv = np.genfromtxt(input, delimiter=',')
        matrix = np.array(csv)
        (self.sg_count,self.word_count)=(matrix.shape)
        return matrix

    def cosine(self,a,b,matrix):
        result = 1 - spatial.distance.cosine(matrix[a], matrix[b])
        return result

    def get_matrix(self,matrix,rate):
        sg_count=self.sg_count
        cos_matrix = np.arange(sg_count*sg_count).reshape(sg_count,sg_count)

        for i in range(0,sg_count):
            for j in range(0,sg_count):
                res = self.cosine(i,j,matrix)

                res = 1 if res >=rate else 0
                cos_matrix[i][j]=res
        return cos_matrix

    def savefile(self,output,matrix):
        np.savetxt(output,matrix, delimiter=",")

    def main(self,input,output,rate):
        matrix = self.readfile(input)
        res = self.get_matrix(matrix,rate)
        self.savefile(output,res)

if __name__=="__main__":
    cos = cos()
    cos.main('CNN/combine_tfidf.csv','CNN/combine_relation.csv',1)