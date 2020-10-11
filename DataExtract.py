import csv
import jieba
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import sqlite3
from bs4 import BeautifulSoup
import pandas as pd
from opencc import OpenCC
from langdetect import detect
from langua import Predict

filename = "en-zh_tw (1).tmx"

def start():
    fp = open(filename, "r", encoding="utf-8")
    soup = BeautifulSoup(fp,"xml")
    ans = soup.find_all("tuv")
    print(ans)
    amountOfData = len(ans)/2
    print(amountOfData)
    temp = {}
    count = 0
    df = pd.DataFrame(columns=["中文", "英文"])
    numOfData = 0
    englishWord = ""
    chineseWord = ""
    for a in ans:
        print(numOfData)
        if numOfData == amountOfData:
            break
        if a.get("xml:lang") == "en":
            temp["英文"] = a.get_text()
            englishWord = a.get_text()
            count = count + 1
        if a.get("xml:lang") == "zh" or a.get("xml:lang") == "zh-tw":
            cc = OpenCC('s2tw')
            text = cc.convert(a.get_text())
            finalword = ""
            inBracket = False
            for letter in text:
                if letter == '(':
                    inBracket = True
                    continue
                elif letter == ")":
                    inBracket = False
                    continue
                if inBracket == False and letter != " ":
                    finalword += letter
                elif inBracket == True:
                    continue
            temp["中文"] = finalword
            chineseWord = finalword
            count = count + 1
        if count == 2:
            count = 0
            if len(chineseWord) == 0 or len(englishWord) == 0:
                temp.clear()
                amountOfData = amountOfData -1
                continue
            if chineseWord[0] == englishWord[0]:
                chineseWord = ""
                englishWord = ""
                amountOfData = amountOfData - 1
                temp.clear()
                continue
            else:
                print(chineseWord)
                print(englishWord)
                df = df.append(temp,ignore_index=True)
                chineseWord = ""
                numOfData = numOfData + 1
    print(df.to_string())
    return df


if __name__ == '__main__':
    finaltable = pd.DataFrame(columns=["中文", "英文"])
    print(start())
    # finaltable = finaltable.append(temp, ignore_index=True)
    # finaltable.to_csv("translation.csv", sep='\t', encoding="utf-8", index=False)


