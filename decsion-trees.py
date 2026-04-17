#Now it's time for decision trees! This is a powerful algorithm that can be used for both classification and regression tasks. Let's start with a simple implementation of a decision tree for classification.
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt

iris = load_iris()
x = iris.data
y = iris.target
xtr, xts, ytr, yts = train_test_split(x, y, test_size=0.2, random_state=42)
model = DecisionTreeClassifier()
model.fit(xtr, ytr)
print("Done Training")

y_pred = model.predict(xts)
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(yts, y_pred)
print("Accuracy:", accuracy)

# Let's also visualize the decision tree using matplotlib and graphviz
from sklearn.tree import plot_tree
plt.figure(figsize=(12,8))
plot_tree(model, filled=True, feature_names=iris.feature_names, class_names=iris.target_names)
plt.show()
