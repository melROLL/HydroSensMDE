"""import PySimpleGUI as sg
import os.path

sg.Window(title="HydroSesMDE", layout=[[]], margins=(100, 50)).read()

# First the window layout in 2 columns


file_list_column = [
    [
        sg.Text("Image Folder"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key="-FILE LIST-")
    ],
]"""
"""
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        # Set columns
        self.cols = 1

        # Set a second Gridlayout
        self.top_grid = GridLayout()
        self.top_grid.cols = 2

        self.top_grid.add_widget(Label(text="Name of the sample: ")) #)), size_hint_x=None, width=500))
        self.top_grid.add_widget(Label(text="John Doe"))
        self.top_grid.add_widget(Label(text="Desired time between 2 pictures in seconds: "))
        self.delta_T = TextInput(multiline=True)
        self.top_grid.add_widget(self.delta_T)

        # Add the new top_grid to our app
        self.add_widget(self.top_grid)

        # Add a button
        self.add_widget(Button(text="Submit", on_press=self.submit_button_pressed, font_size=30, background_color=(3, 2, 4, 1)))



    def submit_button_pressed(self, button):
        print("Submit button pressed!")
 

class MyApp(App):
    def build(self):
        return MyGrid()

if __name__ == "__main__":
    MyApp().run()
"""

import os
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import ImageTk, Image

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("1280x720")

def login():
    print("Test")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

# Use grid columnconfigure to make the first column resizable
frame.columnconfigure(0, weight=1, minsize=200)
frame.columnconfigure(1, weight=1, minsize=200)

title = ctk.CTkLabel(master=frame, text="HydroSens System", font=("Helvetica", 24, "bold"))
title.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

project_name = ctk.CTkEntry(master=frame, placeholder_text="Name of test project", font=("Helvetica", 14))
project_name.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky="ew")

duration_between_pictures = ctk.CTkEntry(master=frame, placeholder_text="Number of seconds between each picture", font=("Helvetica", 14))
duration_between_pictures.grid(row=2, column=0, columnspan=2, padx=15, pady=10, sticky="ew")

#checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
#checkbox.grid(row=3, columnspan=2, column=0, padx=15, pady=10, sticky="w")

def open_folder():
    folder_path = filedialog.askdirectory(title="Select an output folder")
    if folder_path:
        print(f"Selected folder: {folder_path}")
        button.configure(text=str(folder_path), width=10, fg_color="purple", font=("Helvetica", 14))

button = ctk.CTkButton(master=frame, text="Select an output folder",font=("Helvetica", 14), command=open_folder)
button.grid(row=3, columnspan=2, column=0, padx=10, pady=10, sticky="ew")

button_preview = ctk.CTkButton(master=frame, text="Preview", font=("Helvetica", 14), command=login)
button_preview.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

button_execute = ctk.CTkButton(master=frame, text="Launch", font=("Helvetica", 14), command=login)
button_execute.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

image_container = ctk.CTkFrame(master=frame)
image_container.grid(rowspan=4, row=5, columnspan=2, column=0, padx=10, pady=10, sticky="ns")

# Get the path to the image file
image_preview_path = os.path.join("..", "assets", "images", "image_preview.jpg")

# Open the image and create a Tkinter-compatible PhotoImage object
image = Image.open(image_preview_path)

# Resize the image to a new width and height
new_width = 500
new_height = round(new_width*0.75)
resized_image = image.resize((new_width, new_height))

# Create a Tkinter-compatible PhotoImage object
tk_image = ImageTk.PhotoImage(resized_image)

# Create a Label widget and pack it inside the spacer frame
label = tk.Label(image_container, image=tk_image)
label.image = tk_image
label.pack()

# Use grid columnconfigure to make the first column resizable
frame.columnconfigure(0, weight=1)

root.mainloop()


"""# sample code using Python and TensorFlo.py"""
"""
def open_image():
    file_path = filedialog.askopenfilename(title="Select Image File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if file_path:
        image = Image.open(file_path)
        image = image.resize((spacer.winfo_width(), spacer.winfo_height()))
        tk_image = ImageTk.PhotoImage(image)
        label = tk.Label(spacer, image=tk_image)
        label.image = tk_image
        label.pack()


button = tk.Button(root, text="Open Image", command=open_image)
button.pack()"""