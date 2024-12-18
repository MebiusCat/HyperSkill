import numpy as np

class CustomLinearRegression:

    def __init__(self, *, fit_intercept=True):

        self.fit_intercept = fit_intercept
        self.coefficient = None
        self.intercept = None

    def fit(self, x, y):
        X, y = np.array(x).reshape(-1, 1), np.array(y)
        if self.fit_intercept:
            X = np.column_stack((X, np.ones(len(X))))
        coeffs = np.linalg.inv(X.T @ X) @ X.T @ y
        if self.fit_intercept:
            self.coefficient = coeffs[:-1]
            self.intercept = float(coeffs[-1])
        else:
            self.coefficient = coeffs
        print(self.get_weights())

    def get_weights(self):
        return {'Intercept': self.intercept,
                'Coefficient': self.coefficient}


def main():
    x = [4.0, 4.5, 5, 5.5, 6.0, 6.5, 7.0]
    y = [33, 42, 45, 51, 53, 61, 62]

    model = CustomLinearRegression()
    model.fit(x, y)


if __name__ == '__main__':
    main()