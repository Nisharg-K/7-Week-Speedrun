#K-Means using Scikit-learn

import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Generate synthetic data
from sklearn.datasets import make_blobs 
X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
# Fit K-Means
kmeans = KMeans(n_clusters=4)

kmeans.fit(X)
# Get the cluster centers and labels
centers = kmeans.cluster_centers_
labels = kmeans.labels_

# Plot the clusters and centroids
plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', marker='o', edgecolor='k', s=100)
plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='X', s=200, label='Centroids')
plt.title('K-Means Clustering')
plt.xlabel('Feature 1')
plt.ylabel('Feature 2')
plt.legend()
plt.show()
