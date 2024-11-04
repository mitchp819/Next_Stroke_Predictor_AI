import numpy as np
from PIL import Image
import random
import helper_functions as hf
import downscale_data as ds


class img_processer:
    def __init__(self, data_set_128_file: str, data_set_64_file: str = None, data_set_32_file: str = None,
                  data_set_16_file: str = None, data_set_8_file: str= None, data_set_4_file: str = None, input_data = None):
        
        self.downscaled_data  = []
        self.data_set = np.load(data_set_128_file)
        self.downscaled_data.append(self.data_set)
        self.max_index = self.data_set[0]
        print(f"Data Set of shape {self.data_set.shape} Loaded")

        if data_set_64_file != None:
            self.data_set_64 = np.load(data_set_64_file)
            self.downscaled_data.append(self.data_set_64)
            self.dataset_error_check(self.data_set, self.data_set_64)
        else:
            self.downscaled_data.append(-1)

        if data_set_32_file != None:
            self.data_set_32 = np.load(data_set_32_file)
            self.downscaled_data.append(self.data_set_32)
            self.dataset_error_check(self.data_set, self.data_set_32)
        else:
            self.downscaled_data.append(-1)
            
        if data_set_16_file != None:
            self.data_set_16 = np.load(data_set_16_file)
            self.downscaled_data.append(self.data_set_16)
            self.dataset_error_check(self.data_set, self.data_set_16)
        else:
            self.downscaled_data.append(-1)
            
        if data_set_8_file != None:
            self.data_set_8 = np.load(data_set_8_file)
            self.downscaled_data.append(self.data_set_8)
            self.dataset_error_check(self.data_set, self.data_set_8)
        else:
            self.downscaled_data.append(-1)
            
        if data_set_4_file != None:
            self.data_set_4 = np.load(data_set_4_file)
            self.downscaled_data.append(self.data_set_4)
            self.dataset_error_check(self.data_set, self.data_set_4)
        else:
            self.downscaled_data.append(-1)

        
        self.downscaled_data_length = len(self.downscaled_data)
        self.lowest_varience = 100
        self.output_variance = -1
        self.best_image_index = -1
        self.tolerance = 500
        self.previous_matchs = []
        self.prev_match_range = 1
        self.prev_matchs_list_size = 100
        pass
        
        
    def get_variance(self):
        return self.output_variance
        
    def set_tolerance(self, t):
        self.tolerance = t
        pass
    
    def set_data_set(self, ds):
        self.data_set = np.load(ds)
        pass
    
    def dataset_error_check(self, d1, d2):
        d1_shape_0 = d1.shape[0]
        d2_shape_0 = d2.shape[0]
        if d1_shape_0 != d2_shape_0:
            print("ERROR: img_processing \n dataset error! Datasets are of different sizes")
            if d1_shape_0 < d2_shape_0:
                self.max_index = d1_shape_0
            else:
                self.max_index = d2_shape_0
            print(f"New max index = {self.max_index}")
        

    def compare_img_with_downscaled_data_set(self, input_image):

        input_img_ds1 = ds.downscale_img(input_image)
        input_img_ds2 = ds.downscale_img(input_img_ds1)
        input_img_ds3 = ds.downscale_img(input_img_ds2)
        input_img_ds4 = ds.downscale_img(input_img_ds3)
        input_img_ds5 = ds.downscale_img(input_img_ds4)
        input_ds_list = [input_image, input_img_ds1, input_img_ds2, input_img_ds3, input_img_ds4, input_img_ds5]

        if len(input_ds_list) != self.downscaled_data_length:
            print(f"\nError: img_process    compare_img_with_downscaled_data_set() \n input downscaled to a diffrent depth as dataset\n input depth = {len(input_ds_list)} \n dataset depth = {self.downscaled_data_length}")

        pass
        
    def compare_img_with_dataset(self, input_image):
        #reset variables
        temp_index_list = []
        index_list = []
        temp_index_list.clear()
        index_list.clear()
        lowest_varience = 10000000000
        
        #enumerate dataset
        for index, data in enumerate(self.data_set):
            skip_data = prev_match_check(index, self.previous_matchs,  self.prev_match_range)
            if skip_data == False: 
                diff = compare_two_images(input_image, data[0, :])
                if diff < lowest_varience:
                    lowest_varience = diff
                if diff <= lowest_varience + self.tolerance:
                    temp_index_list.append((index, diff))

        #iterate through temp list and add elements less than tolerance to index_list
        max_variance = lowest_varience + self.tolerance
        index_list = trim_data_set(temp_index_list, max_variance)

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

        hf.canvas_np_img_to_png(self.data_set[output_index,0,:], "similar_img.png")
        hf.canvas_np_img_to_png(self.data_set[output_index,1,:], "similar_stroke.png")
        best_associated_stroke = self.data_set[output_index, 1, :]

        #this should set something in draw_to_training
        return best_associated_stroke
    




def trim_data_set(input_list, max_variance):
    index_variance_list = []
    for maybe_img, maybe_variance in input_list:
            if maybe_variance <= max_variance:
                index_variance_list.append((maybe_img, maybe_variance))
    return index_variance_list


def compare_two_images(img1, img2):
        img1_shape = img1.shape[0]

        #check if same shape
        if (img1_shape != img2.shape[0]):
            print(f"\n Error: img_processor,  compare_two_images() \n img1 != img 2 \n img1 = {img1.shape} \n img2 = {img2.shape}")
            return -1

        diff_array = np.abs(img1 - img2)
        diff = np.sum(diff_array)
        variance = diff / img1_shape
        return variance

def prev_match_check(input_index, prev_match_list, drop_range):
    skip_data = False
    for old_match in prev_match_list:
        for x in range(drop_range):
            if input_index == old_match:
                skip_data = True
            if input_index == old_match + x:
                #print(f"Skipping element {index}. Index allready used recently")
                skip_data = True
            if input_index == old_match - x:
                #print(f"Skipping element {index}. Index allready used recently")
                skip_data = True
    return skip_data