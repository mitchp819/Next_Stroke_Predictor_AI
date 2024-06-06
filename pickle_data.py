import numpy as np
import glob
import os
import pickle

path = os.path.join(os.path.dirname(__file__), 'ImageData/*.npy')
files = sorted(glob.glob(path))
arrays = []

for f in files:
    arrays.append(np.load(f))

with open("PickledAllImageData.pkl", "wb") as file:
    pickle.dump(arrays, file)