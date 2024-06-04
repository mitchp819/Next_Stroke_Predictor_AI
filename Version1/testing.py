import numpy as np
from PIL import Image
import network


def initNetwork(file_path):
    net.SGD(file_path, 3.0, 3, 500)

net = network.Network([250000, 30, 250000])
initNetwork(['tempImage.txt', 'output.txt'])