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

class DrawingToolKit(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        self.canvas_scalor = container.get_canvas_scalor()
        

        draw_tool_frame = self.create_draw_tool_frame(container)
        process_data_frame = self.create_process_data_frame(container)

        draw_tool_frame.pack(side=tk.LEFT)
        process_data_frame.pack(side=tk.LEFT)
        self.pack()
        pass

    def create_draw_tool_frame(self, container):
        style = ttk.Style()
        style.configure(
            'DrawTool.TFrame',
            background='lightgray',
            borderwidth=3,
            relief='ridge'
        )
        frame = ttk.Frame(
            container,
            style='DrawTool.TFrame',
            padding=(20,5),
            width=500,
            height=700
        )

        self.brush_size = tk.IntVar()
        self.brush_size.set(1)
        brush_slider = tk.Scale(
            frame,
            from_=1,
            to=50,
            length=200,
            width=20,
            orient='horizontal',
            variable=self.brush_size,
            label="Brush Size",
            command=self.update_sample_brush
        )
    
        self.greyscale_value = tk.IntVar()
        self.greyscale_value.set(0)
        greyscale_slider = tk.Scale(
            frame, 
            from_=0,
            to=255,
            length=200,
            width=20,
            orient='horizontal',
            variable=self.greyscale_value,
            label="Greyscale Value",
            command=self.update_sample_brush
        )

        
        self.sample_brush = tk.Canvas(
            frame,
            width = self.brush_size * self.canvas_scalor,
            height = self.brush_size * self.canvas_scalor,
            bg= hlp_fun.greyscale_value_to_hex(self.greyscale_value)
        )


        self.sample_brush.pack(pady=3)
        brush_slider.pack(expand=True,pady=3)
        greyscale_slider.pack(expand=True, pady=3)
        return frame

    def create_process_data_frame(self, container):
        frame = ttk.Frame(container)
        return frame
    
    def update_sample_brush(self):

        pass