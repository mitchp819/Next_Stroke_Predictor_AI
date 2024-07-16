import numpy as np
from PIL import Image


def create_image_from_np(file):
    data = np.load(file)

    if(data.ndim > 1):
        data.flatten()
    print(data.shape)
    
    greyscale_value = data[-1]
  
    

    data = data[:-1]
    side_length = int(np.sqrt(greyscale_value.shape[0]))
    data = data * 255 * greyscale_value
    image_data = greyscale_value.reshape((side_length,side_length))
    print(image_data)
    image = Image.fromarray(image_data.astype('uint8'), 'L')
    image.save('output.png')

def create_image_from_compiled_np(file: str, index: int, canvas_or_stoke: int):
    """Takes in a   3D np array (canvas_count, 2, side_length * side_length)
                    The index of the image, -1 will produce the last canvas drawn on
                    choose canvas or stroke, Canvas = 0 or Stroke = 1"""

    data = np.load(file)
    image_data = data[index,canvas_or_stoke]
    print(image_data.shape)

    image = image_data[:-1]
    image = image * 255
    print(image.shape)
    side_length = int(np.sqrt(image.shape[0]))
    print(side_length)
    image_shaped = np.reshape(image, (side_length, side_length))
    print(image_shaped.shape)
    image = Image.fromarray(image_shaped.astype('uint8'), 'L')
    image.save('compiled_np_output.png')
    print("image saved under     compiled_np_output.png")


create_image_from_compiled_np('ImageData16384\image8data.npy', -1, 0)