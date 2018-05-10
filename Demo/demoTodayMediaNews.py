import os
from sklearn.externals import joblib

def txt2list(txtattr, txtfile):
    txtFile = open(txtfile, 'r', encoding='utf-8')
    rawTxtList = txtFile.read().rstrip('\n').split('\n')

    txtFile.close()
    
    # 抽取 TITLE 和 CONTENT
    contentList = list()

    for items in rawTxtList:
        # 新聞文檔的格式定義是字串並且符合 Python 字典定義 {key:value}
        # eval() 函數用來執行一個字符串表達式，並返回表達式的值
        # eval(items) -> eval('{key:value}')
        # str2dict = {key:value} 即可使用 Python 字典的特性
        str2dict = eval(items)
        key = "".join(str2dict.keys())
        if(key == 'TITLE' or key =='CONTENT'):
            contentList.append(str2dict[key])
    
    # 加入 txtAttr(性質)
    # 性質標籤字典, 方便對映和增加性質
    txtAttrDict = {
        '中性': '0',
        '其它': '1'
    }

    txtList = list()
    
    # 儲存型式
    # [ [性質, 標題 + 內文], [性質, 標題 + 內文]，... ]
    # [ [     第一則      ], [     第二則      ], ... ]
    # i 表示標題, i+1 表示內文
    for i in range(0, len(contentList), 2):
        txtList.append([txtAttrDict[txtattr], contentList[i] + contentList[i+1]])
    
    return txtList

def NewsClassifierAccuracy(newsmedia, newstxtlist):
    X_newsdata = list()
    y_labels = list()
    
    for item in newstxtlist:
        y_labels.append(item[0])
        X_newsdata.append(item[1])
    
    # predicted = classifier2.predict(X_newsdata)
    classifierAccuracy = classifier2.score(X_newsdata, y_labels)
    print(newsmedia, ": Classifier Accuracy:", classifierAccuracy*100, "%")


cwd = os.getcwd()
PTStxtfile = cwd + '/NewsData/2018-03-29_pts_news.txt'
CHTtxtfile = cwd + '/NewsData/2018-03-29_cht_news.txt'
LTNtxtfile = cwd + '/NewsData/2018-03-29_ltn_news.txt'
APPLEtxtfile = cwd + '/NewsData/2018-03-29_apple_news.txt'

PTStxtList = txt2list('中性', PTStxtfile)
CHTtxtList = txt2list('其它', CHTtxtfile)
LTNtxtList = txt2list('其它', LTNtxtfile)
APPLEtxtList = txt2list('其它', APPLEtxtfile)

classifier2 = joblib.load(cwd + '/NewsClassifier/classifier2.pkl')

NewsClassifierAccuracy('PTS', PTStxtList)
NewsClassifierAccuracy('CHT', CHTtxtList)
NewsClassifierAccuracy('LTN', LTNtxtList)
NewsClassifierAccuracy('APPLE', APPLEtxtList)

# for debug stop point
pass
