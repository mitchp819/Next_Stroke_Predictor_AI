import tkinter as tk
import numpy as np
import os
import re
from PIL import Image, ImageDraw

winHight = 100
winWidth = winHight



class DrawingApp:

    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width = winWidth, height = winHight, bg = 'white')
        self.canvas.pack()
        self.stroke_canvas = tk.Canvas(self.master, width = winWidth, height = winHight, bg = 'white')
        self.image = Image.new('RGB', (winWidth, winHight), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.brush_size = tk.IntVar()
        self.brush_size.set(1)
        self.brush_slider = tk.Scale(self.master, from_=1, to=50, orient = "horizontal", variable = self.brush_size)
        self.brush_slider.pack()

        self.color_scale = tk.Scale(self.master, from_=0, to=100, orient="horizontal")
        self.color_scale.pack()

        self.last_x = None
        self.last_y = None
        self.stroke_count = 0
        
        #get the last file id 
        files_list = [f for f in os.listdir(f'ImageData{winWidth*winHight}') if os.path.isfile(os.path.join(f'ImageData{winWidth*winHight}', f))]
        largest_ID = 0
        for file in files_list:
            integers = [int(s) for s in re.findall(r'\d+', file)]
            if(integers[0] > largest_ID):
                largest_ID = integers[0]
        self.file_count = largest_ID

        #bind buttons 
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<Button-1>", self.new_image)
        self.canvas.bind("<ButtonRelease-1>", self.save_image)

        #self.image.save(f'canvas_{self.stroke_count}.png')
        original_canvas = np.array(self.image.convert('L')).flatten()
        self.last_canvas = original_canvas / 255
        self.data = None



    def new_image(self, event):
        self.stroke_image = Image.new('RGB', (winWidth, winHight), 'white')
        self.stroke_draw = ImageDraw.Draw(self.stroke_image)





    def draw_line(self, event):
        color = scale_to_color(self.color_scale.get())
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width = self.brush_size.get(),fill=color)
            self.draw.line([self.last_x, self.last_y, event.x, event.y],  width = self.brush_size.get(),fill=color)
            self.stroke_canvas.create_line(self.last_x, self.last_y, event.x, event.y, width = self.brush_size.get(), fill=color)
            self.stroke_draw.line([self.last_x, self.last_y, event.x, event.y], width = self.brush_size.get(),fill=color)
        self.last_x = event.x
        self.last_y = event.y



    def save_image(self, event):
        self.last_x = None
        self.last_y = None

        #to save images as png 
        self.stroke_image.save(f'stroke_{self.stroke_count}.png')
        #self.image.save(f'canvas_{self.stroke_count + 1}.png')
        
        stroke_data = np.array(self.stroke_image.convert('L')).flatten()
        stroke_data = stroke_data / 255
        insert_data = np.array([self.last_canvas, stroke_data])
        insert_data = insert_data[np.newaxis, :]

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

        #save npy to folder
        data_relative_path = f'ImageData{winHight*winWidth}/image{self.file_count + 1}data.npy'
        data_absolute_path = os.path.join(os.path.dirname(__file__), data_relative_path)
        np.save(data_absolute_path, self.data)
        #save png to folder
        png_relative_path = f'FinalImagePNG{winHight*winWidth}/image{self.file_count + 1}PNG.png'
        png_absolute_path = os.path.join(os.path.dirname(__file__), png_relative_path)
        self.image.save(png_absolute_path)
        
def scale_to_color(value):
        # Convert the scale value (0-100) to a grayscale color (0-255)
        color_value = int((value / 100) * 255)
        # Convert the color value to a hexadecimal string and pad with zeros if necessary
        hex_color = "{:02x}".format(color_value)
        # Return the color in the format expected by tkinter
        return "#" + hex_color * 3   
    


root = tk.Tk() 
app = DrawingApp(root)
root.mainloop()