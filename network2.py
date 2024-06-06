import random
import pickle
import numpy as np

class Network2(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        self.activation = softplus
        self.activation_prime = softplus_prime



    def SGD(self, learning_rate, epochs):
        with open('AllImageData.pkl', 'rb') as f:
            training_data_list = pickle.load(f)
        list_length = len(training_data_list)
        random.shuffle(training_data_list)
        print(training_data_list)



        

def softplus(z):
    return np.log(1+np.exp(z))

def softplus_prime(z):
    return np.exp(z)/(1+np.exp(z))

net = Network2([160000,30,160000])
Network2.SGD(net, 3, 10)