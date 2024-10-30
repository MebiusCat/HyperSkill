import keras
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

import warnings
warnings.filterwarnings('ignore')

def fit_predict_eval(model, features_train, features_test, target_train, target_test):
    model.fit(features_train, target_train)
    y_pred = model.predict(features_test)
    score = accuracy_score(target_test, y_pred)
    print(f'Model: {model}\nAccuracy: {score}\n')
    return round(score, 3)


(X, y), (_, _) = keras.datasets.mnist.load_data(path='mnist.npz')

X = X.reshape(X.shape[0], -1)

X_train, X_test, y_train, y_test = train_test_split(X[:6000], y[:6000], random_state=40, test_size=0.3)

models = [KNeighborsClassifier(),
          DecisionTreeClassifier(random_state=40),
          LogisticRegression(),
          RandomForestClassifier(random_state=40)
          ]

acc_scores = []

for model in models:
      acc_scores.append(
            fit_predict_eval(
                  model=model,
                  features_train=X_train,
                  features_test=X_test,
                  target_train=y_train,
                  target_test=y_test
            )
      )

best_model = np.argmax(np.array(acc_scores))
best_model_name = models[best_model].__class__.__name__

print(f'The answer to the question: {best_model_name} - {acc_scores[best_model]}')
