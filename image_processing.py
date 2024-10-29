import numpy as np
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
        self.prev_match_range = 10
        self.prev_matchs_list_size = 100
        
        
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

        #reset variables
        temp_index_list = []
        index_list = []
        temp_index_list.clear()
        index_list.clear()
        lowest_varience = 10000000000
        

        #enumerate dataset
        for index, data in enumerate(self.data_set):
            skip_data = False

            #check if element is a previous match
            for old_match in self.previous_matchs:
                for x in range(self.prev_match_range):
                    if index == old_match + x:
                        print(f"Skipping element {index}. Index allready used recently")
                        skip_data = True
                    if index == old_match - x:
                        print(f"Skipping element {index}. Index allready used recently")
                        skip_data = True
            
            if skip_data == False: 
                #finds variance
                element = data[0, :]
                diff_array = np.abs(input_image - element)
                diff = np.sum(diff_array)
                skip_data = False

                if diff < lowest_varience:
                    lowest_varience = diff
                    print(f"New Best Element Found: Index {index} Difference = {diff}")
                if diff <= lowest_varience + self.tolerance:
                    temp_index_list.append((index, diff))

        #iterate through temp list and add elements less than tolerance to index_list
        max_variance = lowest_varience + self.tolerance
        for maybe_img, maybe_variance in temp_index_list:
            print(f"img index {maybe_img}, variance {maybe_variance}")
            if maybe_variance <= max_variance:
                index_list.append((maybe_img, maybe_variance))
        
        #Error Check
        if (len(index_list) == 0): 
            print("No Match Found")
            return -1
        
        #pick random image from list
        output_index, self.output_variance = random.choice(index_list)
        print(f"Output index = {output_index}, Output Variance = {self.output_variance}")

        #add output to previous matches and remove element if to long
        self.previous_matchs.append(output_index)
        if len(self.previous_matchs) > self.prev_matchs_list_size : 
            self.previous_matchs = self.previous_matchs[1:]

        print(f"len of prev matches = {len(self.previous_matchs)}")

        self.canvas_np_img_to_png(self.data_set[output_index,0,:], "similar_img.png")
        self.canvas_np_img_to_png(self.data_set[output_index,1,:], "similar_stroke.png")
        best_associated_stroke = self.data_set[output_index, 1, :]
        return best_associated_stroke
