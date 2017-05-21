import os
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import re

class DocToSG():

    stopWords = None
    # 移除指定字
    specialWords = ['￡1,600','—', 'with', 'without', 'isn', 'don',
                    'much', 'many', 'well',
                    'go', 'take', 'come', 'become', 'call',
                    'new', 'old', 'others', 'rather', 'still', 'latter',
                    'like', 'unlink', 'now', 'past', 'name', 'the']
    # 轉換複數字為單數
    specialNouns = ['fintechs', 'replaces']

    def __init__(self, lang):
        self.stopWords = set(stopwords.words(lang))

    # 將文件讀入，並依據各句子產生出一份SG檔案
    def load_document(self, docfile,days):
        # 檔案資料夾
        file_dir = os.path.dirname(docfile)

        # 建立子資料夾
        '''
        output_dir = os.path.splitext(docfile)[0]
        # 建立資料夾
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        '''

        # 讀取all檔案
        with open(docfile, 'r') as docF:
            SG = docF.readlines()

        # 輸出到個檔案
        for x in range(0,len(SG)):
            file_name = file_dir+"\\D"+str(days)+"SG"+str(x+1)+".txt"
            print("\n[File]: "+file_name)
            with open(file_name, 'w') as SGF:
                res = self.ProcessText(SG[x])
                SGF.write(res)

    # 移除標點符號
    def RemovePunctuation(self, word):
        if word[-1:] in string.punctuation:
            word = word[:len(word) - 1]

        if word != '':
            if word[0] in string.punctuation:
                word = word[1:]

        return word

    # 移除所有格
    def RemovePrime(self, word):
        primeList = ['’', "'"]
        found = True

        for prime in primeList:
            if prime in word:
                break

        if not found:
            return word

        _word = None

        if len(word) > 2:
            # 移除 複數所有格
            if word[-1:] in primeList:
                _word = word[:-1]
                return _word

        if len(word) > 3:
            # 移除 單數所有格 否定 助動詞縮寫
            if word[-2:][0] in primeList:
                _word = word[:-2]
                return _word

        if len(word) > 4:
            # 移除助動詞縮寫
            if word[-3:][0] in primeList:
                _word = word[:-3]
                return _word

        _word = word

        return _word

    # 轉換詞性為原型詞
    def ChangeForm(self, word):
        _text = nltk.pos_tag([word])
        if _text is None:
            return word

        _word2 = None
        _word, _textType = _text[0]

        if _textType in ['CC', 'PRP', 'MD', 'WP', 'IN', 'CD']:
            # 序號 指示代名詞 助動詞 疑問代名詞 介系詞 計數
            print(u"\t詞性 %s:%s" % _text[0])
            return None
        elif _textType[:2] == 'VB':
            # 動詞
            _word2 = WordNetLemmatizer().lemmatize(_word, 'v')
            if _word != _word2:
                print("%s -> %s" % (_word, _word2))
        elif _textType[:2] == 'NN':
            # 名詞
            if _word in self.specialNouns:
                _word2 = _word[:-1]
            else:
                _word2 = WordNetLemmatizer().lemmatize(_word, 'n')

            if _word != _word2:
                print("%s -> %s" % (_word, _word2))
        elif _textType[:2] == 'RB':
            # 副詞
            _word2 = WordNetLemmatizer().lemmatize(_word, 'r')
            if _word != _word2:
                print("%s -> %s" % (_word, _word2))
        elif _textType[:2] == 'JJ':
            # 形容詞
            _word2 = WordNetLemmatizer().lemmatize(_word, 'a')
            if _word != _word2:
                print("%s -> %s" % (_word, _word2))
        else:
            print(u"\t詞性 %s:%s" % _text[0])
            _word2 = word

        return _word2

    def ProcessText(self, content):
        wordList = content.lower().split(' ')
        _wordList = []
        for word in wordList:
            word = word.strip("\n")

            if word in self.stopWords:
                continue

            _word = self.RemovePunctuation(word)
            if _word is None or _word == '':
                continue

            # 過濾最少字元數
            if len(_word) < 4:
                continue

            _word2 = self.RemovePrime(_word)

            _word = self.ChangeForm(_word2)
            if _word is None:
                continue

            # 過濾指定字
            if _word not in self.specialWords:
                res = self.RemovePunctuation(_word)
                _wordList.append(res)
        print(_wordList)
        return ' '.join(_wordList)

# if __name__ == '__main__':
#     # 找出所有檔案清單
#     main_path = os.getcwd()
#     crimea_path = main_path + "\\CNN\\crimea"
#     file_list = []
#     pattern = '.*\d+ \d+.txt'
#     for tops, dirs, files in os.walk(crimea_path):
#         for f in files:
#             # print(os.path.join(tops, f))
#             if re.search(pattern,os.path.join(tops, f)):
#                 file_list.append(os.path.join(tops, f))
#
#     # 產生所有DxSGx檔案
#     worker = DocToSG('english')
#     for i in range(0,len(file_list)):
#         worker.load_document(file_list[i],(i+1))