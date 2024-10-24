import tkinter as tk
import numpy as np
import os
import re
import image_processing
from PIL import Image, ImageDraw

class DrawingApp:
    def __init__(self, master):
        self.master = master 
        
        #set image and windom size
        self.imageHeight = 128
        self.imageWidth = self.imageHeight  
        self.image_scalor = 6
        self.winHeight = self.imageHeight * self.image_scalor
        self.winWidth = self.imageWidth * self.image_scalor

        #build canvas
        self.canvas = tk.Canvas(self.master, width= self.winWidth, height= self.winHeight, bg="white")
        self.canvas.pack(side = tk.RIGHT)

        #store image x image data in np array
        self.np_main_canvas_data = np.ones((self.imageWidth, self.imageHeight), dtype= np.uint8) * 255
        self.np_stroke_canvas_data = np.ones((self.imageWidth, self.imageHeight), dtype= np.uint8) * 255

        #get the last file id 
        dir_path = f'ImageData{self.imageHeight * self.imageWidth}'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        files_list = [f for f in os.listdir(dir_path) 
                      if os.path.isfile(os.path.join(dir_path, f))]
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
        self.brush_slider = tk.Scale(self.master, from_=1, to=50, orient = "horizontal", variable = self.brush_size, label="Brush Size")
        self.brush_slider.pack()

        self.color_scale = tk.Scale(self.master, from_=0, to=255, orient="horizontal", label="Color Scale")
        self.color_scale.pack()

        #save button
        save_button = tk.Button(root, text="Save Image", command = self.save_data)
        save_button.pack() 


        #proccesss_image_button
        self.img_process = image_processing.img_processer("NPY_AllImageData16385.npy", '64x64_dataset.npy', "32x32_dataset.npy", "16x16_dataset.npy", "8x8_dataset.npy", "4x4_dataset.npy")
        process_image_button = tk.Button(root, text = "Process Image", command = self.process_image )
        process_image_button.pack(pady=(100,0))

        #Tolerance 
        self.tolerance = tk.IntVar()
        self.tolerance.set(500)
        self.tolerance_slider = tk.Scale(self.master, from_=1, to=1000, orient="horizontal", variable= self.tolerance, label = "Tolerance")
        self.tolerance_slider.pack()
        
        #Similarity Quality Label
        label = tk.Label(root, text = "hello world")
        label.pack()
        pass



    def process_image(self):
        #sets the tolerance in image_processing [How close data must be from the best variance]
        self.img_process.set_tolerance(self.tolerance)

        #get current canvas to send to image_processing script
        img_flat = self.np_main_canvas_data.flatten() / 255
        filler =  np.array([.5])
        input_img = np.concatenate((img_flat, filler))
        Image.fromarray(self.np_main_canvas_data.astype('uint8'), 'L').save("input_canvas.png")

        #call image_processing script
        output_stroke = self.img_process.compare_img_with_dataset(input_img)

        #get Color from output and shape
        color_value = int(output_stroke[-1] * 255)
        color = color_value_to_hex(color_value)
        stroke_img = output_stroke[:-1]
        stroke_img = shape_img(stroke_img)
        
        #get the associated varience from image_process and update the label

        for row, column_array  in enumerate(stroke_img):
            for col, pixel_value in enumerate(column_array):
                if pixel_value < 1:
                    #print(f"{row},{col}")
                    self.canvas.create_rectangle(row * self.image_scalor, col * self.image_scalor, (row+1) * self.image_scalor , (col+1) * self.image_scalor , outline = color, fill=color)

        #update np canvas data
        #do this real gud some how !!!! its the self.np_main_canavas_data
        pass



    def on_mouse_down(self, event):
        #Create Stroke Canvas
        self.np_stroke_canvas_data = np.ones((self.imageWidth, self.imageHeight), dtype= np.uint8) * 255

        #get selected grayscale color
        color_value = self.color_scale.get()
        color = color_value_to_hex(color_value)

        #Get image cord from win 
        x = event.x // self.image_scalor
        y = event.y // self.image_scalor
            
        #draws on canvas
        rect = self.canvas.create_rectangle(x * self.image_scalor, y * self.image_scalor,
                            (x + 1) * self.image_scalor, (y + 1) * self.image_scalor,
                            fill= color, outline=color, width= self.brush_size.get())
        
        #converts canvas rect into image coords
        x1, y1, x2, y2 = self.canvas.bbox(rect)
        x1 = int(x1 // self.image_scalor)
        y1 = int(y1 // self.image_scalor)
        x2 = int(x2 // self.image_scalor)
        y2 = int(y2 // self.image_scalor)

        #update np canvas data
        for x in range(x1, x2):
            for y in range(y1, y2):
                if (x < self.imageWidth and x >= 0 and y < self.imageHeight and y >= 0):
                    self.np_main_canvas_data[y, x] = color_value
                    self.np_stroke_canvas_data[y, x] = 1



    def on_mouse_drag(self, event):
        #get selected grayscale color
        color_value = self.color_scale.get()
        color = color_value_to_hex(color_value)

        #Get image cord from win
        x = event.x // self.image_scalor
        y = event.y // self.image_scalor

        #draws on canvas
        rect = self.canvas.create_rectangle(x * self.image_scalor, y * self.image_scalor,
                            (x + 1) * self.image_scalor, (y + 1) * self.image_scalor,
                            fill=color, outline=color,width=self.brush_size.get())
        
        #converts canvas rect into image coords
        x1, y1, x2, y2 = self.canvas.bbox(rect)
        x1 = int(x1 // self.image_scalor)
        y1 = int(y1 // self.image_scalor)
        x2 = int(x2 // self.image_scalor)
        y2 = int(y2 // self.image_scalor)

        #update np canvas data
        for x in range(x1, x2):
            for y in range(y1, y2):
                if (x < self.imageWidth and y < self.imageHeight):
                    self.np_main_canvas_data[y, x] = color_value
                    self.np_stroke_canvas_data[y, x] = 1



    def compile_np_array(self, event):
        #converts np canvas_data into and Image
        pil_stroke_img = Image.fromarray(self.np_stroke_canvas_data, mode="L")

        #flatten and normalize between 0-1
        flat_normal_last_canvas = self.last_canvas.flatten() / 255
        flat_normal_stroke_canvas = self.np_stroke_canvas_data.flatten() /255
        
        #saves color values in array
        filler =  np.array([.5])
        color_data = np.array([self.color_scale.get() / 255])
        
        flat_normal_last_canvas = np.concatenate((flat_normal_last_canvas,filler))
        flat_normal_stroke_canvas = np.concatenate((flat_normal_stroke_canvas, color_data))

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
        print("Image and Data Saved")
    
def color_value_to_hex (value):
    return f"#{value:02x}{value:02x}{value:02x}"

def shape_img (image):
        side_length = int(np.sqrt(image.shape[0]))
        #print(f"shape_img:   side_length = {side_length}")
        shaped_image = np.reshape(image, (side_length, side_length))
        #print(f"image reshaped. Shape = {shaped_image.shape}")
        return shaped_image


root = tk.Tk()
app = DrawingApp(root)
root.mainloop()

