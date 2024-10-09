import numpy as np
import pandas as pd
import os
import requests
from matplotlib import pyplot as plt


def one_hot(data: np.ndarray) -> np.ndarray:
    y_train = np.zeros((data.size, data.max() + 1))
    rows = np.arange(data.size)
    y_train[rows, data] = 1
    return y_train


def plot(loss_history: list, accuracy_history: list, filename='plot'):

    # function to visualize learning process at stage 4

    n_epochs = len(loss_history)

    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.plot(loss_history)

    plt.xlabel('Epoch number')
    plt.ylabel('Loss')
    plt.xticks(np.arange(0, n_epochs, 4))
    plt.title('Loss on train dataframe from epoch')
    plt.grid()

    plt.subplot(1, 2, 2)
    plt.plot(accuracy_history)

    plt.xlabel('Epoch number')
    plt.ylabel('Accuracy')
    plt.xticks(np.arange(0, n_epochs, 4))
    plt.title('Accuracy on test dataframe from epoch')
    plt.grid()

    plt.savefig(f'{filename}.png')


def scale(X_train, X_test):
	return X_train / X_train.max(), X_test / X_test.max()


def xavier(n_in, n_out):
    limit = np.sqrt(6.) / np.sqrt(n_in + n_out)
    return np.random.uniform(-limit, limit, (n_in, n_out))


def sigmoid(x):
    return 1. / (1. + np.exp(-x))


def d_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


def mse(y_pred, y_true):
    return np.mean((y_pred - y_true) ** 2)


def d_mse(y_pred, y_true):
    return 2 * (y_pred - y_true)


class OneLayerNeural:
    def __init__(self, n_features, n_classes):
        # Initiate weights and biases using Xavier
        self.w = xavier(n_features, n_classes)
        self.b = xavier(1, n_classes)
        self.f_forward = None

    def forward(self, X):
        # Perform a forward step
        self.f_forward = sigmoid(X @ self.w + self.b)
        return self.f_forward

    def backprop(self, X, y, alpha=0.1):
	    # Calculating gradients for each of
	    # your weights and biases.
        z = X @ self.w + self.b
        grad_mse = d_sigmoid(z) * d_mse(self.f_forward, y) / X.shape[0]
        grad_w = X.T @ grad_mse
        grad_b = np.sum(grad_mse, axis=0)

	    # Updating your weights and biases.
        self.w -= alpha * grad_w
        self.b -= alpha * grad_b

if __name__ == '__main__':

    if not os.path.exists('../Data'):
        os.mkdir('../Data')

    # Download data if it is unavailable.
    if ('fashion-mnist_train.csv' not in os.listdir('../Data') and
            'fashion-mnist_test.csv' not in os.listdir('../Data')):
        print('Train dataset loading.')
        url = "https://www.dropbox.com/s/5vg67ndkth17mvc/fashion-mnist_train.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/fashion-mnist_train.csv', 'wb').write(r.content)
        print('Loaded.')

        print('Test dataset loading.')
        url = "https://www.dropbox.com/s/9bj5a14unl5os6a/fashion-mnist_test.csv?dl=1"
        r = requests.get(url, allow_redirects=True)
        open('../Data/fashion-mnist_test.csv', 'wb').write(r.content)
        print('Loaded.')

    # Read train, test data.
    raw_train = pd.read_csv('../Data/fashion-mnist_train.csv')
    raw_test = pd.read_csv('../Data/fashion-mnist_test.csv')

    X_train = raw_train[raw_train.columns[1:]].values
    X_test = raw_test[raw_test.columns[1:]].values

    y_train = one_hot(raw_train['label'].values)
    y_test = one_hot(raw_test['label'].values)

    X_train_scaled, X_test_scaled = scale(X_train, X_test)

    model = OneLayerNeural(X_train_scaled.shape[1], 10)
    model.forward(X_train_scaled[:2])
    model.backprop(X_train_scaled[:2], y_train[:2])

    a = np.array([-1, 0, 1, 2])
    b = np.array([4, 3, 2, 1])
    print(
        np.array([mse(a, b)]).tolist(),
        d_mse(a, b).tolist(),
        d_sigmoid(a).tolist(),
        np.array([mse(model.forward(X_train_scaled[:2]), y_train[:2])])
    )