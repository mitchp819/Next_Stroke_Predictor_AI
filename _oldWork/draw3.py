import tkinter as tk
import numpy as np
import os
import re
from PIL import Image, ImageDraw

class DrawingApp:
    def __init__(self, master):
        self.master = master 
        
        #set image and windom size
        self.imageHeight = 100
        self.imageWidth = self.imageHeight  
        self.image_scalor = 6
        self.winHeight = self.imageHeight * self.image_scalor
        self.winWidth = self.imageWidth * self.image_scalor

        #build canvas
        self.canvas = tk.Canvas(self.master, width= self.winWidth, height= self.winHeight, bg="white")
        self.canvas.pack()

        #store image x image data in np array
        self.np_main_canvas_data = np.ones((self.imageWidth, self.imageHeight), dtype= np.uint8) * 255
        self.np_stroke_canvas_data = np.ones((self.imageWidth, self.imageHeight), dtype= np.uint8) * 255

        #get the last file id 
        files_list = [f for f in os.listdir(f'ImageData{self.imageHeight * self.imageWidth}') 
                      if os.path.isfile(os.path.join(f'ImageData{self.imageHeight * self.imageWidth}', f))]
        largest_ID = 0
        for file in files_list:
            integers = [int(s) for s in re.findall(r'\d+', file)]
            if(integers[0] > largest_ID):
                largest_ID = integers[0]
        self.file_count = largest_ID

        #bind mouse events  
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.compile_np_array)

        #sets additional var
        self.last_canvas = self.np_main_canvas_data.flatten()
        self.compiled_data = None
        self.stroke_count = 0
        
        #brush size slider
        self.brush_size = tk.IntVar()
        self.brush_size.set(1)
        self.brush_slider = tk.Scale(self.master, from_=1, to=50, orient = "horizontal", variable = self.brush_size)
        self.brush_slider.pack()

        self.color_scale = tk.Scale(self.master, from_=0, to=254, orient="horizontal")
        self.color_scale.pack()

        #save button
        save_button = tk.Button(root, text="Save Image", command = self.save_data)
        save_button.pack()



    def on_mouse_down(self, event):
        #Create Stroke Canvas
        self.np_stroke_canvas_data = np.ones((self.imageWidth, self.imageHeight), dtype= np.uint8) * 255

        #get selected grayscale color
        color_value = self.color_scale.get()
        color = color_value_to_hex(color_value)

        #Get image cord from win 
        x = event.x // self.image_scalor
        y = event.y // self.image_scalor

        #update np canvas data
        self.np_main_canvas_data[y,x] = color_value
        self.np_stroke_canvas_data[y,x] = color_value

        brush_size = self.brush_size.get()

        """ for b in range(brush_size):
            self.np_main_canvas_data[y,x] = color_value
            self.np_stroke_canvas_data[y,x] = color_value """
            

        #draws on canvas
        self.canvas.create_rectangle(x * self.image_scalor, y * self.image_scalor,
                            (x + 1) * self.image_scalor, (y + 1) * self.image_scalor,
                            fill= color, outline=color, width=brush_size)



    def on_mouse_drag(self, event):
        #get selected grayscale color
        color_value = self.color_scale.get()
        color = color_value_to_hex(color_value)

        #Get image cord from win
        x = event.x // self.image_scalor
        y = event.y // self.image_scalor

        #update np canvas data
        self.np_main_canvas_data[y, x] = color_value
        self.np_stroke_canvas_data[y,x] = color_value

        #draws on canvas
        self.canvas.create_rectangle(x * self.image_scalor, y * self.image_scalor,
                            (x + 1) * self.image_scalor, (y + 1) * self.image_scalor,
                            fill=color, outline=color,width=self.brush_size.get())



    def compile_np_array(self, event):
        #converts np canvas_data into and Image
        
        pil_stroke_img = Image.fromarray(self.np_stroke_canvas_data, mode="L")

        #flatten and normalize between 0-1
        flat_normal_last_canvas = self.last_canvas.flatten() / 255
        flat_normal_stroke_canvas = self.np_stroke_canvas_data.flatten() /255

        print(flat_normal_last_canvas.shape)

        insertion_data = np.array([flat_normal_last_canvas, flat_normal_stroke_canvas])
        insertion_data = insertion_data[np.newaxis, :]

        #overwrites data
        self.last_canvas = self.np_main_canvas_data
        self.stroke_count += 1

        #cats insertion data with compiled data
        if self.compiled_data is None:
            self.compiled_data = insertion_data
        else:
            self.compiled_data = np.concatenate((self.compiled_data, insertion_data), axis=0)
        print(self.compiled_data.shape)

    def save_data(self):
        pil_main_img = Image.fromarray(self.np_main_canvas_data, mode="L")

        #save npy to folder
        data_relative_path = f'ImageData{self.imageHeight * self.imageWidth}/image{self.file_count + 1}data.npy'
        data_absolute_path = os.path.join(os.path.dirname(__file__), data_relative_path)
        np.save(data_absolute_path, self.compiled_data)
        #save png to folder
        png_relative_path = f'FinalImagePNG{self.imageHeight * self.imageWidth}/image{self.file_count + 1}PNG.png'
        png_absolute_path = os.path.join(os.path.dirname(__file__), png_relative_path)
        pil_main_img.save(png_absolute_path)
    
def color_value_to_hex (value):
    return f"#{value:02x}{value:02x}{value:02x}"


root = tk.Tk()
app = DrawingApp(root)
root.mainloop()

