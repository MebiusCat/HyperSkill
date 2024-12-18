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
            return X @ np.column_stack(self.coefficient, self.intercept)
        else:
            return X @ self.coefficient

    def r2_score(self, y, yhat):
        pass

    def rmse(self, y, yhat):
        pass


    def get_weights(self):
        return {'Intercept': self.intercept,
                'Coefficient': self.coefficient}


def main():
    # Stage 1
    # x = [4.0, 4.5, 5, 5.5, 6.0, 6.5, 7.0]
    # y = [33, 42, 45, 51, 53, 61, 62]

    # Stage 2
    x = [4, 4.5, 5, 5.5, 6, 6.5, 7]
    w = [1, -3, 2, 5, 0, 3, 6]
    z = [11, 15, 12, 9, 18, 13, 16]
    y = [33, 42, 45, 51, 53, 61, 62]
    X = np.column_stack([x, w, z])
    model = CustomLinearRegression(fit_intercept=False)
    model.fit(X, y)

    print(model.predict(X))


if __name__ == '__main__':
    main()