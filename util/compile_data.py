import numpy as np
import glob
import os
import helper_functions as hlp_fun

def compile_data(dataset_folder_path):
    data_folder_path = dataset_folder_path + "/ImageData16384/*.npy"
    original_np_data = cat_data_folder(data_folder_path)
    
    pass

def cat_data_folder(data_folder_path):
    path = os.path.join(os.path.dirname(__file__), data_folder_path)
    files = sorted(glob.glob(path))
    master_array = []
    for f in files:
        master_array.append(np.load(f))
    result = np.concatenate(master_array,axis=0)
    return result

def flip_and_rotate_dataset(dataset):
    for index, subset in enumerate(dataset):
        canvas = subset[0,:]
        stroke = subset[1,:]

        
    pass

def rotate_image(img):
    color_value = img[-1]
    img = img[:-1]
    shaped_img = hlp_fun.shape_img(img)
    rotated_img = np.rot90(shaped_img)
    rotated_img = rotated_img.flatten()
    rotated_img = np.append(rotated_img, color_value)
    return rotated_img

def mirror_image_horizontal(img):
    color_value = img[-1]
    img = img[:-1]
    shaped_img = hlp_fun.shape_img(img)
    h_mirrored_img = np.fliplr(shaped_img)
    h_mirrored_img = np.append(h_mirrored_img, color_value)
    return h_mirrored_img
   
def mirror_image_vertical(img):
    color_value = img[-1]
    img = img[:-1]
    shaped_img = hlp_fun.shape_img(img)
    v_mirrored_img = np.flipud(shaped_img)
    v_mirrored_img = np.append(v_mirrored_img, color_value)
    return v_mirrored_img

compile_data('data/original-ds')
