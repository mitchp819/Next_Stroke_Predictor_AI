import numpy as np
from PIL import Image



class img_processer:
    def __init__(self, data_set_128_file: str, data_set_64_file: str = None, data_set_32_file: str = None, data_set_16_file: str = None, data_set_8_file: str= None, data_set_4_file: str = None, input_data = None):
        self.data_set = np.load(data_set_128_file)
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

        self.input_data = input_data
        
    
    def get_single_image_data(self, index: int, canvas_or_stroke: int):
        """     -    Takes in a   3D np array (canvas_index, 2, side_length * side_length).
                -    The index of the image, -1 will produce the last canvas drawn on.
                -    Choose canvas or stroke, Canvas = 0 or Stroke = 1."""
        image_data = self.data_set[index,canvas_or_stroke]
        print(f"Chosen image shape = {image_data.shape}")
        self.canvas_np_img_to_png(image_data, "single_img.png")
        return image_data

    def canvas_np_img_to_png(self, canvas_data, save_name):
        #Remove the last value which is a color placeholder value and multiply by 255 to get correct values
        image = canvas_data[:-1]
        image = image * 255
        Image.fromarray(self.shape_img(image).astype('uint8'), 'L').save(save_name)
        print(f"image saved under: {save_name}")

    def downscale_img(self, image):
        #print("-------------Downscaling IMG--------------")
        color_value = 0
        if image.shape[0] % 2 != 0:
            color_value = image[-1]
            image = image[:-1]
            #print(image.shape)
        image_shaped = self.shape_img(image)
        new_shape = (image_shaped.shape[0] // 2, image_shaped.shape[1] // 2)
        downscaled_img = np.zeros(new_shape)
        for i in range(new_shape[0]):
            for j in range(new_shape[1]):
                downscaled_img[i, j] = np.mean(image_shaped[i*2:(i+1)*2, j*2:(j+1)*2])
        flat_downscaled_img = downscaled_img.flatten()
        flat_downscaled_img = np.append(flat_downscaled_img, color_value)
        #print(f"downscaled shape = {downscaled_img.shape} \nFlattened and color value appended {flat_downscaled_img.shape}")
        return flat_downscaled_img
     
    def shape_img (self,image):
        side_length = int(np.sqrt(image.shape[0]))
        shaped_image = np.reshape(image, (side_length, side_length))
        #print(f"image reshaped. Shape = {shaped_image.shape}")
        return shaped_image
    
    def downscale_dataset (self, data_set):
        data_set_size = data_set.shape[0]
        side_length = int(np.sqrt(data_set.shape[2] - 1))
        new_shape = (data_set.shape[0], data_set.shape[1], (side_length//2)**2 + 1)
        print(new_shape)
        downscaled_dataset = np.zeros(new_shape)
        for i in range(data_set_size):
            canvas_img = data_set[i,0,:]
            stroke_img = data_set[i,1,:]
            downscaled_dataset[i,0,:] = self.downscale_img(canvas_img)
            downscaled_dataset[i,1,:] = self.downscale_img(stroke_img)
            print(f"{i}/{data_set_size}")
        return downscaled_dataset

    def downscale_to_all_scales_and_save(self, Dataset_128x128):
        downscaled_dataset1 = img_process.downscale_dataset(Dataset_128x128)
        np.save('64x64_dataset.npy',downscaled_dataset1)
        downscaled_dataset2 = img_process.downscale_dataset(downscaled_dataset1)
        np.save('32x32_dataset.npy',downscaled_dataset2)
        downscaled_dataset3 = img_process.downscale_dataset(downscaled_dataset2)
        np.save('16x16_dataset.npy',downscaled_dataset3)
        downscaled_dataset4 = img_process.downscale_dataset(downscaled_dataset3)
        np.save('8x8_dataset.npy',downscaled_dataset4)
        downscaled_dataset5 = img_process.downscale_dataset(downscaled_dataset4)
        np.save('4x4_dataset.npy',downscaled_dataset5)
    
    def compare_img_with_dataset(self, input_image):
        downscaled64 = img_process.downscale_img(input_image)
        downscaled32 = img_process.downscale_img(downscaled64)
        downscaled16 = img_process.downscale_img(downscaled32)
        downscaled8 = img_process.downscale_img(downscaled16)
        downscaled4 = img_process.downscale_img(downscaled8)

        similar_img_list = []
        
        lowest = 100
        list_size = 0

        for i in range(self.data_set_4.shape[0]):
            sum_of_dif = 0
            for j in range(downscaled4.shape[0]):
                dif_squared = (downscaled4[j] - self.data_set_4[i,0,j])**2
                sum_of_dif += dif_squared
            varience = sum_of_dif / downscaled4.shape[0]
            if (varience < lowest):
                lowest = varience
            if(varience <= .075):
                list_size += 1
                similar_img_list.append(i)
            print(varience)
        print(lowest)
        print(list_size)



img_process = img_processer("NPY_AllImageData16385.npy", "64x64_dataset.npy", "32x32_dataset.npy", "16x16_dataset.npy", "8x8_dataset.npy", "4x4_dataset.npy")
img_process.input_data = img_process.get_single_image_data(12, 0)
img_process.compare_img_with_dataset(img_process.input_data)
#downscaled1 = img_process.downscale_img(img_process.input_data)
#img_process.downscale_to_all_scales_and_save(img_process.data_set)


