import numpy as np


class Perceptron:
    def __init__(self):
        self.weights = np.random.uniform(-1, 1, 2)

    def guess(self, inputs):
        summation = np.dot(inputs, self.weights)
        return 1 if summation > 0 else 0 
    
    def train(self, inputs, target):
        guess = self.guess(inputs)
        error = target - guess
        
        for i in range(len(self.weights)):
            self.weights[i] += error * inputs[i]

                            