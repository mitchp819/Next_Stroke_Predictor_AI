import numpy as np
import sys
#np.set_printoptions(threshold=sys.maxsize)
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

        self.input_data = input_data
        self.lowest_varience = 100
        self.best_image_index = -1
        
        
    
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
        #print(f"shape_img:   side_length = {side_length}")
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
            #print(f"{i}/{data_set_size}")
        return downscaled_dataset

    def downscale_to_all_scales_and_save(self):
        downscaled_dataset1 = self.downscale_dataset(self.data_set)
        np.save('64x64_dataset.npy',downscaled_dataset1)
        print(f"Scaled to 64x6 {downscaled_dataset1.shape} -------------------------------------------------------------############")

        downscaled_dataset2 = self.downscale_dataset(downscaled_dataset1)
        np.save('32x32_dataset.npy',downscaled_dataset2)
        print(f"Scaled to 32x32 {downscaled_dataset2.shape} -------------------------------------------------------------############")

        downscaled_dataset3 = self.downscale_dataset(downscaled_dataset2)
        np.save('16x16_dataset.npy',downscaled_dataset3)
        print(f"Scaled to 16x16 {downscaled_dataset3.shape} -------------------------------------------------------------############")

        downscaled_dataset4 = self.downscale_dataset(downscaled_dataset3)
        np.save('8x8_dataset.npy',downscaled_dataset4)
        print(f"Scaled to 8x8 {downscaled_dataset4.shape} -------------------------------------------------------------############")

        downscaled_dataset5 = self.downscale_dataset(downscaled_dataset4)
        np.save('4x4_dataset.npy',downscaled_dataset5)
        print(f"Scaled to 4x4 {downscaled_dataset5.shape} -------------------------------------------------------------############")
    
    def compare_img_with_dataset(self, input_image):
        index_list = []
        lowest_varience = 1000000
        best_index = -1
        for index, data in enumerate(self.data_set):
            element = data[0, :]
            diff_array = np.abs(input_image - element)
            diff = np.sum(diff_array)
            if diff < lowest_varience:
                lowest_varience = diff
                best_index = index
            if diff < lowest_varience + 500:
                print(diff)
                index_list.append(index)
        print(lowest_varience)
        print(index_list)
        print(best_index)
        self.canvas_np_img_to_png(self.data_set[best_index,0,:], "similar_img.png")
        best_associated_stroke = self.data_set[best_index, 1, :]
        print(best_associated_stroke.shape)
        return best_associated_stroke

    def drop_ran_from_list(self, percentage, input_list):
        list_size = len(input_list)
        num_dropped = int(list_size * percentage) 
        print(f"{num_dropped} items dropped from list")
        for i in range(num_dropped):
            drop_index = random.randint(0,list_size - 1 - i)
            del input_list[drop_index]
        print(f"New list size is {len(input_list)}")
        return input_list


""" img_process = img_processer("NPY_AllImageData16385.npy", "64x64_dataset.npy", "32x32_dataset.npy", "16x16_dataset.npy", "8x8_dataset.npy", "4x4_dataset.npy")
img_process.input_data = img_process.get_single_image_data(0, 0)
output_img = img_process.compare_img_with_dataset(img_process.input_data)
print(f"output image index = {output_img}")
img_process.canvas_np_img_to_png(img_process.data_set[output_img,0,:], "similar_img.png")
#downscaled1 = img_process.downscale_img(img_process.input_data)
#img_process.downscale_to_all_scales_and_save() """

#img_process = img_processer("NPY_AllImageData16385.npy", "64x64_dataset.npy", "32x32_dataset.npy", "16x16_dataset.npy", "8x8_dataset.npy", "4x4_dataset.npy")
#img_process.downscale_to_all_scales_and_save() 
