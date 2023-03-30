def list_ports():
    """
    Test the ports and returns a tuple with the available ports and the ones that are working.
    """
    non_working_ports = []
    dev_port = 0
    working_ports = []
    available_ports = []
    while len(non_working_ports) < 4: # if there are more than 5 non working ports stop the testing. 
        camera = cv2.VideoCapture(dev_port)
        if not camera.isOpened():
            non_working_ports.append(dev_port)
        else:
            is_reading, img = camera.read()
            w = camera.get(3)
            h = camera.get(4)
            if is_reading:
                working_ports.append(dev_port)
            else:
                available_ports.append(dev_port)
        dev_port +=1
    return available_ports,working_ports,non_working_ports

#//////////////////////////////////////////////////////////////

"""HydroSens GUI"""

import os
import cv2
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import ImageTk, Image
import OS_function
import camera_function

ctk.set_appearance_mode("system")
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
frame.columnconfigure(2, weight=1, minsize=200)
frame.columnconfigure(3, weight=1, minsize=200)

title = ctk.CTkLabel(master=frame, text="HydroSens System", font=("Helvetica", 24, "bold"))
title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

project_name = ctk.CTkEntry(master=frame, placeholder_text="Name of test project", font=("Helvetica", 14))
project_name.grid(row=1, column=0, columnspan=4, padx=15, pady=10, sticky="ew")

duration_between_pictures = ctk.CTkEntry(master=frame, placeholder_text="Number of seconds between each picture", font=("Helvetica", 14))
duration_between_pictures.grid(row=2, column=0, columnspan=4, padx=15, pady=10, sticky="ew")

camera_box_var = ctk.StringVar()

def gui_camera_port():
    global cameras 
    cameras = camera_function.list_ports2()

    if len(cameras) != 0:

        if 'camera_box' in globals() and camera_box.winfo_exists():
            camera_box.destroy()

        camera_box_var.set(cameras[0])

        camera_box = ctk.CTkComboBox(master=frame, values=cameras, variable=camera_box_var)
        camera_box.grid(row=3, column=0, columnspan=3, padx=15, pady=10, sticky="ew")

    else:
        camera_box = ctk.CTkLabel(master=frame, text="No camera detected! Please check the connection with the camera and retry.", font=("Helvetica", 14))
        camera_box.grid(row=3, column=0, columnspan=3, padx=15, pady=10, sticky="ew")

gui_camera_port()

button_update_cam = ctk.CTkButton(master=frame, text="Update",font=("Helvetica", 14), command=gui_camera_port)
button_update_cam.grid(row=3, column=3, padx=10, pady=10, sticky="ew")

def open_folder():
    folder_path = filedialog.askdirectory(title="Select an output folder")
    if folder_path:
        print(f"Selected folder: {folder_path}")
        button_path_export.configure(text=str(folder_path), width=10, fg_color="purple", font=("Helvetica", 14))

button_path_export = ctk.CTkButton(master=frame, text="Select an output folder",font=("Helvetica", 14), command=open_folder)
button_path_export.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

def display_image():
    image_container = ctk.CTkFrame(master=frame)
    image_container.grid(rowspan=4, row=6, columnspan=4, column=0, padx=10, pady=10, sticky="ns")

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the relative path to the image file
    image_preview_path = os.path.join(script_dir, "..", "assets", "images", "image_preview.jpg")

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

display_image()

button_preview = ctk.CTkButton(master=frame, text="Preview", font=("Helvetica", 14), \
    command=lambda: (camera_function.take_picture(True, cameras.index(camera_box_var.get())), display_image()))
button_preview.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

button_execute = ctk.CTkButton(master=frame, text="Launch", font=("Helvetica", 14), command=login)
button_execute.grid(row=5, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

#def user_theme():
#    if folder_path:

#checkbox = ctk.CTkCheckBox(master=frame, text="Theme" command=user_theme())
#checkbox.grid(row=16, columnspan=2, column=0, padx=15, pady=10, sticky="w")

# Use grid columnconfigure to make the first column resizable
frame.columnconfigure(0, weight=1)

root.mainloop()


#//////////////////////////////////////////////////////////////


import cv2
import os
import tkinter as tk

class WebcamCaptureApp:

    def __init__(self):
        # create the main window
        self.root = tk.Tk()
        self.root.title("HydroSens")

        # create the capture button
        self.capture_button = tk.Button(self.root, text="Capture", command=self.capture)
        self.capture_button.pack(pady=10)

        # create the quit button
        self.quit_button = tk.Button(self.root, text="Quit", command=self.quit)
        self.quit_button.pack(pady=10)

        # initialize the camera
        self.cap = cv2.VideoCapture(0)

    def capture(self):
        # capture a frame
        ret, frame = self.cap.read()

        # save the captured image to a file
        cv2.imwrite("image.jpg", frame)

    def quit(self):
        # release the camera and close the window
        self.cap.release()
        self.root.destroy()

    def run(self):
        # start the main loop
        self.root.mainloop()

# create the app object and run it
app = WebcamCaptureApp()
app.run()


#//////////////////////////////////////////////////////////////