import random
import pickle
import numpy as np

class Network2(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y,1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        self.activation = softplus
        self.activation_prime = softplus_prime



    def SGD(self, learning_rate, epochs, mini_batch_size):
        #maybe do this and pickle to make it faster to load data
        training_data = np.load('NPY_AllImageData160000.npy')

        n = training_data.shape[0]
        
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

        for image in mini_batch:
            delta_nabla_b, delta_nabla_w = self.backprop(image[0,:], image[1,:])
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
        self.weights = [w - (learning_rate / len(mini_batch)) * nw for w, nw in zip(self.weights, nabla_w)]
        self.biases = [b - (learning_rate / len(mini_batch)) * nb for b, nb in zip(self.biases, nabla_b)]



    def backprop(self, canvas, stroke):
        """It is assumed that the input a is an (n, 1) Numpy ndarray, not a (n,) vector.
        Here, n is the number of inputs to the network.
        If you try to use an (n,) vector as input you'll get strange results. 
        Although using an (n,) vector appears the more natural choice, 
        using an (n, 1) ndarray makes it particularly easy to modify the code to feedforward multiple inputs at once, 
        and that is sometimes convenient."""
        canvas = canvas[:, np.newaxis]
        stroke = stroke[:, np.newaxis]

        #creates copys of biases and weights filled with zeros 
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]
        
        #feedforward: store output of each layer in list activations
        activation = canvas
        activations = [canvas]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = softplus(z)
            activations.append(activation)

        #backward pass 
        delta = self.cost_derivative(activations[-1], stroke) * softplus_prime(zs[-1])
        nabla_b[-1] = delta
        nabla_w[-1] = np.dot(delta, activations[-2].transpose())
        for l in range(2, self.num_layers):
            z = zs[-l]
            sp = self.activation_prime(z)
            delta = np.dot(self.weights[-l + 1].transpose(), delta) * sp
            nabla_b[-l] = delta
            nabla_w[-l] = np.dot(delta, activations[-l - 1].transpose())
    
        return (nabla_b, nabla_w)
    


    def cost_derivative(self, output_activations, y):
        return (output_activations - y)
    


    def feedforward(self, a):
        a = a[:, np.newaxis]
        for b, w in zip(self.biases, self.weights):
            a = self.activation(np.dot(w, a) + b)
        return a



def softplus(z):
    z = np.nan_to_num(z, nan=0.0, posinf=np.finfo(np.float64).max, neginf=np.finfo(np.float64).min)
    return np.logaddexp(0,z)

def softplus_prime(z):
    # Clip z to avoid overflow
    z = np.clip(z, -500, 500)
    
    # Compute the sigmoid function
    with np.errstate(over='ignore', invalid='ignore'):
        result = np.where(z > 30, 1.0, np.exp(z) / (1 + np.exp(z)))
    
    return result


net = Network2([160000, 100, 50, 160000])
Network2.SGD(net, 3, 2, 10)

input_data = np.load('ImageData/image1data.npy')
generated_data = Network2.feedforward(input_data)
print(generated_data.shape)
np.save('generated_image.npy', generated_data)