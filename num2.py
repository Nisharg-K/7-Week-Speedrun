import numpy as np


# SHAPE & INSPECTION

arr_1d = np.array([22, 25, 21, 18, 24, 27, 20, 19, 23, 26])

print("1D Array Shape:", arr_1d.shape)  
print("---")

#RESHAPING DATA

# Original array with 20 elements
data = np.array([22, 25, 21, 18, 24, 27, 20, 19, 23, 26, 22, 25, 21, 18, 24, 27, 20, 19, 23, 26])

# Manual Reshape
grid_4x5 = data.reshape(4, 5)

# Auto-Reshape
data_12 = data[:12]
grid_auto = data_12.reshape(3, -1) 

print("Reshaped 4x5 Grid:\n", grid_4x5)
print("\nReshaped 3x4 (Auto) Grid:\n", grid_auto)
print("---")


# SLICING & CREATION
square = np.arange(0, 12).reshape(3, 4)[0:2, 0:2]

print("Top-left 2x2 slice:\n", square)
print("---")


# BOOLEAN INDEXING

scores = np.array([
    [85, 90, 78, 92],
    [88, 82, 95, 89],  
    [75, 80, 85, 70]   
])

mask = scores > 90

print("Boolean Mask (Scores > 90):\n", mask)
print("\nActual High Scores:", scores[mask])