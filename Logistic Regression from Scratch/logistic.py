# Logistic regression
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_breast_cancer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class CustomLogisticRegression:

    def __init__(self, fit_intercept=True, l_rate=0.01, n_epoch=100):
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch

    def sigmoid(self, t) -> float:
        return 1. / (1. + np.exp(-t))

    def predict_proba(self, row, coef_):
        bias, *t = coef_
        return self.sigmoid(bias * self.fit_intercept + t @ row)

    def fit_mse(self, X_train, y_train):
        self.coef_ = np.zeros(X_train.shape[1] + 1)  # initialized weights

        for _ in range(self.n_epoch):
            for i, row in enumerate(X_train):
                y_hat = self.predict_proba(row, self.coef_)
                y_calc = (y_hat - y_train[i]) * y_hat * (1 - y_hat)
                self.coef_[1:] = self.coef_[1:] - self.l_rate * y_calc * row
                self.coef_[0] = self.fit_intercept * (self.coef_[0] - self.l_rate * y_calc)

    def predict(self, X_test, cut_off=0.5):
        predictions = []
        for row in X_test:
            y_hat = self.predict_proba(row, self.coef_)
            predictions.append(1 if y_hat >= 0.5 else 0)
        return np.array(predictions).tolist()  # predictions are binary values - 0 or 1


data = load_breast_cancer(as_frame=True)
X = data.data[['worst concave points', 'worst perimeter', 'worst radius']].copy()
y = data.target

X = (X - X.mean()) / X.std()

X_train, X_test, y_train, y_test = (
    train_test_split(X, y, train_size=0.8, random_state=43))

# w = np.array([0.77001597, -2.12842434, -2.39305793])
# model = CustomLogisticRegression()
# result = X_test[:10].apply(model.predict_proba, args=(w,), axis=1)
# print(result.tolist())

model = CustomLogisticRegression(n_epoch=1000)
model.fit_mse(X_train.to_numpy(), y_train.to_numpy())
y_pred = model.predict(X_test.to_numpy())
result = {'coef_': np.array(model.coef_).tolist(),
          'accuracy': accuracy_score(y_test, y_pred)}
print(result)