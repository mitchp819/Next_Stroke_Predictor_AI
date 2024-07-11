import random
import numpy as np
import generateImage

class Network(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        self.activation = softplus
        self.activation_prime = softplus_prime

    def SGD(self, images_list, learning_rate, epochs, canvas_size):
        """
        image_list: List of paths to image files each containing every frame 
        each image is its own mini batch. 

        for each epoch 
            for each image file 
                update network 
        """
        images_list = list(images_list) 
        n = len(images_list)
        
        for j in range(epochs):
            random.shuffle(images_list)
            for image_file in images_list:
                print("updating network with image {}".format(image_file))
                self.update_network(image_file, learning_rate, canvas_size)
            print("Epoch {} compete".format(j)) 
            
    def update_network(self, image_file, learning_rate, canvas_size):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        with open(image_file, 'r') as file:
            lines = file.readlines()
        image_data = [list(map(float, line.strip().split())) for line in lines]
        image_array = np.array(image_data, dtype=np.single)

        
        print("shape of images in array{}".format(image_array.shape))
        
        image_count = image_array.shape[0]//canvas_size
        image_count
        print(image_count)

        for x in range(image_count):
            i = x * canvas_size 
            print("i = ", i)
            sub_array = []
            while(i < x * canvas_size + canvas_size  ):
                for item in image_array[i] :
                    sub_array.append(item)
                i += 1
            print(len(sub_array))
            delta_nabla_b, delta_nabla_w = self.backprop(sub_array, canvas_size)
            nabla_b = [nb + dnb for nb, dnb in zip(nabla_b, delta_nabla_b)]
            nabla_w = [nw + dnw for nw, dnw in zip(nabla_w, delta_nabla_w)]
            pass
            

    

    def backprop(self, x, canvas_size):
        nabla_b = [np.zeros(b.shape) for b in self.biases]
        nabla_w = [np.zeros(w.shape) for w in self.weights]

        #forward pass
        activation = x
        activations = [x]
        zs = []
        for b, w in zip(self.biases, self.weights):
            z = np.dot(w, activation) + b
            zs.append(z)
            activation = self.activation(z)
            activations.append(activation)
        
        generateImage.create_image_from_np(activations)

        return (nabla_b, nabla_w)





        


def softplus(z):
    return np.log(1+np.exp(z))

def softplus_prime(z):
    return np.exp(z)/(1+np.exp(z))