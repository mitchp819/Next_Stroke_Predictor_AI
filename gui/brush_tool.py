import tkinter as tk
from tkinter import ttk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass
 
import window_header as wh
import util.helper_functions as hlp_fun

class BrushTool(tk.Tk):
    def __init__(self, x = 10, y = 100, image_scalor = 6):
        super().__init__()
        self.geometry(f'120x500+{x}+{y}')
        self.resizable(True, True)
        self.overrideredirect(True)
        self.img_sclr = image_scalor

        self.brush_size = tk.IntVar()
        self.brush_size.set(1)
        self.greyscale_value = tk.IntVar()
        self.greyscale_value.set(0)

        wh.create_header_frame(self, True)
        self.create_sample_brush_frame()
        self.create_slider_frame()
        pass

    def create_sample_brush_frame(self):
        frame = tk.Frame(
            self,
            height = 60,
            width=60,
            bg='white'
        )

        sample_brush = tk.Frame(
            frame,
            bg='blue'
        )
        sample_brush.pack(anchor='center')
        frame.pack(padx=2,pady=2)
        pass

    def create_slider_frame(self):
        slider_frame = ttk.Frame()
        slider_frame.columnconfigure(0, weight=1)
        slider_frame.columnconfigure(1, weight=1)

        brush_size_label = tk.Label(slider_frame, text="Size")
        brush_size_label.grid(column=0, row=0, pady=3)

        brush_size_slider = tk.Scale(
            slider_frame,
            from_=50,
            to=1,
            length=300,
            orient='vertical',
            variable=self.brush_size,
            showvalue=False,
            width=30,
            bg='lightblue'
        )
        brush_size_slider.grid(column=0,row=1, padx=3,pady=3)

        greyscale_value_label = tk.Label(slider_frame, text="Color")
        greyscale_value_label.grid(column=1, row=0, pady=3)

        greyscale_value_slider = tk.Scale(
            slider_frame,
            from_=255,
            to=0,
            length=300,
            orient='vertical',
            variable=self.greyscale_value,
            showvalue=False,
            width=30,
            bg='lightblue'
        )
        greyscale_value_slider.grid(column=1,row=1, padx=3, pady=3)
        slider_frame.pack()
        pass

    def update_sample_brush(self):
        greyscale_hex = hlp_fun.greyscale_value_to_hex(self.greyscale_value.get())
        sample_width = self.brush_size.get() + self.img_sclr
        sample_padding = ((self.max_brush_size + self.canvas_scalor) - sample_width)//2
        self.sample_brush.config(
            width = sample_width,
            height = sample_width,
            bg=greyscale_hex
        )
        self.sample_brush.pack_configure(pady = sample_padding + 10)
        pass

if __name__ == "__main__":
    brush_tool = BrushTool()
    brush_tool.mainloop()
        