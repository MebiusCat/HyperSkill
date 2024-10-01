# Logistic regression
import numpy as np

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

    def fit_mse(self, X, y):
        if self.fit_intercept:
            X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)

        self.coef_ = np.zeros(X.shape[1])

        for _ in range(self.n_epoch):
            y_hat = self.sigmoid(X @ self.coef_)
            y_grad = (y_hat - y) * y_hat * (1 - y_hat)
            self.coef_ -= self.l_rate * X.T @ y_grad

    def fit_log_loss(self, X, y):
        if self.fit_intercept:
            X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)

        self.coef_ = np.zeros(X.shape[1])

        for _ in range(self.n_epoch):
            y_hat = self.sigmoid(X @ self.coef_)
            self.coef_ -= self.l_rate * X.T @ (y_hat - y) / X.shape[0]

    def predict(self, X, cut_off=0.5):
        if self.fit_intercept:
            X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)

        y_pred = self.sigmoid(X @ self.coef_)
        return [1 if y >= cut_off else 0 for y in y_pred]


data = load_breast_cancer(as_frame=True)
X = data.data[['worst concave points', 'worst perimeter', 'worst radius']].copy()
y = data.target

X = (X - X.mean()) / X.std()

X_train, X_test, y_train, y_test = (
    train_test_split(X, y, train_size=0.8, random_state=43))

model = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)
model.fit_log_loss(X_train, y_train)
acc = accuracy_score(y_test, model.predict(X_test))

print({'coef_': model.coef_.tolist(), 'accuracy': acc})
