import numpy as np
from PIL import Image


def create_image_from_np(file):
    data = np.load(file)
    if(data.ndim > 1):
        data.flatten()
    greyscale_value = data[-1]
    data = data[:-1]
    side_length = int(np.sqrt(data.shape[0]))
    data = data * 255 * greyscale_value
    image_data = data.reshape((side_length,side_length))
    print(image_data)
    image = Image.fromarray(image_data.astype('uint8'), 'L')
    image.save('output.png')

create_image_from_np('generated_image.npy')