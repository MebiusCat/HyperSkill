# Logistic regression
import numpy as np

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


class CustomLogisticRegression:

    def __init__(self, fit_intercept=True, l_rate=0.01, n_epoch=100):
        self.fit_intercept = fit_intercept
        self.l_rate = l_rate
        self.n_epoch = n_epoch
        self.errors = []

    def sigmoid(self, t) -> float:
        return 1. / (1. + np.exp(-t))

    def predict_proba(self, row, coef_):
        bias, *t = coef_
        return self.sigmoid(bias * self.fit_intercept + t @ row)

    def fit_mse(self, X, y):
        if self.fit_intercept:
            X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)

        self.coef_ = np.zeros(X.shape[1])
        errors = []
        for _ in range(self.n_epoch):
            y_hat = self.sigmoid(X @ self.coef_)
            y_grad = (y_hat - y) * y_hat * (1 - y_hat)
            self.coef_ -= self.l_rate * X.T @ y_grad

            self.errors.append((y_hat - y)** 2 / X.shape[0])

    def fit_log_loss(self, X, y):
        if self.fit_intercept:
            X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)

        self.coef_ = np.zeros(X.shape[1])

        for _epoch in range(self.n_epoch):
            y_hat = self.sigmoid(X @ self.coef_)
            self.coef_ -= self.l_rate * X.T @ (y_hat - y) / X.shape[0]
            self.errors.append(-(y * np.log(y_hat) + (1 - y) * np.log(1 - y_hat) )/ X.shape[0])

    def fit_predict_sklearn(self, X, y, X_test):
        model = LogisticRegression(fit_intercept=self.fit_intercept)
        model.fit(X, y)
        return model.predict(X_test)

    def predict(self, X, cut_off=0.5):
        if self.fit_intercept:
            X = np.concatenate((np.ones((X.shape[0], 1)), X), axis=1)

        y_pred = self.sigmoid(X @ self.coef_)
        return [1 if y >= cut_off else 0 for y in y_pred]

def main():
    data = load_breast_cancer(as_frame=True)
    X = data.data[['worst concave points', 'worst perimeter', 'worst radius']].copy()
    y = data.target

    X = (X - X.mean()) / X.std()

    X_train, X_test, y_train, y_test = (
        train_test_split(X, y, train_size=0.8, random_state=43))

    model_mse = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)
    model_mse.fit_mse(X_train, y_train)
    acc_mse = accuracy_score(y_test, model_mse.predict(X_test))
    errors_mse = model_mse.errors

    model_log_loss = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)
    model_log_loss.fit_log_loss(X_train, y_train)
    acc_log_loss = accuracy_score(y_test, model_mse.predict(X_test))
    errors_log_loss = model_log_loss.errors

    model_sklearn = CustomLogisticRegression(fit_intercept=True, l_rate=0.01, n_epoch=1000)
    acc_sklearn = accuracy_score(y_test, model_sklearn.fit_predict_sklearn(X_train, y_train, X_test))

    print({'mse_accuracy': acc_mse,
           'logloss_accuracy': acc_log_loss,
           'sklearn_accuracy': acc_sklearn,
           'mse_error_first': errors_mse[1].tolist(),
           'mse_error_last': errors_mse[-1].tolist(),
           'logloss_error_first': errors_log_loss[1].tolist(),
           'logloss_error_last': errors_log_loss[-1].tolist(),
           })

    print('Answers to the questions:')
    print(f'1) {min(errors_mse[1]):.5f}')
    print(f'2) {min(errors_mse[-1]):.5f}')
    print(f'3) {max(errors_log_loss[1]):.5f}')
    print(f'4) {max(errors_log_loss[-1]):.5f}')
    print(f'5) expanded')
    print(f'6) expanded')


if __name__ == '__main__':
    main()