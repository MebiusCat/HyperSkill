import numpy as np
from sklearn.datasets import load_wine
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

# scroll down to the bottom to implement your solution


def plot_comparison(data: np.ndarray, predicted_clusters: np.ndarray, true_clusters: np.ndarray = None,
                    centers: np.ndarray = None, show: bool = True):

    # Use this function to visualize the results on Stage 6.

    if true_clusters is not None:
        plt.figure(figsize=(20, 10))

        plt.subplot(1, 2, 1)
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=predicted_clusters, palette='deep')
        if centers is not None:
            sns.scatterplot(x=centers[:, 0], y=centers[:, 1], marker='X', color='k', s=200)
        plt.title('Predicted clusters')
        plt.xlabel('alcohol')
        plt.ylabel('malic_acid')
        plt.grid()

        plt.subplot(1, 2, 2)
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=true_clusters, palette='deep')
        if centers is not None:
            sns.scatterplot(x=centers[:, 0], y=centers[:, 1], marker='X', color='k', s=200)
        plt.title('Ground truth')
        plt.xlabel('alcohol')
        plt.ylabel('malic_acid')
        plt.grid()
    else:
        plt.figure(figsize=(10, 10))
        sns.scatterplot(x=data[:, 0], y=data[:, 1], hue=predicted_clusters, palette='deep')
        if centers is not None:
            sns.scatterplot(x=centers[:, 0], y=centers[:, 1], marker='X', color='k', s=200)
        plt.title('Predicted clusters')
        plt.xlabel('alcohol')
        plt.ylabel('malic_acid')
        plt.grid()

    plt.savefig('Visualization.png', bbox_inches='tight')
    if show:
        plt.show()


class CustomKMeans:
    def __init__(self, k):
        self.k = k
        self.centers = None

    def fit(self, X, eps=1e-6):
        self.centers = X[:self.k]

        while True:
            labels = self.predict(X)
            new_centers = self.calculate_new_centers(X, labels, self.k)
            if np.linalg.norm(self.centers - new_centers) < eps:
                break

            self.centers = new_centers

    def predict(self, X):
        return self.find_nearest_center(X, self.centers)

    @staticmethod
    def find_nearest_center(X, centers):
        labels = np.argmin(np.linalg.norm(X[:, np.newaxis] - centers, axis=2), axis=1)
        return labels

    @staticmethod
    def calculate_new_centers(X, labels, n_clusters):
        new_centers = []
        for label in range(n_clusters):
            new_centers.append(X[labels == label].mean(axis=0))
        return np.array(new_centers)

    def inertia(self, X, labels, n_clusters):
        return np.sum(
            [np.sum(
                np.linalg.norm(X[label == labels] - self.centers[label], axis=1) ** 2) for label in range(n_clusters)])

    @staticmethod
    def search_k_value(X_full):
        for n_k in range(2, 10 + 1):
            model = CustomKMeans(k=n_k)
            model.fit(X_full)

            y_pred = model.predict(X_full)
            inertia_data.append(model.inertia(X_full, y_pred, n_k))
            silhouette_data.append(silhouette_score(X_full, y_pred))

        # print(np.array(silhouette_data).tolist())
        return list(range(2, 10 + 1))[np.argmax(silhouette_data)]


if __name__ == '__main__':

    # Load data
    data = load_wine(as_frame=True, return_X_y=True)
    X_full, y_full = data

    # Permutate it to make things more interesting
    rnd = np.random.RandomState(42)
    permutations = rnd.permutation(len(X_full))
    X_full = X_full.iloc[permutations]
    y_full = y_full.iloc[permutations]

    # From dataframe to ndarray
    X_full = X_full.values
    y_full = y_full.values

    # Scale data
    scaler = StandardScaler()
    X_full = scaler.fit_transform(X_full)

    inertia_data = []
    silhouette_data = []

    best_k = CustomKMeans.search_k_value(X_full)

    model = CustomKMeans(best_k)
    model.fit(X_full)

    y_pred = model.predict(X_full)
    # plot_comparison(X_full, y_pred, y_full, model.centers)

    print(np.array(y_pred[:20]).tolist())