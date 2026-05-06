import tensorflow as tf
import numpy as np

# STEP 1 — Dataset
x = np.array([1, 2, 3, 4], dtype=np.float32) 
y = np.array([3, 5, 7, 9], dtype=np.float32) 


# STEP 2 — Initialize Parameters
w = tf.Variable(0.5)
b = tf.Variable(0.1)

# STEP 3 — Hyperparameters
learning_rate = 0.01
epochs = 1000

# STEP 4 — Training Loop
for epoch in range(epochs):

    # Record operations for automatic differentiation
    with tf.GradientTape() as tape:

        # Forward Propagation
        y_pred = w * x + b

        # Loss Calculation (MSE)
        loss = tf.reduce_mean((y_pred - y) ** 2)

    # STEP 5 — Compute Gradients
    dw, db = tape.gradient(loss, [w, b])

    # STEP 6 — Gradient Descent Update
    w.assign_sub(learning_rate * dw)
    b.assign_sub(learning_rate * db)

    # Print progress
    if epoch % 100 == 0:
        print(f"Epoch {epoch}")
        print(f"Loss: {loss.numpy():.4f}")
        print(f"w: {w.numpy():.4f}, b: {b.numpy():.4f}")
        print("-------------------")

# Final Result
print("Training Complete")
print(f"Final Weight (w): {w.numpy()}")
print(f"Final Bias (b): {b.numpy()}")