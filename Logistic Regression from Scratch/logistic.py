# Logistic regression
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split

class CustomLogisticRegression:

    def __init__(self, fit_intercept=True, l_rate=0.01, n_epoch=100):
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch

    def sigmoid(self, t) -> float:
        return 1. / (1. + np.exp(-t))

    def predict_proba(self, row, coef_):
        t = np.sum(row * coef_)
        return self.sigmoid(t)


data = load_breast_cancer(as_frame=True)
X = data.data[['worst concave points', 'worst perimeter']].copy()

X = (X - X.mean()) / X.std()
X.insert(0, 'intercept', 1.)

X_train, X_test, y_train, y_test = (
    train_test_split(X.to_numpy(), data.target.to_numpy(), train_size=0.8, random_state=43))

model = CustomLogisticRegression()
w = np.array([0.77001597, -2.12842434, -2.39305793])
result = np.array([round(model.predict_proba(row, w), 5) for row in X_test[: 10]])
print(result.tolist())
