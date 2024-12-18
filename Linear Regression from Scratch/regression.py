import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

class CustomLinearRegression:

    def __init__(self, *, fit_intercept=True):

        self.fit_intercept = fit_intercept
        self.coefficient = None
        self.intercept = None

    def fit(self, x, y):
        X, y = np.array(x), np.array(y)
        if self.fit_intercept:
            X = np.column_stack((X, np.ones(len(X))))
        coeffs = np.linalg.inv(X.T @ X) @ X.T @ y
        if self.fit_intercept:
            self.coefficient = coeffs[:-1]
            self.intercept = float(coeffs[-1])
        else:
            self.coefficient = coeffs

    def predict(self, X):
        if self.fit_intercept:
            return (np.column_stack((X, np.ones(len(X))))
                    @ np.hstack((self.coefficient, self.intercept)))
        else:
            return X @ self.coefficient

    def r2_score(self, y, yhat):
        return 1. - np.sum((y - yhat) ** 2) / np.sum((y - np.mean(y)) ** 2)

    def rmse(self, y, yhat):
        return np.sqrt(1. / len(y) * np.sum((y - yhat) ** 2))


    def get_weights(self, y, yhat):
        return {'Intercept': self.intercept,
                'Coefficient': self.coefficient,
                'R2': float(self.r2_score(y, yhat)),
                'RMSE': float(self.rmse(y, yhat)),
                }


def main():
    # Stage 1
    # x = [4.0, 4.5, 5, 5.5, 6.0, 6.5, 7.0]
    # y = [33, 42, 45, 51, 53, 61, 62]

    # Stage 2
    # x = [4, 4.5, 5, 5.5, 6, 6.5, 7]
    # w = [1, -3, 2, 5, 0, 3, 6]
    # z = [11, 15, 12, 9, 18, 13, 16]
    # y = [33, 42, 45, 51, 53, 61, 62]

    # Stage 3
    # x = [0.9, 0.5, 1.75, 2.0, 1.4, 1.5, 3.0, 1.1, 2.6, 1.9]
    # w = [11, 11, 9, 8, 7, 7, 6, 5, 5, 4]
    # y = [21.95, 27.18, 16.9, 15.37, 16.03, 18.15, 14.22, 18.72, 15.4, 14.69]

    # Stage 4
    f1 = [2.31, 7.07, 7.07, 2.18, 2.18, 2.18, 7.87, 7.87, 7.87, 7.87]
    f2 = [65.2, 78.9, 61.1, 45.8, 54.2, 58.7, 96.1, 100.0, 85.9, 94.3]
    f3 = [15.3, 17.8, 17.8, 18.7, 18.7, 18.7, 15.2, 15.2, 15.2, 15.2]
    y = [24.0, 21.6, 34.7, 33.4, 36.2, 28.7, 27.1, 16.5, 18.9, 15.0]

    X = np.column_stack([f1, f2, f3])
    model = CustomLinearRegression()
    model.fit(X, y)

    result = model.get_weights(y, model.predict(X))

    regSci = LinearRegression(fit_intercept=True)
    regSci.fit(X, y)
    resultSci = {'Intercept': float(regSci.intercept_),
                'Coefficient': regSci.coef_,
                'R2': r2_score(y, regSci.predict(X)),
                'RMSE': float(np.sqrt(mean_squared_error(y, regSci.predict(X)))),
                }
    diff = {}
    for key, value in result.items():
        diff[key] = result[key] - resultSci[key]

    print(diff)


if __name__ == '__main__':
    main()