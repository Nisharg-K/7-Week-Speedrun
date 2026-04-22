from sklearn.decomposition import PCA
from sklearn.svm import SVC
from sklearn.datasets import make_classification

X, y = make_classification(n_samples=300, n_features=20, n_informative=10, n_redundant=10, random_state=0)

pca = PCA(n_components=5)
X_reduced = pca.fit_transform(X)
model = SVC()

model.fit(X_reduced, y)

print(f"Training Accuracy: {model.score(X_reduced, y):.2f}")

