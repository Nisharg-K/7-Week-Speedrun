from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

data = fetch_california_housing()

x = data.data
y = data.target

xtr, xts, ytr, yts = train_test_split(x, y, test_size=0.2, random_state=42)


model = LinearRegression()
model.fit(xtr, ytr)

print("Done Training")



y_pred = model.predict(xts)



mse = mean_squared_error(yts, y_pred)
r2 = r2_score(yts, y_pred)
print("Mean Squared Error:", mse)
print("R^2 Score:", r2)

#in percentage accuracy
accuracy = r2 * 100
print("Accuracy:", accuracy, "%")
