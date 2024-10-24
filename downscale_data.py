import numpy as np    

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
    