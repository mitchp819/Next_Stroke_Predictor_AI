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



    def SGD(self, learning_rate, epochs, mini_batch_size):
        #maybe do this and pickle to make it faster to load data
        input_data = np.load('NPY_AllImageData160000.npy')
        n = input_data.shape[0]
        training_data = []
        zipped_data_point = zip(input_data[5, 0, :], input_data[5, 1, :])
        print(zipped_data_point)
        for x in range(n):
            zipped_data_point = zip(input_data[x, 0, :], input_data[x, 1, :])
            training_data.append(zipped_data_point)
        



"""         n = training_data.shape[0]
        
        for j in range(epochs):
            #shuffles training data along axis=0
            idx = np.random.rand(*training_data.shape).argsort(axis=0)
            np.take_along_axis(training_data, idx, axis=0)

            #splits training data into minibatches 
            num_groups = training_data.shape[0]//mini_batch_size
            mini_batches = np.array_split(training_data, num_groups)

            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, learning_rate)
            print("Epoch {} complete".format(j))

    def update_mini_batch(self, mini_batch, learning_rate):
        #creates copys of biases and weights filled with zeros 
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        for image in mini_batch: """



        

def softplus(z):
    return np.log(1+np.exp(z))

def softplus_prime(z):
    return np.exp(z)/(1+np.exp(z))

net = Network2([160000,30,160000])
Network2.SGD(net, 3, 2, 10)