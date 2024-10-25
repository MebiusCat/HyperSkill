import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline

random_state = np.random.RandomState(seed=29)

df = pd.read_csv('../data/music.csv')

X, y = df.drop(columns=['Class']), df['Class']
enc = LabelEncoder()
y_transformed = enc.fit_transform(y)
X_train, X_test, y_train, y_test =\
    train_test_split(X, y_transformed, test_size=0.2, stratify=y, random_state=random_state)

result = {}


def eval_model(model_name, clf):
    pipe = Pipeline([('scaler', StandardScaler()), (model_name, clf)])

    y_pred = pipe.fit(X_train, y_train).predict(X_train)
    f1_train = f1_score(y_train, y_pred, average="macro", labels=[0, 1, 2, 3])

    y_pred = pipe.predict(X_test)
    f1_test = f1_score(y_test, y_pred, average="macro", labels=[0, 1, 2, 3])

    result[model_name] = {'f1_train': round(float(f1_train), 3),
                          'f1_test': round(float(f1_test), 3)}


eval_model('sgd', SGDClassifier(random_state=random_state))
eval_model('dt', DecisionTreeClassifier(random_state=random_state))
eval_model('kn', KNeighborsClassifier())
eval_model('sv', SVC(random_state=random_state, probability=True))

print(result)
