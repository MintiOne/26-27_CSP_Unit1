import numpy as np

class neuron:
    def __init__(self, weight, bias):
        self.weight = weight
        self.bias = bias
        self.z = 0
        self.activation = 0
    def forward(self, x):
        self.z = self.weight * x + self.bias
        self.activation = 1 / (1 + np.exp(-self.z))
        return self.activation

inputs = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]
outputs = [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4]