import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import svm
from sklearn import tree
from sklearn import preprocessing
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier
trainfile = "/Users/raghavan/PycharmProjects/DataScience/Stage1/Code/trainFeature.csv"
testfile = "/Users/raghavan/PycharmProjects/DataScience/Stage1/Code/testFeature.csv"
df = pd.read_csv(trainfile)
tdf = pd.read_csv(testfile)
n_splits = 10
skf = StratifiedKFold(n_splits, random_state=1)
y_col = 'label'
target = df[y_col].values
test_target = tdf[y_col].values
del df[y_col]
del tdf[y_col]
skf.get_n_splits(df, target)
train_data = df.values
test_data = tdf.values
decisiontree_classifier = tree.DecisionTreeClassifier(criterion="entropy")
precision_list = []
recall_list = []
fscore_list = []
for train_index, test_index in skf.split(train_data, target):
    decisiontree_classifier.fit(train_data[train_index],target[train_index])
    y_pred = decisiontree_classifier.predict(train_data[test_index])
    precision,recall,fscore,support = precision_recall_fscore_support(target[test_index], y_pred, average='macro')
    precision_list.append(precision)
    recall_list.append(recall)
    fscore_list.append(fscore)
print("\n\nMax Precision: "+ str(max(precision_list))+ "\nMax Recall: " + str(max(recall_list))+ "\nMax fscore: "+ str(max(fscore_list)))

randomforest = RandomForestClassifier(random_state=1)
precision_list = []
recall_list = []
fscore_list = []
for train_index, test_index in skf.split(train_data, target):
    randomforest.fit(train_data[train_index],target[train_index])
    y_pred = randomforest.predict(train_data[test_index])
    precision,recall,fscore,support = precision_recall_fscore_support(target[test_index], y_pred, average='macro')
    precision_list.append(precision)
    recall_list.append(recall)
    fscore_list.append(fscore)
print("\n\nMax Precision: " + str(max(precision_list)) + "\nMax Recall: " + str(max(recall_list)) + "\nMax fscore: " + str(max(fscore_list)))


linreg = LinearRegression()
precision_list = []
recall_list = []
fscore_list = []
for train_index, test_index in skf.split(train_data, target):
    linreg.fit(train_data[train_index],target[train_index])
    y_pred = linreg.predict(train_data[test_index])
    thresh = round(np.mean(y_pred), 2)
    y_pred = np.where(y_pred > thresh, 1, 0)
    precision,recall,fscore,support = precision_recall_fscore_support(target[test_index], y_pred, average='macro')
    precision_list.append(precision)
    recall_list.append(recall)
    fscore_list.append(fscore)
print("\n\nMax Precision: " + str(max(precision_list)) + "\nMax Recall: " + str(max(recall_list)) + "\nMax fscore: " + str(max(fscore_list)))


logreg = LogisticRegression(C = 100.0, random_state = 1)
precision_list = []
recall_list = []
fscore_list = []
for train_index, test_index in skf.split(train_data, target):
    logreg.fit(train_data[train_index],target[train_index])
    y_pred = logreg.predict(train_data[test_index])
    precision,recall,fscore,support = precision_recall_fscore_support(target[test_index], y_pred, average='macro')
    precision_list.append(precision)
    recall_list.append(recall)
    fscore_list.append(fscore)
print("\n\nMax Precision: " + str(max(precision_list)) + "\nMax Recall: " + str(max(recall_list)) + "\nMax fscore: " + str(max(fscore_list)))

logreg = LogisticRegression(C = 100.0, random_state=1)
logreg.fit(train_data, target)
y_pred = logreg.predict(test_data)
precision, recall, fscore ,support = precision_recall_fscore_support(test_target, y_pred, average='macro')
print("Precision on Test Set: "+ str(precision) +
      "\nRecall on Test Set: "+ str(recall) +
      "\nFScore on Test Set: "+ str(fscore))

svm_clf = svm.SVC(kernel = 'rbf', random_state = 1, gamma = 0.1, C = 100.0)
precision_list = []
recall_list = []
fscore_list = []
for train_index, test_index in skf.split(train_data, target):
    svm_clf.fit(train_data[train_index],target[train_index])
    y_pred = svm_clf.predict(train_data[test_index])
    precision,recall,fscore,support = precision_recall_fscore_support(target[test_index], y_pred, average='macro')
    precision_list.append(precision)
    recall_list.append(recall)
    fscore_list.append(fscore)
print("\n\nMax Precision: " + str(max(precision_list)) + "\nMax Recall: " + str(max(recall_list)) + "\nMax fscore: " + str(max(fscore_list)))