from PIL import Image
import numpy as np

def create_image(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    #for each line strip white space before and after and split each int divided by space
    image_data = [list(map(float, line.strip().split())) for line in lines]

    image_array = np.array(image_data, dtype=np.uint8)
    image_array = image_array * 255
    image = Image.fromarray(image_array)
    image.save('genImage.png')

create_image('tempImage.txt')