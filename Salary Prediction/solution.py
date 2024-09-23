import os
import requests

import pandas as pd
from itertools import combinations
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_percentage_error as mape


def linear_model():
    # read data
    data = pd.read_csv('../Data/data.csv')
    X, y = data[['rating']], data['salary']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print('{:.5f} {:.5f} {:.5f}'.format(
        model.intercept_,
        model.coef_[0],
        mape(y_test, y_pred)))


def pow_model():
    # read data
    data = pd.read_csv('../Data/data.csv')

    result = {}
    for mult in range(2, 5):
        X, y = data[['rating']] ** mult, data['salary']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        result[mult] = mape(y_test, y_pred)
    print(f'{min(result.values()):.5f}')


def multi_model():
    # read data
    data = pd.read_csv('../Data/data.csv')

    X, y = data.drop(['salary'], axis=1), data['salary']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

    model = LinearRegression()
    model.fit(X_train, y_train)

    print(*model.coef_, sep=', ')


def analysis():
    # read data
    data = pd.read_csv('../Data/data.csv')

    result = {}
    variations = ['rating', 'age', 'experience']

    drops = variations + [[*el] for el in list(combinations(variations, 2))]
    for i, col in enumerate(drops):
        X, y = data.drop(col, axis=1).drop('salary', axis=1), data['salary']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        result[i] = (col, mape(y_test, y_pred))

    print(f'{min(result.values(), key=lambda x: x[1])[1]:.5f}')

# checking ../Data directory presence
if not os.path.exists('../Data'):
    os.mkdir('../Data')

# download data if it is unavailable
if 'data.csv' not in os.listdir('../Data'):
    url = "https://www.dropbox.com/s/3cml50uv7zm46ly/data.csv?dl=1"
    r = requests.get(url, allow_redirects=True)
    open('../Data/data.csv', 'wb').write(r.content)

analysis()
