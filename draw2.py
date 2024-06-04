import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw

winHight = 400
winWidth = winHight

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width = winWidth, height = winHight, bg = 'white')
        self.canvas.pack()
        self.stroke_canvas = tk.Canvas(self.master, width = winWidth, height = winHight, bg = 'white')
        self.image = Image.new('RGB', (winWidth, winHight), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.last_x = None
        self.last_y = None
        self.stroke_count = 0
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<Button-1>", self.new_image)
        self.canvas.bind("<ButtonRelease-1>", self.save_image)
        self.image.save(f'canvas_{self.stroke_count}.png')
        original_canvas = np.array(self.image.convert('L')).flatten()
        self.last_canvas = original_canvas / 255
        self.data = None

    def new_image(self, event):
        self.stroke_image = Image.new('RGB', (winWidth, winHight), 'white')
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

        #to save images as png 
        #self.stroke_image.save(f'stroke_{self.stroke_count}.png')
        #self.image.save(f'canvas_{self.stroke_count + 1}.png')
        
        stroke_data = np.array(self.stroke_image.convert('L')).flatten()
        stroke_data = stroke_data / 255
        insert_data = np.array([self.last_canvas, stroke_data])
        insert_data = np.expand_dims(insert_data, axis = 0)

        #cats new data with self data
        if self.data is None:
            self.data = insert_data
        else:
            self.data = np.concatenate((self.data, insert_data), axis = 0)


        print(self.data.shape)
        #over write last_canvas for following iteration
        last_canvas = np.array(self.image.convert('L')).flatten()
        self.last_canvas = last_canvas / 255
        self.stroke_count += 1

        #over write np save
        np.save('image1data.npy', self.data)
 

root = tk.Tk() 
app = DrawingApp(root)
root.mainloop()