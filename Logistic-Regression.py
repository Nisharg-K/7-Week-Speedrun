import numpy as np
import matplotlib.pyplot as plt

x_train = np.array([1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0])

y_train = np.array([300.0, 450.0, 500.0, 750.0, 800.0, 1050.0, 1200.0])

m = len(x_train)

print(m)


plt.scatter(x_train, y_train, marker='x', color='red')
plt.title('Training Data')
plt.xlabel('Size of House (1000 sqft)')
plt.ylabel('Price of House (1000 dollars)')
plt.show()

def compute_model_output(x, w, b):

    
    m = x.shape[0]
    y = np.zeros(m)
    
    for i in range(m):
        y[i] = w * x[i] + b
        
    return y

def compute_cost(x, y, w, b):
    m = x.shape[0]
    cost = 0.0
    
    for i in range(m):
        f_wb_i = w * x[i] + b
        cost = cost + (f_wb_i - y[i]) ** 2
        
    cost = cost / (2 * m)
    
    return cost

w = 100.0
b = 100.0

cost = compute_cost(x_train, y_train, w, b)
print(f"Cost at w={w}, b={b} is {cost}")