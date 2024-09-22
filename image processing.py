import numpy as np
from PIL import Image
import random


class img_processer:
    def __init__(self, data_set_128_file: str, data_set_64_file: str = None, data_set_32_file: str = None, data_set_16_file: str = None, data_set_8_file: str= None, data_set_4_file: str = None, input_data = None):
        self.data_set = np.load(data_set_128_file)
        np.random.shuffle(self.data_set)
        
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
        
        print("\n---------------- 4x4 ---------------")
        index_list4 = self.find_similar(downscaled4, self.data_set_4, None, .075, .0001)
        if (len(index_list4)==0):
            print("no match 4x4")
            #some sort of error
        print("\n---------------- 8x8 ---------------")
        index_list8 = self.find_similar(downscaled8, self.data_set_8, index_list4, .07, 0) 
        if (len(index_list8)==0):
            print("no match 8x8")
            return index_list4[random.randint(0, len(index_list4)-1)]
        print("\n---------------- 16x16 ---------------")
        index_list16 = self.find_similar(downscaled16, self.data_set_16, index_list8, .06, 0)
        if (len(index_list16)==0):
            print("no match 16x16")
            return index_list8[random.randint(0, len(index_list8)-1)]
        print("\n---------------- 32x32 ---------------")
        index_list32 = self.find_similar(downscaled32, self.data_set_32, index_list16, .05, 0)
        if (len(index_list32)==0):
            print("no match 32x32")
            return index_list16[random.randint(0, len(index_list16)-1)]
        print("\n---------------- 64x64 ---------------")
        index_list64 = self.find_similar(downscaled64, self.data_set_64, index_list32, .05, 0)
        if (len(index_list64)==0):
            print("no match 64x64")
            return index_list32[random.randint(0, len(index_list32)-1)]
        print("\n---------------- 126x128 ---------------")
        index_list128 = self.find_similar(input_image, self.data_set, index_list64, .05, 0)
        if (len(index_list128) == 0):
            print("no match 128x128")
            return index_list64[random.randint(0, len(index_list64)-1)]
        return index_list128[random.randint(0, len(index_list128)-1)]

    def find_similar(self, input_img, data_set, img_index_list = None, variance_upper_bound = 1, varience_lower_bond = 0, drop_percent = .05):
        lowest = 100
        new_index_list = []

        if(img_index_list == None):
            for i in range(data_set.shape[0]):
                sum_of_dif = 0
                for j in range(input_img.shape[0]):
                    dif_squared = (input_img[j] - data_set[i,0,j])**2
                    sum_of_dif += dif_squared
                varience = sum_of_dif / (input_img.shape[0] - 1) 
                if(varience < variance_upper_bound and varience > varience_lower_bond):
                    if (varience < lowest):
                        lowest = varience
                    new_index_list.append(i)
            print(f"Lowest Variance in 4x4 similiarity is {lowest}")
            print(f"List size after 4x4 run is {len(new_index_list)}")
        else:
            for i in range(len(img_index_list)):
                sum_of_dif = 0 
                for j in range(input_img.shape[0]):
                    dif_squared = (input_img[j] - data_set[img_index_list[i],0,j])**2 
                    sum_of_dif += dif_squared
                varience = sum_of_dif / (input_img.shape[0] - 1) 
                if(varience < variance_upper_bound and varience > varience_lower_bond):
                    if (varience < lowest):
                        lowest = varience
                    new_index_list.append(i)
            print(f"Lowest Variance in similiarity is {lowest}")
            print(f"List size after run is {len(new_index_list)}")

        new_index_list = self.drop_ran_from_list(drop_percent, new_index_list)
        return new_index_list


    def drop_ran_from_list(self, percentage, input_list):
        list_size = len(input_list)
        num_dropped = int(list_size * percentage) 
        print(f"{num_dropped} items dropped from list")
        for i in range(num_dropped):
            drop_index = random.randint(0,list_size - 1 - i)
            del input_list[drop_index]
        print(f"New list size is {len(input_list)}")
        return input_list



img_process = img_processer("NPY_AllImageData16385.npy", "64x64_dataset.npy", "32x32_dataset.npy", "16x16_dataset.npy", "8x8_dataset.npy", "4x4_dataset.npy")
img_process.input_data = img_process.get_single_image_data(0, 0)
output_img = img_process.compare_img_with_dataset(img_process.input_data)
print(f"output image index = {output_img}")
img_process.canvas_np_img_to_png(img_process.data_set[output_img,0,:], "similar_img.png")
#downscaled1 = img_process.downscale_img(img_process.input_data)
#img_process.downscale_to_all_scales_and_save(img_process.data_set)


