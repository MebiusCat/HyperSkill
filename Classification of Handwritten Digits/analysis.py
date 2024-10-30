import keras

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import GridSearchCV

import warnings
warnings.filterwarnings('ignore')


def fit_predict_eval(model, features_train, features_test, target_train, target_test):
    model.fit(features_train, target_train)
    y_pred = model.predict(features_test)
    score = accuracy_score(target_test, y_pred)
    print(f'Model: {model}\nAccuracy: {score}\n')
    return round(score, 3)

def base_models():
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
                features_train=X_train_norm,
                features_test=X_test_norm,
                target_train=y_train,
                target_test=y_test
            )
        )

    print('The answer to the 1st question: yes')
    print('The answer to the 2nd question: KNeighborsClassifier-0.953, RandomForestClassifier-0.937')


(X, y), (_, _) = keras.datasets.mnist.load_data(path='mnist.npz')

X = X.reshape(X.shape[0], -1)

X_train, X_test, y_train, y_test = train_test_split(X[:6000], y[:6000], random_state=40, test_size=0.3)

normalizer = Normalizer()
normalizer.fit(X_train, y_train)
X_train_norm = normalizer.transform(X_train)
X_test_norm = normalizer.transform(X_test)

def eval(model, params):
    grid_search = GridSearchCV(model, param_grid=params, n_jobs=-1)
    grid_search.fit(X_train_norm, y_train)

    # print(name)
    # print(f'best estimator: {grid_search.best_estimator_}')
    # print(grid_search.best_params_)
    # print(f'accuracy: {grid_search.best_score_}')
    return grid_search.best_estimator_

kn_params = {
    'n_neighbors': [3, 4],
    'weights': ['uniform', 'distance'],
    'algorithm': ['auto', 'brute'],
    'p': [1, 2],
}

rf_params = {
    'n_estimators': [300, 500, 600],
    'max_features': ['sqrt', 'log2'],
    'class_weight': ['balanced', 'balanced_subsample']
}
knn = eval(KNeighborsClassifier(), kn_params)
print('K-nearest neighbours algorithm')
print(f'best estimator: {knn}')
print(f'accuracy: {accuracy_score(y_test, knn.predict(X_test_norm))}')

rf = eval(RandomForestClassifier(random_state=40), rf_params)
print('Random forest algorithm')
print(f'best estimator: {rf}')
print(f'accuracy: {accuracy_score(y_test, rf.predict(X_test_norm))}')