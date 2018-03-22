import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
import os
import random
from sklearn import metrics

#  ******************************************************************************
#  * Function: txt2list
#  *
#  * Description:
#  *  性質屬性加上抽取新聞文檔中的標題和內文，存成 txtList
#  *
#  * Parameters: 
#  *  txtattr : 性質屬性, txtfile : 新聞文檔
#  *
#  * Return value: 
#  *  txtList : [ [性質, 標題, 內文], [性質, 標題, 內文]，... ]
#  *            [ [     第一則     ], [     第二則     ], ... ]
#  ******************************************************************************
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
    txtList = list()
    
    # 儲存型式
    # [ [性質, 標題, 內文], [性質, 標題, 內文]，... ]
    # [ [     第一則     ], [     第二則     ], ... ]
    # i 即表示第幾則
    for i in range(0, len(contentList), 2):
        txtList.append([txtattr, contentList[i], contentList[i+1]])
    
    return txtList

#  ******************************************************************************
#  * Function: gendata
#  *
#  * Description:
#  *  産生分詞資料 : X_newsdata, 標籤資料 : y_labels
#  *
#  * Parameters: 
#  *  newslist : 所有的新聞資料
#  *
#  * Return value: 
#  *  X_newsdata, y_labels
#  *
#  ******************************************************************************
def gendata(newslist):
    
    X_newsdata = list()
    y_labels = list()

    # 性質標籤字典, 方便對映和增加性質
    txtAttrDict = {
        '中性': 0,
        '其它': 1
    }

    # i 表示第幾則新聞
    for i in range(len(newslist)):
        # 主題 + 內容去作分詞
        wordcut = jieba.cut( newslist[i][1] + newslist[i][2], cut_all=False )
        
        # 分詞後放入 X_newsdata
        X_newsdata.append(" ".join(wordcut))

        # 設定性質標籤
        y_labels.append(txtAttrDict[newslist[i][0]])
    
    return X_newsdata, y_labels

# 當前工作目錄
cwd = os.getcwd()

# 新聞文件檔
PTStxtfile = cwd + '/NewsClassifier/2018-03-07_pts_news.txt'
CHTtxtfile = cwd + '/NewsClassifier/2018-03-07_cht_news.txt'

if __name__ == '__main__':
    # use list to save txt contents
    # 公視
    PTStxtlist = txt2list('中性', PTStxtfile)

    # 中時
    CHTtxtlist = txt2list('其它', CHTtxtfile)

    # 合併成一個新聞資料集
    newslist = list()
    newslist.extend(PTStxtlist)
    newslist.extend(CHTtxtlist)
    
    # generate 分詞資料:X_newsdata, 標籤資料:y_labels
    X_newsdata, y_labels = gendata(newslist)

    # zip : 把對應的分詞資料, 標籤資料放在一起
    # 隨機化 (分詞資料, 標籤資料)
    zip2list = list(zip(X_newsdata, y_labels))
    random.shuffle(zip2list)

    # 還原成 X_newsdata, y_labels
    [X_newsdata, y_labels] = zip(*zip2list)

    # 將 X_newsdata 生成詞語的 tf-idf 向量空間模型
    tfidfvectorizer = TfidfVectorizer(lowercase=False)
    tfidfmatrix = tfidfvectorizer.fit_transform(X_newsdata)

    # 把資料分成訓練集和測試集
    # 訓練集 : 70%
    ix = int((len(y_labels) * 0.7)) + 1

    tfidfmatrixTrain = tfidfmatrix[:ix]
    y_labelsTrain = y_labels[:ix]

    # 測試集 : 30%
    tfidfmatrixTest = tfidfmatrix[ix:]
    y_labelsTest = y_labels[ix:]
    
    # 採用 LinearSVC 演算法訓練
    classifier = LinearSVC()
    
    # 訓練
    classifier.fit(tfidfmatrixTrain, y_labelsTrain)
    
    # 儲存模型
    joblib.dump(classifier, cwd + '/NewsClassifier/classifier.pkl')

    # 先寫著，以後若要分成 test.py, copy 即可 
    # 加載模型
    # classifier = joblib.load(cwd + '/NewsClassifier/classifier.pkl')

    # 預測結果
    predicted = classifier.predict(tfidfmatrixTest)
    
    # 實際結果
    actual = y_labelsTest
    
    # 分類器準確度
    classifierAccuracy = classifier.score(tfidfmatrixTest, y_labelsTest)
    print("Classifier Accuracy:", classifierAccuracy*100, "%")
    
    # 分類器報告
    print("Classification report for classifier %s:\n%s\n"
      % (classifier, metrics.classification_report(actual, predicted)))

# for debug
pass
