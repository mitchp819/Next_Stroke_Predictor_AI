import numpy as np
from PIL import Image
import random


class img_processer:
    def __init__(self, data_set_128_file: str, data_set_64_file: str = None, data_set_32_file: str = None,
                  data_set_16_file: str = None, data_set_8_file: str= None, data_set_4_file: str = None, input_data = None):
       
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
        index_list4 = []
        index_list8 = []
        index_list16 = []
        index_list32 = []
        index_list64 = []
        index_list128 = []
        index_list4.clear()
        index_list8.clear()
        index_list16.clear()
        index_list32.clear()
        index_list64.clear()
        index_list128.clear()

        downscaled64 = self.downscale_img(input_image)
        downscaled32 = self.downscale_img(downscaled64)
        downscaled16 = self.downscale_img(downscaled32)
        downscaled8 = self.downscale_img(downscaled16)
        downscaled4 = self.downscale_img(downscaled8)
        print(f"dataset 4 shape = {self.data_set_4.shape}")


        start_varience = .01
        variance_interval = .01
        max_varience = .5
        
        print("\n---------------- 4x4 ---------------")
        v = start_varience

        while(len(index_list4) <= 200 and v < max_varience):
            index_list4 = self.find_similar(downscaled4, self.data_set_4, None, v, .00001)
            v += variance_interval
            print(f"v = {v}")
        if (len(index_list4)==0):
            print("no match 4x4")
            #some sort of error
            print("ERROR: compare_img_with_dataset did not find a similar image")
            return -1
        
        print("\n---------------- 8x8 ---------------")
        v = start_varience

        while(len(index_list8) <= 170 and v < max_varience):
            index_list8 = self.find_similar(downscaled8, self.data_set_8, index_list4, v, 0) 
            v += variance_interval
            print(f"v = {v}")

        if (len(index_list8)==0):
            print("no match 8x8")
            return_value = index_list4[random.randint(0, len(index_list4)-1)]
            self.canvas_np_img_to_png(self.data_set[return_value,0,:], "similar_img.png")
            return
        
        print("\n---------------- 16x16 ---------------")
        v = start_varience

        while(len(index_list16) <= 100 and v < max_varience):
            index_list16 = self.find_similar(downscaled16, self.data_set_16, index_list8, v, 0)
            v += variance_interval
            print(f"v = {v}")

        if (len(index_list16)==0):
            print("no match 16x16")
            return_value = index_list8[random.randint(0, len(index_list8)-1)]
            self.canvas_np_img_to_png(self.data_set[return_value,0,:], "similar_img.png")
            return
        
        print("\n---------------- 32x32 ---------------")
        v = start_varience

        while(len(index_list32) <= 30 and v < max_varience):
            index_list32 = self.find_similar(downscaled32, self.data_set_32, index_list16, v, 0)
            v += variance_interval
            print(f"v = {v}")

        if (len(index_list32)==0):
            print("no match 32x32")
            return_value = index_list16[random.randint(0, len(index_list16)-1)]
            self.canvas_np_img_to_png(self.data_set[return_value,0,:], "similar_img.png")
            return
        
        print("\n---------------- 64x64 ---------------")
        v = start_varience

        while(len(index_list64) <= 10 and v < max_varience):
            index_list64 = self.find_similar(downscaled64, self.data_set_64, index_list32, v, 0)
            v += variance_interval
            print(f"v = {v}")

        if (len(index_list64)==0):
            print("no match 64x64")
            return_value = index_list32[random.randint(0, len(index_list32)-1)]
            self.canvas_np_img_to_png(self.data_set[return_value,0,:], "similar_img.png")
            return
        
        print("\n---------------- 126x128 ---------------")
        v = start_varience

        while(len(index_list128) <= 5 and v < max_varience):
            index_list128 = self.find_similar(input_image, self.data_set, index_list64, v, 0)
            v += variance_interval
            print(f"v = {v}")

        if (len(index_list128) == 0):
            print("no match 128x128")
            return_value = index_list64[random.randint(0, len(index_list64) -1)]
            self.canvas_np_img_to_png(self.data_set[return_value,0,:], "similar_img.png")
            return
        
        return_value = index_list128[random.randint(0, len(index_list128)-1)]
        self.canvas_np_img_to_png(self.data_set[return_value,0,:], "similar_img.png")
        return return_value

    def find_similar(self, input_img, data_set, img_index_list = None, variance_upper_bound = 1, varience_lower_bond = 0, drop_percent = .05):
        lowest = 100
        new_index_list = []
        new_index_list.clear()

        if(img_index_list == None):
            for i in range(data_set.shape[0]):
                sum_of_dif = 0
                for j in range(input_img.shape[0]):
                    dif_squared = (input_img[j] - data_set[i,0,j])**2
                    sum_of_dif += dif_squared
                varience = sum_of_dif / (input_img.shape[0] - 1) 
                if (varience < lowest):
                        lowest = varience
                if(varience < variance_upper_bound and varience > varience_lower_bond):
                    new_index_list.append(i)
            print(f"Lowest Variance in 4x4 similiarity is {lowest}")
            print(f"List size after 4x4 run is {len(new_index_list)}")
            print(new_index_list)
        else:
            for i in range(len(img_index_list)):
                sum_of_dif = 0 
                for j in range(input_img.shape[0]):
                    dif_squared = (input_img[j] - data_set[img_index_list[i],0,j])**2 
                    sum_of_dif += dif_squared
                varience = sum_of_dif / (input_img.shape[0] - 1) 
                if (varience < lowest):
                        lowest = varience
                if(varience < variance_upper_bound and varience > varience_lower_bond):
                    new_index_list.append(img_index_list[i])
            print(f"Lowest Variance in similiarity is {lowest}")
            print(f"List size after run is {len(new_index_list)}")
            print(new_index_list)

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


""" img_process = img_processer("NPY_AllImageData16385.npy", "64x64_dataset.npy", "32x32_dataset.npy", "16x16_dataset.npy", "8x8_dataset.npy", "4x4_dataset.npy")
img_process.input_data = img_process.get_single_image_data(0, 0)
output_img = img_process.compare_img_with_dataset(img_process.input_data)
print(f"output image index = {output_img}")
img_process.canvas_np_img_to_png(img_process.data_set[output_img,0,:], "similar_img.png")
#downscaled1 = img_process.downscale_img(img_process.input_data)
#img_process.downscale_to_all_scales_and_save() """

#img_process = img_processer("NPY_AllImageData16385.npy", "64x64_dataset.npy", "32x32_dataset.npy", "16x16_dataset.npy", "8x8_dataset.npy", "4x4_dataset.npy")
#img_process.downscale_to_all_scales_and_save() 
