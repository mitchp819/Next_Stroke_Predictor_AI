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
        self.max_brush_size = 50

        left_tool_frame = tk.Frame(container)
        draw_tool_frame = self.create_draw_tool_frame(left_tool_frame)
        process_data_frame = self.create_process_data_frame(left_tool_frame)

        draw_tool_frame.pack()
        process_data_frame.pack()
        left_tool_frame.pack(side = tk.LEFT, padx= 10)
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
            to=self.max_brush_size,
            length=200,
            width=20,
            orient='horizontal',
            variable=self.brush_size,
            label="Brush Size Selector",
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
            label="Greyscale Value Selector",
            command=self.update_sample_brush
        )

        sample_width = self.brush_size.get() * self.canvas_scalor
        sample_padding = ((self.max_brush_size + self.canvas_scalor) - sample_width)//2
        self.sample_brush = tk.Canvas(
            frame,
            width = sample_width,
            height = sample_width,
            bg= hlp_fun.greyscale_value_to_hex(self.greyscale_value.get())
        )


        self.sample_brush.pack(pady=sample_padding + 10)
        brush_slider.pack(expand=True,pady=3)
        greyscale_slider.pack(expand=True, pady=3)
        return frame

    def create_process_data_frame(self, container):
        style = ttk.Style()
        style.configure(
            'ProcessTool.TButton'
        )
        style.map(
            'ProcessTool.TButton',
              background=[('active', 'lightgreen'), ('pressed', 'blue')], 
              foreground=[('active', 'black'), ('pressed', 'white')])

        frame = ttk.Frame(
            container,
            padding=(20,5),
            width=500,
            height=700
        )

        self.threshold = tk.IntVar()
        self.threshold.set(500)
        threshold_slider = tk.Scale(
            frame,
            from_=1,
            to=1000,
            length=200,
            width=20,
            orient='horizontal',
            variable=self.threshold,
            label="Threshold Selector",
            command=self.update_sample_brush,
            bg="white"
        )

        process_img_btn = ttk.Button(
            frame, 
            text = "Generate Next Stroke",
            command = self.process_image,
            style= 'ProcessTool.TButton'
        )

        self.process_x_times_btn = ttk.Button(
            frame, 
            text = "Generate x Next Strokes",
            command = self.process_image,
            style= 'ProcessTool.TButton'
        )

        threshold_slider.pack(expand=True,pady=3)
        process_img_btn.pack(expand=True, pady=3, ipadx=3, ipady=3)
        self.process_x_times_btn.pack(expand=True, pady=3, ipadx=3, ipady=3)
        return frame
    
    def update_sample_brush(self, value):
        greyscale_hex = hlp_fun.greyscale_value_to_hex(self.greyscale_value.get())
        sample_width = self.brush_size.get() + self.canvas_scalor
        sample_padding = ((self.max_brush_size + self.canvas_scalor) - sample_width)//2
        self.sample_brush.config(
            width = sample_width,
            height = sample_width,
            bg=greyscale_hex
        )
        self.sample_brush.pack_configure(pady = sample_padding + 10)
        pass

    def process_image(self):
        pass

