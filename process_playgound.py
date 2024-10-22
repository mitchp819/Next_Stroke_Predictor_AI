import numpy as np
import sys
#np.set_printoptions(threshold=sys.maxsize)
from PIL import Image
import random

data_set = np.load("NPY_AllImageData16385.npy")

white_canvas = np.ones(16385)
white_canvas[-1] = .5

print(white_canvas)

num_elements = data_set.shape[0]

count = 0 
for data in data_set:
    comaprison_element = data[0,:]
    diff_array = np.subtract(white_canvas, comaprison_element)
    diff = np.sum(diff_array)
    if diff < 5:
        count += 1
print(count)
         