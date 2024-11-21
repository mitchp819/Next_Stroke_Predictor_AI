import tkinter as tk
from tkinter import ttk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass
  

import sys
sys.path.append('C:/Users/mpalc/OneDrive/Desktop/_projects/next-brush-stroke-predictor_workspace/next_brush_stroke_predictor_app')
from util import helper_functions as hlp_fun
import window_header as wh


class BrushTool(tk.Tk):
    def __init__(self, x = 30, y = 200, image_scalor = 6):
        super().__init__()
        self.geometry(f'120x530+{x}+{y}')
        self.resizable(True, True)
        self.overrideredirect(True)
        self.attributes
        self.img_sclr = image_scalor

        self.brush_size = tk.IntVar()
        self.brush_size.set(1)
        self.greyscale_value = tk.IntVar()
        self.greyscale_value.set(0)
        
        wh.create_header_frame(self, True)
        self.create_sample_brush_frame()
        self.create_slider_frame()
        pass

    def get_greyscale_value(self):
        return self.greyscale_value
    def get_brush_size(self):
        return self.brush_size

    def create_sample_brush_frame(self):
        frame = tk.Frame(
            self,
            height = 80,
            width= 80,
            bg='lightblue',
            border=4,
            relief='raised'
        )

        frame.pack_propagate(False)

        self.sample_brush = tk.Canvas(
            frame,
            width = 30,
            height = 30,
            bg = 'black'
        )
        self.sample_brush.pack(expand=True)
        frame.pack(padx=2,pady=5)
        pass

    def create_slider_frame(self):
        slider_frame = ttk.Frame()
        slider_frame.columnconfigure(0, weight=1)
        slider_frame.columnconfigure(1, weight=1)

        self.greyscale_value_label = tk.Label(slider_frame, text="x")
        self.greyscale_value_label.grid(column=1, row=0)
        self.brush_size_label = tk.Label(slider_frame, text="x")
        self.brush_size_label.grid(column=0, row=0)

        brush_size_slider = tk.Scale(
            slider_frame,
            from_=50,
            to=1,
            length=300,
            orient='vertical',
            variable=self.brush_size,
            showvalue=False,
            width=30,
            bg='lightblue',
            command = self.update_sample_brush
        )
        brush_size_slider.grid(column=0,row=1, padx=3,pady=3)

        greyscale_value_slider = tk.Scale(
            slider_frame,
            from_=255,
            to=0,
            length=300,
            orient='vertical',
            variable=self.greyscale_value,
            showvalue=False,
            width=30,
            bg='lightblue',
            command = self.update_sample_brush
        )
        greyscale_value_slider.grid(column=1,row=1, padx=3, pady=3)
        
        greyscale_value_txt = tk.Label(slider_frame, text="Color")
        greyscale_value_txt.grid(column=1, row=3)
        brush_size_txt = tk.Label(slider_frame, text="Size")
        brush_size_txt.grid(column=0, row=3)

        slider_frame.pack()
        self.update_sample_brush(0)
        pass

    def update_sample_brush(self,v):
        greyscale_hex = hlp_fun.greyscale_value_to_hex(self.greyscale_value.get())
        sample_width = self.brush_size.get() + self.img_sclr
        self.sample_brush.config(
            width = sample_width,
            height = sample_width,
            bg = greyscale_hex
        )
        self.greyscale_value_label.config(text=self.greyscale_value.get())
        self.brush_size_label.config(text= self.brush_size.get())
        pass

if __name__ == "__main__":
    brush_tool = BrushTool()
    brush_tool.mainloop()