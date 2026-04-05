import numpy as np

# BROADCASTING
prices = np.array([100, 200, 300])
discount = np.array([0.1])
discounted_prices = prices - (prices * discount)

print("Discounted Prices:\n", discounted_prices)
print("---")

# TWO-WAY BROADCASTING
A = np.array([[10], [20], [30]]) 
B = np.array([1, 2, 3])          
grid_add = A + B

print("Two-Way Broadcast (3x3):\n", grid_add)
print("---")

# STACKING ARRAYS
class_a = np.array([101, 102, 103])
class_b = np.array([201, 202, 203])

h_stack = np.hstack((class_a, class_b))
v_stack = np.vstack((class_a, class_b))

print("Horizontal Stack:\n", h_stack)
print("Vertical Stack:\n", v_stack)
print("---")

# RANDOM DATA & MATH ACROSS AXES
raw_temp = np.random.randint(15, 36, 168)
days_and_hrs = raw_temp.reshape(7, 24)

hourly_avg = days_and_hrs.mean(axis=0)
daily_max = days_and_hrs.max(axis=1)

print("Hourly Averages (24 elements):\n", hourly_avg)
print("\nDaily Maximums (7 elements):\n", daily_max)