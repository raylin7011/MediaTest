import csv
import os
from sklearn.externals import joblib
from sklearn import metrics

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

    # load test dataset
    csvTestData = cwd + '/NewsData/dataSetTest.csv'
    [X_newsdataTest, y_labelsTest] = loaddata(csvTestData)

    # 加載模型
    classifier2 = joblib.load(cwd + '/NewsClassifier/classifier2.pkl')

    # 預測結果
    predicted = classifier2.predict(X_newsdataTest)
    
    # 實際結果
    actual = y_labelsTest
    
    # 分類器準確度
    classifierAccuracy = classifier2.score(X_newsdataTest, y_labelsTest)
    print("Classifier Accuracy:", classifierAccuracy*100, "%")
    
    # 分類器報告
    print("Classification report for classifier %s:\n%s\n"
      % (classifier2, metrics.classification_report(actual, predicted)))
    
    print("Confusion matrix:\n%s" % metrics.confusion_matrix(actual, predicted))
    
    # for debug stop point
    pass
