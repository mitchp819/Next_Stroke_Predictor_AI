import tkinter as tk
from tkinter import ttk
import numpy as np
import os
import re
import glob
import time
from PIL import Image, ImageDraw
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

import util.image_processor as image_processing
import util.helper_functions as hlp_fun

class DrawingCanvasFrame(ttk.Frame):
    def __init__(self, container, image_width = 128,image_height = 128):
        super().__init__(container)

        self.img_x = image_width
        self.img_y = image_height
        self.img_sclr = container.get_canvas_scalor()
        self.win_x = self.img_x * self.img_sclr
        self.win_y = self.img_y * self.img_sclr
        
        #gui
        self.canvas = tk.Canvas(self, width=self.win_x, height=self.win_y, bg='white')
        self.canvas.pack()
        self.pack(side=tk.LEFT, expand= True)

        #numpy arrays for canvas and stroke
        self.np_main_canvas_data = np.ones((self.img_x, self.img_y), dtype= np.uint8) * 255
        self.np_stroke_canvas_data = np.ones((self.img_x, self.img_y), dtype= np.uint8) * 255
        self.last_canvas = self.np_main_canvas_data.flatten()
        self.compiled_date = None
        self.stroke_count = 0

        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_released)
        pass
    
    def on_mouse_down(self, event):
        pass

    def on_mouse_drag(self, event):
        pass

    def on_mouse_released(self, event):
        pass
        