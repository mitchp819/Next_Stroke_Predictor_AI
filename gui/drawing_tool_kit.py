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
    def __init__(self, container, canvas_scalor):
        super().__init__(container)

        self.canvas_scalor = canvas_scalor
        self.max_brush_size = 50
        self.manual_data_gathering = False
        self.auto_generating = False
        self.drawing_canvas = None

        left_tool_frame = tk.Frame(container)
        draw_tool_frame = self.create_draw_tool_frame(left_tool_frame)
        data_gather_mode_frame = self.create_data_gather_mode_frame(left_tool_frame)
        process_data_frame = self.create_process_data_frame(left_tool_frame)

        draw_tool_frame.pack()
        data_gather_mode_frame.pack()
        process_data_frame.pack()
        left_tool_frame.pack(side = tk.LEFT, padx= 10)
        self.pack()
        pass

    def get_manual_data_gathering(self):
        return self.manual_data_gathering
    def get_greyscale_value(self):
        return self.greyscale_value.get()  
    def get_brush_size(self):
        return self.brush_size.get()
    
    def set_drawing_canvas(self, drawing_canvas):
        self.drawing_canvas = drawing_canvas
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
        
        #brush size slider
        self.brush_size = tk.IntVar()
        self.brush_size.set(1)
        brush_slider = tk.Scale(
            frame,
            from_=1,
            to=self.max_brush_size,
            length=250,
            width=20,
            orient='horizontal',
            variable=self.brush_size,
            label="Brush Size Selector",
            command=self.update_sample_brush,
            bg='white'
        )

        #greyscale slider
        self.greyscale_value = tk.IntVar()
        self.greyscale_value.set(0)
        greyscale_slider = tk.Scale(
            frame, 
            from_=0,
            to=255,
            length=250,
            width=20,
            orient='horizontal',
            variable=self.greyscale_value,
            label="Greyscale Value Selector",
            command=self.update_sample_brush,
            bg='white'
        )

        #sample brush
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

    def create_data_gather_mode_frame(self,container):
        frame = ttk.Frame(
            container,
            padding=(20,5),
            width=500,
            height=700
        )

        #Data Capture Mode
        self.data_capture_mode_label = tk.Label(
            frame, 
            text="Data Capture Mode: Auto",
            font=("TkDefaultFont", 10),
            bg='black',
            fg='white'
        )
        self.data_capture_mode_btn = ttk.Button(
            frame, 
            text="Switch to Manual",
            command=self.on_data_capture_toggle
        )
        self.save_stroke_btn = tk.Button(
            frame,
            text= "Save Stroke",
            bg='lightblue',
            font=("TkDefaultFont", 12),
            command=self.save_stroke_data
        )
        self.reset_stroke_btn = ttk.Button(
            frame, 
            text="Reset Stroke",
            command=lambda: self.drawing_canvas.reset_stroke()
        )
        self.data_capture_mode_label.pack(expand=True, pady=(20,3), ipadx=5, fill='x')
        self.data_capture_mode_btn.pack(expand=True, pady=3, fill='x')
        return frame

    def create_process_data_frame(self, container):
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

        # Threshold Slider
        self.threshold = tk.IntVar()
        self.threshold.set(500)
        threshold_slider = tk.Scale(
            frame,
            from_=1,
            to=1000,
            length=250,
            width=20,
            orient='horizontal',
            variable=self.threshold,
            label="Threshold Selector",
            command=self.update_sample_brush,
            bg="white"
        )
        
        #process image tools
        process_img_btn = tk.Button(
            frame, 
            text = "Generate Next Stroke",
            command = self.process_image,
            bg='lightblue',
            font=("TkDefaultFont", 12),
        )
        self.x_times = tk.IntVar()
        self.x_times.set(10)
        self.process_x_times_btn = ttk.Button(
            frame, 
            text = f"Generate Next {self.x_times.get()} Strokes",
            command = self.process_image
        )

        self.process_x_times_slider = tk.Scale(
            frame,
            from_=2,
            to=20,
            length=250,
            width=20,
            orient='horizontal',
            variable=self.x_times,
            command=self.set_process_times,
            bg="white"
        )

        self.auto_generate_btn = tk.Button(
            frame, 
            text ="Auto Generate : OFF\nToggle to Start",
            command = self.auto_generate_toggle,
            justify='center',
            bg='white',
            fg='black'
        )

        threshold_slider.pack(expand=True,pady=3)
        process_img_btn.pack(expand=True, pady=10, ipadx=3, ipady=3, fill ='x')
        self.process_x_times_btn.pack(expand=True, pady=(3,0), ipadx=3, ipady=3,fill='x')
        self.process_x_times_slider.pack(expand=True, pady=(0,3), fill='x')
        self.auto_generate_btn.pack(expand=True, pady=10, ipadx=3, ipady=3, fill ='x')
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
    
    def on_data_capture_toggle(self):
        if self.manual_data_gathering:
            self.manual_data_gathering = False
            self.data_capture_mode_label.config(text="Data Capture Mode: Auto")
            self.data_capture_mode_btn.config(text="Switch to Manual Mode")
            self.save_stroke_btn.pack_forget()
            self.reset_stroke_btn.pack_forget()
        else:
            self.manual_data_gathering = True
            self.data_capture_mode_label.config(text="Data Capture Mode: Manual")
            self.data_capture_mode_btn.config(text="Switch to Auto Mode")
            self.save_stroke_btn.pack(expand=True, pady=(20,3), fill='both')
            self.reset_stroke_btn.pack(expand=True, pady=(3,3), fill='both')
        pass
    
    def set_process_times(self,x):
        self.process_x_times_btn.config(text=f"Generate Next {x} Strokes")
        pass
    
    def auto_generate_toggle(self):
        if self.auto_generating:
            self.auto_generating = False
            self.auto_generate_btn.config(
                text ="Auto Generate : OFF\nToggle to Start",
                bg='white'
            )
            print("Auto Generate Brush Strokes Toggled OFF")
        else:
            self.auto_generating = True
            self.auto_generate_btn.config(
                text ="Auto Generate : ON\nToggle to Stop",
                bg='lightblue'
            )
            print("Auto Generate Brush Strokes Toggled ON")
        pass

    def process_image(self):
        pass

    def save_stroke_data(self):
        if (self.drawing_canvas != None):
            self.drawing_canvas.save_to_data_set()
        else: 
            print("Must pass drawing_canvas class to toolkit class for saving to work.")
        pass
