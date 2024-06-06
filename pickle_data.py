import numpy as np
import glob
import os
import pickle

path = os.path.join(os.path.dirname(__file__), 'ImageData/*.npy')
files = sorted(glob.glob(path))
zipped_data = []

# convert each image np 
for image_file in files:
    image_npArray = np.load(image_file)
    print(image_npArray.shape)
    axis01_list = [[image_npArray[i, j, :].tolist() for j in range(image_npArray.shape[1])] for i in range(image_npArray.shape[0])] 
    
    for entry in axis01_list:
        print(len(entry))
        zipped_data.append(list(zip(*entry)))

print(len(zipped_data))
with open("PickledAllImageData.pkl", "wb") as file:
    pickle.dump(zipped_data, file)