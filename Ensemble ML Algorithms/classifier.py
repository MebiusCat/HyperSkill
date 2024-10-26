import numpy as np
import pandas as pd

from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import make_scorer, f1_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.ensemble import VotingClassifier

import warnings
warnings.filterwarnings('ignore')

random_state = np.random.RandomState(seed=29)

df = pd.read_csv('../data/music.csv')

X, y = df.drop(columns=['Class']), df['Class']
enc = LabelEncoder()
y_transformed = enc.fit_transform(y)
X_train, X_test, y_train, y_test =\
    train_test_split(X, y_transformed, test_size=0.2, stratify=y, random_state=random_state)

sgd_params = {
    "clf__loss": ["log_loss", "huber"],
    "clf__penalty": ["l2", "l1"],
    "clf__alpha": [1e-4, 1e-3, 1e-2, 1e-1,],
    "clf__learning_rate": ["constant", "adaptive"],
    "clf__eta0": [1e-4, 1e-3, 1e-2, 1e-1]
}

dt_params = {
    "clf__max_features": ["sqrt", "log2"],
    "clf__criterion": ["gini", "entropy", "log_loss"],
    'clf__max_depth': [None, 10, 20, 30],
    'clf__min_samples_split': [2, 5, 10],
    'clf__min_samples_leaf': [1, 2, 3, 4]
}

kn_params = {
    "clf__metric": ["minkowski", "cosine", "nan_euclidean", "manhattan"],
    "clf__n_neighbors": [2, 3, 4, 5, 6, 7, 8, 9],
    'clf__weights': ['uniform', 'distance'],
    'clf__algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'clf__leaf_size': [30, 60],
    'clf__p': [1, 2],
}

sv_params = {
    "clf__kernel": ["poly", "sigmoid", "rbf"],
    "clf__C": [1e-4, 1e-2, 1.0, 1e2, 1e4],
    "clf__decision_function_shape": ["ovo", "ovr"],
    "clf__degree": [2, 3, 4],
    "clf__gamma": ['scale', 'auto'] + [0.1, 1.0, 10.0],
    "clf__coef0": [0.0, 1.0],
    "clf__shrinking": [True, False]
}

result = {}

def eval_model(model_name, clf, params):
    pipe = Pipeline([('scaler', StandardScaler()), ('clf', clf)])

    f1 = make_scorer(f1_score, average="macro", labels=[0, 1, 2, 3])

    grid_search = GridSearchCV(pipe, param_grid=params, scoring=f1, n_jobs=-1)
    grid_search.fit(X_train, y_train)

    y_pred = grid_search.best_estimator_.predict(X_train)
    f1_train = f1_score(y_train, y_pred, average="macro", labels=[0, 1, 2, 3])

    y_pred = grid_search.best_estimator_.predict(X_test)
    f1_test = f1_score(y_test, y_pred, average="macro", labels=[0, 1, 2, 3])

    result[model_name] = {'f1_train': round(float(f1_train), 3),
                          'f1_test': round(float(f1_test), 3)}
    return grid_search.best_estimator_


clf_sgd = eval_model('sgd', SGDClassifier(random_state=random_state), sgd_params)
clf_dt = eval_model('dt', DecisionTreeClassifier(random_state=random_state), dt_params)
clf_kn = eval_model('kn', KNeighborsClassifier(), kn_params)
clf_sv = eval_model('sv', SVC(random_state=random_state, probability=True), sv_params)

eclf = VotingClassifier(estimators=[
    ('sgd', clf_sgd),
    ('sv', SVC(random_state=random_state, probability=True)),
], voting='soft')
eclf.fit(X_train, y_train)

result = classification_report(y_test, eclf.predict(X_test), output_dict=True)
pd.DataFrame(result).to_csv('../data/stage4.csv')
