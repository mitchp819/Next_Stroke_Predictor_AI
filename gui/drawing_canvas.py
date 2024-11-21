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
    def __init__(self, container, tool_kit, image_scalor = 6, image_width = 128, image_height = 128):
        super().__init__(container)

        self.img_x = image_width
        self.img_y = image_height
        self.img_sclr = image_scalor
        self.win_x = self.img_x * self.img_sclr
        self.win_y = self.img_y * self.img_sclr
        self.tool_kit = tool_kit
        
        #gui
        self.canvas = tk.Canvas(self, width=self.win_x, height=self.win_y, bg='white')
        self.canvas.pack()
        self.pack(side=tk.LEFT, expand= True)

        #numpy arrays for canvas and stroke
        self.np_main_canvas_data = np.ones((self.img_x, self.img_y), dtype= np.uint8) * 255
        self.np_stroke_canvas_data = np.full((self.img_x, self.img_y), -1)
        self.last_canvas = self.np_main_canvas_data.flatten()
        self.compiled_data = None
        self.stroke_count = 0

        #Event binding
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.create_mark)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_released)
        pass
    
    def on_mouse_down(self, event):
        if  self.tool_kit.get_manual_data_gathering() == False:
            #Whipe np stroke canvas
            self.np_stroke_canvas_data = np.full((self.img_x, self.img_y), -1)
        self.create_mark(event)
        pass

    def on_mouse_released(self, event):
        if self.tool_kit.get_manual_data_gathering() == False:
            self.save_to_data_set()
        pass

    def create_mark(self, event):
        #variables
        greyscale_value = self.tool_kit.get_greyscale_value()
        greyscale_hex = hlp_fun.greyscale_value_to_hex(greyscale_value)
        brush_size = self.tool_kit.get_brush_size()
        
        x = event.x // self.img_sclr
        y = event.y // self.img_sclr

        rect = self.canvas.create_rectangle(x * self.img_sclr, y * self.img_sclr,
                            (x + 1) * self.img_sclr, (y + 1) * self.img_sclr,
                            fill= greyscale_hex, outline=greyscale_hex, width= brush_size)

        #converts canvas rect into image coords
        x1, y1, x2, y2 = self.canvas.bbox(rect)
        x1 = int(x1 // self.img_sclr)
        y1 = int(y1 // self.img_sclr)
        x2 = int(x2 // self.img_sclr)
        y2 = int(y2 // self.img_sclr)

        #update np canvas data
        for x in range(x1, x2):
            for y in range(y1, y2):
                if (x < self.img_x and x >= 0 and y < self.img_y and y >= 0):
                    self.np_main_canvas_data[y, x] = greyscale_value
                    self.np_stroke_canvas_data[y, x] = greyscale_value
        pass
    
    def save_to_data_set(self):
        #flatten and normalize between 0-1
        flat_normal_last_canvas = self.last_canvas.flatten() / 255
        flat_normal_stroke_canvas = self.np_stroke_canvas_data.flatten() /255
        
        #saves color values in array
        filler =  np.array([.5])
        color_data = np.array([self.tool_kit.get_greyscale_value() / 255])
        
        flat_normal_last_canvas = np.concatenate((flat_normal_last_canvas,filler))
        flat_normal_stroke_canvas = np.concatenate((flat_normal_stroke_canvas, color_data))

        insertion_data = np.array([flat_normal_last_canvas, flat_normal_stroke_canvas])
        insertion_data = insertion_data[np.newaxis, :]

        #overwrites data
        self.last_canvas = self.np_main_canvas_data
        self.stroke_count += 1

        #cats insertion data with compiled data
        if self.compiled_data is None:
            self.compiled_data = insertion_data
        else:
            self.compiled_data = np.concatenate((self.compiled_data, insertion_data), axis=0)
        print(self.compiled_data.shape)
        pass

    def reset_stroke(self):
        self.np_stroke_canvas_data = np.full((self.img_x, self.img_y), -1)
        print("Stroke Data Reset")