import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


random_state = np.random.RandomState(seed=29)

df = pd.read_csv('../data/music.csv')

X, y = df.drop(columns=['Class']), df['Class']
enc = LabelEncoder()
y_transformed = enc.fit_transform(y)
X_train, X_test, y_train, y_test =\
    train_test_split(X, y_transformed, test_size=0.2)

answer = {
    'train': [X_train.shape, y_train.shape],
    'test': [X_test.shape, y_test.shape],
    }
print(answer)
