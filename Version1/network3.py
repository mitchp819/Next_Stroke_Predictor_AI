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
        #open pickled file
        with open('PickledAllImageData.pkl', 'rb') as file:
            training_data = pickle.load(file)
        
        training_data = list(training_data)
        n = len(training_data)
        
        for j in range(epochs):
            random.shuffle(training_data)
            mini_batches = [training_data[k:k + mini_batch_size] for k in range(0, n, mini_batch_size)]
            for mini_batch in mini_batches:
                self.update_mini_batch(mini_batch, learning_rate)
            print(f"Epoch {j} complete")
    
    def update_mini_batch(self, mini_batch, learning_rate):
        #creates copys of biases and weights filled with zeros 
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        for x,y in mini_batch:
            print(x)
                
           

        

def softplus(z):
    return np.log(1+np.exp(z))

def softplus_prime(z):
    return np.exp(z)/(1+np.exp(z))

net = Network2([160000,30,160000])
Network2.SGD(net, 3, 2, 10)