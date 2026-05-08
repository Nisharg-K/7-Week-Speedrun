import math

# -----------------------------
# STEP 1 — Sigmoid Function
# -----------------------------
def sigmoid(x):
    return 1 / (1 + math.exp(-x))


# -----------------------------
# STEP 2 — Training Data
# -----------------------------
x = 2
y = 9
#x and y are the input and output of our training data. We will use this data to train our neural network to learn the relationship between x and y.
#we can add multiple data points to make the training more robust

# -----------------------------
# STEP 3 — Initialize Parameters
# -----------------------------
w1 = 0.5
b1 = 0.1

w2 = 0.3
b2 = 0.2


# -----------------------------
# STEP 4 — Hyperparameters
# -----------------------------
learning_rate = 0.1
epochs = 1000


# -----------------------------
# STEP 5 — Training Loop
# -----------------------------
for epoch in range(epochs):

    # =============================
    # FORWARD PROPAGATION
    # =============================

    # Hidden layer
    h = w1 * x + b1

    # Activation
    a_h = sigmoid(h)

    # Output layer
    y_pred = w2 * a_h + b2

    # =============================
    # LOSS FUNCTION
    # =============================

    loss = (y_pred - y) ** 2

    # =============================
    # BACKPROPAGATION
    # =============================

    # dL/dy_pred
    dL_dypred = 2 * (y_pred - y)

    # Gradients for output layer
    dL_dw2 = dL_dypred * a_h
    dL_db2 = dL_dypred

    # Sigmoid derivative
    da_h_dh = a_h * (1 - a_h)

    # Chain rule backward
    dL_dh = dL_dypred * w2 * da_h_dh

    # Gradients for hidden layer
    dL_dw1 = dL_dh * x
    dL_db1 = dL_dh

    # =============================
    # GRADIENT DESCENT
    # =============================

    w1 = w1 - learning_rate * dL_dw1
    b1 = b1 - learning_rate * dL_db1

    w2 = w2 - learning_rate * dL_dw2
    b2 = b2 - learning_rate * dL_db2

    # =============================
    # PRINT PROGRESS
    # =============================

    if epoch % 100 == 0:
        print(f"Epoch {epoch}")
        print(f"Loss: {loss:.6f}")
        print(f"Prediction: {y_pred:.6f}")
        print("---------------------")


# -----------------------------
# FINAL RESULTS
# -----------------------------
print("\nTraining Complete")
print(f"Final Prediction: {y_pred}")
print(f"Final Loss: {loss}")

print("\nFinal Parameters:")
print(f"w1 = {w1}")
print(f"b1 = {b1}")
print(f"w2 = {w2}")
print(f"b2 = {b2}")

print("Accuracy:", 1 - loss)
print("Actual Value:", y)