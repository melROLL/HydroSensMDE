"""HydroSens GUI"""

import os
import cv2
import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import ImageTk, Image
import OS_function
import camera_function

class HydroSensApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hydrosens System")
        self.geometry("1280x785")
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")

        self.frame = ctk.CTkFrame(master=self)
        self.frame.pack(pady=20, padx=60, fill="both", expand=True)

        # Use grid columnconfigure to make the first column resizable
        self.frame.columnconfigure(0, weight=1, minsize=200)
        self.frame.columnconfigure(1, weight=1, minsize=200)
        self.frame.columnconfigure(2, weight=1, minsize=200)
        self.frame.columnconfigure(3, weight=1, minsize=200)

        self.title = ctk.CTkLabel(master=self.frame, text="HydroSens System", \
            font=("Helvetica", 24, "bold"))
        self.title.grid(row=0, column=0, columnspan=4, padx=20, pady=20)

        self.project_name = ctk.CTkEntry(master=self.frame, \
            placeholder_text="Name of test project", font=("Helvetica", 14))
        self.project_name.grid(row=1, column=0, columnspan=4, padx=15, pady=10, sticky="ew")

        self.duration_between_pictures = ctk.CTkEntry(master=self.frame, \
            placeholder_text="Number of seconds between each picture", font=("Helvetica", 14))
        self.duration_between_pictures.grid(row=2, column=0, columnspan=4, padx=15, pady=10, sticky="ew")
        
        self.camera_box_var = ctk.StringVar()
        self.gui_camera_port(self.frame)

        self.button_update_cam = ctk.CTkButton(master=self.frame, text="Update",font=("Helvetica", 14), \
            command=lambda: self.gui_camera_port(self.frame))
        self.button_update_cam.grid(row=3, column=3, padx=10, pady=10, sticky="ew")

        self.button_path_export = ctk.CTkButton(master=self.frame, text="Select an output folder", \
            font=("Helvetica", 14), command=lambda: self.open_folder(self.frame))
        self.button_path_export.grid(row=4, column=0, columnspan=4, padx=10, pady=10, sticky="ew")

        self.display_image(self.frame)

        self.button_preview = ctk.CTkButton(master=self.frame, text="Preview", font=("Helvetica", 14), \
            command=lambda: (camera_function.take_picture(True, self.cameras.index(self.camera_box_var.get())), \
                self.display_image(self.frame)))
        self.button_preview.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.button_execute = ctk.CTkButton(master=self.frame, text="Launch", font=("Helvetica", 14), command=self.login)
        self.button_execute.grid(row=5, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

        self.check_sys_color = ctk.StringVar(value="on")
        self.checkbox_sys_color = ctk.CTkCheckBox(master=self.frame, text="Theme", command=self.user_theme, \
            variable=self.check_sys_color, onvalue="on", offvalue="off")
        self.checkbox_sys_color.grid(row=10, columnspan=2, column=0, padx=15, pady=10, sticky="w")

    def gui_camera_port(self, frame):
        self.cameras = camera_function.list_ports()

        if len(self.cameras) != 0:

            if 'camera_box' in globals() and camera_box.winfo_exists():
                camera_box.destroy()

            self.camera_box_var.set(self.cameras[0])

            camera_box = ctk.CTkComboBox(master=frame, values=self.cameras, variable=self.camera_box_var)
            camera_box.grid(row=3, column=0, columnspan=3, padx=15, pady=10, sticky="ew")

        else:

            camera_box = ctk.CTkLabel(master=self.frame, \
                text="No camera detected! Please check the connection with the camera and retry.", font=("Helvetica", 14))
            camera_box.grid(row=3, column=0, columnspan=3, padx=15, pady=10, sticky="ew")

    def display_image(self, frame):
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

    def open_folder(self, frame):
        folder_path = filedialog.askdirectory(title="Select an output folder")
        if folder_path:
            print(f"Selected folder: {folder_path}")
            self.button_path_export.configure(text=str(folder_path), width=10, \
                fg_color="purple", font=("Helvetica", 14))
    
    def user_theme(self):
        print("System color dark:", self.check_sys_color.get())
        if self.check_sys_color.get()=="on":
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
    
    def login(self):
        pass
    #    if folder_path is defined, name projecxt, duration -> execute:

def main():
    app = HydroSensApp()
    app.mainloop()

if __name__ == "__main__":
    main()
