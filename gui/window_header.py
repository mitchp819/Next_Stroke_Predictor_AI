import tkinter as tk
from tkinter import ttk
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except ImportError:
    print("Error: windll not imported. Text may be blurred")
    pass

def start_move(event, root):
    root.x = event.x
    root.y = event.y

def move_window(event, root):
    x = root.winfo_pointerx() - root.x 
    y = root.winfo_pointery() - root.y 
    root.geometry(f"+{x}+{y}")

def close_window(root):
    root.destroy()


def create_header_frame(container, include_close_btn = False):
    header = tk.Frame(
        container,
        bg='#48A5E6',
        height=4,
        border=4,
        relief= 'ridge'
    )

    if include_close_btn:
        close_btn = tk.Button(
            header,
            text='x',
            command=lambda: close_window(container),
            bg='#ADA992',
            font=("TkDefaultFont", 5)
        )
        close_btn.pack(side=tk.RIGHT, expand=False, pady=3, padx=(0,5),)
    
    header.pack(fill='x', padx=2,pady=2)

    header.bind("<ButtonPress-1>", lambda event: start_move(event, container)) 
    header.bind("<B1-Motion>", lambda event: move_window(event, container))
