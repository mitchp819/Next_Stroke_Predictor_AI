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

import sys
sys.path.append('C:/Users/mpalc/OneDrive/Desktop/_projects/next-brush-stroke-predictor_workspace/next_brush_stroke_predictor_app')
#personal scripts
import util.image_processor as image_processor
from gui.drawing_canvas import DrawingCanvasFrame
import gui.window_header as wh
from gui.brush_tool import BrushTool



class NDSPDrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Next Brush Stroke Predictor')

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        print(f"scrn width ={screen_width}, scrn height ={screen_height} ")

        self.geometry(f"{screen_width - 200}x{screen_height - 200}+5+5")
        self.resizable(True, True)
        
        self.canvas_scalor = int((screen_height - 200) // 128)

        brush_tool = BrushTool()
        #canvas = DrawingCanvasFrame(drawing_app, brush_tool, drawing_app.get_canvas_scalor())

        pass

    def get_canvas_scalor(self):
        return self.canvas_scalor

if __name__ == "__main__":
    drawing_app = NDSPDrawingApp()
    
    drawing_app.mainloop()