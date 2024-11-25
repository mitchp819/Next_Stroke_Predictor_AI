import tkinter as tk
from tkinter import ttk
import numpy as np
import os
import re
import glob
from PIL import Image
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

#personal scripts
import util.image_processor as image_processor
import gui.drawing_canvas as drawing_canvas
from gui.drawing_canvas import DrawingCanvasFrame
import gui.drawing_tool_kit as drawing_tool_kit
from gui.drawing_tool_kit import DrawingToolKit



class DrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Next Brush Stroke Predictor')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        print(f"scrn width ={screen_width}, scrn height ={screen_height} ")

        self.geometry(f"{screen_width - 200}x{screen_height - 200}+5+5")
        self.resizable(True, True)
        
        self.canvas_scalor = int((screen_height - 200) // 128)
        pass

    def get_canvas_scalor(self):
        return self.canvas_scalor

if __name__ == "__main__":
    drawing_app = DrawingApp()
    tool_kit = DrawingToolKit(drawing_app, drawing_app.get_canvas_scalor())
    canvas = DrawingCanvasFrame(drawing_app, tool_kit, drawing_app.get_canvas_scalor())
    tool_kit.set_drawing_canvas(canvas)
    drawing_app.mainloop()