import tkinter as tk
import numpy as np
from PIL import Image, ImageDraw

class DrawingApp:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, width=500, height=500, bg='white')
        self.canvas.pack()
        self.image = Image.new('RGB', (500, 500), 'white')
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.save_image)

    def draw_line(self, event):
        self.canvas.create_line(event.x, event.y, event.x + 1, event.y + 1, fill='black')
        self.draw.line([event.x, event.y, event.x + 1, event.y + 1], fill='black')

    def save_image(self, event):
        self.image.save('canvas.png')
        img_array = np.array(self.image.convert('L'))
        np.savetxt("myfile.txt", img_array)
        print(img_array)

root = tk.Tk()
app = DrawingApp(root)
root.mainloop()