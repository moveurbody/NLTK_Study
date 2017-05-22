# -*- coding: utf-8 -*-
# @Time    : 2017/5/21 下午 04:27
# @Author  : Yuhsuan
# @File    : tfidf.py
# @Software: PyCharm Community Edition
# 算出tf-idf

import numpy as np
import csv
import codecs
import math


class tfidf():
    def __init__(self):
        self.list_csv = []
        self.sg_count=0
        self.word_count=0

    def read_csv(self,path):
        list_csv=[]
        with codecs.open(path,'r',encoding='utf8', errors='ignore') as csvFile:
            reader = csv.reader(csvFile)
            for line in reader:
                list_csv.append(line)

        self.word_count= len(list_csv[0])-1
        self.sg_count= len(list_csv)-1
        self.list_csv=list_csv

    def tf(self,list):
        word_count = self.word_count
        sg_count = self.sg_count
        matrix=[]
        for i in range(1,sg_count+1):
            line = []
            for j in range(1,word_count+1):
                line.append(int(list[i][j]))
            matrix.append(line)
        matrix = np.asmatrix(matrix)
        return matrix


    def idf(self,list):
        # 每個字串列表
        word_count = self.word_count
        sg_count = self.sg_count
        word_list = []
        idf=[]

        for i in range(1,word_count):
            word_list.append(list[0][i])

        for j in range(1,word_count+1):
            count = 0
            for i in range(1,sg_count+1):
                if int(list[i][j])!=0:
                    count=count+1
            count = 1+math.log2(sg_count/count)
            idf.append(count)
        return idf

    def tf_idf(self,tf,idf):
        sg_count = self.sg_count
        word_count = self.word_count

        tf = np.asmatrix(tf)

        matrix=[]
        for i in range(0,sg_count):
            row=[]
            for j in range(0,word_count):
                row.append(tf[i,j]*idf[j])
            matrix.append(row)
        matrix = np.asmatrix(matrix)
        return matrix

    def main(self,input,output):
        res = self.read_csv(input)
        idf = self.idf(self.list_csv)
        tf = self.tf(self.list_csv)
        res = self.tf_idf(tf,idf)
        np.savetxt(output,res,delimiter=",")

if __name__=="__main__":
    tfidf = tfidf()
    tfidf.main("CNN/combinematrix.csv","CNN/combine_tfidf.csv")