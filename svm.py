from sklearn.model_selection import train_test_split

from sklearn.datasets import load_iris

from sklearn.svm import SVC

from sklearn.metrics import accuracy_score



iris = load_iris()

x = iris.data
y = iris.target

xtr, xts, ytr, yts = train_test_split(x, y, test_size=0.2, random_state=42)
svm = SVC(kernel='linear')
svm.fit(xtr, ytr)

print("Done Training")

y_pred = svm.predict(xts)
accuracy = accuracy_score(yts, y_pred)
print("Accuracy:", accuracy)
