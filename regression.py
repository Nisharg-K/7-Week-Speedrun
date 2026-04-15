from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score  
import matplotlib.pyplot as plt


digits = load_digits()

x = digits.data
y = digits.target

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)    
print(x_train.shape)
print(x_test.shape)


model = LogisticRegression(max_iter=1000)


model.fit(x_train, y_train)

print("Done Training")

y_pred = model.predict(x_test)


accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("Predicted:", y_pred[:25])
print("Actual   :", y_test[:25])





