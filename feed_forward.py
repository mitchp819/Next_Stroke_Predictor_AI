import os
import pickle
import numpy as np
class feedforward_network(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1).astype(np.float16) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x).astype(np.float16) for x, y in zip(sizes[:-1], sizes[1:])]
        self.activation = softplus

    def feedforward(self, input, input_weights, input_biases):
            input = input[:, np.newaxis]
            print(input.shape)
            for b, w in zip(self.biases, self.weights):
                print(a.shape)
                input = softplus(np.dot(w, input) + b)
            return input

    def load_data(self, input_weights, input_biases):
        with open(input_weights, 'rb') as w:
            self.weights = pickle.load(w)
        with open(input_biases, 'rb') as b:
            self.biases = pickle.load(b)
        print("Data loaded")
        print(self.weights[0])
        print(len(self.biases))


def softplus(z):
    z = np.nan_to_num(z, nan=0.0, posinf=np.finfo(np.float64).max, neginf=np.finfo(np.float64).min)
    return np.logaddexp(0,z)

net = feedforward_network([16385, 512, 1024,16385])

net.load_data('weights.pkl', 'biases.pkl')