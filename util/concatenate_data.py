import numpy as np
import glob
import os

path = os.path.join(os.path.dirname(__file__), 'data/original-ds/ImageData16384/*.npy')
files = sorted(glob.glob(path))
arrays = []

for f in files:
    arrays.append(np.load(f))

result = np.concatenate(arrays,axis=0)
print(f"Data concatenated into np array shape = {result.shape}")
np.save(f'NPY_AllImageData{result.shape[2]}.npy', result)