import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from tqdm import tqdm

np.random.seed(52)


def convert_embarked(x):
    if x == 'S':
        return 0
    elif x == 'C':
        return 1
    else:
        return 2

def create_bootstrap(features, labels):
    mask = np.random.choice(len(labels), size=len(labels))
    return features[mask], labels[mask]


class RandomForestClassifier():
    def __init__(self, n_trees=10, max_depth=np.iinfo(np.int64).max, min_error=1e-6):

        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_error = min_error

        self.forest = []
        self.is_fit = False

    def fit(self, X_train, y_train):

        for _ in tqdm(range(self.n_trees)):
            new_tree = DecisionTreeClassifier(
                max_features='sqrt',
                max_depth=self.max_depth,
                min_impurity_decrease=self.min_error)
            new_tree.fit(*create_bootstrap(X_train, y_train))
            self.forest.append(new_tree)

        self.is_fit = True

    def predict(self, X_test, y_test):

        if not self.is_fit:
            raise AttributeError('The forest is not fit yet! Consider calling .fit() method.')

        y_pred = self.forest[0].predict(X_test)
        print(f'{accuracy_score(y_pred, y_test):.3}')


if __name__ == '__main__':
    data = pd.read_csv('https://www.dropbox.com/s/4vu5j6ahk2j3ypk/titanic_train.csv?dl=1')

    data.drop(
        ['PassengerId', 'Name', 'Ticket', 'Cabin'],
        axis=1,
        inplace=True
    )
    data.dropna(inplace=True)

    # Separate these back
    y = data['Survived'].astype(int)
    X = data.drop('Survived', axis=1)

    X['Sex'] = X['Sex'].apply(lambda x: 0 if x == 'male' else 1)
    X['Embarked'] = X['Embarked'].apply(lambda x: convert_embarked(x))

    X_train, X_val, y_train, y_val = \
        train_test_split(X.values, y.values, stratify=y, train_size=0.8)

    # Stage 1
    # Make some tree...
    # model = DecisionTreeClassifier()
    # model.fit(X_train, y_train)
    #
    # y_pred = model.predict(X_val)
    # print(f'{accuracy_score(y_pred, y_val):.3f}')

    # Stage 2
    # X_sub, y_sub = create_bootstrap(X_train, y_train)
    # print(y_sub[:10].tolist())

    # Stage 3
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    model.predict(X_val, y_val)
