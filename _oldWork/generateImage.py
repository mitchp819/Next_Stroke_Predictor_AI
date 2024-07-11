from PIL import Image
import numpy as np

def create_image_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    #for each line strip white space before and after and split each floar divided by space
    image_data = [list(map(float, line.strip().split())) for line in lines]

    image_array = np.array(image_data, dtype = np.uint8)
    image_array = image_array * 255
    image = Image.fromarray(image_array)
    image.save('genImage.png')

def create_image_from_np(image):
    image_array = [i*255 for i in image]
    np_image_array = np.array(image_array)
    np_image = np.split(np_image_array,500)
    print(np_image)
    image = Image.fromarray(np_image)
    image.save('genNPImage.png')

