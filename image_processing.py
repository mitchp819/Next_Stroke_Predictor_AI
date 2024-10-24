import numpy as np
import sys
#np.set_printoptions(threshold=sys.maxsize)
from PIL import Image
import random


class img_processer:
    def __init__(self, data_set_128_file: str, data_set_64_file: str = None, data_set_32_file: str = None,
                  data_set_16_file: str = None, data_set_8_file: str= None, data_set_4_file: str = None, input_data = None):
       
        self.data_set = np.load(data_set_128_file)
        #np.random.shuffle(self.data_set)
        print(f"Data Set of shape {self.data_set.shape} Loaded")

        if data_set_64_file != None:
            self.data_set_64 = np.load(data_set_64_file)
        if data_set_32_file != None:
            self.data_set_32 = np.load(data_set_32_file)
        if data_set_16_file != None:
            self.data_set_16 = np.load(data_set_16_file)
        if data_set_8_file != None:
            self.data_set_8 = np.load(data_set_8_file)
        if data_set_4_file != None:
            self.data_set_4 = np.load(data_set_4_file)

        #is this needed? 
        self.input_data = input_data

        self.lowest_varience = 100
        self.output_variance = -1
        self.best_image_index = -1
        self.tolerance = 500
        self.previous_matchs = []
        
        
    def get_variance(self):
        return self.output_variance
        
    def set_tolerance(self, t):
        self.tolerance = t

    def canvas_np_img_to_png(self, canvas_data, save_name):
        '''Turns a np array with values 0-1 and a extranious last element into a png image.'''
        #Remove the last value which is a color placeholder value and multiply by 255 to get correct values
        image = canvas_data[:-1]
        image = image * 255
        Image.fromarray(self.shape_img(image).astype('uint8'), 'L').save(save_name)
        print(f"image saved under: {save_name}")
    
    def shape_img (self,image):
        '''Turns a flattened np array into an image format. Note deminsion must be square.'''
        side_length = int(np.sqrt(image.shape[0]))
        shaped_image = np.reshape(image, (side_length, side_length))
        return shaped_image
    
    
    def compare_img_with_dataset(self, input_image):
        index_list = []
        lowest_varience = 1000000
        best_index = -1
        for index, data in enumerate(self.data_set):
            element = data[0, :]
            diff_array = np.abs(input_image - element)
            diff = np.sum(diff_array)
            if diff < lowest_varience:
                lowest_varience = diff
                best_index = index
                print(f"Difference = {diff}")
            if diff < lowest_varience + self.tolerance:
                index_list.append(index)
        #print(lowest_varience)
        #print(index_list)
        print(best_index)
        self.canvas_np_img_to_png(self.data_set[best_index,0,:], "similar_img.png")
        best_associated_stroke = self.data_set[best_index, 1, :]
        #print(best_associated_stroke.shape)
        return best_associated_stroke
