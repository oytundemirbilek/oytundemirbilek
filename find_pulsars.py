import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

pd.set_option('colheader_justify', 'center')

def plot(Xtest, ytest, index_max, preds, model):
    fig = plt.figure()

    for x, gt in zip(Xtrain, ytrain):
        
        if gt == 0:
            color = 'red'
        else:
            color = 'green'
        plt.scatter(x[0], x[index_max], c=color, marker='.')

    plt.savefig('plot.png')
    plt.show()

def renaming(df):
    change_to = ['Mean Profile',
                'Stdev Profile',
                'Kurtosis  Profile',
                'Skewness Profile',
                'Mean Curve',
                'Stdev Curve',
                'Kurtosis Curve',
                'Skewness Curve',
                'Is Pulsar']

    legend = {}
    for col, to in zip(df.columns, change_to):
        legend[col] = to
    df = df.rename(columns=legend)
    table = {}
    table['Column Name'] = list(legend.values())
    table['Explanation'] = list(legend.keys())
    legend = pd.DataFrame(data=table)
    return legend, df

def pulsar_classifier():
    df = pd.read_csv('./data/pulsar_stars.csv')
    df = df.round(3)
    data_matrix = df.drop('target_class', axis=1).values
    data_labels = df['target_class'].values
    Xtrain, Xtest, ytrain, ytest = train_test_split(data_matrix, data_labels, test_size = 0.1)
    legend, df = renaming(df)
    clf = DTC()
    clf.fit(Xtrain, ytrain)
    preds = clf.predict(Xtest)

    f1 = f1_score(ytest, preds)
    f_importance = list(clf.feature_importances_)
    index_max = f_importance.index(max(f_importance))

    #plot(Xtest, ytest, index_max, preds, clf)
    print("F1Score of the predictions: ", f1)
    print("Most important feature: ", df.columns[index_max])

    output = {'err': None, 
            'score': 'F1 Score of the Model: ' + str(f1), 
            'feature': 'Most Important Feature: ' + df.columns[index_max]
            'output': ''}
    legendhtml = legend.to_html(classes='tablestyle')
    datahtml = df.iloc[:10].to_html(classes='tablestyle')
    return output, datahtml, legendhtml
            
