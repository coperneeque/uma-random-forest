#! /usr/bin/env python3

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics

import sys

if __name__ == "__main__":
    path = sys.argv[1]
    n_treas = int(sys.argv[2])
    data = pd.read_csv(path)

    keys = data.keys()
    X = data[keys[1:keys.__len__()-2]]
    y = data[keys[keys.__len__()-1]]
    
    for i in range(5):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

        clf=RandomForestClassifier(n_estimators=n_treas)

        clf.fit(X_train,y_train)

        y_pred=clf.predict(X_test)

        print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
