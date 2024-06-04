import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw

winHight = 500
winWidth = winHight
imageFmt = '%.3f'

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width = winWidth, height = winHight, bg = 'white')
        self.canvas.pack()
        self.image = Image.new('RGB', (winWidth, winHight), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.last_x = None
        self.last_y = None
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.save_image)

    def draw_line(self, event):
        if self.last_x is not None and self.last_y is not None:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill='black')
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill='black')
        self.last_x = event.x
        self.last_y = event.y

    def save_image(self, event):
        self.last_x = None
        self.last_y = None
        self.image.save('canvas.png')
        img_array = np.array(self.image.convert('L'))
        #img_array = np.where(img_array < 128, 0, 1) converts to binary values
        img_array = img_array / 255.0
        np.savetxt("tempImage.txt", img_array, imageFmt)
        append_file("tempImage.txt", "compiledImages.txt")


def append_file(file1_path, file2_path):
    with open(file1_path, 'r') as file1:
        with open(file2_path, 'a+') as file2:
            file2.write(file1.read())   

root = tk.Tk() 
app = DrawingApp(root)
root.mainloop()