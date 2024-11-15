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
        self.geometry("2400x1000")
        self.title('Next Brush Stroke Predictor')
        self.resizable(True, True)
        
        self.canvas_scalor = 6
        pass

    def get_canvas_scalor(self):
        return self.canvas_scalor





if __name__ == "__main__":
    drawing_app = DrawingApp()
    DrawingToolKit(drawing_app)
    DrawingCanvasFrame(drawing_app)
    drawing_app.mainloop()