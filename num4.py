import numpy as np

# Calculating a single prediction from an artificial neuron
inputs = np.array([2, 3])
weights = np.array([4, 5])
prediction = inputs @ weights
print(f"Inputs: {inputs}")
print(f"Weights: {weights}")
print(f"Dot Product Prediction (2*4 + 3*5): {prediction}\n")


# Flipping axes (Remember: It requires a 2D array to actually flip visually!)
inputs_2d = np.array([[0.5, -0.2, 0.8]]) 
print(f"Original 2D Shape: {inputs_2d.shape}")
print(inputs_2d)

input_transpose = inputs_2d.T
print(f"\nTransposed Shape: {input_transpose.shape}")
print(input_transpose, "\n")

# Generating random AI weights clustered around 0
random_weights = np.random.randn(5)
print(f"5 Random Weights (Standard Normal Distribution):\n{random_weights}")

# Proving the statistical center
massive_sample = np.random.randn(10000)
print(f"Average of 10,000 weights (Should be very close to 0): {massive_sample.mean():.4f}\n")


# Cleaning corrupted data instantly without loops
ages = np.array([25, 30, -1, 45, -1])
print(f"Original Data: {ages}")

# np.where(condition, value_if_true, value_if_false)
cleaned_ages = np.where(ages < 0, 20, ages)
print(f"Cleaned Data:  {cleaned_ages}\n")

# 1. Flattening a 2D image grid into a 1D line
image = np.array([
    [255, 128], 
    [ 64,   0]
])
print("Original 2x2 Image:")
print(image)

flat_image = image.flatten()
print(f"\nFlattened 1D Image: {flat_image} | Shape: {flat_image.shape}")

# 2. Adding a New Axis (np.newaxis) to create a vertical 'batch'
vertical_batch = flat_image[:, np.newaxis]
print(f"\nVertical Batch Shape: {vertical_batch.shape}")
print(vertical_batch)