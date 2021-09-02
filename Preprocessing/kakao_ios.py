import tkinter
from tkinter import filedialog

import re
import pandas as pd
from datetime import datetime

import csv

import numpy as np

class kakao_tocsv():
    def __init__(self,filename,chat) -> None:
        self.filename = filename
        self.chat = chat

    def kakaoRegEx(self):
        #필요한 데이터 정규식
        p = re.compile("(?P<Datetime>\d{4}\. \d{1,2}\. \d{1,2}\. (오전|오후) \d{1,2}:\d{1,2}), (?P<Username>\w+) : (?P<Contents>[^\n]+)")
        #필요없는 부분의 데이터 정규식
        del_p = re.compile("(?P<day>\d{4}년 \d{1,2}월 \d{1,2}일 (월|화|수|목|금|토|일)요일)")

        temp=[]
        new_chat=[]

        for chatting in self.chat:
            try:
                m = del_p.search(chatting)
                if m.group("day") is True:
                    del chatting
            except AttributeError:
                temp.append(chatting)

        for chatting in temp:
            try:
                m = p.search(chatting)
                if m.group(2) =="오전":
                    n= re.sub("오전","am",chatting,1)
                elif m.group(2)=="오후":
                    n= re.sub("오후","pm",chatting,1)
                new_chat.append(n)
            except AttributeError:
                pass
        
    def list2csv(self,new_chat):
        self.listchat = new_chat
        s = re.compile(
            "(?P<Datetime>\d{4}\. \d{1,2}\. \d{1,2}\. \w{2} \d{1,2}:\d{1,2}), (?P<Username>\w+) : (?P<Contents>[^\n]+)")
        kko_parse_result = []

        for chat in self.listchat:
            kko_pattern_result = s.findall(chat)
            token = list(kko_pattern_result[0])
            kko_parse_result.append(token)

        kko_parse_result = pd.DataFrame(kko_parse_result, columns=["Datetime", "Speaker", "contents"])
        kko_parse_result.to_csv("kko_regex.csv", index=False)
        

def preprocessing(text):
    # 개행문자 제거
    text = re.sub('\\\\n', ' ', str(text))
    # 특수문자,자음 제거
    text = re.sub('[.,;:\)*?!~`’^\-_+<>@\#$%&=#/(}※ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎㅠㅜ]', '', text)
    # 중복 생성 공백값
    text = re.sub(' +', ' ', text)
    text = re.sub(' ', '', text)
    return text


# 불용어 제거
def remove_stopwords(text):
    # 띄어쓰기 기준으로 단어삭제# 불용어 제거

    tokens = text.split(' ')
    stops = ['ㅎㅎㅎ', 'ㅎㅎ', 'ㅋㅋ', 'ㅋ', 'ㅎㅎ', 'ㅎ', 'ㅋㅋㅋ', 'ㅋㅋ', 'ㅠㅠㅠㅠ', 'ㅠㅠ',
             "그냥", "거기", "지금", "이제", "우리", "일단", "한번", "나도", "하는", "그게", "약간", "그거", "해서", "재미", "뭔가", "이모티콘",
             "존나", "누가", "하기", "하는데", "거의", "할게", "이번", "이건", "사실", "정도", "갑자기", "혹시", "보고", "하노", ]
    meaningful_words = [w for w in tokens if not w in stops]
    return ' '.join(meaningful_words)

def set_data(text_data) :
  with open(text_data, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    data = list(reader)
    return data


if __name__=="__main__":

    root = tkinter.Tk()
    root.withdraw()
    filename = filedialog.askopenfilename()
    print("\ndir_path : ", filename)

    with open(filename, 'r', encoding='utf-8') as f:
        chat = f.readlines()

    df = pd.read_csv("kko_regex.csv")

    df['new'] = df['contents'].apply(preprocessing)
    df['refine_contents'] = df['new'].apply(remove_stopwords)

    df.head()

    df.drop(['contents','new'],axis=1,inplace=True)

    df.to_csv('kakao_text.txt')
    
    text_data = set_data('kakao_text.txt')
    data_text = []
    for i in text_data :    
        data_text.append({'Datetime' : i['Datetime'], 'Speaker' : i['Speaker'], 'refine_contents' : i['refine_contents']})
    print(data_text)



