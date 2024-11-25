import tkinter as tk
from tkinter import ttk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass
  

import sys
sys.path.append('C:/Users/mpalc/OneDrive/Desktop/_projects/next-brush-stroke-predictor_workspace/next_brush_stroke_predictor_app')
import util.helper_functions as hlp_fun
import window_header as wh

class GenerateUtilGUI(tk.Tk):
    def __init__(self, x = -30, y = 200):
        super().__init__()
        self.geometry(f'400x300{x}+{y}')
        self.overrideredirect(True)

        self.threhold = tk.IntVar()
        self.threhold.set(500)

        wh.create_header_frame(self, True)
        notebook = self.create_notebook()
        basic_tab = tk.Frame(self)
        self.pack_gen_thresh_widget(basic_tab)
        adv_gen_tab = self.create_adv_gen_tab(notebook)
        adv_thresh_tab = self.create_adv_thresh_tab(notebook)
        basic_tab.pack()
        adv_gen_tab.pack()
        adv_gen_tab.pack()

        notebook.add(basic_tab, text = "Basic")
        notebook.add(adv_gen_tab, text = "Adv Generation") 
        notebook.add(adv_thresh_tab, text = "Adv Thresholding")

    def get_threshold(self):
        return self.threhold

    def create_notebook(self):
        style = ttk.Style()
        style.configure('TNotebook', background = 'darkgrey', padding = [0,5,0,0])
        style.configure('TNotebook.Tab', padding=[0,0,10,0])
        style.configure('TNotebook.Separator', background = 'red', borderwidth=2)

        notebook = ttk.Notebook(self, style='TNotebook')
        notebook.pack(fill='both', padx=5, pady=5, expand=True)
        return notebook
    
    def pack_gen_thresh_widget(self,container):
        process_img_btn = tk.Button(
            container,
            text="Generate Next Stroke",
            command = self.process_image,
            borderwidth=5,
            relief='groove'
        )
        process_img_btn.pack(fill='x', expand=True, pady=3, padx=3)
        frame = tk.Frame(container)
        label = tk.Label(frame, text= "Threshold:").pack(side=tk.LEFT, padx=3,pady=3)
        threshold_slider = tk.Scale(frame,
                                    from_=1,
                                    to=1000,
                                    width=20,
                                    orient='horizontal',
                                    variable=self.threhold)
        threshold_slider.pack(side=tk.LEFT, fill='x', expand=True, pady=3, padx=3)
        frame.pack(fill='x', expand=True)
        pass
    
    def create_adv_gen_tab(self, container):
        frame = tk.Frame(container)
        label = tk.Label(frame, text="nothing new yet")
        label.pack()
        self.pack_gen_thresh_widget(frame)
        return frame
    
    def create_adv_thresh_tab(self, container):
        frame = tk.Frame(container)
        return frame
    
    def process_image(self):
        pass



if __name__ == "__main__":
    gen_util_gui = GenerateUtilGUI()
    gen_util_gui.mainloop()