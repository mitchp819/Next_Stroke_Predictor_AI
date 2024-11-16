import numpy as np
from PIL import Image
import os
import re
import random

def canvas_np_img_to_png(canvas_data, save_name):
        '''Turns a np array with values 0-1 and a extranious last element into a png image.'''
        #Remove the last value which is a color placeholder value and multiply by 255 to get correct values
        image = canvas_data[:-1]
        image = image * 255
        Image.fromarray(shape_img(image).astype('uint8'), 'L').save(save_name)
        print(f"image saved under: {save_name}")

def shape_img (image):
    '''Turns a flattened np array into an image format. Note deminsion must be square.'''
    side_length = int(np.sqrt(image.shape[0]))
    shaped_image = np.reshape(image, (side_length, side_length))
    return shaped_image

def get_last_file_by_id(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    files_list = [f for f in os.listdir(dir_path)
                  if os.path.isfile(os.path.join(dir_path, f))]
    largest_id = 0 
    for file in files_list:
        integers = [int(s) for s in re.findall(r'\d+', file)]
        if(integers[0] > largest_id):
            largest_id = integers[0]
    return largest_id

def greyscale_value_to_hex(value):
     return f"#{value:02x}{value:02x}{value:02x}"