import numpy as np
import glob
import os


def compile_data(dataset_folder_path):
    data_folder_path = dataset_folder_path + "/ImageData16384/*.npy"
    path = os.path.join(os.path.dirname(__file__), data_folder_path)
    files = sorted(glob.glob(path))

    
    pass


compile_data('data/original-ds')
