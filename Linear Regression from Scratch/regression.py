import numpy as np

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
    x = [0.9, 0.5, 1.75, 2.0, 1.4, 1.5, 3.0, 1.1, 2.6, 1.9]
    w = [11, 11, 9, 8, 7, 7, 6, 5, 5, 4]
    y = [21.95, 27.18, 16.9, 15.37, 16.03, 18.15, 14.22, 18.72, 15.4, 14.69]

    X = np.column_stack([x, w])
    model = CustomLinearRegression()
    model.fit(X, y)

    print(model.get_weights(y, model.predict(X)))


if __name__ == '__main__':
    main()