import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
import os
import csv

#  ******************************************************************************
#  * Function: loaddata
#  *
#  * Description:
#  *  讀取標籤新聞檔，並分成X_newsdata，y_labels
#  *
#  * Parameters: 
#  *  csvfile: 標籤新聞檔
#  *
#  * Return value: 
#  *  X_newsdata: 標題 + 內文
#  *  y_labels: 0:中性, 1:其它
#  ******************************************************************************
def loaddata(csvfile):
    csvFile = open(csvfile, 'r', encoding='utf-8')
    csvCursor = csv.reader(csvFile)

    X_newsdata = list()
    y_labels = list()

    for row in csvCursor:
        y_labels.append(row[0])
        X_newsdata.append(row[1])
    
    csvFile.close()

    return X_newsdata, y_labels

if __name__ == '__main__':
    # 當前工作目錄
    cwd = os.getcwd()

    csvTrainData = cwd + '/NewsData/dataSetTrain.csv'

    X_newsdataTrain = list()
    y_labelsTrain = list()

    # load train dataset
    [X_newsdataTrain, y_labelsTrain] = loaddata(csvTrainData)
    
    # 第一步，分詞，並生成詞語的 tf-idf 向量空間模型
    step1 = ('tfidf', TfidfVectorizer(binary=False, tokenizer=jieba.cut))
    
    # 第二步，採用 LinearSVC 演算法訓練
    step2 = ('classifier2', LinearSVC())
    classifier2 = Pipeline(steps=[step1, step2])
    
    # 訓練
    classifier2 = classifier2.fit(X_newsdataTrain, y_labelsTrain)
    
    # 儲存模型
    joblib.dump(classifier2, cwd + '/NewsClassifier/classifier2.pkl')
     
    # 分類器準確度
    csvTestData = cwd + '/NewsData/dataSetTest.csv'
    [X_newsdataTest, y_labelsTest] = loaddata(csvTestData)
    classifierAccuracy = classifier2.score(X_newsdataTest, y_labelsTest)
    print("Classifier Accuracy:", classifierAccuracy*100, "%")

# for debug stop point
pass