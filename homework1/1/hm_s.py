import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

iris = load_iris()
X = iris.data


def show_table(centroids, labels, i):
    plt.scatter(centroids[:, 0], centroids[:, 1], c='blue', marker='x', label='Центроиды на шаге {}'.format(i + 1))
    for j in range(optimal_n_clusters):
        plt.scatter(X[labels == j, 0], X[labels == j, 1], label='Кластер {}'.format(j + 1))

    print(i)

    plt.legend()
    plt.title('Шаг {}'.format(i + 1))
    plt.xlabel('Sepal Length')
    plt.ylabel('Sepal Width')
    plt.show()


# Реализация алгоритма k-means
def k_means(X, n_clusters, max_iters=24):
    centroids = X[np.random.choice(range(len(X)), n_clusters, replace=False)]

    for i in range(max_iters):
        distances = np.sqrt(((X - centroids[:, np.newaxis]) ** 2).sum(axis=2))
        labels = np.argmin(distances, axis=0)

        prev_centroids = centroids.copy()

        for j in range(n_clusters):
            centroids[j] = np.mean(X[labels == j], axis=0)

        if np.all(prev_centroids == centroids):
            break

        show_table(centroids, labels, i)

    return centroids, labels


optimal_n_clusters = 3
centroids, labels = k_means(X, optimal_n_clusters)

plt.figure(figsize=(10, 6))

# Выводим начальные центроиды
plt.scatter(X[:, 0], X[:, 1], c='gray', marker='o', label='Исходные точки')
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', marker='x', label='Начальные центроиды')

centroids, labels = k_means(X, optimal_n_clusters)
