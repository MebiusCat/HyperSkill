import keras
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split


(X, y), (_, _) = keras.datasets.mnist.load_data(path='mnist.npz')

X = X.reshape(X.shape[0], -1)

X_train, X_test, y_train, y_test = train_test_split(X[:6000], y[:6000], random_state=40, test_size=0.3)

print(f"x_train shape: {X_train.shape}",
      f"x_test shape: {X_test.shape}",
      f"y_train shape: {y_train.shape}",
      f"y_test shape: {y_test.shape}",
      "Proportion of samples per class in train set:",
      pd.Series(y_train).value_counts(normalize=True), sep='\n'
)

# print(f"Classes: {np.unique(y_train)}",
#       f"Features' shape: {X_train.shape}",
#       f"Target's shape: {y_train.shape})",
#       f"min: {np.min(X_train)}, max: {np.max(X_train)}", sep='\n')
