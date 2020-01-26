import pandas as pd
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

def plot():
    x = 0
    return x

def pulsar_classifier():
    df = pd.read_csv('./data/pulsar_stars.csv')
    data_matrix = df.drop('target_class', axis=1).values
    data_labels = df['target_class'].values
    Xtrain, Xtest, ytrain, ytest = train_test_split(data_matrix, data_labels, test_size = 0.1)

    clf = DTC()
    clf.fit(Xtrain, ytrain)
    preds = clf.predict(Xtest)

    f1 = f1_score(ytest, preds)
    f_importance = list(clf.feature_importances_)
    index_max = f_importance.index(max(f_importance))

    print("F1Score of the predictions:", f1)
    print("Most important feature:", df.columns[index_max])