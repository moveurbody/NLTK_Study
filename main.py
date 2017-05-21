import os
from DocToSG import *
import re
import csv


def get_file_list(dict, pattern):
    file_list = []

    work_path = os.getcwd()
    full_path = work_path + dict

    for tops, dirs, files in os.walk(full_path):
        for f in files:
            if re.search(pattern, os.path.join(tops, f)):
                file_list.append(os.path.join(tops, f))
    return file_list

def create_files(path):
    # 找出所有檔案清單
    pattern = '.*\d+ \d+.txt'
    file_list = get_file_list(path, pattern)

    # 產生所有DxSGx檔案
    worker = DocToSG('english')
    for i in range(0, len(file_list)):
        worker.load_document(file_list[i], (i + 1))

def create_words(path):
    main_path = os.getcwd()
    full_path = main_path + path

    str_list = []
    pattern = '.*D\d+SG\d+.txt'
    file_list = get_file_list(path, pattern)

    for i in range(0, len(file_list)):
        with open(file_list[i], 'r') as f:
            res = f.readline()
            res = res.split(" ")
            for i in res:
                str_list.append(i)

    new_list = list(set(str_list))
    print(len(new_list))
    res = ' '.join(new_list)
    with open(full_path+"\\words.txt", "w+") as f:
        f.write(res)

def create_matrix(path):
    work_path = os.getcwd()
    full_path = work_path + path
    text_list = []
    match_list = []
    match_result=[]

    result = open(full_path+"matrix.csv", 'a+', newline='')
    wr = csv.writer(result, dialect='excel')

    # 建立字詞清單
    text_list.append("file_names")
    with open(full_path+"\\words.txt", 'r') as f:
        temp = f.readline().strip().split(' ')
        text_list.extend(temp)
    wr.writerow(text_list)

    # 單文件比對字詞數
    pattern = '.*D\d+SG\d+.txt'
    file_list = get_file_list(path, pattern)
    for files in range(0, len(file_list)):
        with open(file_list[files], 'r') as f:
            match_list = f.readline().strip().split(' ')

        # 開始比對
        for i in range(0, len(text_list)):
            # 將match_result都寫0
            match_result.append(0)
            for match_text in match_list:
                if match_text in text_list[i]:
                    match_result[i] = match_result[i]+1
        match_result[0] = file_list[files]
        wr.writerow(match_result)
        match_result =[]

def main():
    path = "\\CNN\\combine"
    create_files(path)
    create_words(path)
    create_matrix(path)

if __name__ == '__main__':
    main()
