import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw

winHight = 500
winWidth = winHight

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width = winWidth, height = winHight, bg = 'white')
        self.canvas.pack()
        self.stroke_canvas = tk.Canvas(self.master, width = winWidth, height = winHight, bg = 'white')
        #self.stroke_canvas.pack()
        self.image = Image.new('RGB', (winWidth, winHight), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.last_x = None
        self.last_y = None
        self.stroke_count = 0
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<Button-1>", self.new_image)
        self.canvas.bind("<ButtonRelease-1>", self.save_image)
        self.image.save(f'canvas_{self.stroke_count}.png')

    def new_image(self, event):
        self.stroke_image = Image.new('RGBA', (winWidth, winHight), (0,0,0,0))
        self.stroke_draw = ImageDraw.Draw(self.stroke_image)

    def draw_line(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill='black')
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill='black')
            self.stroke_canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill='black')
            self.stroke_draw.line([self.last_x, self.last_y, event.x, event.y], fill='black')
        self.last_x = event.x
        self.last_y = event.y

    def save_image(self, event):
        self.last_x = None
        self.last_y = None
        self.stroke_image.save(f'stroke_{self.stroke_count}.png')
        self.image.save(f'canvas_{self.stroke_count + 1}.png')
        self.stroke_count += 1
 

root = tk.Tk() 
app = DrawingApp(root)
root.mainloop()